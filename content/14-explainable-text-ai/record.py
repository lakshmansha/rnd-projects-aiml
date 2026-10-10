PORT = 8514
VOICE = ("Most AI can't tell you why it decided. This one highlights the exact words. "
         "I trained a simple classifier on real newsgroup posts. Type a sentence and it picks a topic, with green words pushing toward the answer. "
         "Now a trick sentence: rocket engine, horsepower, hockey puck. Red words pull toward the runner-up, so I can watch it argue with itself. "
         "It's 84.8 percent accurate on posts it never saw, and when it's wrong, I can see why. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "WHY did the AI|decide that?"), (3, 11, "Green = pushes|toward the answer"),
            (11, 19, "Red = pulls toward|the runner-up"), (19, 27, "84.8% accuracy|on unseen posts"),
            (27, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.wait_for_selector("text=Accuracy on unseen posts", timeout=300000)
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(0.5)
    page.get_by_role("button", name="Space").click()
    page.wait_for_timeout(1500)
    T.at(3)
    T.scroll(350)
    T.at(8)
    T.scroll(-400)
    T.at(10.5)
    page.get_by_role("button", name="Tricky").click()
    page.wait_for_timeout(1500)
    T.at(12)
    T.scroll(350)
    T.at(17)
    T.scroll(300)
    T.at(19)
    T.at(27)
