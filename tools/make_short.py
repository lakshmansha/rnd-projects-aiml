"""Build one 30s Short: python tools/make_short.py 16   (needs the app running on its port; see content/<proj>/record.py)

record.py defines: PORT, VOICE (narration text), CAPTIONS [(t0, t1, text)], actions(page, T) where T.at(sec) waits until `sec` seconds into the clip.
Pipeline: edge-tts voice -> Playwright video (540x960) -> ffmpeg: trim, upscale 1080x1920, captions, avatar, mux. Output content/<proj>/out/short.mp4 (+ short.srt).
"""
import asyncio
import importlib.util
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
VOICE_NAME = "en-US-AndrewNeural"
FONT = r"C\:/Windows/Fonts/arialbd.ttf"
AVATAR = ROOT / "content/_assets/avatar.png"


class Timeline:
    def __init__(self, page):
        self.page, self.t0 = page, time.time()

    def scroll(self, px, smooth=True):
        """Scroll Streamlit's main container by px."""
        self.page.evaluate("([y, s]) => { const m = document.querySelector('[data-testid=stMain]') || document.scrollingElement;"
                           " m.scrollBy({top: y, behavior: s ? 'smooth' : 'auto'}); }", [px, smooth])

    def at(self, sec):
        left = sec - (time.time() - self.t0)
        if left > 0:
            self.page.wait_for_timeout(int(left * 1000))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def tts(text, path):
    import edge_tts
    asyncio.run(edge_tts.Communicate(text, VOICE_NAME, rate="+4%").save(str(path)))


def main(num):
    d = next(p for p in (ROOT / "content").iterdir() if p.name.startswith(f"{int(num):02d}-"))
    spec = importlib.util.spec_from_file_location("rec", d / "record.py")
    rec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rec)
    out = d / "out"
    out.mkdir(exist_ok=True)
    tmp = out / "tmp"
    tmp.mkdir(exist_ok=True)
    mp3 = out / "voice.mp3"
    tts(rec.VOICE, mp3)
    dur = duration(mp3)
    print(f"voice {dur:.1f}s")

    with sync_playwright() as p:
        b = p.chromium.launch()
        c = b.new_context(viewport={"width": 540, "height": 960}, record_video_dir=str(tmp),
                          record_video_size={"width": 540, "height": 960}, device_scale_factor=1)
        page = c.new_page()
        t_ctx = time.time()
        page.goto(f"http://localhost:{rec.PORT}/?embed=true")
        page.wait_for_selector("[data-testid=stApp]")
        getattr(rec, "prepare", lambda pg: pg.wait_for_timeout(3000))(page)
        offset = time.time() - t_ctx
        rec.actions(page, Timeline(page))
        vid = Path(page.video.path())
        c.close()
        b.close()

    filt = ["scale=1080:1920:flags=lanczos"]
    for i, (t0, t1, text) in enumerate(rec.CAPTIONS):
        tf = tmp / f"cap{i}.txt"
        tf.write_bytes(text.replace("|", chr(10)).encode("utf-8"))
        tfp = str(tf).replace("\\", "/").replace(":", r"\:")
        filt.append(f"drawtext=fontfile='{FONT}':textfile='{tfp}':fontsize=60:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=18:line_spacing=10"
                    f":x=(w-text_w)/2:y=h*0.74:enable='between(t,{t0},{t1})'")
    chain = ",".join(filt)
    fc = f"[0:v]{chain}[o]"
    mp4 = out / "short.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{offset:.2f}", "-i", str(vid), "-i", str(mp3), "-filter_complex", fc.replace("[0:v]", "[0:v]tpad=stop_mode=clone:stop_duration=10,", 1),
           "-map", "[o]", "-map", "1:a", "-t", f"{dur + 0.4:.2f}", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "20", "-c:a", "aac", "-b:a", "160k", str(mp4)]
    subprocess.run(cmd, check=True)
    print("wrote", mp4, f"{duration(mp4):.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
