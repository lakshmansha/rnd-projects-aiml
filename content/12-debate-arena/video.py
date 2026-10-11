"""Spec for the 12 full video (tools/make_full.py 12). Needs the app on PORT (python -m streamlit run 12-debate-arena/app.py --server.port 8512).

Two real debates against Azure (2 rounds each = 5 small calls per debate). After each verdict the recorder writes SCRATCH/req_<n>.json
(transcript, verdict text) and waits for SCRATCH/after_<n>.txt (my opinion 0-10 after reading), then sets the 'after' slider.
"""
import json
import time
from pathlib import Path

PORT = 8512
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "12-debate-arena"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g12")
DEBATES = [("Pineapple belongs on pizza.", 4), ("Tabs are better than spaces.", 7)]   # (motion, my opinion before, 0-10)
TRIM = {}
for _n in (1, 2):  # keep only the static part of each scene (the recorder scrolls near the end of most of them)
    TRIM.update({f"d{_n}_setup": 3.0, f"d{_n}_ready": 4.0, f"d{_n}_turns": 2.0, f"d{_n}_turns2": 3.0,
                 f"d{_n}_verdict": 6.0, f"d{_n}_mind": 1.4, f"d{_n}_after": 7.5})
CODE = {"say": ("app.py", 36, 41), "judge": ("app.py", 45, 49)}
SECTIONS = [
    [("app", "d1_turns"), ("app", "d1_verdict")],
    [("card", "A model can argue any side|and sounds equally sure"), ("card", "Who judges?|LLM-as-a-judge, with the scores in view")],
    [("card", "Debater = a stance + the debate so far|about 60 words per speech"), ("code", "say")],
    [("card", "Judge = strict JSON scores|logic, evidence, persuasion, clarity, rebuttal"), ("code", "judge")],
    [("app", "d1_setup"), ("app", "d1_ready"), ("app", "d1_turns"), ("app", "d1_turns2"), ("app", "d1_verdict"), ("app", "d1_mind"), ("app", "d1_after")],
    [("app", "d2_setup"), ("app", "d2_ready"), ("app", "d2_turns"), ("app", "d2_turns2"), ("app", "d2_verdict"), ("app", "d2_mind"), ("app", "d2_after")],
    [("card", "Close results: 40-36 and 44-42|totals say little about why"), ("card", "Radar charts overlap|scores of 7-9 everywhere")],
    [("card", "Honest limits|two debates, one model in all three roles|no test for position bias")],
    [("card", "Next: swap the sides|a different model as judge, many runs"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:1.0}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.get_by_role("button", name="Start debate").wait_for(timeout=90000)
    page.wait_for_timeout(1500)


def _scroll_to(page, text, offset=-20):
    page.evaluate("""([t, off]) => {
        const m = document.querySelector('[data-testid=stMain]');
        const el = [...m.querySelectorAll('h1,h2,h3,p,div')].find(e => e.children.length < 3 && e.innerText && e.innerText.trim().startsWith(t));
        if (el) { const y = el.getBoundingClientRect().top - m.getBoundingClientRect().top + m.scrollTop + off; m.scrollTo({top: y, behavior: 'smooth'}); }
    }""", [text, offset])


def _set_slider(page, which, value, lo=0):
    s = page.get_by_role("slider").nth(which) if which >= 0 else page.get_by_role("slider").last
    s.focus()
    page.keyboard.press("Home")
    for _ in range(value - lo):
        page.keyboard.press("ArrowRight")
    page.wait_for_timeout(500)


def _wait(name):
    f = SCRATCH / name
    while not f.exists():
        time.sleep(1)
    return f.read_text(encoding="utf-8").strip()


def record(page, mark):
    for n, (motion, before) in enumerate(DEBATES, 1):
        mark(f"d{n}_setup")
        page.wait_for_timeout(3500)
        page.get_by_role("combobox").first.click()
        page.wait_for_timeout(500)
        page.get_by_role("option", name=motion).click()
        page.wait_for_timeout(900)
        _set_slider(page, 1, before)
        mark(f"d{n}_ready")
        page.wait_for_timeout(4500)
        page.get_by_role("button", name="Start debate").click()
        page.wait_for_selector(f"text=Motion: {motion}", timeout=120000)
        page.wait_for_selector("text=Verdict", timeout=120000)
        page.wait_for_timeout(1500)
        transcript = page.locator("[data-testid=stChatMessage]").all_inner_texts()
        _scroll_to(page, "Motion:")
        page.wait_for_timeout(1200)
        mark(f"d{n}_turns")
        page.wait_for_timeout(2000)
        page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollBy({top: 330, behavior: 'smooth'}); }")
        page.wait_for_timeout(3500)
        mark(f"d{n}_turns2")
        page.wait_for_timeout(3000)
        _scroll_to(page, "⚖️")
        page.wait_for_timeout(1500)
        mark(f"d{n}_verdict")
        main = page.locator("[data-testid=stMain]").inner_text()
        (SCRATCH / f"req_{n}.json").write_text(json.dumps({"transcript": transcript, "main": main}, ensure_ascii=False, indent=1), encoding="utf-8")
        after = int(_wait(f"after_{n}.txt"))
        _scroll_to(page, "Did they change")
        page.wait_for_timeout(1500)
        mark(f"d{n}_mind")
        page.wait_for_timeout(1500)
        _set_slider(page, -1, after)
        page.wait_for_timeout(1200)
        mark(f"d{n}_after")
        page.wait_for_timeout(8000)
        page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: 0}); }")
        page.wait_for_timeout(1000)
    mark("end")
    page.wait_for_timeout(3000)
