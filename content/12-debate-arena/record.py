PORT = 8512
VOICE = ("Two AIs argue about pineapple on pizza, and a third one judges. "
         "I built this with Claude Code. First I rate how much I agree with the motion. "
         "Then I start the debate, and a pro bot and a con bot trade short, punchy arguments. "
         "Next the judge scores both sides on logic, evidence, persuasion, clarity and rebuttal, "
         "and a radar chart shows who won. "
         "The real test is rating my opinion again, to see whether the bots moved me. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "AI vs AI:|pineapple on pizza"), (3.5, 10, "Pro vs Con,|60 words max"),
            (10, 19, "Judge scores|5 criteria"), (19, 27, "Did they change|YOUR mind?"),
            (27, 40, "Follow for more AI/ML builds")]


def actions(page, T):
    T.at(3)
    sl = page.get_by_role("slider")
    sl.nth(0).focus()
    page.keyboard.press("ArrowLeft")      # rounds 2 -> 1 (budget)
    sl.nth(1).focus()
    for _ in range(2):
        page.keyboard.press("ArrowLeft")  # before: 5 -> 3
    page.wait_for_timeout(500)
    T.at(5)
    page.get_by_role("button", name="Start debate").click()
    page.wait_for_selector("text=Verdict", timeout=90000)
    page.wait_for_timeout(1200)
    print("DEBATE:", page.locator("[data-testid=stChatMessage]").all_inner_texts(), flush=True)
    T.at(max(12, __import__("time").time() - T.t0))
    T.scroll(450)
    T.at(17)
    T.scroll(500)
    T.at(21)
    page.get_by_role("slider").last.focus()
    for _ in range(3):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
    T.at(24)
    T.scroll(400)
    T.at(28)
