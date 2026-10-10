"""Channel art for Watch It Learn: profile picture (1080x1080, circle-safe) and YouTube banner (2560x1440, safe area centred).
Output: content/_brand/ (committed; no personal photo is used)."""
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brand  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "content/_brand"
OUT.mkdir(parents=True, exist_ok=True)
CYAN = brand.CYAN


def canvas(w, h):
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w / 2) / max(w, h)) ** 2 + ((y - h / 2) / max(w, h)) ** 2)
    g = np.clip(1 - d * 2.4, 0, 1) ** 2
    a = np.zeros((h, w, 3), np.float32)
    a[..., 0], a[..., 1], a[..., 2] = 8 + 40 * g, 12 + 75 * g, 32 + 160 * g
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def glow_text(img, lines, cy, size, gap, blur=18):
    """lines drawn centred around y=cy with a cyan glow."""
    w, h = img.size
    layer = Image.new("RGB", (w, h), (0, 0, 0))
    core = Image.new("RGB", (w, h), (0, 0, 0))
    f = brand.font(size)
    total = len(lines) * size + (len(lines) - 1) * gap
    y = cy - total / 2
    for t in lines:
        for im, col in ((layer, CYAN), (core, (255, 255, 255))):
            d = ImageDraw.Draw(im)
            b = d.textbbox((0, 0), t, font=f)
            d.text(((w - (b[2] - b[0])) / 2 - b[0], y - b[1] * 0.2), t, font=f, fill=col)
        y += size + gap
    glow = layer.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(img, np.float32) + np.asarray(glow, np.float32) * 1.4
    c = np.asarray(core, np.float32)
    c[..., 0] *= 0.6
    return Image.fromarray((a + c).clip(0, 255).astype(np.uint8))


def bolts(img, seed, n, area):
    w, h = img.size
    rng = random.Random(seed)
    layer = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = area
    for _ in range(n):
        s = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        e = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        d.line(brand.bolt(rng, s, e, 90, 6), fill=CYAN if rng.random() < .7 else brand.VIOLET, width=4)
    glow = layer.filter(ImageFilter.GaussianBlur(10))
    a = np.asarray(img, np.float32) + np.asarray(glow, np.float32) * 1.6 + np.asarray(layer, np.float32)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def profile():
    img = canvas(1080, 1080)
    img = bolts(img, 4, 5, (80, 80, 1000, 1000))
    img = glow_text(img, ["WATCH", "IT", "LEARN"], 540, 190, 14, 20)  # inside the circle crop
    img.save(OUT / "profile_1080.png")
    img.resize((400, 400), Image.LANCZOS).save(OUT / "profile_400.png")
    m = Image.new("L", (1080, 1080), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 1079, 1079), fill=255)
    prev = Image.new("RGB", (1080, 1080), (30, 30, 30))
    prev.paste(img, (0, 0), m)
    prev.resize((300, 300)).save(OUT / "profile_circle_preview.png")


def banner():
    w, h = 2560, 1440  # YouTube safe area for all devices: centre 1546x423
    img = canvas(w, h)
    img = bolts(bolts(img, 9, 4, (0, 250, 700, 1190)), 11, 4, (1860, 250, w, 1190))
    img = glow_text(img, ["WATCH IT LEARN"], h / 2 - 40, 190, 0, 24)
    f = brand.font(64)
    d = ImageDraw.Draw(img)
    t = "AI/ML builds in 30 seconds. A new project every day."
    b = d.textbbox((0, 0), t, font=f)
    d.text(((w - (b[2] - b[0])) / 2, h / 2 + 90), t, font=f, fill=(190, 210, 240))
    img.save(OUT / "youtube_banner_2560x1440.png")


if __name__ == "__main__":
    profile()
    banner()
    print("wrote", sorted(p.name for p in OUT.iterdir()))
