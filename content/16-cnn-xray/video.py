"""Spec for the 16 full video (tools/make_full.py 16). Needs the app on PORT (python -m streamlit run 16-cnn-xray/app.py --server.port 8516)."""
import json
from pathlib import Path

PORT = 8516
QUERY = "?sample=banana.jpg"
APP_DIR = Path(__file__).resolve().parents[2] / "16-cnn-xray"
CODE = {"load": ("app.py", 22, 25), "full": ("app.py", 28, 44), "hook": ("app.py", 29, 31), "fwd": ("app.py", 32, 37),
        "grad": ("app.py", 36, 39), "cam": ("app.py", 40, 44), "pick": ("app.py", 82, 85), "heat": ("app.py", 47, 53)}
SECTIONS = [
    [("app", "banana")],                                                                     # cold open
    [("card", "A label and a confidence number|says nothing about WHY"), ("card", "Right for the wrong reason|the husky-on-snow problem"),
     ("card", "Grad-CAM: gradients -> a heat map|red = pixels that pushed the decision")],
    [("card", "CNN: edges - textures - parts - objects"), ("card", "Grad-CAM recipe|weight each feature map by its mean gradient|sum - ReLU - upsample"),
     ("card", "MobileNetV2|3.5M parameters|no GPU, no API calls")],
    [("code", "load"), ("code", "full"), ("code", "hook"), ("code", "fwd"), ("code", "grad"), ("code", "cam"), ("code", "pick"), ("code", "heat")],
    [("app", "banana"), ("app", "alpha"), ("app", "cat"), ("app", "cat2"), ("app", "dog"), ("app", "dog2"), ("app", "pizza"),
     ("app", "pizza2"), ("card", "Upload a photo or use the webcam|try something weird")],
    [("card", "Low confidence is normal|ImageNet splits the world into fine categories"), ("card", "The runner-up has its own evidence|a single number hides it"),
     ("card", "A heat map looks convincing|it is a coarse picture")],
    [("card", "Honest limits|Grad-CAM is low resolution"), ("card", "Only 1,000 ImageNet classes|it always picks one, even when it should not")],
    [("card", "Next: attention visualiser for the tiny GPT|a bigger network|the husky-on-snow bias demo"), ("card", "Watch It Learn|follow for more AI/ML builds")],
]

RESULTS = Path(__file__).resolve().parent / "out" / "full" / "results.json"


def prepare(page):
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.85}")
    page.wait_for_selector("text=Top 5 guesses", timeout=120000)
    page.wait_for_timeout(2500)


def _open(page, sample):
    page.goto(f"http://localhost:{PORT}/?sample={sample}")
    page.add_style_tag(content="header[data-testid=stHeader], [data-testid=stToolbar], [data-testid=stDecoration]{display:none!important} html{zoom:0.85}")
    page.wait_for_selector("text=Top 5 guesses", timeout=120000)
    page.wait_for_timeout(2500)


def _snap(page, res, tag):
    res[tag] = page.locator("[data-testid=stMain]").inner_text()[:700]


def _second(page):
    page.locator("[data-testid=stMain] [data-testid=stRadio] label").nth(1).click()
    page.wait_for_timeout(3500)


def record(page, mark):
    res = {}
    mark("banana")
    _snap(page, res, "banana")
    page.wait_for_timeout(16000)

    mark("alpha")
    s = page.get_by_role("slider", name="Heatmap strength")
    s.focus()
    for _ in range(6):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(500)
    page.wait_for_timeout(6000)
    for _ in range(6):
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(500)
    page.wait_for_timeout(5000)

    mark("cat")
    _open(page, "cat.jpg")
    _snap(page, res, "cat")
    page.wait_for_timeout(14000)

    mark("cat2")
    _second(page)
    _snap(page, res, "cat2")
    page.wait_for_timeout(16000)

    mark("dog")
    _open(page, "dog.jpg")
    _snap(page, res, "dog")
    page.wait_for_timeout(12000)

    mark("dog2")
    _second(page)
    _snap(page, res, "dog2")
    page.wait_for_timeout(14000)

    mark("pizza")
    _open(page, "pizza.jpg")
    _snap(page, res, "pizza")
    page.wait_for_timeout(12000)

    mark("pizza2")
    _second(page)
    _snap(page, res, "pizza2")
    page.wait_for_timeout(18000)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
