"""Spec for the 17 full video (tools/make_full.py 17). Needs the app on PORT (python -m streamlit run 17-flappy-evolution/app.py --server.port 8517)."""
from pathlib import Path

PORT = 8517
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "17-flappy-evolution"
FIT = {"run"}       # stretch the real evolution run (about 25 s) to the narration
CODE = {"course": ("app.py", 18, 20), "think": ("app.py", 27, 29), "gen": ("app.py", 41, 50), "evo": ("app.py", 74, 88)}
SECTIONS = [
    [("app", "idle"), ("app", "run")],
    [("card", "Gradient descent needs labelled examples"), ("card", "A game only tells you how far you got|score in, evolution out"),
     ("card", "Neuroevolution: try - score - breed - mutate - repeat")],
    [("card", "The game|gravity - flap - pipes|fitness = steps survived"), ("code", "course"), ("code", "think")],
    [("code", "gen"), ("code", "gen")],
    [("card", "Selection - crossover - mutation"), ("code", "evo")],
    [("app", "idle"), ("app", "run"), ("app", "end")],
    [("card", "Making the game fair mattered|as much as the evolution code"), ("card", "The seed matters|seed 2: 3 generations|seed 3: 7|seed 4: 8")],
    [("card", "Honest limits|same course every generation|a toy, not real Flappy Bird")],
    [("card", "Next: a fresh course every generation|draw your own course"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.85}")
    page.wait_for_selector("button:has-text('Evolve')", timeout=60000)
    page.wait_for_timeout(2000)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(9000)

    mark("run")
    page.get_by_role("button", name="Evolve").click()
    page.wait_for_selector("text=learned to play", timeout=240000)
    page.wait_for_timeout(1500)

    mark("end")
    page.wait_for_timeout(14000)
