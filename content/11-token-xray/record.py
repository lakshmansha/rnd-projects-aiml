PORT = 8511
VOICE = ("ChatGPT can't see letters. Here's what it reads instead. "
         "Type any text and it splits into colored chips, each one a token. "
         "Even strawberry is one chunk, so the model never sees its letters. "
         "Now the same greeting in Hindi, Japanese, Arabic and Russian. "
         "Twenty-one tokens on the newer GPT-4o vocabulary, and forty-one on the older one. "
         "Models work on chunks, not letters, which is why some languages cost more. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "LLMs don't|read letters"), (3.5, 10, "Every chip = 1 token"),
            (10, 17, "Same greeting,|4 languages"), (17, 23, "21 tokens vs 41 tokens"),
            (23, 27, "Chunks, not letters"), (27, 40, "Follow for more AI/ML builds")]


def actions(page, T):
    T.at(0.5)
    T.scroll(300)
    T.at(10)
    T.scroll(-300)
    page.wait_for_timeout(700)
    page.get_by_role("button", name="Other languages").click()
    page.wait_for_timeout(800)
    T.scroll(300)
    T.at(17)
    page.get_by_role("tab", name="cl100k_base").click()
    T.at(21)
    T.scroll(500)
    T.at(26)
