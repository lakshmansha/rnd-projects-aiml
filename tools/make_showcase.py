"""Build the channel showcase video: python tools/make_showcase.py

Voice-over comes from content/_showcase/full.md (section "Voice-over script"), one edge-tts clip per sentence.
Picture = the already-recorded shorts (content/NN-*/out/short_v2.mp4, intro/outro trimmed) in a portrait frame on a blurred
background, with chapter title + sentence captions in a right-hand ASS panel. No LLM calls, no avatar, nothing is uploaded.
Output: content/_showcase/out/showcase.mp4 (+ showcase.srt, chapters.txt)
"""
import asyncio
import re
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content/_showcase/full.md"
OUT = ROOT / "content/_showcase/out"
TMP = OUT / "tmp"
VOICE = "en-US-AndrewNeural"
GAP, SEC_GAP = 0.25, 0.7
TRIM_HEAD, TRIM_TAIL = 4.0, 5.0

CLIPS = {  # section index -> project numbers shown
    0: [6, 7, 2, 10, 4, 9],
    1: [6, 16, 14],
    2: [4, 7, 13, 6],
    3: [1, 2, 3, 5, 8, 11, 12, 15],
    4: [6, 13, 14],
    5: [4, 7, 16],
    6: [9, 10],
    7: [16, 13, 14],
    8: [6, 2, 9, 14, 10],
    9: [7, 3, 12],
}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


def parse():
    text = SRC.read_text(encoding="utf-8")
    body = text.split("## Voice-over script")[1].split("## Shot list")[0]
    secs = []
    for m in re.finditer(r"### \[(\d+:\d+)\] (.+?)\n(.*?)(?=\n### |\Z)", body, re.S):
        title = re.sub(r"\s*\(\d+ s\)\s*$", "", m.group(2)).strip()
        t = m.group(3).replace("[pause]", " ").replace("**", "")
        t = re.sub(r"\s+", " ", t).strip()
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
        secs.append((title, sents))
    return secs


async def tts_all(jobs):
    sem = asyncio.Semaphore(6)

    async def one(i, s):
        async with sem:
            await edge_tts.Communicate(s, VOICE).save(str(TMP / f"s{i:03d}.mp3"))
    await asyncio.gather(*[one(i, s) for i, s in jobs])


def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}" if not srt else f"{h:02d}:{m:02d}:{int(s):02d},{int(s % 1 * 1000):03d}"


def sh(*a):
    subprocess.run([str(x) for x in a], check=True, capture_output=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(exist_ok=True)
    secs = parse()
    flat = [s for _, ss in secs for s in ss]
    if not all((TMP / f"s{i:03d}.mp3").exists() for i in range(len(flat))):
        asyncio.run(tts_all(list(enumerate(flat))))
    # timeline
    t, idx, sent_t, sec_t = 0.0, 0, [], []
    for si, (title, ss) in enumerate(secs):
        t0 = t
        for s in ss:
            d = dur(TMP / f"s{idx:03d}.mp3")
            sent_t.append((t, t + d, s))
            t += d + GAP
            idx += 1
        t += SEC_GAP - GAP
        sec_t.append((title, t0, t))
    total = t
    print(f"{len(flat)} sentences, {total / 60:.1f} min")
    # audio: silence-padded concat
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", GAP, TMP / "gap.wav")
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", SEC_GAP, TMP / "secgap.wav")
    lst, idx = [], 0
    for title, ss in secs:
        for k, _ in enumerate(ss):
            lst.append(TMP / f"s{idx:03d}.mp3")
            lst.append(TMP / ("secgap.wav" if k == len(ss) - 1 else "gap.wav"))
            idx += 1
    (TMP / "a.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in lst), encoding="utf-8")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", TMP / "a.txt", "-ar", "24000", "-ac", "1", TMP / "voice.wav")
    # video segments
    segs = []
    for si, (title, a, b) in enumerate(sec_t):
        nums = CLIPS[si]
        per = (b - a) / len(nums)
        for k, n in enumerate(nums):
            src = next((ROOT / "content").glob(f"{n:02d}-*/out/short_v2.mp4"))
            avail = dur(src) - TRIM_HEAD - TRIM_TAIL
            seg = TMP / f"v{si}_{k}.mp4"
            start = TRIM_HEAD + (0 if per >= avail else (avail - per) / 2 * 0)
            vf = ("[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                  "boxblur=40:5,eq=brightness=-0.25[bg];[b]scale=-2:980[fg];[bg][fg]overlay=110:50,fps=25,format=yuv420p")
            sh("ffmpeg", "-y", "-stream_loop", "-1", "-ss", f"{start:.2f}", "-i", src, "-t", f"{per:.3f}",
               "-filter_complex", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", seg)
            segs.append(seg)
    (TMP / "v.txt").write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", TMP / "v.txt", "-c", "copy", TMP / "video.mp4")
    # ASS panel
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "",
           "[V4+ Styles]",
           "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
           "Style: Title,Arial,64,&H0000E1FF,&H0000E1FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,4,0,7,820,60,110,1",
           "Style: Cap,Arial,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,3,3,0,4,820,60,0,1",
           "Style: Brand,Arial,34,&H00DDDDDD,&H00DDDDDD,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,9,60,60,40,1",
           "", "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    for title, a, b in sec_t:
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Title,,0,0,0,,{title}")
    for a, b, s in sent_t:
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b + 0.15)},Cap,,0,0,0,,{s.replace(chr(10), ' ')}")
    ass.append(f"Dialogue: 0,{ts(0)},{ts(total)},Brand,,0,0,0,,Watch It Learn")
    (TMP / "p.ass").write_text("\n".join(ass), encoding="utf-8")
    srt = []
    for i, (a, b, s) in enumerate(sent_t, 1):
        srt.append(f"{i}\n{ts(a, True)} --> {ts(b, True)}\n{s}\n")
    (OUT / "showcase.srt").write_text("\n".join(srt), encoding="utf-8")
    (OUT / "chapters.txt").write_text(
        "\n".join(f"{int(a // 60)}:{int(a % 60):02d} {title}" for title, a, _ in sec_t), encoding="utf-8")
    # final mux (run inside TMP so the ass path has no drive colon)
    subprocess.run(["ffmpeg", "-y", "-i", "video.mp4", "-i", "voice.wav", "-vf", "ass=p.ass", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "22", "-c:a", "aac", "-b:a", "128k", "-shortest", "../showcase.mp4"],
                   cwd=TMP, check=True, capture_output=True)
    print("done", OUT / "showcase.mp4", f"{dur(OUT / 'showcase.mp4') / 60:.1f} min")


if __name__ == "__main__":
    main()
