"""Build short_v2.mp4 (brand intro card + corrected voice + end card) from EXISTING raw footage; nothing is re-recorded.  Usage: python tools/make_short2.py <NN>

Reads content/<proj>/record.py: VOICE2 (falls back to VOICE) and CAPTIONS2 (falls back to CAPTIONS).
Footage: out/raw.json {file, offset} if present, else the newest out/tmp/*.webm with the offset estimated by matching short.mp4's first frame.
Does not touch out/short.mp4.
"""
import asyncio
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import re
sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand

ROOT = Path(__file__).resolve().parent.parent
VOICE_NAME = "en-US-AndrewNeural"
FONT = r"C\:/Windows/Fonts/arialbd.ttf"
BRAND = "WATCH IT LEARN"
TAGLINE = "AI/ML builds in 30 seconds"
END_LINE = "Follow for daily AI builds"
NAMES = {1: "Prompt Arena", 2: "Prompt Injection Lab", 3: "Semantic Map", 4: "Neural Net Playground",
         5: "Spot the Hallucination", 6: "Draw a Digit", 7: "Tiny GPT Trainer", 8: "AI 20 Questions",
         9: "RL Gridworld", 10: "Evolving Rockets", 11: "Token X-ray", 12: "AI Debate Arena",
         13: "Clustering Lab", 14: "Explainable Text AI", 15: "Prompt Gym", 16: "CNN X-ray"}


def run(*a):
    subprocess.run(a, check=True)


def probe(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout.strip())


def frames(path, fps, ss=None, t=None, size=(54, 96)):
    cmd = ["ffmpeg", "-loglevel", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", str(path)] + \
          (["-t", str(t)] if t else []) + ["-vf", f"fps={fps},scale={size[0]}:{size[1]},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, size[1], size[0]).astype(float)


def estimate_offset(raw, short):
    """Time in raw where short.mp4 starts: match first frame (top 60% only, captions sit below)."""
    fps = 10
    r = frames(raw, fps)
    s = frames(short, fps, t=6)
    n = min(len(s), 40)
    best = None
    for i in range(0, len(r) - n):
        d = np.abs(r[i:i + n, :58] - s[:n, :58]).mean()
        if best is None or d < best[0]:
            best = (d, i)
    return best[1] / fps, best[0]


def tts(text, path):
    import edge_tts
    for k in range(5):
        try:
            asyncio.run(edge_tts.Communicate(text, VOICE_NAME, rate="+4%").save(str(path)))
            return
        except Exception:  # edge-tts is flaky (NoAudioReceived): retry
            if k == 4:
                raise


def esc(p):
    return str(p).replace("\\", "/").replace(":", r"\:")


def textfile(path, text):
    path.write_bytes(text.replace("|", chr(10)).encode("utf-8"))
    return esc(path)


def main(num):
    d = next(p for p in (ROOT / "content").iterdir() if p.name.startswith(f"{int(num):02d}-"))
    spec = importlib.util.spec_from_file_location("rec", d / "record.py")
    rec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rec)
    out, tmp = d / "out", d / "out" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    voice_text = getattr(rec, "VOICE2", rec.VOICE)
    caps = getattr(rec, "CAPTIONS2", rec.CAPTIONS)
    # the spoken follow call now lives only on the end card: drop it from the main clip
    voice_text = re.sub(r"\s*(Built with Claude Code\.\s*)?Follow for more[^.]*\.?\s*$", "", voice_text.strip()).strip()
    caps = [c for c in caps if "ollow" not in c[2]]

    meta = out / "raw.json"
    if meta.exists():
        j = json.loads(meta.read_text())
        raw, offset = Path(j["file"]), j["offset"]
    else:
        raw = max(tmp.glob("*.webm"), key=lambda p: p.stat().st_mtime)
        offset, err = estimate_offset(raw, out / "short.mp4")
        print(f"estimated offset {offset:.1f}s (match error {err:.1f})")
        meta.write_text(json.dumps({"file": str(raw), "offset": offset}))

    brand_mp3, voice_mp3 = tmp / "brand.mp3", tmp / "voice2.mp3"
    if not brand_mp3.exists():
        tts("Watch It Learn.", brand_mp3)
    tts(voice_text, voice_mp3)
    dv, db = probe(voice_mp3), probe(brand_mp3)
    print(f"voice {dv:.1f}s")

    # main segment: footage + captions
    filt = ["tpad=stop_mode=clone:stop_duration=10", "scale=1080:1920:flags=lanczos"]
    for i, (t0, t1, text) in enumerate(caps):
        tf = textfile(tmp / f"c2_{i}.txt", text)
        filt.append(f"drawtext=fontfile='{FONT}':textfile='{tf}':fontsize=60:fontcolor=white:box=1:boxcolor=black@0.65"
                    f":boxborderw=18:line_spacing=10:text_align=center:x=(w-text_w)/2:y=h*0.74:enable='between(t,{t0},{t1})'")
    main = tmp / "seg_main.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-ss", f"{offset:.2f}", "-i", str(raw), "-i", str(voice_mp3),
        "-vf", ",".join(filt), "-map", "0:v", "-map", "1:a", "-t", f"{dv + 0.4:.2f}", "-r", "30", "-c:v", "libx264",
        "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-ar", "44100", "-ac", "2", str(main))

    assets = ROOT / "content/_assets"
    intro_base, outro, zap = assets / "intro_base.mp4", assets / "outro.mp4", assets / "zap.wav"
    if not intro_base.exists():
        brand.zap_wav(zap)
        mixed = assets / "intro_audio.wav"
        run("ffmpeg", "-y", "-loglevel", "error", "-i", str(zap), "-i", str(brand_mp3), "-filter_complex",
            "[1:a]adelay=800|800,volume=1.4[v];[0:a][v]amix=inputs=2:normalize=0,aresample=44100[a]", "-map", "[a]", str(mixed))
        brand.render(lambda i, n: brand.intro_frame(i, n, ["AI/ML builds", "in 30 seconds"], ""), 72, mixed, intro_base)
    if not outro.exists():
        cta = assets / "cta.mp3"
        tts("Follow Watch It Learn for a new AI build every day.", cta)
        n = int((probe(cta) + 0.7) * 30)
        lines = [("Follow for daily", 72, brand.GREEN), ("AI builds", 72, brand.GREEN), ("New project every day", 46, (170, 190, 220))]
        run("ffmpeg", "-y", "-loglevel", "error", "-i", str(cta), "-af", "adelay=300|300,apad", "-t", f"{n / 30:.2f}", str(assets / "cta.wav"))
        brand.render(lambda i, n: brand.outro_frame(i, n, lines), n, assets / "cta.wav", outro)
    num_i = int(d.name[:2]) if d.name[:2].isdigit() else 0
    pretty = NAMES.get(num_i, d.name[3:].replace("-", " ").title())
    intro = tmp / "seg_intro.mp4"
    tf = textfile(tmp / "tag.txt", f"#{num_i:02d} {pretty}")
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(intro_base), "-vf",
        f"drawtext=fontfile='{FONT}':textfile='{tf}':fontsize=54:fontcolor=0x39d98a:x=(w-text_w)/2:y=h*0.745:enable='gte(t,1.2)'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "copy", str(intro))
    outro_seg = tmp / "seg_outro.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(outro), "-c", "copy", str(outro_seg))

    lst = tmp / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'" + chr(10) for p in (intro, main, outro_seg)))
    final = out / "short_v2.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(final))
    print("wrote", final, f"{probe(final):.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
