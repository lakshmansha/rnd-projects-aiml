"""Spec for the 07 full video (tools/make_full.py 07). Needs the app on PORT (python -m streamlit run 07-tiny-gpt/app.py --server.port 8507)."""
from pathlib import Path

PORT = 8507
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "07-tiny-gpt"
FIT = {"train"}      # time-lapse the real training run to the narration length
CODE = {"block": ("model.py", 7, 20), "gpt": ("model.py", 22, 35), "batch": ("model.py", 59, 62), "gen": ("model.py", 36, 45)}
SECTIONS = [
    [("app", "app0"), ("app", "train")],                                                        # cold open
    [("card", "Why build a tiny GPT?|the same ingredients as a chatbot|just much smaller"),
     ("card", "818,176 parameters|65 characters|no tokenizer")],                                 # why
    [("card", "model.py|about 70 lines of PyTorch"), ("code", "block"), ("code", "gpt"), ("code", "batch"), ("code", "gen")],
    [("app", "app0"), ("app", "train"), ("app", "samples"), ("app", "gen"), ("app", "gen_low"), ("app", "gen_high")],
    [("card", "Structure is cheap|meaning is expensive"), ("card", "Temperature changes the personality|same model, same weights")],
    [("card", "Honest limits|looks like a play|does not make sense"), ("card", "Context: 128 characters max|~4-6 steps/s on my CPU")],
    [("card", "Next: attention visualiser"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important}")
    page.wait_for_selector("text=Train from scratch", timeout=90000)
    page.wait_for_timeout(2500)


def _scroll_to(page, text):
    page.locator(f"text={text}").first.scroll_into_view_if_needed()


def record(page, mark):
    mark("app0")
    page.wait_for_timeout(9000)

    mark("train")
    page.get_by_role("button", name="Train from scratch").click()
    page.wait_for_selector("text=Done in", timeout=600000)
    page.wait_for_timeout(1500)

    mark("samples")
    _scroll_to(page, "What the model writes as it learns")
    page.wait_for_timeout(8000)
    page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollBy({top: 500, behavior: 'smooth'}); }")
    page.wait_for_timeout(9000)
    page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollBy({top: 700, behavior: 'smooth'}); }")
    page.wait_for_timeout(9000)

    mark("gen")
    _scroll_to(page, "Generate with your trained model")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Generate").click()
    page.wait_for_timeout(14000)

    mark("gen_low")
    sl = page.get_by_role("slider", name="Temperature")
    sl.focus()
    page.keyboard.press("Home")
    page.wait_for_timeout(1500)
    page.get_by_role("button", name="Generate").click()
    page.wait_for_timeout(14000)

    mark("gen_high")
    sl.focus()
    page.keyboard.press("End")
    page.keyboard.press("ArrowLeft")
    page.wait_for_timeout(1500)
    page.get_by_role("button", name="Generate").click()
    page.wait_for_timeout(14000)
