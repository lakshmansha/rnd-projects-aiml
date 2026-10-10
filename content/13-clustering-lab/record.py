PORT = 8513
VOICE = ("Same data. Four algorithms. Only one gets it right. "
         "This is K-means, step by step. Every point joins its nearest cross, then each cross moves to the middle of its points. "
         "Drag the slider and watch it settle. "
         "Now the showdown. On the moons and circles, K-means slices the shapes in half. DBSCAN follows the density and nails both. "
         "Every algorithm assumes a shape. There's no best one, only the right one for your data. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "SAME DATA.|4 ALGORITHMS."), (3, 11, "K-means:|assign, move, repeat"),
            (11, 15, "K-means cuts|the moons in half"), (15, 20, "DBSCAN gets it"),
            (20, 27, "Every algorithm|assumes a shape"), (27, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.wait_for_selector(".js-plotly-plot", state="attached", timeout=60000)
    page.get_by_role("tab", name="Algorithm showdown").click()
    page.wait_for_selector(".js-plotly-plot", state="attached", timeout=60000)
    page.wait_for_timeout(4000)
    page.get_by_role("tab", name="K-means step by step").click()
    page.wait_for_timeout(2500)


def actions(page, T):
    T.at(3)
    sl = page.get_by_role("slider", name="Iteration")
    sl.focus()
    page.keyboard.press("Home")
    page.wait_for_timeout(500)
    for i in range(12):
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(450)
        if i == 0:
            T.at(5)
    T.at(11)
    page.get_by_role("tab", name="Algorithm showdown").click()
    page.wait_for_timeout(2500)
    T.at(12)
    T.scroll(380)
    T.at(16)
    T.scroll(450)
    T.at(21)
    T.scroll(900)
    T.at(27)
