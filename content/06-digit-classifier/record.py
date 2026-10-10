import math

PORT = 8506
VOICE = ("Four AI models just voted on my handwriting. "
         "I built this with Claude Code. It trains an SVM, a neural net, a random forest and k-NN on tiny eight by eight digit images, right when the app starts. "
         "I draw a seven, lift the mouse, and the app shrinks it to eight by eight pixels. That blurry blob is all the models ever see. "
         "Each one votes, and the majority wins. On held-out test data they score about 98 to 99 percent. "
         "Follow for more AI and ML builds.")
CAPTIONS = [(0, 3, "4 models. 1 digit.|Vote."), (3, 11, "Trained live on|1,797 images"),
            (11, 19, "What the models see: 8x8"), (19, 27, "~98-99% on unseen data"),
            (27, 40, "Follow for more AI/ML builds")]
VOICE2 = ("Four AI models are about to vote on my handwriting. "
          "Built with Claude Code: four models, tiny eight by eight digit images, and 98 to 99.8 percent on unseen test data. "
          "Now I draw a seven. "
          "The app shrinks it to eight by eight pixels, and that blur is all they see. "
          "Three vote seven, the neural net says five. The majority wins. "
          "Follow for more AI and ML builds.")
CAPTIONS2 = [(0, 3, "4 models. 1 digit.|Vote."), (11, 14.5, "Draw a 7"), (15, 19.5, "Models see 8x8 pixels"), (20, 23, "Majority wins"), (21.7, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.wait_for_selector("canvas#cv", timeout=60000)
    page.wait_for_timeout(2500)


def _stroke(page, pts):
    page.mouse.move(*pts[0])
    page.mouse.down()
    for p in pts[1:]:
        page.mouse.move(*p, steps=4)
    page.mouse.up()


def actions(page, T):
    T.at(0.5)
    T.scroll(250)                  # accuracy table
    T.at(8)
    T.scroll(-250)
    page.wait_for_timeout(500)
    T.at(11)
    b = page.locator("canvas#cv").bounding_box()
    x0, y0, w, h = b["x"], b["y"], b["width"], b["height"]
    P = lambda u, v: (x0 + u * w, y0 + v * h)
    _stroke(page, [P(.2, .2), P(.8, .2), P(.62, .5), P(.45, .8)])   # a big 7
    page.wait_for_timeout(1500)
    T.at(14)
    T.scroll(400)                  # 8x8 view + majority vote
    T.at(19)
    T.scroll(450)                  # bar chart + votes
    T.at(27)
