"""Spec for the 01 full video (tools/make_full.py 01). Needs the app on PORT (python -m streamlit run 01-llm-arena/app.py --server.port 8501).

Two real fights against Azure (4 small calls per battle). Starts from a reset leaderboard; the battles' prompts are random (app behaviour).
After the recording, SCRATCH/result_*.json holds the on-screen texts and the app's elo.json for the script.
"""
import json
import shutil
from pathlib import Path

PORT = 8501
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "01-llm-arena"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g01")
FIGHTS = [("Concise", "Expert", 3), ("Pirate", "Step-by-step", 2)]    # (fighter A, fighter B, battles)
TRIM = {"empty": 8.5, "setup1": 6.5, "setup2": 6.5, "res1": 6.5, "res2": 6.5, "board1": 8.5, "board2": 8.5}
TRIM.update({f"f{k}b{j}": 8.5 for k in (1, 2) for j in (1, 2, 3)})  # the recorder moves on after ~9 s
CODE = {"battle": ("app.py", 63, 71), "judge": ("app.py", 52, 55), "elo": ("app.py", 43, 47)}
SECTIONS = [
    [("app", "f1b2"), ("app", "board1")],
    [("card", "Prompting styles, not different models|same model, different instruction"), ("card", "Five styles: concise, step by step, ELI5, pirate, expert"),
     ("card", "A second call judges|convenient, and a trap")],
    [("card", "One battle = 4 small calls|2 answers + 2 judge calls"), ("code", "battle"), ("code", "judge")],
    [("card", "Elo: everyone starts at 1000|a win over an equal = +16"), ("code", "elo")],
    [("app", "setup1"), ("app", "run1"), ("app", "res1"), ("app", "f1b1"), ("app", "f1b2"), ("app", "f1b3"), ("app", "board1")],
    [("app", "setup2"), ("app", "run2"), ("app", "res2"), ("app", "f2b1"), ("app", "f2b2"), ("app", "board2")],
    [("card", "The judge asked for concise|so concise wins by design"), ("card", "Same question, simple answer|styles collapse into one")],
    [("card", "Honest limits|5 battles, random prompts|ratings across fights are not comparable")],
    [("card", "Next: every pair against every pair|another judge model, editable rules"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.85}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.get_by_role("button", name="Fight!").wait_for(timeout=90000)
    page.wait_for_timeout(1500)


def _open_sidebar(page):
    if not page.locator("[data-testid=stSidebar]").get_by_role("combobox").first.is_visible():
        page.locator("[data-testid=stExpandSidebarButton], [data-testid=stSidebarCollapsedControl] button").first.click()
        page.wait_for_timeout(700)


def _pick(page, which, name):
    page.locator("[data-testid=stSidebar]").get_by_role("combobox").nth(which).click()
    page.wait_for_timeout(400)
    page.get_by_role("option", name=name, exact=True).click()
    page.wait_for_timeout(500)


def _top(page, y):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: y, behavior: 'smooth'}); }", y)


def record(page, mark):
    _open_sidebar(page)
    page.get_by_role("button", name="Reset leaderboard").click()
    page.wait_for_selector("text=No battles yet", timeout=30000)
    page.wait_for_timeout(1200)
    mark("empty")
    page.wait_for_timeout(9000)
    total = 0
    cur = 2   # the slider starts at 2 battles
    for k, (fa, fb, n) in enumerate(FIGHTS, 1):
        _open_sidebar(page)
        _pick(page, 0, fa)
        _pick(page, 1, fb)
        s = page.locator("[data-testid=stSidebar]").get_by_role("slider")
        s.focus()
        for _ in range(abs(n - cur)):
            page.keyboard.press("ArrowRight" if n > cur else "ArrowLeft")
        cur = n
        page.wait_for_timeout(600)
        mark(f"setup{k}")
        page.wait_for_timeout(7000)
        page.get_by_role("button", name="Fight!").click()
        page.wait_for_timeout(1500)
        mark(f"run{k}")
        total += n
        page.wait_for_selector(f"text={total} battles recorded", timeout=300000)
        page.wait_for_timeout(1500)
        mark(f"res{k}")
        page.wait_for_timeout(7000)
        # open each battle (newest fight's rows are the last n expanders) to show the two answers side by side
        rows = page.locator("[data-testid=stExpander] summary")
        cnt = rows.count()
        for j in range(n):
            row = rows.nth(cnt - n + j)
            row.scroll_into_view_if_needed()
            row.click()
            page.wait_for_timeout(1200)
            page.evaluate("(el) => el.scrollIntoView({behavior: 'smooth', block: 'start'})", row.element_handle())
            page.wait_for_timeout(1500)
            mark(f"f{k}b{j + 1}")
            page.wait_for_timeout(9000)
        _top(page, 100000)
        page.wait_for_timeout(1500)
        mark(f"board{k}")
        page.wait_for_timeout(9000)
        _top(page, 0)
        page.wait_for_timeout(800)
        shutil_copy = APP_DIR / "elo.json"
        (SCRATCH / f"elo_{k}.json").write_text(shutil_copy.read_text(encoding="utf-8"), encoding="utf-8")
    mark("end")
    page.wait_for_timeout(2000)
