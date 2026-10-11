PORT = 8518
VOICE = ("A tiny GPT is reading Shakespeare, and I can see where each attention head looks. I built this with Claude Code. "
         "In layer one, head two looks exactly one character back, ninety-nine percent of the time. Head one looks exactly two back. "
         "By layer four it's no longer a simple offset. "
         "The model's first trick is simple: look at the letter before. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "Where does a GPT|look?"), (3.5, 9, "Layer 1: 1 char back"), (9, 14, "Head 1: 2 chars back"),
            (15, 26, "Layer 4: vertical stripes"), (26, 40, "Follow for more AI/ML builds")]
VOICE2 = VOICE
CAPTIONS2 = CAPTIONS


def prepare(page):
    page.wait_for_selector("text=Layer 1, head 1", timeout=90000)
    page.wait_for_timeout(2500)


def actions(page, T):
    T.at(0.5)
    T.scroll(420)          # layer 1, heads 1 and 2
    T.at(9)
    T.scroll(450)          # heads 3 and 4
    T.at(14)
    T.scroll(-900)
    T.at(15)
    page.locator("[data-testid=stRadio] label").nth(4).click()   # layer 4
    T.at(16.5)
    T.scroll(420)
    T.at(26)
