"""Spec for the 14 full video (tools/make_full.py 14). Needs the app on PORT (python -m streamlit run 14-explainable-text-ai/app.py --server.port 8514)."""
from pathlib import Path

PORT = 8514
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "14-explainable-text-ai"
CODE = {"train": ("app.py", 34, 37), "contrib": ("app.py", 68, 73)}
SECTIONS = [
    [("app", "idle"), ("app", "tricky")],
    [("card", "A black box says: Space|but not why"), ("card", "Classic model: TF-IDF + logistic regression|one weight per word"),
     ("card", "Every word's push can be read off|green: toward the answer, red: away")],
    [("card", "Train on real newsgroup posts|~3,500 posts, 6 topics"), ("code", "train")],
    [("card", "Push = (weight gap between top two topics) x TF-IDF"), ("code", "contrib"), ("code", "contrib")],
    [("app", "idle"), ("app", "idle2"), ("app", "tricky"), ("app", "tricky")],
    [("app", "words"), ("app", "words")],
    [("app", "confused"), ("app", "confused")],
    [("card", "Why this is useful|you can see the model is right for the right reasons")],
    [("card", "Honest limits|84.8% accuracy on 6 topics|newsgroup language from the 1990s")],
    [("card", "Next: your own labelled text|compare with a neural model"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.8}")
    page.wait_for_selector("text=Accuracy on unseen posts", timeout=240000)
    page.wait_for_selector("text=Why Space", timeout=60000)
    page.wait_for_timeout(2500)


def _top(page, y):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: y, behavior: 'smooth'}); }", y)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(14000)

    page.get_by_role("button", name="Hockey").click()
    page.wait_for_selector("text=Why Hockey", timeout=30000)
    page.wait_for_timeout(800)
    mark("idle2")
    page.wait_for_timeout(11000)

    page.get_by_role("button", name="Tricky").click()
    page.wait_for_selector("text=53% confident", timeout=30000)
    page.wait_for_timeout(800)
    mark("tricky")
    page.wait_for_timeout(16000)

    page.get_by_role("tab", name="What each topic's words are").click()
    page.wait_for_timeout(2500)
    mark("words")
    page.locator("[data-testid=stSelectbox]").first.click()
    page.wait_for_timeout(800)
    page.get_by_role("option", name="Space").click()
    page.wait_for_timeout(14000)

    page.get_by_role("tab", name="Where it gets confused").click()
    page.wait_for_timeout(2500)
    mark("confused")
    page.wait_for_timeout(16000)
