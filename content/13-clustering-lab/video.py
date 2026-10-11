"""Spec for the 13 full video (tools/make_full.py 13). Needs the app on PORT (python -m streamlit run 13-clustering-lab/app.py --server.port 8513)."""
from pathlib import Path

PORT = 8513
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "13-clustering-lab"
CODE = {"kmeans": ("app.py", 41, 50), "algos": ("app.py", 73, 76)}
SECTIONS = [
    [("app", "idle"), ("app", "steps")],
    [("card", "Unsupervised learning|no labels, find the groups"), ("card", "K-means: assign, move, repeat"),
     ("card", "But what if the groups are not round?")],
    [("card", "K-means in a few lines|pick k points, then loop"), ("code", "kmeans"), ("code", "kmeans")],
    [("app", "i0"), ("app", "steps"), ("app", "conv")],
    [("app", "elbow"), ("app", "elbow")],
    [("card", "Four algorithms|five datasets|one grid"), ("code", "algos"), ("app", "show")],
    [("app", "show"), ("app", "show2"), ("app", "show3")],
    [("card", "No algorithm wins everywhere|the data's shape picks the winner")],
    [("card", "Honest limits|2-D toy data, default settings|scores computed offline, not shown in the app")],
    [("card", "Next: your own CSV|silhouette score and a cluster-count finder"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.8}")
    page.wait_for_selector(".js-plotly-plot", state="attached", timeout=60000)
    page.get_by_role("tab", name="Algorithm showdown").click()
    page.wait_for_selector(".js-plotly-plot", state="attached", timeout=60000)
    page.wait_for_timeout(4000)
    page.get_by_role("tab", name="K-means step by step").click()
    page.wait_for_timeout(2500)


def _top(page, y):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: y, behavior: 'smooth'}); }", y)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(10000)

    mark("i0")
    sl = page.get_by_role("slider", name="Iteration")
    sl.focus()
    page.keyboard.press("Home")
    page.wait_for_timeout(9000)

    mark("steps")
    for i in range(8):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(2600)

    mark("conv")
    page.wait_for_timeout(9000)

    page.get_by_text("Elbow chart").click()
    page.wait_for_timeout(3000)
    mark("elbow")
    _top(page, 500)
    page.wait_for_timeout(14000)
    _top(page, 0)
    page.wait_for_timeout(500)

    page.get_by_role("tab", name="Algorithm showdown").click()
    page.wait_for_timeout(3500)
    mark("show")
    page.wait_for_timeout(9000)

    mark("show2")
    _top(page, 380)
    page.wait_for_timeout(14000)

    mark("show3")
    _top(page, 900)
    page.wait_for_timeout(14000)
