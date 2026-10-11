PORT = 8517
VOICE = ("Sixty birds with random brains try to fly through pipes. I built this with Claude Code. "
         "Generation one: they all crash. Nobody teaches them. The best birds breed, and their children mutate. "
         "Watch the score climb. By generation eight, a bird flies the whole course. "
         "Evolution, not programming. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "60 birds.|Random brains."), (3.5, 10, "Gen 1: all crash"), (10, 20, "Best birds breed,|children mutate"),
            (20, 27, "Evolution, not programming"), (27, 40, "Follow for more AI/ML builds")]
VOICE2 = VOICE
CAPTIONS2 = [(0, 3, "60 birds.|Random brains."), (3, 8, "Nobody teaches them"), (8, 15, "Best birds breed,|children mutate"),
             (15, 22, "Evolution,|not programming"), (22, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.wait_for_selector("button:has-text('Evolve')", timeout=60000)
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(0.4)
    page.get_by_role("button", name="Evolve").click()
    T.at(30)
