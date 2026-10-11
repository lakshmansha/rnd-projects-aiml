"""Spec for the 11 full video (tools/make_full.py 11). Needs the app on PORT (python -m streamlit run 11-token-xray/app.py --server.port 8511)."""
from pathlib import Path

PORT = 8511
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "11-token-xray"
CODE = {"split": ("app.py", 35, 42), "chips": ("app.py", 52, 56)}
SECTIONS = [
    [("app", "idle"), ("app", "straw")],
    [("card", "LLMs never see letters|they see token IDs"), ("card", "A token is a chunk of text|a word, part of a word, a space or a symbol"),
     ("card", "Tokens decide what you pay|and what fits in the context window")],
    [("card", "A tokenizer is a fixed vocabulary|text in, integer IDs out"), ("code", "split"), ("code", "chips")],
    [("app", "straw"), ("app", "ids"), ("app", "straw")],
    [("app", "num"), ("app", "num")],
    [("app", "lang"), ("app", "lang2"), ("app", "lang2")],
    [("app", "emoji"), ("app", "cost")],
    [("card", "Strawberry is one token|so the model has to remember its spelling"), ("card", "Same text, other vocabulary|21 tokens vs 41 tokens")],
    [("card", "Honest limits|two OpenAI vocabularies only|no model is run, this is tokenisation only")],
    [("card", "Next: compare more tokenizers|show the token IDs side by side"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.8}")
    page.get_by_text("Chars per token").first.wait_for(timeout=60000)
    page.wait_for_timeout(2500)


def _top(page, y):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo({top: y, behavior: 'smooth'}); }", y)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(9000)

    mark("straw")
    page.wait_for_timeout(12000)

    mark("ids")
    page.get_by_text("Token IDs").first.click()
    page.wait_for_timeout(9000)
    page.get_by_text("Token IDs").first.click()
    page.wait_for_timeout(1000)

    mark("num")
    page.get_by_role("button", name="Numbers").click()
    page.wait_for_timeout(15000)

    mark("lang")
    page.get_by_role("button", name="Other languages").click()
    page.wait_for_timeout(11000)

    mark("lang2")
    page.get_by_role("tab", name="cl100k_base").click()
    page.wait_for_timeout(5000)
    _top(page, 400)
    page.wait_for_timeout(9000)
    _top(page, 0)
    page.get_by_role("tab", name="o200k_base").click()
    page.wait_for_timeout(1000)

    mark("emoji")
    page.get_by_role("button", name="Emoji").click()
    page.wait_for_timeout(12000)

    mark("cost")
    _top(page, 500)
    page.wait_for_timeout(14000)
