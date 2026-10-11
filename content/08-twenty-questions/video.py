"""Spec for the 08 full video (tools/make_full.py 08). Needs the app on PORT (python -m streamlit run 08-twenty-questions/app.py --server.port 8508).

Both modes are played live against Azure (about 1 small call per question). After every turn the recorder writes
SCRATCH/req_<mode>_<n>.json and waits for SCRATCH/ans_<mode>_<n>.txt (my next question in mode A, or Yes/No/Sometimes/Correct/Nope in mode B).
"""
import json
import os
import time
from pathlib import Path

PORT = 8508
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "08-twenty-questions"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g08")
CODE = {"ask": ("app.py", 32, 35), "host": ("app.py", 55, 57), "turn": ("app.py", 74, 77)}
SECTIONS = [
    [("app", "a_q3"), ("app", "a_end"), ("app", "b_q4"), ("app", "b_q18")],
    [("card", "Two skills in one game|host: keep a secret honestly|guesser: ask questions that split"), ("card", "Both directions in one app|about 1 tiny call per question"),
     ("card", "Max 60 tokens per reply|a whole game costs very little")],
    [("card", "The secret is picked in Python|never sent to the player"), ("code", "ask"), ("code", "host")],
    [("app", "a_start"), ("app", "a_q1"), ("app", "a_q2"), ("app", "a_q3"), ("app", "a_q4"), ("app", "a_q5"), ("app", "a_q6"), ("app", "a_end")],
    [("card", "The guesser only sees the history|questions and answers so far"), ("code", "turn")],
    [("app", "b_start"), ("app", "b_q1"), ("app", "b_q5"), ("app", "b_q9"), ("app", "b_q14"), ("app", "b_q18"), ("app", "b_end")],
    [("card", "Good start: living? man-made? big?|then it wandered"), ("card", "Real questions are vague|the host has to say Sometimes")],
    [("card", "Honest limits|one game each way, not a benchmark|my own secrets and judgments")],
    [("card", "Next: a scoreboard and harder categories|measure questions needed over many objects"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:1.15}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.get_by_role("button", name="Start game").wait_for(timeout=90000)
    page.wait_for_timeout(1500)


def _wait(name):
    f = SCRATCH / name
    while not f.exists():
        time.sleep(1)
    return f.read_text(encoding="utf-8").strip()


def _chat(page):
    return page.locator("[data-testid=stChatMessage]")


def _dump(page, tag, n):
    msgs = _chat(page).all_inner_texts()
    alerts = page.locator("[data-testid=stAlert]").all_inner_texts()
    (SCRATCH / f"req_{tag}_{n}.json").write_text(json.dumps({"chat": msgs, "alerts": alerts}, ensure_ascii=False, indent=1), encoding="utf-8")


def _open_sidebar(page):
    if not page.locator("[data-testid=stSidebar]").get_by_text("GPT guesses your secret").is_visible():
        page.locator("[data-testid=stExpandSidebarButton], [data-testid=stSidebarCollapsedControl] button").first.click()
        page.wait_for_timeout(700)


def _wait_chat_growth(page, before, timeout=60000):
    page.wait_for_function("(n) => document.querySelectorAll('[data-testid=stChatMessage]').length > n", arg=before, timeout=timeout)
    page.wait_for_timeout(900)


def _wait_pending(page, before, timeout=60000):
    """Mode B: after an answer the log grows by 2 and GPT's next message (assistant avatar) is last, with no spinner."""
    page.wait_for_function("""(n) => { const m = document.querySelectorAll('[data-testid=stChatMessage]');
        return m.length >= n + 2 && m[m.length - 1].innerText.startsWith('smart_toy') && !document.querySelector('[data-testid=stSpinner]'); }""",
                           arg=before, timeout=timeout)
    page.wait_for_timeout(900)


def record(page, mark):
    # ---------- Mode A: I guess GPT's secret ----------
    mark("a_start")
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Start game").click()
    page.wait_for_selector("[data-testid=stChatInput] textarea", timeout=30000)
    page.wait_for_timeout(1200)
    mark("a_q0")
    n = 0
    while True:
        n += 1
        _dump(page, "a", n)
        q = _wait(f"ans_a_{n}.txt")
        if q == "STOP":
            break
        mark(f"a_q{n}")
        before = _chat(page).count()
        box = page.locator("[data-testid=stChatInput] textarea")
        box.click()
        page.keyboard.type(q, delay=35)
        page.wait_for_timeout(500)
        page.keyboard.press("Enter")
        try:
            _wait_chat_growth(page, before)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        if page.locator("[data-testid=stAlert]").count():
            break
    page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: m.scrollHeight, behavior: 'smooth'}); }")
    page.wait_for_timeout(1200)
    mark("a_end")
    _dump(page, "a", n + 1)
    page.wait_for_timeout(9000)
    if os.environ.get("G08_ONLY") == "a":
        return

    # ---------- Mode B: GPT guesses mine ----------
    _open_sidebar(page)
    page.locator("[data-testid=stSidebar]").get_by_text("GPT guesses your secret").click()
    page.wait_for_selector("button:has-text('Start game')", timeout=30000)
    page.wait_for_timeout(1500)
    mark("b_start")
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Start game").click()
    page.wait_for_selector("[data-testid=stChatMessage]", timeout=60000)
    page.wait_for_timeout(1500)
    n = 0
    while True:
        n += 1
        mark(f"b_q{n}")
        _dump(page, "b", n)
        ans = _wait(f"ans_b_{n}.txt")
        if page.locator("[data-testid=stAlert]").count() or ans == "STOP":
            break
        before = _chat(page).count()
        label = {"Yes": "Yes", "No": "No", "Sometimes": "Sometimes", "Correct": "Correct!", "Nope": "Nope"}[ans]
        page.get_by_role("button", name=label, exact=label in ("Yes", "No", "Sometimes")).click()
        if ans == "Correct":
            page.wait_for_selector("[data-testid=stAlert]", timeout=15000)
            page.wait_for_timeout(1500)
            break
        try:
            _wait_pending(page, before)
        except Exception:
            pass
        page.wait_for_timeout(1200)
        if page.locator("[data-testid=stAlert]").count():
            break
    mark("b_end")
    _dump(page, "b", n + 1)
    page.wait_for_timeout(9000)
