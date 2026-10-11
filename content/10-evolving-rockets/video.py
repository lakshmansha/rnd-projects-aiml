"""Spec for the 10 full video (tools/make_full.py 10). Needs the app on PORT (python -m streamlit run 10-evolving-rockets/app.py --server.port 8510)."""
from pathlib import Path

PORT = 8510
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "10-evolving-rockets"
CODE = {"phys": ("app.py", 27, 30), "fit": ("app.py", 43, 46), "all": ("app.py", 49, 71), "elite": ("app.py", 61, 63),
        "select": ("app.py", 63, 64), "cross": ("app.py", 65, 66), "mut": ("app.py", 67, 69), "concat": ("app.py", 70, 71),
        "init": ("app.py", 52, 53)}
SECTIONS = [
    [("app", "gen1"), ("app", "scrub")],                                                      # cold open
    [("card", "Try - score - keep the best|mix - mutate"), ("card", "Evolution works on anything you can score|no gradients needed")],
    [("card", "DNA = 140 thrusts|(x, y) per time step"), ("code", "phys"), ("code", "fit")],  # DNA, physics, fitness
    [("code", "all"), ("code", "all"), ("code", "elite"), ("code", "select"), ("code", "cross"), ("code", "mut"),
     ("code", "concat"), ("code", "init")],                                                    # evolve()
    [("app", "overview"), ("app", "gen1"), ("app", "scrub"), ("app", "end"), ("app", "levels")],   # live demo
    [("card", "Selection + noise = a route"), ("card", "Mutation rate matters|too high scrambles a good route|too low can get stuck")],
    [("app", "zig"), ("card", "Honest limits|fixed open-loop DNA, no sensors|one seed = one sample")],
    [("card", "Next: evolve a neural network|moving obstacles|draw your own walls"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important}")
    page.wait_for_selector("[data-testid=stMain] input[type=range]", timeout=90000)
    page.wait_for_timeout(3000)


def _slider(page):
    s = page.locator("[data-testid=stMain] input[type=range]").first
    s.focus()


def _level(page, name):
    page.locator("[data-testid=stSidebar] [data-testid=stSelectbox]").first.click()
    page.get_by_role("option", name=name).click()
    page.wait_for_timeout(5000)


def record(page, mark):
    mark("overview")
    page.wait_for_timeout(16000)

    mark("gen1")
    _slider(page)
    page.keyboard.press("Home")
    page.wait_for_timeout(20000)

    mark("scrub")
    _slider(page)
    for _ in range(79):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(360)

    mark("end")
    page.wait_for_timeout(24000)

    mark("levels")
    for name in ("Open sky", "Wall", "Gap"):
        _level(page, name)
        _slider(page)
        page.keyboard.press("End")
        page.wait_for_timeout(6500)

    mark("zig")
    _level(page, "Zig-zag")
    _slider(page)
    page.keyboard.press("End")
    page.wait_for_timeout(22000)
