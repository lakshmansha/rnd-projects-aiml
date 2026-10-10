"""Start every demo (and the hub on :8500). Ctrl+C stops them all.   Usage: python run_all.py [number ...]"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
APPS = sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit() and (p / "app.py").exists())
want = sys.argv[1:]
procs = []
try:
    for name in APPS:
        n = int(name[:2])
        if want and str(n) not in want and f"{n:02d}" not in want:
            continue
        cmd = [sys.executable, "-m", "streamlit", "run", f"{name}/app.py", "--server.headless", "true",
               "--server.port", str(8500 + n)]
        procs.append(subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        print(f"{name:32s} http://localhost:{8500 + n}")
    procs.append(subprocess.Popen([sys.executable, "-m", "streamlit", "run", "hub/app.py", "--server.headless", "true",
                                   "--server.port", "8500"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    print(f"{'hub':32s} http://localhost:8500\nCtrl+C to stop.")
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    pass
finally:
    for p in procs:
        p.terminate()
