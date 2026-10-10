import re
import time

PORT = 8508
VOICE = ("Can an AI read your mind in twenty questions? "
         "I built this with Claude Code. I switch the sidebar to GPT guesses your secret, think of something, "
         "and just answer Yes, No or Sometimes. "
         "Watch the progress bar count down. Each question tries to split the possibilities in half, like a binary search. "
         "Then it makes a guess, and I press Correct or Nope. The other mode flips it, and you grill GPT about its secret. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "Think of anything.|Can GPT read your mind?"), (3, 11, "Answer: Yes / No / Sometimes"),
            (11, 19, "20 questions left,|counting down"), (19, 27, "Then it makes a guess"),
            (27, 40, "Follow for more AI/ML builds")]

# my secret is an umbrella; answer GPT's questions with simple keyword rules
RULES = [(r"living|alive|animal|breath|eat|edible|food|electr|battery|plug|screen|digital|vehicle|kitchen|bedroom|furniture|bigger than|larger|heavy|person|place|city", "No"),
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
    for _ in range(8):
        if page.get_by_text("Correct!").count():
            break
        msgs = page.locator("[data-testid=stChatMessage]")
        q = msgs.last.inner_text()
        print("Q:", q.replace("\n", " "), flush=True)
        T.at(min(time.time() - T.t0 + 1.5, 26))
        a = answer(q)
        page.get_by_role("button", name=a, exact=True).click()
        page.wait_for_selector("button:has-text('Yes'), button:has-text('Correct')", timeout=40000)
        page.wait_for_timeout(500)
        if time.time() - T.t0 > 24:
            break
    if page.get_by_text("Correct!").count():
        print("GUESS:", page.locator("[data-testid=stChatMessage]").last.inner_text().replace("\n", " "), flush=True)
        T.at(min(time.time() - T.t0 + 1.5, 26))
        page.get_by_text("Correct!").first.click() if "umbrella" in page.locator("[data-testid=stChatMessage]").last.inner_text().lower() else page.get_by_text("Nope").first.click()
        page.wait_for_timeout(2000)
    T.at(28)
