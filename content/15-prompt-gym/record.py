PORT = 8515
VOICE = ("Can you make GPT reply with exactly ten words? Harder than it sounds. "
         "I built this prompt gym with Claude Code. There are six levels. "
         "You write the prompt, GPT answers, and plain Python code checks the result. "
         "No vibes, just pass or fail. "
         "On level four I summarise in exactly ten words, and the checker shows me the real word count. "
         "Then I make the prompt specific. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "EXACTLY|10 WORDS?"), (3.5, 11, "You prompt.|Python grades."),
            (11, 19, "Checker shows|the real word count"), (19, 27, "Specific prompt|= better odds"),
            (27, 40, "Follow for more AI/ML builds")]


def actions(page, T):
    T.at(3)
    page.get_by_role("combobox").first.click()
    page.get_by_role("option", name="Level 4").click()
    page.wait_for_timeout(800)
    ta = page.get_by_label("Your prompt")
    T.at(7)
    ta.click()
    ta.type("Summarise this.", delay=60)
    page.keyboard.press("Control+Enter")
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Run").click()
    page.wait_for_selector("text=Model output", timeout=60000)
    print("RES1:", page.locator("[data-testid=stAlert]").last.inner_text(), flush=True)
    T.at(max(13, __import__("time").time() - T.t0))
    page.wait_for_timeout(1500)
    ta = page.get_by_label("Your prompt")
    ta.click()
    page.keyboard.press("Control+a")
    ta.type("Summarise the INPUT in exactly 10 words. Output only the summary, no preamble.", delay=25)
    page.keyboard.press("Control+Enter")
    page.wait_for_timeout(1000)
    T.at(19)
    page.get_by_role("button", name="Run").click()
    page.wait_for_selector("text=/Attempts on this level: 2|Levels cleared/", timeout=60000)
    page.wait_for_timeout(2500)
    if page.locator("[data-testid=stExpandSidebarButton]").count():
        page.locator("[data-testid=stExpandSidebarButton]").click()
    page.wait_for_timeout(1500)
    print("SIDEBAR:", page.locator("[data-testid=stSidebar]").inner_text().replace(chr(10), " "), flush=True)
    T.at(26)
    T.at(28)
