PORT = 8503
VOICE = ("This map shows how an AI understands meaning. "
         "Sixty sentences, six topics, each turned into a vector. Same topic, same cluster. "
         "Now I ask: why does bread rise? A gold star lands in the map, with dotted lines to the sentences it found. "
         "Feed those neighbours to the model as context and you get a grounded answer. That's RAG. "
         "Built with Claude Code. Follow for more AI and ML builds.")
CAPTIONS = [(0, 3.5, "How AI sees meaning"), (3.5, 8, "60 sentences,|6 topics, 1 map"),
            (8, 15, "Ask: why does|bread rise?"), (15, 24, "Nearest neighbours|-> RAG answer"),
            (24, 40, "Follow for more AI/ML builds")]


def prepare(page):
    page.wait_for_selector(".js-plotly-plot", timeout=120000)
    page.wait_for_timeout(1500)


def actions(page, T):
    T.at(1)
    T.scroll(0)
    T.at(7)
    box = page.get_by_placeholder("e.g. Why does bread rise?")
    box.click()
    page.keyboard.type("Why does bread rise?", delay=60)
    page.keyboard.press("Enter")
    page.wait_for_selector("text=RAG answer", timeout=90000)
    page.wait_for_timeout(2500)
    T.at(14)
    T.scroll(420)
    T.at(19)
    T.scroll(300)
    T.at(26)
