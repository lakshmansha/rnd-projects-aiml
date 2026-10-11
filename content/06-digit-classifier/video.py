"""Spec for the 06 full video (tools/make_full.py 06). Needs the app on PORT (python -m streamlit run 06-digit-classifier/app.py --server.port 8506)."""
from pathlib import Path

PORT = 8506
APP_DIR = Path(__file__).resolve().parents[2] / "06-digit-classifier"
CODE = {"train": ("app.py", 62, 78), "augment": ("app.py", 53, 60), "to8": ("app.py", 80, 92), "vote": ("app.py", 109, 112)}
SECTIONS = [
    [("app", "overview"), ("app", "draw7")],                                   # cold open
    [("card", "Why a digit classifier?|examples + labels|fit a model|test on unseen data"),
     ("card", "1,797 images|8 x 8 pixels|values 0 to 16"),
     ("card", "99% on the test split|is not|99% on YOUR handwriting")],       # why it matters
    [("card", "One file, ~120 lines|train - augment - convert - vote"), ("code", "train"), ("code", "augment"),
     ("code", "to8"), ("code", "vote")],                                       # build
    [("app", "overview"), ("app", "draw7"), ("app", "draw3"), ("app", "draw4")],   # demo
    [("code", "to8"), ("app", "table"), ("card", "A test score describes the test set,|not you")],        # surprises
    [("card", "Honest limits|8x8 pixels = a toy|no measured accuracy on my own drawings"), ("app", "draw4")],
    [("card", "Next: a CNN, or your own labelled drawings"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.wait_for_selector("canvas#cv", timeout=90000)
    page.wait_for_timeout(2500)


def _stroke(page, pts):
    page.mouse.move(*pts[0])
    page.mouse.down()
    for p in pts[1:]:
        page.mouse.move(*p, steps=8)
    page.mouse.up()


def _scroll(page, px):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]') || document.scrollingElement;"
                  " m.scrollBy({top: y, behavior: 'smooth'}); }", px)


def record(page, mark):
    b = page.locator("canvas#cv").bounding_box()
    x0, y0, w, h = b["x"], b["y"], b["width"], b["height"]
    P = lambda u, v: (x0 + u * w, y0 + v * h)
    clear = lambda: (page.locator("button#clr").click(), page.wait_for_timeout(1500))

    mark("overview")
    page.wait_for_timeout(9000)
    _scroll(page, 350)
    page.wait_for_timeout(7000)
    _scroll(page, -350)
    page.wait_for_timeout(5000)

    mark("draw7")
    _stroke(page, [P(.2, .2), P(.8, .2), P(.62, .5), P(.45, .8)])
    page.wait_for_timeout(9000)
    _scroll(page, 250)
    page.wait_for_timeout(9000)
    _scroll(page, -250)
    page.wait_for_timeout(8000)

    mark("draw3")
    clear()
    _stroke(page, [P(.25, .2), P(.7, .25), P(.45, .48), P(.7, .62), P(.65, .8), P(.25, .85)])
    page.wait_for_timeout(16000)

    mark("draw4")
    clear()
    _stroke(page, [P(.3, .15), P(.25, .55), P(.8, .55)])        # open-top messy four
    page.wait_for_timeout(1000)
    _stroke(page, [P(.62, .25), P(.62, .9)])
    page.wait_for_timeout(14000)
    _scroll(page, 250)
    page.wait_for_timeout(9000)
    _scroll(page, -250)
    page.wait_for_timeout(8000)

    mark("table")
    page.locator("text=Test accuracy").first.scroll_into_view_if_needed()
    page.wait_for_timeout(16000)
