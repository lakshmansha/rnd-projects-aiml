"""Electric Watch It Learn intro/outro cards: Pillow-rendered frames piped to ffmpeg + a synthesized zap/whoosh sound."""
import math
import random
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
BOLD = "C:/Windows/Fonts/arialbd.ttf"
CYAN, VIOLET, GREEN = (60, 220, 255), (150, 90, 255), (57, 217, 138)
_Y, _X = np.mgrid[0:H, 0:W]
_D = np.sqrt(((_X - W / 2) / W) ** 2 + ((_Y - H * 0.42) / H) ** 2)
_G = np.clip(1 - _D * 2.2, 0, 1) ** 2


def font(size):
    return ImageFont.truetype(BOLD, size)


def bg(t, pulse=1.0):
    """Dark navy with a pulsing radial glow."""
    g = _G * (0.55 + 0.25 * math.sin(t * 9)) * pulse
    img = np.zeros((H, W, 3), np.float32)
    img[..., 0] = 8 + 40 * g
    img[..., 1] = 12 + 70 * g
    img[..., 2] = 32 + 150 * g
    return Image.fromarray(img.clip(0, 255).astype(np.uint8))


def bolt(rng, start, end, jitter=70, depth=6):
    pts = [start, end]
    for _ in range(depth):
        new = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            m = ((a[0] + b[0]) / 2 + rng.uniform(-jitter, jitter), (a[1] + b[1]) / 2 + rng.uniform(-jitter, jitter))
            new += [m, b]
        pts, jitter = new, jitter * 0.55
    return pts


def glow_layer(draw_fn, blur=14):
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer.filter(ImageFilter.GaussianBlur(blur)), layer


def add(img, *layers):
    a = np.asarray(img, np.float32)
    for layer in layers:
        a = a + np.asarray(layer, np.float32)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def centered(draw, text, y, size, fill, scale=1.0, dx=0):
    f = font(int(size * scale))
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - (box[2] - box[0])) / 2 + dx - box[0], y), text, font=f, fill=fill)


def ease_out_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def intro_frame(i, n, sub_lines, tag):
    t = i / FPS
    rng = random.Random(i // 2)  # bolts re-roll every 2 frames = crackle
    img = bg(t)
    act = 1.0 if t < 0.7 else (0.35 if rng.random() < 0.35 else 0)
    if act:
        def arcs(d):
            for _ in range(int(3 + 4 * act)):
                s = (rng.choice([0, W]) if rng.random() < .5 else rng.uniform(0, W), rng.uniform(0, H * 0.7))
                e = (W / 2 + rng.uniform(-260, 260), H * 0.38 + rng.uniform(-90, 90))
                d.line(bolt(rng, s, e), fill=CYAN if rng.random() < .7 else VIOLET, width=int(rng.choice([3, 4, 6])))
        glow, core = glow_layer(arcs, 12)
        img = add(img, glow, glow, core)
    flash = max(0.0, 1 - abs(t - 0.62) / 0.09)
    if flash:
        img = add(img, Image.new("RGB", (W, H), (int(150 * flash),) * 3))
    p = min(max((t - 0.6) / 0.3, 0), 1)
    if p > 0:
        sc = 0.7 + 0.3 * ease_out_back(p) if p < 1 else 1 + 0.015 * math.sin(t * 22)
        flick = 1 if (t > 1.3 or int(t * 30) % 3) else 0.55  # electric flicker, then steady
        y1, y2 = H * 0.27, H * 0.27 + 230 * sc

        def title(d):
            centered(d, "WATCH IT", y1, 190, CYAN, sc)
            centered(d, "LEARN", y2, 190, CYAN, sc)
        glow, _ = glow_layer(title, 22)
        main = Image.new("RGB", (W, H), (0, 0, 0))
        dm = ImageDraw.Draw(main)
        col = (int(255 * flick),) * 3
        centered(dm, "WATCH IT", y1, 190, col, sc, dx=4)
        centered(dm, "LEARN", y2, 190, col, sc, dx=4)
        a = np.asarray(main, np.float32)
        a[..., 0] *= 0.55  # cyan-ish tint
        img = add(img, glow, Image.fromarray(a.clip(0, 255).astype(np.uint8)))
    if t > 0.95:
        k = min((t - 0.95) / 0.25, 1)

        def bar(d):
            d.rectangle((W / 2 - 380 * k, H * 0.585, W / 2 + 380 * k, H * 0.585 + 10), fill=GREEN)
        glow, core = glow_layer(bar, 10)
        img = add(img, glow, core)
    if t > 1.15:
        al = min((t - 1.15) / 0.3, 1)
        txt = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(txt)
        for j, line in enumerate(sub_lines):
            centered(d, line, H * 0.63 + j * 70, 54, (int(190 * al), int(210 * al), int(240 * al)))
        centered(d, tag, H * 0.74, 52, (int(57 * al), int(217 * al), int(138 * al)))
        img = add(img, txt)
    return img


def outro_frame(i, n, lines):
    t = i / FPS
    rng = random.Random(i // 3)
    img = bg(t, 1.1)
    if rng.random() < 0.3:
        def arcs(d):
            for _ in range(3):
                d.line(bolt(rng, (rng.uniform(0, W), 0), (W / 2 + rng.uniform(-300, 300), H * 0.4), 60), fill=CYAN, width=3)
        glow, core = glow_layer(arcs, 10)
        img = add(img, glow, core)
    sc = 0.85 + 0.15 * ease_out_back(min(t / 0.35, 1))
    y1, y2 = H * 0.24, H * 0.24 + 185 * sc

    def title(d):
        centered(d, "WATCH IT", y1, 150, CYAN, sc)
        centered(d, "LEARN", y2, 150, CYAN, sc)
    glow, _ = glow_layer(title, 18)
    main = Image.new("RGB", (W, H), (0, 0, 0))
    centered(ImageDraw.Draw(main), "WATCH IT", y1, 150, (255, 255, 255), sc)
    centered(ImageDraw.Draw(main), "LEARN", y2, 150, (255, 255, 255), sc)
    img = add(img, glow, main)
    txt = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(txt)
    pulse = 1 + 0.04 * math.sin(t * 8)
    for j, (line, size, col) in enumerate(lines):
        centered(d, line, H * 0.52 + j * 95, size, col, pulse if j == 0 else 1)
    return add(img, txt)


def render(frames_fn, n, audio, out):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", str(audio), "-map", "0:v", "-map", "1:a", "-t", f"{n / FPS:.3f}", "-c:v", "libx264",
           "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-ar", "44100", "-ac", "2", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frames_fn(i, n).tobytes())
    p.stdin.close()
    p.wait()


def zap_wav(path, dur=2.2, sr=44100):
    """Crackle + rising sweep + impact thump at 0.62s."""
    n = int(dur * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(3)
    y = np.zeros(n)
    for ts in np.sort(rng.uniform(0, 0.6, 14)):  # crackle bursts
        i0 = int(ts * sr)
        m = min(int(0.03 * sr), n - i0)
        y[i0:i0 + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / (0.006 * sr)) * 0.5
    ramp = np.clip(t / 0.62, 0, 1)
    sw = np.sin(2 * np.pi * np.cumsum(200 + 2600 * ramp ** 2) / sr) * ramp * (t < 0.62) * 0.35
    th = np.sin(2 * np.pi * 55 * (t - 0.62)) * np.exp(-(t - 0.62) * 6) * (t >= 0.62) * 0.9
    hit = rng.standard_normal(n) * np.exp(-(t - 0.62) * 25) * (t >= 0.62) * 0.4
    y = y + sw + th + hit
    y = y / max(1e-9, np.abs(y).max()) * 0.8
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    out = Path("D:/tmp/brand_test")
    out.mkdir(parents=True, exist_ok=True)
    zap_wav(out / "zap.wav")
    n = 66
    render(lambda i, n: intro_frame(i, n, ["AI/ML builds", "in 30 seconds"], "#16 CNN X-ray"), n, out / "zap.wav", out / "intro.mp4")
    ts = (0.2, 0.55, 0.65, 0.9, 1.4, 2.0)
    for t in ts:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(out / "intro.mp4"), "-frames:v", "1",
                        "-vf", "scale=270:480", str(out / f"f{t}.png")])
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for t in ts:
        cmd += ["-i", str(out / f"f{t}.png")]
    subprocess.run(cmd + ["-filter_complex", "hstack=6", str(out / "strip.png")])
