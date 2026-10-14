"""Make 1280x720 YouTube thumbnails for the long videos: python tools/make_thumbs.py [NN ...]

Takes a frame of the app from content/<proj>/out/full.mp4, crops to 16:9, darkens it, and adds the project's thumbnail text
(from full.md, max 4 words) plus the channel avatar. Output: content/_thumbs/<NN>.jpg (under 2 MB, as YouTube requires).
Override the frame time per project in FRAME_AT (seconds into the full video).
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_sheet import C, meta  # noqa: E402

OUT = C / "_thumbs"
FRAME_AT = {"17": 280.0}   # seconds into the full video; default is 55% of the duration
FOCUS = {}   # {"NN": (x, y)}: top-left (in the 1600x860 app picture + 160/30 offset) of the 1350-px-wide crop, default (260, 50)
W, H = 1280, 720


def font(size):
    for n in ("impact.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()


def grab(d, t):
    tmp = OUT / "_frame.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(d / "out/full.mp4"), "-frames:v", "1", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    return im


def duration(d):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(d / "out/full.mp4")],
                         capture_output=True, text=True).stdout
    return float(out)


def lines_for(text):
    words = text.upper().replace('"', "").split()
    if len(words) <= 2:
        return [" ".join(words)]
    best = min(range(1, len(words)), key=lambda k: max(len(" ".join(words[:k])), len(" ".join(words[k:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def make(num):
    d = next(C.glob(f"{num}-*"))
    md = (d / "full.md").read_text(encoding="utf-8")
    text = meta(md)["thumb"]
    t = FRAME_AT.get(num, duration(d) * 0.55)
    fr = grab(d, t)
    app = fr.crop((160, 30, 1760, 890))                       # the 1600x860 app picture, no captions
    bg = Image.new("RGB", (W, H), (10, 13, 24))
    gd = ImageDraw.Draw(bg)
    for x in range(W):                                        # subtle blue glow towards the right
        c = int(34 * x / W)
        gd.line([(x, 0), (x, H)], fill=(10 + c // 3, 13 + c // 2, 24 + c))
    pw, ph = 640, 380
    cw = 1350
    cx, cy = FOCUS.get(num, (260, 50))
    panel = app.crop((cx - 160, cy - 30, cx - 160 + cw, cy - 30 + round(cw * ph / pw))).resize((pw, ph), Image.LANCZOS)
    px, py = W - pw - 40, 170
    sh = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((30, 30, pw + 30, ph + 30), fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    bg.paste(sh, (px - 30, py - 20), sh)
    ImageDraw.Draw(bg).rectangle((px - 7, py - 7, px + pw + 6, py + ph + 6), fill=(57, 217, 138))
    bg.paste(panel, (px, py))
    app = bg
    dr = ImageDraw.Draw(app)
    ls = lines_for(text)
    size = 190
    while size > 70 and max(dr.textlength(l, font=font(size)) for l in ls) > W * 0.40:
        size -= 6
    f = font(size)
    y = (H - len(ls) * size * 1.05) / 2 - 20
    for i, l in enumerate(ls):
        col = (255, 225, 0) if i == 0 else (255, 255, 255)
        dr.text((50, y + i * size * 1.05), l, font=f, fill=col, stroke_width=max(6, size // 18), stroke_fill=(0, 0, 0))
    dr.text((50, H - 70), "WATCH IT LEARN", font=font(40), fill=(57, 217, 138), stroke_width=3, stroke_fill=(0, 0, 0))
    ava = Image.open(C / "_brand/profile_400.png").convert("RGBA").resize((110, 110), Image.LANCZOS)
    mask = Image.new("L", (110, 110), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 109, 109), fill=255)
    app.paste(ava, (W - 160, 14), mask)
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{num}.jpg"
    app.save(out, quality=90)
    print(num, text, f"-> {out.name} {out.stat().st_size // 1024} KB (frame at {t:.0f}s)")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    nums = sys.argv[1:] or sorted(p.name[:2] for p in C.glob("[0-9][0-9]-*"))
    for n in nums:
        make(n)
