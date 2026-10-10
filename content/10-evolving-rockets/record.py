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
VOICE2 = ("Generation one: a hundred rockets, and none reach the target. "
          "I built this with Claude Code. Each rocket's DNA is a list of random thrusts, and the best ones breed. "
          "Scrub forward, and by generation six, one rocket slips through the gap and hits the target. "
          "Nobody programmed that route. "
          "By generation eighty, seventy-eight of a hundred make it. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3.5, "Gen 1: none arrive"), (10.5, 14, "Gen 6: first arrival"), (19, 23, "Gen 80: 78/100 arrive"), (21.2, 40, "Follow for more AI/ML builds")]


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
    T.at(17)
    for _ in range(6):             # 6 -> 12, then jump to the last generation
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
    T.at(22)
    page.keyboard.press("End")     # generation 80
    page.wait_for_timeout(800)
    T.at(24)
    T.scroll(500)
    T.at(28)
