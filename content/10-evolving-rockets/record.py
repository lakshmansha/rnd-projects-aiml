PORT = 8510
VOICE = ("Generation one: a hundred rockets, and ninety-nine crash. "
         "I built this with Claude Code. Each rocket's DNA is just a list of random thrusts. The best ones breed, the children mutate. "
         "Now watch me scrub through generations. By generation six, the first rocket slips through the gap and hits the target. "
         "Nobody programmed that route. "
         "Selection plus a little mutation finds a path you never wrote. By generation eighty, most rockets make it. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "99 of 100 crash"), (3.5, 11, "DNA = a list of thrusts"),
            (11, 18, "Gen 6: first rocket|arrives"), (18, 27, "Nobody programmed|the route"),
            (27, 40, "Follow for more AI/ML builds")]


def _slider(page):
    return page.locator("[data-testid=stMain] input[type=range]").first


def prepare(page):
    page.wait_for_selector("[data-testid=stMain] input[type=range]")
    page.wait_for_timeout(2500)
    s = _slider(page)
    s.focus()
    page.keyboard.press("Home")    # generation 1
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(8)
    s = _slider(page)
    s.focus()
    for _ in range(5):             # 1 -> 6
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(500)
    T.at(15)
    page.keyboard.press("PageUp") if False else None
    for _ in range(74):            # 6 -> 80
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(120)
    T.at(22)
    T.scroll(500)
    T.at(26)
