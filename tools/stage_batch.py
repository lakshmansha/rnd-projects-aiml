"""Stage a BATCH of shorts for scheduling.   python tools/stage_batch.py [count=6] [start_date=tomorrow] [hour=19]

Takes the next `count` unposted items from content/queue.json (built from tools/upload_plan.py), runs the quality gate on
each short_v2.mp4, and writes content/_outbox/batch_<start>/ :
  <day>_<NN>/short.mp4, youtube.txt, instagram.txt, publish_at.txt   and   SCHEDULE.md (one row per day).
Nothing is uploaded. Scheduling (YouTube 'schedule', Instagram/Meta Business Suite 'schedule') uses publish_at.txt.
"""
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import upload_plan as up  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "content/queue.json"


def load_queue():
    if QUEUE.exists():
        return json.loads(QUEUE.read_text(encoding="utf-8"))
    q = [{"n": n, "folder": f, "title": t, "what": w, "tags": tags, "status": "ready"} for n, f, t, w, tags in up.ITEMS]
    save_queue(q)
    return q


def save_queue(q):
    QUEUE.write_text(json.dumps(q, indent=1, ensure_ascii=False), encoding="utf-8")


def gate(path):
    """Returns (ok, notes). Checks format, length, audio and long silences."""
    notes, ok = [], True
    pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height", "-show_entries", "format=duration",
                         "-of", "json", str(path)], capture_output=True, text=True)
    info = json.loads(pr.stdout)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    has_a = any(s["codec_type"] == "audio" for s in info["streams"])
    dur = float(info["format"]["duration"])
    if not v or (v["width"], v["height"]) != (1080, 1920):
        ok = False
        notes.append("size is not 1080x1920")
    if not 20 <= dur <= 35:
        ok = False
        notes.append(f"duration {dur:.1f}s outside 20-35s")
    if not has_a:
        ok = False
        notes.append("no audio")
    sil = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "silencedetect=n=-45dB:d=1.5", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    long_sil = re.findall(r"silence_duration: ([0-9.]+)", sil)
    if long_sil:
        ok = False
        notes.append(f"silence of {long_sil[0]}s")
    notes.append(f"{dur:.1f}s ok" if ok else "FAILED")
    return ok, notes


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    start = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date.today() + dt.timedelta(days=1)
    hour = int(sys.argv[3]) if len(sys.argv) > 3 else 19
    q = load_queue()
    todo = [it for it in q if it["status"] == "ready"][:count]
    if not todo:
        print("queue is empty: no ready items")
        return
    batch = ROOT / f"content/_outbox/batch_{start.isoformat()}"
    batch.mkdir(parents=True, exist_ok=True)
    rows = ["# Batch schedule", "", f"Times are your local time. Nothing has been uploaded.", "",
            "| Day | Publish at | # | Title | Gate |", "|---|---|---|---|---|"]
    for i, it in enumerate(todo):
        when = dt.datetime.combine(start + dt.timedelta(days=i), dt.time(hour, 0))
        src = ROOT / "content" / it["folder"] / "out/short_v2.mp4"
        ok, notes = gate(src) if src.exists() else (False, ["short_v2.mp4 missing"])
        d = batch / f"{i + 1}_{it['n']:02d}"
        d.mkdir(exist_ok=True)
        if src.exists():
            shutil.copy2(src, d / "short.mp4")
        disc = up.DISCLOSURE
        (d / "youtube.txt").write_text(f"{it['title']}\n\n{it['what']}\n\nProject {it['n']:02d} of the Watch It Learn series. {disc}\n\n"
                                       f"{it['tags']} #Shorts\n", encoding="utf-8")
        (d / "instagram.txt").write_text(f"{it['title']}\n\n{it['what']}\n\nFollow @watchitlearn for a new AI build every day.\n\n{it['tags']}\n",
                                         encoding="utf-8")
        (d / "publish_at.txt").write_text(when.strftime("%Y-%m-%d %H:%M") + "\n", encoding="utf-8")
        it["status"] = "staged" if ok else "needs_fix"
        it["batch"], it["publish_at"] = batch.name, when.isoformat()
        rows.append(f"| {i + 1} | {when:%a %d %b %H:%M} | {it['n']:02d} | {it['title']} | {'; '.join(notes)} |")
    (batch / "SCHEDULE.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    save_queue(q)
    print("\n".join(rows))
    print(f"\nstaged in {batch}")


if __name__ == "__main__":
    main()
