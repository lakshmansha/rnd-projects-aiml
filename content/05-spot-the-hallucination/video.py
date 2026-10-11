"""Spec for the 05 full video (tools/make_full.py 05). Needs the app on PORT (python -m streamlit run 05-spot-the-hallucination/app.py --server.port 8505).

The recording plays real rounds against Azure (1 call per round). After each round is shown, the statements are written to
SCRATCH/req_N.json and the recorder waits for SCRATCH/choice_N.txt (0-4), so the picks are genuine reads, not a script.
"""
import json
import time
from pathlib import Path

PORT = 8505
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "05-spot-the-hallucination"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g05")
TOPICS = ["Space", "Programming", "Human body", "Geography"]
CROPS = {f"{k}{n}": (470, 140, 960) for k in ("r", "pick") for n in range(1, 5)}
TRIM = {f"pick{n}": 8.6 for n in range(1, 5)}  # after ~9 s the recorder moves on to the next round
CODE = {"prompt": ("app.py", 30, 35), "play": ("app.py", 47, 52)}
SECTIONS = [
    [("app", "r1")],
    [("card", "LLMs state falsehoods|in the same tone as facts"), ("card", "4 true statements, 1 subtly false|find the fake"),
     ("card", "You feel it, instead of reading about it")],
    [("card", "One prompt|strict JSON back"), ("code", "prompt"), ("code", "play")],
    [("app", "r1"), ("app", "pick1")],
    [("app", "r2"), ("app", "pick2")],
    [("app", "r3"), ("app", "pick3"), ("app", "r4"), ("app", "pick4")],
    [("app", "score")],
    [("card", "The answer key can be wrong too|GPT writes the fake and the correction"), ("card", "Asking GPT to check GPT|does not fix it")],
    [("card", "Honest limits|4 rounds, my own knowledge|no fact-checking in the app")],
    [("card", "Next: check answers against a source|difficulty and a leaderboard"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:1.15}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.wait_for_selector("[data-testid=stRadio] label", timeout=90000)
    page.wait_for_timeout(1500)


def _ask(page, n, topic):
    labels = page.locator("[data-testid=stRadio] label").all_inner_texts()
    (SCRATCH / f"req_{n}.json").write_text(json.dumps({"topic": topic, "statements": labels[1:]}, ensure_ascii=False), encoding="utf-8")
    f = SCRATCH / f"choice_{n}.txt"
    while not f.exists():
        time.sleep(1)
    return int(f.read_text().strip())


def _open_sidebar(page):
    if not page.locator("[data-testid=stSidebar]").get_by_role("combobox").is_visible():
        page.locator("[data-testid=stExpandSidebarButton], [data-testid=stSidebarCollapsedControl] button").first.click()
        page.wait_for_timeout(700)


def _topic(page, name):
    _open_sidebar(page)
    page.locator("[data-testid=stSidebar]").get_by_role("combobox").click()
    page.wait_for_timeout(400)
    page.get_by_role("option", name=name).click()
    page.wait_for_timeout(600)
    page.wait_for_timeout(500)


def record(page, mark):
    results = []
    for n, topic in enumerate(TOPICS, 1):
        if n > 1:
            _topic(page, topic)
            page.get_by_role("button", name="New round").click()
            page.wait_for_timeout(2500)
            page.wait_for_selector("[data-testid=stRadio] label", timeout=60000)
            page.wait_for_timeout(1500)
        mark(f"r{n}")
        page.wait_for_timeout(1000)
        c = _ask(page, n, topic)
        mark(f"look{n}")           # (the pause while a reader decides is in this scene; only its first seconds are used)
        page.wait_for_timeout(500)
        page.locator("[data-testid=stRadio] label").nth(1 + c).click()
        page.wait_for_selector("[data-testid=stAlert]", timeout=15000)
        page.wait_for_timeout(600)
        mark(f"pick{n}")
        page.wait_for_timeout(9000)
        txt = " | ".join(page.locator("[data-testid=stAlert]").all_inner_texts())
        score = page.locator("[data-testid=stSidebar]").inner_text() if page.locator("[data-testid=stSidebar]").count() else ""
        results.append({"n": n, "topic": topic, "choice": c, "alerts": txt})
        (SCRATCH / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    _open_sidebar(page)
    page.wait_for_timeout(1500)
    mark("score")
    results.append({"score": page.locator("[data-testid=stSidebar]").inner_text()})
    (SCRATCH / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    page.wait_for_timeout(8000)
