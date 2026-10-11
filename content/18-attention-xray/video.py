"""Spec for the 18 full video (tools/make_full.py 18). Needs the app on PORT (python -m streamlit run 18-attention-xray/app.py --server.port 8518)."""
from pathlib import Path

PORT = 8518
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "18-attention-xray"
CODE = {"xray": ("app.py", 38, 52)}
SECTIONS = [
    [("app", "idle"), ("app", "l1")],
    [("card", "The famous diagram|is usually drawn by hand"), ("card", "Here: a real model small enough to train on a CPU"),
     ("card", "Query x key match -> softmax -> heatmap|causal: only look backwards")],
    [("card", "Reuse the model from project 7|ask the attention layer for its weights"), ("code", "xray")],
    [("app", "l1"), ("app", "l2"), ("app", "l4")],
    [("app", "pred0"), ("app", "pred5"), ("app", "pred22"), ("app", "pred20")],
    [("card", "An attention map is a clue, not an explanation"), ("card", "One model, one seed, a modest sample|treat the percentages as examples")],
    [("card", "Next: watch the heads form during training|knock out a head and measure"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.62}")
    page.wait_for_selector("text=Layer 1, head 1", timeout=90000)
    page.wait_for_timeout(3000)


def _layer(page, n):
    page.locator("[data-testid=stRadio] label").nth(n).click()
    page.wait_for_timeout(2500)


def _pos(page, pos):
    s = page.locator("[data-testid=stMain] input[type=range]").first
    s.focus()
    page.keyboard.press("Home")
    for _ in range(pos):
        page.keyboard.press("ArrowRight")
    page.wait_for_timeout(2500)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(9000)

    mark("l1")
    page.wait_for_timeout(26000)

    mark("l2")
    _layer(page, 2)
    page.wait_for_timeout(14000)

    mark("l4")
    _layer(page, 4)
    page.wait_for_timeout(16000)

    mark("pred0")
    _layer(page, 1)
    page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: m.scrollHeight, behavior: 'smooth'}); }")
    page.wait_for_timeout(9000)

    mark("pred5")
    _pos(page, 5)
    page.wait_for_timeout(14000)

    mark("pred22")
    _pos(page, 22)
    page.wait_for_timeout(14000)

    mark("pred20")
    _pos(page, 20)
    page.wait_for_timeout(14000)
