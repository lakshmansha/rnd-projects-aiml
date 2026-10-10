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
VOICE2 = ("ChatGPT can't see letters. Here's what it reads instead. "
          "Type any text and it splits into colored chips, one per token. "
          "Even strawberry is one chip, so it never sees letters. "
          "Now the same greeting in four languages. "
          "Twenty-one tokens on the newer vocabulary, forty-one on the older one. "
          "Same text, double the tokens, so some languages cost more. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3.5, "LLMs don't|read letters"), (3.5, 8, "One chip = 1 token"),
             (8, 12, "strawberry = 1 chip"), (12.2, 14.8, "Same greeting,|4 languages"),
             (14.8, 19, "21 vs 41 tokens"), (19, 23, "Chunks, not letters"),
             (23.5, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.get_by_text("Chars per token").first.wait_for(timeout=30000)
    page.wait_for_timeout(1500)


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
