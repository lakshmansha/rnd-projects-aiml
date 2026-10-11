"""Spec for the 09 full video (tools/make_full.py 09). Needs the app on PORT (python -m streamlit run 09-rl-gridworld/app.py --server.port 8509)."""
from pathlib import Path

PORT = 8509
QUERY = ""   # keep the sidebar (embed mode hides it)
APP_DIR = Path(__file__).resolve().parents[2] / "09-rl-gridworld"
CODE = {"consts": ("app.py", 14, 16), "full": ("app.py", 37, 56), "pick": ("app.py", 37, 42), "loop": ("app.py", 43, 53),
        "diff": ("app.py", 46, 50), "nudge": ("app.py", 48, 50), "snap": ("app.py", 41, 42), "greedy": ("app.py", 59, 66)}
SECTIONS = [
    [("app", "ep1"), ("app", "scrub")],                                                      # cold open
    [("card", "Supervised: given answers|RL: given a score"),
     ("card", "Explore to learn|but exploring near a cliff is expensive")],               # why
    [("app", "world"), ("code", "consts"), ("app", "world")],                               # the world
    [("code", "full"), ("code", "full"), ("code", "pick"), ("code", "loop"), ("code", "diff"), ("code", "nudge"),
     ("code", "snap"), ("code", "greedy")],                                                 # the code
    [("app", "ep1"), ("app", "scrub"), ("app", "end"), ("app", "chart"),
     ("card", "epsilon = 0|no random moves|both agents score the same: 38")],               # live demo
    [("card", "Optimal is not the same as safe"), ("card", "Q-learning learns the best path|SARSA learns the path it actually walks")],
    [("card", "Honest limits|a lookup table on a tiny grid"), ("app", "lava"), ("app", "doors")],
    [("card", "Next: a deep Q-network|draw your own cliff|add wind"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.wait_for_selector("[data-testid=stMain] input[type=range]", timeout=90000)
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important}")
    page.wait_for_timeout(3000)


def _slider(page):
    s = page.locator("[data-testid=stMain] input[type=range]").first
    s.focus()
    return s


def _scroll(page, px):
    page.evaluate("(y) => { const m = document.querySelector('[data-testid=stMain]') || document.scrollingElement;"
                  " m.scrollBy({top: y, behavior: 'smooth'}); }", px)


def _world(page, name):
    page.locator("[data-testid=stSidebar] [data-testid=stSelectbox]").first.click()
    page.get_by_role("option", name=name).click()
    page.wait_for_timeout(6000)
    _slider(page)
    page.keyboard.press("End")
    page.wait_for_timeout(2000)


def record(page, mark):
    _slider(page)
    page.keyboard.press("Home")
    page.wait_for_timeout(1500)
    mark("ep1")
    page.wait_for_timeout(22000)

    mark("scrub")
    _slider(page)
    for _ in range(39):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(430)

    mark("end")
    page.wait_for_timeout(24000)

    mark("chart")
    _scroll(page, 700)
    page.wait_for_timeout(32000)

    mark("world")
    _scroll(page, -1500)
    page.wait_for_timeout(22000)

    mark("lava")
    _world(page, "Lava maze")
    page.wait_for_timeout(18000)

    mark("doors")
    _world(page, "Two doors")
    page.wait_for_timeout(18000)
