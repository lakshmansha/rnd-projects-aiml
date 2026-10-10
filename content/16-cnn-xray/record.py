PORT = 8516
VOICE = ("This neural network is 95 percent sure it's a banana. Here's where it looked. "
         "A real MobileNetV2 guesses the photo, and Grad-CAM paints the pixels that mattered, red for decisive. "
         "Now the cat. Tiger cat, 22 percent. Tabby, 13. I switch to the runner-up and the heat moves to different pixels. "
         "Even a guess that's wrong has a reason you can see. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "95% BANANA.|Where did it look?"), (3.5, 11, "Red = decisive pixels"),
            (11, 19, "Switch guess,|heat moves"), (19, 27, "Not a black box"), (27, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.goto(f"http://localhost:{PORT}/?embed=true&sample=banana.jpg")
    page.wait_for_selector("img")
    page.wait_for_timeout(2500)


def actions(page, T):
    T.at(0.5)
    T.scroll(650)          # reveal the Grad-CAM heatmap
    T.at(5)
    T.scroll(700)          # top-5 bars
    T.at(10)
    page.goto(f"http://localhost:{PORT}/?embed=true&sample=cat.jpg")
    page.wait_for_selector("img")
    page.wait_for_timeout(1500)
    T.scroll(650)
    T.at(13)
    page.get_by_text("tabby", exact=False).first.click()
    T.at(19)
    page.get_by_text("tiger cat", exact=False).first.click()
    T.at(26)
