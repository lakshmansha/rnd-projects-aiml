"""Spec for the 03 full video (tools/make_full.py 03). Needs the app on PORT (python -m streamlit run 03-semantic-map/app.py --server.port 8503).

Four real questions against Azure (1 small call each). The retrieved sentences and answers are saved to SCRATCH/q_<n>.txt for the script.
"""
import re
from pathlib import Path

PORT = 8503
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "03-semantic-map"
SCRATCH = Path(r"C:\Users\user\AppData\Local\Temp\claude\D--Research-Source-rnd-projects-aiml\ea7fa4bc-504b-41ae-882d-1a0e2d599e14\scratchpad\g03")
QUESTIONS = ["Why does bread rise?", "How do I stop my savings losing value over time?", "Which team won the most World Cups?", "Who painted the Mona Lisa?"]
TRIM = {"pca": 8.5}
for _n, _q in enumerate(QUESTIONS, 1):  # typing scene = typed question only; result scenes end before the recorder scrolls
    TRIM.update({f"q{_n}t": len(_q) * 0.045 + 0.4, f"q{_n}": 4.5, f"q{_n}r": 8.5})
CODE = {"embed": ("../common/llm.py", 49, 54), "search": ("app.py", 52, 55), "rag": ("app.py", 75, 78)}
SECTIONS = [
    [("app", "q1"), ("app", "q1r")],
    [("card", "RAG = retrieve, then generate|the model reads only what you hand it"), ("card", "An embedding is a list of numbers|similar texts, similar lists")],
    [("card", "No embedding model deployed|so: character n-gram hashing, free and local"), ("code", "embed")],
    [("code", "search"), ("code", "rag")],
    [("app", "map"), ("app", "pca")],
    [("app", "q1t"), ("app", "q1"), ("app", "q1r")],
    [("app", "q2t"), ("app", "q2r")],
    [("app", "q3t"), ("app", "q3r"), ("app", "q4t"), ("app", "q4r")],
    [("card", "3 of 4 answers: I don't know|retrieval was not enough, and the prompt said so"), ("card", "Good matches score low|about 0.28 with character n-grams")],
    [("card", "Honest limits|60 sentences, character hashes, 4 questions|top-k is fixed, noise gets through")],
    [("card", "Next: a real embedding model|similarity cut-off, longer documents"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.85}")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for f in SCRATCH.iterdir():
        f.unlink()
    page.wait_for_selector(".js-plotly-plot", timeout=180000)
    page.wait_for_timeout(2500)


def _top(page, y):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: y, behavior: 'smooth'}); }", y)


def _open_sidebar(page):
    if not page.locator("[data-testid=stSidebar]").get_by_text("Projection").first.is_visible():
        page.locator("[data-testid=stExpandSidebarButton], [data-testid=stSidebarCollapsedControl] button").first.click()
        page.wait_for_timeout(700)


def record(page, mark):
    mark("map")
    page.wait_for_timeout(11000)

    _open_sidebar(page)
    page.locator("[data-testid=stSidebar]").get_by_text("PCA", exact=True).click()
    page.wait_for_selector(".js-plotly-plot", timeout=60000)
    page.wait_for_timeout(1500)
    mark("pca")
    page.wait_for_timeout(9000)
    page.locator("[data-testid=stSidebar]").get_by_text("t-SNE", exact=True).click()
    page.wait_for_timeout(4000)

    box = page.get_by_placeholder("e.g. Why does bread rise?")
    for n, q in enumerate(QUESTIONS, 1):
        box.click()
        box.fill("")
        page.wait_for_timeout(600)
        mark(f"q{n}t")
        page.keyboard.type(q, delay=45)
        page.wait_for_timeout(500)
        page.keyboard.press("Enter")
        page.wait_for_selector("text=RAG answer", timeout=90000)
        page.get_by_text(re.compile(r"^\d+\.\ds$")).wait_for(timeout=90000)
        page.wait_for_timeout(2500)
        mark(f"q{n}")
        page.wait_for_timeout(5000)
        _top(page, 520)
        page.wait_for_timeout(1500)
        mark(f"q{n}r")
        page.wait_for_timeout(9000)
        (SCRATCH / f"q_{n}.txt").write_text(page.locator("[data-testid=stMain]").inner_text(), encoding="utf-8")
        _top(page, 0)
        page.wait_for_timeout(1200)
    mark("end")
    page.wait_for_timeout(2000)
