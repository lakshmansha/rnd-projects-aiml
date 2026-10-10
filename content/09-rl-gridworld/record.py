PORT = 8509
VOICE = ("Two AI agents walk along a cliff. Only one learns to play it safe. "
         "I built this with Claude Code. Both agents start knowing nothing. Every step costs one point, the cliff costs a hundred. "
         "Watch the arrows appear as they learn. "
         "Here's the surprise. Q-learning hugs the cliff edge, the shortest path, and keeps falling in while it explores. "
         "SARSA takes the safe route up top. "
         "SARSA counts its own clumsy exploring, Q-learning doesn't. Safe beats short. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "Which AI survives|the cliff?"), (3.5, 11, "No rules given.|Just trial and error."),
            (11, 16, "Q-learning: shortest path,|keeps falling"), (16, 21, "SARSA:|the safe route"),
            (21, 27, "Safe beats short"), (27, 40, "Follow for more AI/ML builds")]


def _slider(page, key, n=1):
    s = page.locator("[data-testid=stMain] input[type=range]").first
    s.focus()
    for _ in range(n):
        page.keyboard.press(key)
        page.wait_for_timeout(20)


def prepare(page):
    page.wait_for_selector("[data-testid=stMain] input[type=range]")
    page.wait_for_timeout(2500)
    _slider(page, "Home")          # start of training (episode 0)
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(3.5)
    T.scroll(250)
    T.at(5)
    s = page.locator("[data-testid=stMain] input[type=range]").first
    s.focus()
    for _ in range(40):            # scrub through training, ~5s
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(110)
    T.at(12)
    T.scroll(350)
    T.at(18)
    T.scroll(600)                  # reward chart
    T.at(24)
    T.scroll(600)                  # info box
    T.at(27)
