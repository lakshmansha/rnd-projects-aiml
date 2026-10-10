PORT = 8507
VOICE = ("This GPT starts out knowing nothing. Watch what it learns. "
         "I built it with Claude Code: a real transformer, under a million parameters, trained on Shakespeare on my CPU. "
         "Step one is pure gibberish. "
         "As the loss falls, you see letters, then words, then something shaped like a play. "
         "It only ever predicts the next character. Everything else emerges from that. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "A GPT that|knows NOTHING"), (3.5, 11, "818,176 parameters"),
            (11, 19, "Gibberish -> words|-> a play"), (19, 27, "Just predicts the|next character"),
            (27, 40, "Follow for more AI/ML builds")]
VOICE2 = ("This GPT starts out knowing nothing. Watch what it learns. "
          "I built it with Claude Code: a real transformer, 818 thousand parameters, trained on my CPU. "
          "Step one is pure gibberish. "
          "Then, as the loss falls from four point four to two, letters become words, and then something shaped like a play. "
          "It only ever predicts the next character. Everything else emerges from that. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3.5, "A GPT that|knows NOTHING"), (3.5, 6, "818,176 parameters"), (21.5, 24, "Just predicts the|next character"), (24.4, 40, "Follow for more AI/ML builds")]
SB = "[data-testid=stSidebar]"


def _open_sidebar(page):
    page.locator("[data-testid=stExpandSidebarButton], [data-testid=collapsedControl]").first.click()
    page.wait_for_selector(SB + " input[type=range]")
    page.wait_for_timeout(600)


def _close_sidebar(page):
    page.locator(SB + " button[kind=headerNoPadding], [data-testid=stSidebarCollapseButton] button").first.click()
    page.wait_for_timeout(600)


def _slider(page, idx, key, presses=1):
    s = page.locator(SB + " input[type=range]").nth(idx)
    s.focus()
    page.keyboard.press(key)


def prepare(page):
    # not part of the clip: train 300 steps on CPU (~2-3 min), sample every 50; the clip replays the finished run
    page.wait_for_timeout(2500)
    _open_sidebar(page)
    _slider(page, 3, "Home")
    page.keyboard.press("ArrowRight")
    page.keyboard.press("ArrowRight")
    _slider(page, 5, "Home")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(800)
    page.get_by_role("button", name="Train from scratch").click()
    page.wait_for_selector("text=Done in", timeout=600000)
    _close_sidebar(page)
    page.wait_for_timeout(500)
    T = page.evaluate("() => { const m = document.querySelector('[data-testid=stMain]'); m.scrollTo(0,0); }")


def actions(page, T):
    T.at(1)
    T.scroll(0)
    T.at(4)
    T.scroll(300)
    T.at(11)
    T.scroll(450)
    T.at(15)
    T.scroll(450)
    T.at(19)
    T.scroll(500)
    T.at(23)
    T.scroll(500)
    T.at(26)
