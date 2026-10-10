import re
import time

PORT = 8508
VOICE = ("Can an AI read your mind in twenty questions? "
         "I built this with Claude Code. I think of something, and GPT asks the questions. "
         "I just answer Yes, No or Sometimes. "
         "Watch the counter drop from twenty. Each question tries to cut the possibilities in half, like a binary search. "
         "There is also a reverse mode, where you grill GPT about its secret. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "Think of anything.|Can GPT read your mind?"), (3, 11, "Answer: Yes / No / Sometimes"),
            (11, 19, "20 questions left,|counting down"), (19, 26, "Each question halves|the options"),
            (26, 40, "Follow for more AI/ML builds")]
VOICE2 = ("Can an AI read your mind in twenty questions? "
          "I built this with Claude Code. I think of something, and GPT asks the questions. "
          "I answer Yes, No or Sometimes, and the counter drops from twenty. "
          "It starts with big questions: living thing, man-made, found in nature, then narrows down. "
          "Each question tries to cut the options roughly in half. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3, "Think of anything.|Can GPT read your mind?"), (3, 8, "Answer: Yes / No / Sometimes"), (17, 21.5, "Each question halves|the options"), (21.5, 40, "Follow for more AI/ML builds")]

# my secret is an umbrella; answer GPT's questions with simple keyword rules
RULES = [(r"living|alive|animal|vehicle|transport|wheel|microwave|breath|eat|edible|food|electr|battery|plug|screen|digital|vehicle|kitchen|bedroom|furniture|bigger than|larger|heavy|person|place|city", "No"),
         (r"weather|rain|sun|protect|hand|carry|portable|household|everyday|outdoor|outside|fold|fabric|cover|wear|tool|common|use|object|man-made", "Yes")]


def answer(q):
    q = q.lower()
    for pat, a in RULES:
        if re.search(pat, q):
            return a
    return "Sometimes"


def prepare(page):
    page.wait_for_selector("text=Start game")
    page.locator("[data-testid=stExpandSidebarButton]").click()
    page.wait_for_timeout(500)
    page.get_by_text("GPT guesses your secret").click()
    page.wait_for_timeout(700)
    page.locator("[data-testid=stSidebarCollapseButton]").click()
    page.wait_for_selector("text=Start game")
    page.wait_for_timeout(800)


def actions(page, T):
    T.at(3)
    page.get_by_text("Start game").click()
    page.wait_for_selector("button:has-text('Yes'), button:has-text('Correct')", timeout=40000)
    for _ in range(4):
        msgs = page.locator("[data-testid=stChatMessage]")
        q = [t for t in msgs.all_inner_texts() if t.split()[-1] not in ("Yes", "No", "Sometimes") or len(t.split()) > 3][-1]
        print("Q:", q.replace(chr(10), " "), flush=True)
        T.at(min(time.time() - T.t0 + 1.5, 26))
        page.get_by_role("button", name=answer(q), exact=True).click()
        page.wait_for_selector("button:has-text('Yes'), button:has-text('Correct')", timeout=40000)
        page.wait_for_timeout(500)
        if page.get_by_text("Correct!").count():
            break
    T.at(26.5)
