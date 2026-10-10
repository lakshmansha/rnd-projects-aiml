PORT = 8507
VOICE = ("This GPT starts out knowing nothing. Watch it learn. "
         "I built it with Claude Code: a real transformer, under a million parameters, training on Shakespeare on my CPU. "
         "I press Train from scratch. Step one is pure gibberish. "
         "As the loss falls, you see letters, then words, then something shaped like a play. "
         "It only ever predicts the next character. Everything else emerges from that. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "A GPT that|knows NOTHING"), (3.5, 11, "818,176 parameters"),
            (11, 19, "Gibberish -> words|-> a play"), (19, 27, "Just predicts the|next character"),
            (27, 40, "Follow for more AI/ML builds")]
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
    # not part of the clip: shorten the run so live training fits the narration (100 steps, sample every 25)
    page.wait_for_timeout(2500)
    _open_sidebar(page)
    _slider(page, 3, "Home")
    _slider(page, 5, "Home")
    page.wait_for_timeout(800)
    _close_sidebar(page)
    page.wait_for_timeout(500)


def actions(page, T):
    T.at(1)
    T.scroll(0)
    T.at(4)
    _open_sidebar(page)
    page.get_by_role("button", name="Train from scratch").click()
    page.wait_for_timeout(500)
    _close_sidebar(page)
    T.at(11)
    T.scroll(500)
    T.at(19)
    T.scroll(700)
    T.at(26)
