PORT = 8505
VOICE = ("Can you spot the one lie an AI slipped in? GPT writes five short facts. Four are true, one is subtly false. "
         "I pick the topic Space and deal a new round. Which one is fake? I take a guess. "
         "Let's see if I caught it. "
         "Language models state falsehoods in the same tone as facts, so always check the number, the name, the cause. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "1 of these 5|is an AI LIE"), (3.5, 11, "GPT: 4 true,|1 subtly false"),
            (11, 19, "Which one is fake?"), (19, 27, "Confident != correct"),
            (27, 40, "Follow for more AI/ML builds")]
VOICE2 = ("Can you spot the one lie an AI slipped in? GPT writes five short facts: four true, one subtly false. "
          "I pick Space, then deal a new round. Five fresh statements about space. "
          "Which one is fake? Sixty thousand spins a minute sounds off, so I pick it. "
          "Caught it! The truth is thousands, not sixty thousand. "
          "Models state falsehoods as confidently as facts, so always check the number. Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3.5, "1 of these 5|is an AI LIE"), (3.5, 9.5, "4 true,|1 subtly false"),
             (10, 12.5, "Which one is fake?"), (13.5, 22, "Caught it!"),
             (22, 40, "Confident != correct")]


def prepare(page):
    page.wait_for_selector("[data-testid=stRadio] label", timeout=60000)
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(3.5)
    page.locator("[data-testid=stExpandSidebarButton]").click()
    page.wait_for_timeout(700)
    sb = page.locator("[data-testid=stSidebar]")
    sb.get_by_role("combobox").click()
    page.wait_for_timeout(400)
    page.get_by_role("option", name="Space").click()
    page.wait_for_timeout(500)
    page.locator("[data-testid=stSidebarCollapseButton] button").click()
    page.wait_for_timeout(700)
    T.at(7)
    page.get_by_role("button", name="New round").click()
    page.wait_for_timeout(2500)
    page.wait_for_selector("[data-testid=stRadio] label", timeout=60000)
    page.wait_for_timeout(2500)
    T.at(13)
    page.locator("[data-testid=stRadio] label").nth(2).click()
    page.wait_for_selector("[data-testid=stAlert]", timeout=15000)
    page.wait_for_timeout(1000)
    T.at(17)
    T.scroll(400)
    T.at(26)
