"""Spec for the 04 full video (tools/make_full.py 04). Needs the app on PORT (python -m streamlit run 04-neural-playground/app.py --server.port 8504)."""
from pathlib import Path

PORT = 8504
QUERY = ""
APP_DIR = Path(__file__).resolve().parents[2] / "04-neural-playground"
FIT = {"run", "run2"}
CODE = {"fwd": ("app.py", 40, 45), "step": ("app.py", 47, 58)}
SECTIONS = [
    [("app", "idle"), ("app", "run")],
    [("card", "A decision boundary|is the line between the classes"), ("card", "A network bends it|by adjusting weights"),
     ("card", "Backprop from scratch|numpy only, no framework")],
    [("card", "Layers of weights and an activation|input -> 8 -> 8 -> 1"), ("code", "fwd")],
    [("code", "step"), ("code", "step")],
    [("app", "idle"), ("app", "run"), ("app", "end"), ("app", "run2"), ("app", "end2")],
    [("card", "Capacity decides what can be learned|too small: training cannot help")],
    [("card", "Honest limits|one dataset, one seed|full-batch gradient descent, toy sizes")],
    [("card", "Next: watch single neurons|add dropout and regularisation"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.8}")
    page.wait_for_selector("button:has-text('Train')", timeout=60000)
    page.wait_for_timeout(2500)


def record(page, mark):
    mark("idle")
    page.wait_for_timeout(9000)

    mark("run")
    page.get_by_role("button", name="Train").click()
    page.wait_for_selector("text=1500 /", timeout=240000)
    page.wait_for_timeout(1500)

    mark("end")
    print("RESULT 8,8:", page.locator("[data-testid=stMetric]").first.inner_text().replace("\n", " "))
    page.wait_for_timeout(12000)

    box = page.get_by_label("Hidden layers")
    box.fill("2")
    box.press("Enter")
    page.wait_for_timeout(2500)
    mark("run2")
    page.get_by_role("button", name="Train").click()
    page.wait_for_selector("text=1500 /", timeout=240000)
    page.wait_for_timeout(1500)

    mark("end2")
    print("RESULT 2:", page.locator("[data-testid=stMetric]").first.inner_text().replace("\n", " "))
    page.wait_for_timeout(12000)
