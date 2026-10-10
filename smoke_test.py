"""Run every app headlessly with Streamlit AppTest and report exceptions.  Usage: python smoke_test.py [number ...]"""
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parent
want = sys.argv[1:]
apps = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:2].isdigit() and (p / "app.py").exists())
apps.append(ROOT / "hub")
bad = 0
for d in apps:
    if want and not any(d.name.startswith(w.zfill(2)) for w in want):
        continue
    try:
        at = AppTest.from_file(str(d / "app.py"), default_timeout=180).run()
        errs = [e.value for e in at.exception]
    except Exception as e:  # noqa: BLE001
        errs = [repr(e)]
    print(("FAIL " if errs else "ok   ") + d.name, *(e[:150] for e in errs))
    bad += bool(errs)
sys.exit(1 if bad else 0)
