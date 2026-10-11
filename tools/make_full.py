"""Build a long (flagship) video: python tools/make_full.py 06 [--record] [--audio-only]

Reads content/<proj>/full.md (voice-over, '### time title' sections) and content/<proj>/video.py:
    PORT, CODE = {name: (file, first_line, last_line)}, SECTIONS = [[visual, ...], ...] (one list per voice-over section),
    record(page, mark): drives the live app at 1600x860 and calls mark('scene') at the start of each scene.
Visuals: ('app', scene) | ('code', name) | ('card', 'text|text').
Markers inside the voice-over advance to the next visual of the section: a ``` code block, or [SCREEN: ...] / [Draw...].
Sync: every sentence is its own edge-tts clip decoded to wav; captions and picture timing come from the decoded sample counts.
Output: content/<proj>/out/full.mp4 (+ full.srt, chapters.txt). No LLM calls, nothing uploaded.
"""
import asyncio
import importlib.util
import json
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
VOICE = "en-US-AndrewNeural"
GAP, SEC_GAP, FPS = 0.28, 0.8, 25
W, H, VW, VH, VX, VY = 1920, 1080, 1600, 860, 160, 30
BG = (14, 17, 26)


def sh(*a, cwd=None):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True, cwd=cwd)
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])


def wdur(p):
    with wave.open(str(p)) as f:
        return f.getnframes() / f.getframerate()


def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(s % 1 * 1000):03d}" if srt else f"{h}:{m:02d}:{s:05.2f}"


def font(size, bold=False):
    for n in ("consolab.ttf" if bold else "consola.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()


def parse(md):
    body = md.split("## Voice-over")[1]
    secs = []
    for m in re.finditer(r"### ([\d:]+) (.+?)\n(.*?)(?=\n### |\Z)", body, re.S):
        raw = m.group(3)
        raw = re.sub(r":?\s*```.*?```", ". @C ", raw, flags=re.S)
        raw = re.sub(r"\*\*\[CODE[^\]]*\]\*\*[^\n]*", " @C ", raw)
        raw = re.sub(r"\*?\*?\[(?:SCREEN|AVATAR)[^\]]*\]\*?\*?", " @S ", raw)
        raw = re.sub(r"\[Draw[^\]]*\]", " @D ", raw)
        raw = raw.replace("`", "").replace("**", "")
        raw = re.sub(r"\s+", " ", raw)
        sents, step, carry = [], 0, []
        for chunk in re.split(r"(?<=[.!?])\s+", raw):
            carry += re.findall(r"@([CDS])", chunk)
            text = re.sub(r"@[CDS]", "", chunk).strip()
            if not text.strip(" ."):
                continue
            if sents and carry:  # leading markers (before the first sentence) do not advance
                step += len(carry)
                if "C" in carry or "D" in carry:  # the sentence that introduces the code/drawing switches too
                    sents[-1] = (sents[-1][0], step)
            carry = []
            sents.append((text, step))
        secs.append((m.group(1), re.sub(r"\s*\(.*?\)\s*$", "", m.group(2).strip()), sents))
    return secs


def code_png(rec, name, out):
    from pygments import highlight
    from pygments.formatters import ImageFormatter
    from pygments.lexers import PythonLexer
    f, a, b = rec.CODE[name]
    import textwrap
    lines = []
    for ln in (Path(rec.APP_DIR) / f).read_text(encoding="utf-8").splitlines()[a - 1:b]:
        ind = len(ln) - len(ln.lstrip())
        lines += textwrap.wrap(ln, 74, subsequent_indent=" " * (ind + 4), initial_indent="", drop_whitespace=False)             if len(ln) > 74 else [ln]
    fmt = ImageFormatter(font_name="Consolas", font_size=34, style="monokai", line_numbers=True, line_number_start=a,
                         image_pad=24, line_pad=6)
    tmp = out.with_suffix(".raw.png")
    tmp.write_bytes(highlight("\n".join(lines), PythonLexer(), fmt))
    im = Image.open(tmp).convert("RGB")
    s = min(VW / im.width, VH / im.height, 1.5)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    c = Image.new("RGB", (VW, VH), (39, 40, 34))
    c.paste(im, ((VW - im.width) // 2, (VH - im.height) // 2))
    c.save(out)
    tmp.unlink()


def card_png(text, out):
    c = Image.new("RGB", (VW, VH), BG)
    d = ImageDraw.Draw(c)
    ls = text.split("|")
    size = 84
    while size > 36 and max(d.textlength(l, font=font(size, True)) for l in ls) > VW - 120:
        size -= 4
    f = font(size, True)
    y = VH // 2 - len(ls) * 60
    for i, l in enumerate(ls):
        w = d.textlength(l, font=f)
        d.text(((VW - w) / 2, y + i * 120), l, font=f, fill=(255, 225, 0) if i == 0 else (255, 255, 255))
    c.save(out)


def still_clip(png, frames, out):
    sh("ffmpeg", "-y", "-loop", "1", "-framerate", FPS, "-i", png, "-frames:v", frames, "-vf", "format=yuv420p",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out)


def app_clip(scene, frames, out):
    """Cut the recorded scene; slow down slightly or hold the last frame if the narration is longer."""
    src, t0, t1 = scene
    avail = t1 - t0
    need = frames / FPS
    vf = f"fps={FPS},tpad=stop_mode=clone:stop_duration={max(need - avail, 0) + 1:.2f},format=yuv420p"
    sh("ffmpeg", "-y", "-ss", f"{t0:.2f}", "-t", f"{avail:.2f}", "-i", src, "-vf", vf, "-frames:v", frames,
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out)


def record_scenes(proj, rec, out_dir):
    from playwright.sync_api import sync_playwright
    tmp = out_dir / "rec"
    tmp.mkdir(parents=True, exist_ok=True)
    marks = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        c = b.new_context(viewport={"width": VW, "height": VH}, record_video_dir=str(tmp),
                          record_video_size={"width": VW, "height": VH}, device_scale_factor=1)
        page = c.new_page()
        t0 = time.time()
        page.goto(f"http://localhost:{rec.PORT}/{getattr(rec, 'QUERY', '?embed=true')}")
        page.wait_for_selector("[data-testid=stApp]")
        rec.prepare(page)
        rec.record(page, lambda n: marks.append((n, time.time() - t0)))
        marks.append(("_end", time.time() - t0))
        vid = Path(page.video.path())
        c.close()
        b.close()
    (out_dir / "scenes.json").write_text(json.dumps({"file": str(vid), "marks": marks}))


def finish(proj):
    """Electric intro + main + spoken end card (same brand cards as the shorts, portrait cards centred on a blurred landscape frame)."""
    sys.path.insert(0, str(ROOT / "tools"))
    from make_short2 import NAMES, FONT, esc
    assets = ROOT / "content/_assets"
    n = int(proj.name[:2])
    out = proj / "out" / "full"
    tag = out / "tag.txt"
    tag.write_bytes(f"#{n:02d} {NAMES.get(n, proj.name[3:].title())}".encode("utf-8"))
    comp = ("[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:5,"
            "eq=brightness=-0.3[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,fps=25,format=yuv420p[v]")
    sh("ffmpeg", "-y", "-i", assets / "intro_base.mp4", "-filter_complex",
       f"[0:v]drawtext=fontfile='{FONT}':textfile='{esc(tag)}':fontsize=54:fontcolor=0x39d98a:x=(w-text_w)/2:y=h*0.745:enable='gte(t,1.2)'[t];"
       + comp.replace("[0:v]", "[t]", 1), "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
       "-c:a", "aac", "-ar", "44100", "-ac", "2", out / "intro_l.mp4")
    sh("ffmpeg", "-y", "-i", assets / "outro.mp4", "-filter_complex", comp, "-map", "[v]", "-map", "0:a", "-c:v", "libx264",
       "-crf", "20", "-preset", "veryfast", "-c:a", "aac", "-ar", "44100", "-ac", "2", out / "outro_l.mp4")
    sh("ffmpeg", "-y", "-i", out / "intro_l.mp4", "-i", proj / "out/full_main.mp4", "-i", out / "outro_l.mp4", "-filter_complex",
       "[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];[1:a]aresample=44100,aformat=channel_layouts=stereo[a1];"
       "[2:a]aresample=44100,aformat=channel_layouts=stereo[a2];[0:v][1:v][2:v]concat=n=3:v=1:a=0[v];[a0][a1][a2]concat=n=3:v=0:a=1[a]",
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "21", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac",
       "-b:a", "160k", proj / "out/full.mp4")
    print("done", proj / "out/full.mp4")


def main():
    proj_no = sys.argv[1]
    proj = next((ROOT / "content").glob(f"{proj_no}-*"))
    if "--finish" in sys.argv:
        return finish(proj)
    out = proj / "out" / "full"
    out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("rec", proj / "video.py")
    rec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rec)
    if "--record" in sys.argv or not (out / "scenes.json").exists():
        record_scenes(proj, rec, out)
    sc = json.loads((out / "scenes.json").read_text())
    scenes = {}
    for (n, a), (_, b) in zip(sc["marks"], sc["marks"][1:]):
        scenes[n] = (sc["file"], a, b)

    secs = parse((proj / "full.md").read_text(encoding="utf-8"))
    flat = [s for _, _, ss in secs for s, _ in ss]
    for i, s in enumerate(flat):
        mp3, wav, txt = out / f"s{i:03d}.mp3", out / f"s{i:03d}.wav", out / f"s{i:03d}.txt"
        if not (wav.exists() and txt.exists() and txt.read_text(encoding="utf-8") == s):
            wav.unlink(missing_ok=True)
            for attempt in range(5):
                try:
                    asyncio.run(edge_tts.Communicate(s, VOICE).save(str(mp3)))
                    break
                except Exception as e:  # edge-tts sometimes returns no audio for short lines; retry, then pad the text
                    print("tts retry", i, type(e).__name__)
                    time.sleep(2)
                    if attempt == 3:
                        s = s.rstrip(".") + " ."
            sh("ffmpeg", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav)
            txt.write_text(flat[i], encoding="utf-8")
    # timeline
    t, idx, sent_t, sec_t = 0.0, 0, [], []
    for title_t, title, ss in secs:
        t0 = t
        for s, step in ss:
            d = wdur(out / f"s{idx:03d}.wav")
            sent_t.append((t, t + d, s, step))
            t += d + GAP
            idx += 1
        t += SEC_GAP - GAP
        sec_t.append((title, t0, t))
    total = t
    print(f"{len(flat)} sentences, {total / 60:.1f} min")
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", GAP, out / "gap.wav")
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", SEC_GAP, out / "secgap.wav")
    lst, idx = [], 0
    for _, _, ss in secs:
        for k, _ in enumerate(ss):
            lst += [out / f"s{idx:03d}.wav", out / ("secgap.wav" if k == len(ss) - 1 else "gap.wav")]
            idx += 1
    (out / "a.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in lst), encoding="utf-8")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", out / "a.txt", "-c", "copy", out / "voice.wav")
    if "--audio-only" in sys.argv:
        return
    # visual segments: each visual covers the sentences between markers; frame-exact boundaries
    segs, si, k = [], 0, 0
    sidx = 0
    for (title_t, title, ss), vis in zip(secs, rec.SECTIONS):
        n = len(ss)
        groups = {}
        marked = any(st for _, st in ss)
        for j, (_, step) in enumerate(ss):
            g = min(step, len(vis) - 1) if marked else min(j * len(vis) // max(n, 1), len(vis) - 1)
            groups.setdefault(g, []).append(sidx + j)
        sec_end = sec_t[si][2]
        order = sorted(groups)
        for gi, g in enumerate(order):
            a = sent_t[groups[g][0]][0] if gi else sec_t[si][1]
            b = sent_t[groups[order[gi + 1]][0]][0] if gi + 1 < len(order) else sec_end
            segs.append((vis[g], a, b))
        sidx += n
        si += 1
    # fill gaps by cumulative rounding so the picture never drifts
    clips = []
    bounds = [round(a * FPS) for _, a, _ in segs] + [round(total * FPS)]
    for i, (v, a, b) in enumerate(segs):
        frames = max(bounds[i + 1] - bounds[i], 1)
        o = out / f"v{i:03d}.mp4"
        kind, arg = v
        if kind == "app":
            app_clip(scenes[arg], frames, o)
        else:
            png = out / f"{kind}_{abs(hash(arg)) % 10**8 if kind == 'card' else arg}.png"
            if kind == "code":
                code_png(rec, arg, png)
            else:
                card_png(arg, png)
            still_clip(png, frames, o)
        clips.append(o)
    (out / "v.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", out / "v.txt", "-c", "copy", out / "video.mp4")
    # captions: bottom band
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "", "[V4+ Styles]",
           "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
           "Style: Cap,Arial,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,3,3,0,2,110,110,28,1",
           "Style: Brand,Arial,30,&H00DDDDDD,&H00DDDDDD,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,9,40,40,16,1",
           "", "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    for a, b, s, _ in sent_t:
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b + 0.15)},Cap,,0,0,0,,{s}")
    ass.append(f"Dialogue: 0,{ts(0)},{ts(total)},Brand,,0,0,0,,Watch It Learn")
    (out / "p.ass").write_text("\n".join(ass), encoding="utf-8")
    (proj / "out" / "full.srt").write_text(
        "\n".join(f"{i}\n{ts(a, True)} --> {ts(b, True)}\n{s}\n" for i, (a, b, s, _) in enumerate(sent_t, 1)), encoding="utf-8")
    (proj / "out" / "chapters.txt").write_text(
        "\n".join(f"{int(a // 60)}:{int(a % 60):02d} {title}" for title, a, _ in sec_t), encoding="utf-8")
    # background canvas with the 1600x860 picture placed on it
    fc = (f"color=c=0x0e111a:s={W}x{H}:r={FPS}[bg];[0:v]scale={VW}:{VH}[fg];[bg][fg]overlay={VX}:{VY}:shortest=1,ass=p.ass[o]")
    sh("ffmpeg", "-y", "-i", "video.mp4", "-i", "voice.wav", "-filter_complex", fc, "-map", "[o]", "-map", "1:a",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
       "-t", f"{total:.2f}", "../full_main.mp4", cwd=out)
    finish(proj)


if __name__ == "__main__":
    main()
