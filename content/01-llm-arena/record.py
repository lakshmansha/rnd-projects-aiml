PORT = 8501
VOICE = ("Which prompt style wins, pirate or expert? This is Prompt Arena. Same model, two prompting styles. "
         "I press Fight and each style answers the same question. "
         "Then a judge scores both answers, twice, with the order swapped, so position bias cancels out. "
         "If it disagrees with itself, it's a draw. "
         "Elo ranks the results. One win over an equal moves you just sixteen points, so rankings need many battles. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "Pirate vs Expert:|who wins?"), (3.5, 11, "Same model.|Different prompt style."),
            (11, 19, "Judge runs TWICE,|order swapped"), (19, 27, "Elo: +16 for a win|vs an equal"),
            (27, 40, "Follow for more AI/ML builds")]
VOICE2 = ("Pirate or expert, which prompt style wins? Same model, two prompting styles. "
          "Each battle is two answers plus two judge calls. I pick Pirate against Expert and press Fight. "
          "A judge scores both answers twice, with the order swapped, so position bias cancels out. "
          "Expert wins, but Elo moves the ratings only about fifteen points, so rankings need many battles. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3.3, "Pirate vs Expert"), (3.3, 9, "Same model,|two prompt styles"),
             (9.3, 19, "Judge runs TWICE,|order swapped"), (19.5, 22, "Expert wins"),
             (22, 24.5, "Elo: only ~15 points"), (26, 40, "Follow for more AI/ML builds")]


def actions(page, T):
    sb = page.locator("[data-testid=stSidebar]")
    T.at(3.3)
    page.locator("[data-testid=stExpandSidebarButton]").click()
    page.wait_for_timeout(700)
    sb.get_by_role("combobox").nth(0).click()
    page.wait_for_timeout(400)
    page.get_by_role("option", name="Pirate").click()
    page.wait_for_timeout(500)
    sb.get_by_role("combobox").nth(1).click()
    page.wait_for_timeout(400)
    page.get_by_role("option", name="Expert").click()
    page.wait_for_timeout(500)
    sb.get_by_role("slider").focus()
    page.keyboard.press("ArrowLeft")      # 1 battle
    T.at(9)
    page.locator("[data-testid=stSidebarCollapseButton] button").click()
    page.wait_for_timeout(700)
    T.at(10)
    page.get_by_role("button", name="Fight!").click()
    page.wait_for_selector(".js-plotly-plot", timeout=60000)   # leaderboard chart after the battle
    page.wait_for_timeout(1500)
    T.at(14)
    page.locator("[data-testid=stExpander] summary").first.click()   # open the two answers
    page.wait_for_timeout(800)
    T.at(19)
    T.scroll(500)
    T.at(24)
    T.scroll(600)
    T.at(27)
