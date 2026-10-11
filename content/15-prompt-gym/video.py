"""Spec for the 15 full video (tools/make_full.py 15). Needs the app on PORT (python -m streamlit run 15-prompt-gym/app.py --server.port 8515).

Played live against Azure (1 small call per attempt). Before each attempt the recorder writes SCRATCH/req_<n>.json (level, goal, last result)
and waits for SCRATCH/prompt_<n>.txt (the prompt I write; the single word STOP ends the session).
"""
import json
import time
from pathlib import Path

PORT = 8515
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "15-prompt-gym"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g15")
PROMPTS = [  # the ten prompts I wrote in the first (interactive) recording; replayed so the verdict is in view
    "Say banana.",
    "Reply with exactly one word: banana. Lowercase only, no punctuation, no emoji, nothing else.",
    "What is the sentiment of this review?",
    "Classify the sentiment of the review below as positive, negative or mixed. Answer with only that one lowercase word.",
    "Extract the people, the city and the date from the text and return them as JSON with keys person, city and date.",
    "Extract the people, the city and the date from the text. Return only valid JSON with keys person (a list), city and date. Do not use markdown code fences and do not add any commentary.",
    "Summarise the text in exactly 10 words.",
    "Write 3 short bullet points about the topic below.",
    "Write exactly 3 markdown bullets, each starting with '- ', about the topic below. Each bullet must be at most 6 words. No introduction and no closing line, only the 3 bullets.",
    "Translate the text into Spanish and end every sentence with an exclamation mark.",
]
CODE = {"json": ("app.py", 22, 26), "run": ("app.py", 72, 79)}
SECTIONS = [
    [("app", "t1"), ("app", "o1")],
    [("card", "Prompting is easy until|code has to read the answer"), ("card", "Goal + input + a Python checker|pass or fail, no opinions"),
     ("card", "Stars: 3 first try|2 within 3 tries, then 1")],
    [("card", "A checker is just a function|output in, pass/fail out"), ("code", "json"), ("code", "run")],
    [("app", "g1"), ("app", "t1"), ("app", "o1"), ("app", "t2"), ("app", "o2")],
    [("app", "g3"), ("app", "t3"), ("app", "o3"), ("app", "t4"), ("app", "o4")],
    [("app", "g5"), ("app", "t5"), ("app", "o5"), ("app", "t6"), ("app", "o6")],
    [("app", "g7"), ("app", "t7"), ("app", "o7")],
    [("app", "g8"), ("app", "t8"), ("app", "o8"), ("app", "t9"), ("app", "o9")],
    [("app", "g10"), ("app", "t10"), ("app", "o10")],
    [("app", "final")],
    [("card", "Name the format|the allowed values, the limits, what to leave out"), ("card", "A failed attempt is feedback|the checker prints what it saw")],
    [("card", "Honest limits|one person, one model, one run|my own checkers")],
    [("card", "Next: few-shot levels and refusal levels|same prompts on several models"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:1.0}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.wait_for_selector("[data-testid=stTextArea] textarea", timeout=90000)
    page.wait_for_timeout(1500)


def _wait(name):
    f = SCRATCH / name
    while not f.exists():
        time.sleep(1)
    return f.read_text(encoding="utf-8").strip()


def record(page, mark):
    n = 0
    last = ""
    log = []
    while True:
        n += 1
        mark(f"g{n}")
        main = page.locator("[data-testid=stMain]").inner_text()
        side = page.locator("[data-testid=stSidebar]").inner_text() if page.locator("[data-testid=stSidebar]").count() else ""
        (SCRATCH / f"req_{n}.json").write_text(json.dumps({"main": main, "sidebar": side}, ensure_ascii=False, indent=1), encoding="utf-8")
        prompt = PROMPTS[n - 1] if n <= len(PROMPTS) else "STOP"
        if prompt == "STOP":
            break
        box = page.locator("[data-testid=stTextArea] textarea")
        box.click()
        box.fill("")
        mark(f"t{n}")
        page.keyboard.type(prompt, delay=22)
        page.keyboard.press("Control+Enter")   # commit the text area so Run is enabled
        page.wait_for_timeout(1500)
        mark(f"r{n}")
        page.get_by_role("button", name="Run").click()
        page.wait_for_timeout(1200)
        page.wait_for_function("() => !document.querySelector('[data-testid=stStatusWidget]')", timeout=60000)
        page.wait_for_timeout(2500)
        page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: m.scrollHeight, behavior: 'smooth'}); }")
        page.wait_for_timeout(1200)
        mark(f"o{n}")
        page.wait_for_timeout(8000)
        log.append({"n": n, "prompt": prompt})
        (SCRATCH / f"out_{n}.txt").write_text(page.locator("[data-testid=stMain]").inner_text(), encoding="utf-8")
        (SCRATCH / "log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
        page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: 0}); }")
    mark("final")
    page.wait_for_timeout(8000)
