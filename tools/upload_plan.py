"""Generate content/UPLOAD_PLAN.md (posting order, titles, captions, hashtags). Nothing is uploaded by this script."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (project number, folder, title <60, what it shows (true to the recorded footage), hashtags)
ITEMS = [
    (6, "06-digit-classifier", "I drew a digit and 4 ML models voted on it",
     "Four classic ML models (SVM, neural net, random forest, k-NN) train on 8x8 digit images, then vote on the number I draw.",
     "#MachineLearning #Python #Streamlit #sklearn #AI"),
    (9, "09-rl-gridworld", "Two AIs, one cliff: only one plays it safe",
     "Q-learning and SARSA learn to cross a cliff by trial and error. One takes the risky edge, the other the safe route.",
     "#ReinforcementLearning #MachineLearning #Python #AI #QLearning"),
    (7, "07-tiny-gpt", "I trained a tiny GPT from scratch on my CPU",
     "A character-level transformer (818,176 parameters) goes from gibberish to Shakespeare-like text while training on a CPU.",
     "#GPT #Transformer #PyTorch #DeepLearning #AI"),
    (10, "10-evolving-rockets", "100 rockets, zero programming: they evolve a route",
     "A genetic algorithm evolves rocket steering until they reach the target. I scrub through the generations.",
     "#GeneticAlgorithm #Evolution #MachineLearning #Python #AI"),
    (2, "02-prompt-injection-lab", "I tried to hack an AI guarding a password",
     "A prompt-injection lab with five defense levels: the weakest bot leaks the secret, stronger setups hold.",
     "#PromptInjection #AISecurity #LLM #Python #AI"),
    (16, "16-cnn-xray", "What does an AI actually look at? Grad-CAM X-ray",
     "A real MobileNetV2 guesses the photo and Grad-CAM paints the pixels that drove its decision.",
     "#DeepLearning #ComputerVision #GradCAM #PyTorch #AI"),
    (17, "17-flappy-evolution", "60 AI birds learn to fly with zero training",
     "Sixty tiny neural nets evolve to play a Flappy-style game: the best birds breed, children mutate, and by generation 8 one flies the course.",
     "#NeuralNetwork #Evolution #MachineLearning #Python #AI"),
    (18, "18-attention-xray", "I looked inside a GPT: where does each head look?",
     "A tiny GPT reads Shakespeare and every attention head is plotted: in layer 1 one head looks exactly one character back, another exactly two.",
     "#Transformer #Attention #GPT #MachineLearning #Python"),
    (4, "04-neural-playground", "Watch a neural net learn a spiral, live",
     "A numpy neural net learns the spiral dataset while the decision boundary bends. Capacity decides what it can learn.",
     "#NeuralNetworks #MachineLearning #Python #Backprop #AI"),
    (11, "11-token-xray", "What ChatGPT actually reads (it isn't letters)",
     "Text is split into tokens, not letters. The same greeting costs 21 tokens in one vocabulary and 41 in another.",
     "#LLM #Tokenization #ChatGPT #AI #Python"),
    (13, "13-clustering-lab", "K-means cuts this in half. This one doesn't.",
     "Same data, four clustering algorithms. Each one assumes a shape, so each wins on different data.",
     "#MachineLearning #Clustering #KMeans #DBSCAN #Python"),
    (14, "14-explainable-text-ai", "Which words made the AI decide? It shows me.",
     "A text classifier highlights the words behind each decision, including a tricky sentence that it gets torn on.",
     "#ExplainableAI #MachineLearning #NLP #Python #AI"),
    (5, "05-spot-the-hallucination", "Can YOU spot the AI lie? 1 of 5 facts is fake",
     "GPT writes five facts and one is false. Can you find it? LLMs state falsehoods as confidently as facts.",
     "#AI #LLM #Hallucination #Streamlit #Python"),
    (15, "15-prompt-gym", "Can you make GPT write exactly 10 words?",
     "Prompt Gym grades prompts with strict Python checks. A lazy prompt fails, a specific one passes.",
     "#PromptEngineering #GPT #LLM #Python #AI"),
    (12, "12-debate-arena", "I made two AIs debate pineapple on pizza",
     "A pro bot and a con bot debate, a judge scores them, and I see whether they changed my mind.",
     "#AI #GPT4o #Debate #Streamlit #Python"),
    (1, "01-llm-arena", "Two AI prompts fight. A judge picks the winner.",
     "Pirate-style vs expert-style prompts battle. A judge scores both answer orders and Elo updates the ranking.",
     "#PromptEngineering #LLM #GPT #Elo #AI"),
    (3, "03-semantic-map", "I turned 60 sentences into a map of meaning",
     "Sentences become points on a map, and a question retrieves the closest ones for a RAG answer.",
     "#RAG #Embeddings #LLM #Python #AI"),
    (8, "08-twenty-questions", "Can GPT read my mind in 20 questions?",
     "GPT asks yes/no questions to narrow down what I am thinking of while the counter drops.",
     "#AI #GPT #20Questions #Streamlit #Python"),
]

DISCLOSURE = "Narration is AI-generated. Built with Claude Code (Python, Streamlit). No personal data is shown."


def main():
    L = ["# Watch It Learn: upload plan (shorts first)", "",
         "Nothing is uploaded automatically. Upload the files yourself. Use `out/short_v2.mp4` (1080x1920) of each project folder.", "",
         "## 1. Set up (about 20 minutes)", "",
         "1. **YouTube:** profile menu -> Create a channel (or Settings -> Add or manage channel) -> make a **Brand Account** channel named `Watch It Learn`. "
         "Your existing Google login is fine.",
         "2. **Instagram:** create a **new** account (new username + a separate email or phone), then Settings -> Add account to switch with your personal one. "
         "Switch it to a **Professional (Creator)** account.",
         "3. **Handles to check (I cannot check them):** `@watchitlearn`, `@watchitlearn.ai`, `@watchitlearn.lab`. Use the same handle on both platforms.",
         "4. **Art (already made):** profile picture `content/_brand/profile_1080.png` (round-crop safe) and YouTube banner `content/_brand/youtube_banner_2560x1440.png`.",
         "5. Turn on the AI-content label when asked (voice is synthetic).", "",
         "## 2. Bio text", "",
         "**Instagram bio (<150 chars):**", "",
         "```", "AI/ML builds in 30 seconds.", "A new project every day: watch it learn.", "Built with Claude Code", "```", "",
         "**YouTube channel description:**", "",
         "```",
         "Watch It Learn: 30-second demos of small AI and machine-learning projects, one new build every day.",
         "Neural nets, reinforcement learning, tiny GPTs, evolution, prompt security and more, all built in Python.",
         "Built with Claude Code. Narration is AI-generated.", "```", "",
         "## 3. Posting schedule (one a day, strongest hooks first)", "",
         "Suggested time: evening in your audience's time zone (for India, about 7-9 PM). Post the same short on YouTube Shorts and Instagram Reels the same day. "
         "Pin a comment: *Which project should I build next?*", ""]
    L += ["| Day | # | Title (<60) | File |", "|---|---|---|---|"]
    for d, (n, folder, title, _, _) in enumerate(ITEMS, 1):
        L.append(f"| {d} | {n:02d} | {title} ({len(title)}) | `content/{folder}/out/short_v2.mp4` |")
    L += ["", "## 4. Copy-paste text per video", ""]
    for d, (n, folder, title, what, tags) in enumerate(ITEMS, 1):
        L += [f"### Day {d}: #{n:02d} {title}", "",
              "**YouTube title:**", "", f"`{title}`", "",
              "**YouTube description:**", "", "```", what, "", f"Project {n:02d} of the Watch It Learn series. {DISCLOSURE}", "",
              f"{tags} #Shorts", "```", "",
              "**Instagram caption:**", "", "```", f"{title}", "", what, "", "Follow @watchitlearn for a new AI build every day.", "",
              f"{tags}", "```", ""]
    L += ["## 5. Tips", "",
          "- Reply to every comment in the first hour. Ask a question to start a thread.",
          "- After 3-4 posts check which got the most average view duration (YouTube Studio) and make more like that.",
          "- If a short underperforms, change only the first 3 seconds (hook) and repost later, not the whole video.",
          "- Titles and descriptions use only facts shown in the clips. Keep it that way."]
    (ROOT / "content/UPLOAD_PLAN.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote content/UPLOAD_PLAN.md")


if __name__ == "__main__":
    main()
