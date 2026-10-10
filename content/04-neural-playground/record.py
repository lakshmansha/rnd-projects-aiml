PORT = 8504
VOICE = ("Can a tiny network untangle this spiral? "
         "A neural network I wrote from scratch in numpy. Two hidden layers of eight. I press Train and the decision boundary starts bending. "
         "It finds the spiral: ninety-eight percent accuracy. Now shrink it to two neurons. Same data, same training, fifty-seven percent. Barely better than a coin flip. "
         "Depth and width let a boundary curve. Too little capacity, and training can't help. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "Untangle the spiral"), (3, 11, "Backprop from scratch,|~30 lines of numpy"),
            (11, 19, "8,8 -> 98 pct|2 -> 57 pct"), (19, 27, "Capacity decides|what it can learn"),
            (27, 40, "Follow for more AI/ML builds")]
VOICE2 = ("Can a tiny network untangle a spiral? A network I wrote from scratch in numpy, two hidden layers of eight. "
          "I press Train and the boundary wraps around the spiral, with accuracy hitting ninety-eight percent. "
          "Now I shrink it to just two neurons and train again with the same settings. "
          "Accuracy stalls at fifty-seven percent, barely better than a coin flip, and the boundary stays almost straight. "
          "Too little capacity, and training can't fix it. Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3, "Untangle the spiral"), (3, 9.5, "From scratch|in numpy"),
             (9.5, 12, "98% accuracy"), (12, 19.5, "Shrink to 2 neurons"),
             (19.5, 26, "57%: too little capacity"), (27, 40, "Follow for more AI/ML builds")]


def _open_sidebar(page):
    page.locator("[data-testid=stExpandSidebarButton], [data-testid=stSidebarCollapsedControl] button").first.click()
    page.wait_for_timeout(700)


def _close_sidebar(page):
    page.locator("[data-testid=stSidebarCollapseButton] button, [data-testid=stSidebarHeader] button").first.click()
    page.wait_for_timeout(600)


def actions(page, T):
    T.at(0.5)
    _open_sidebar(page)            # show the settings: Spiral, 8,8, tanh
    T.at(3.2)
    page.get_by_role("button", name="Train").click()
    page.wait_for_timeout(300)
    _close_sidebar(page)           # watch the boundary bend
    T.at(6)
    T.scroll(120)
    T.at(11)
    _open_sidebar(page)
    box = page.get_by_label("Hidden layers")
    box.fill("2")
    box.press("Enter")
    page.wait_for_timeout(500)
    T.at(13)
    page.get_by_role("button", name="Train").click()
    page.wait_for_timeout(300)
    _close_sidebar(page)
    T.at(19)
    T.at(27)
