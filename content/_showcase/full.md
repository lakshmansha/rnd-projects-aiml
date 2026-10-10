# Channel intro / showcase: "I built 16 AI/ML projects in a day with an AI pair-programmer" (about 10 min)

Facts used (from HANDOFF.md, README.md, PLAN.md and the code): 16 single-file Streamlit apps plus a hub page (ports 8501-8516, hub on 8500), `run_all.py`, `smoke_test.py` (all 16 apps and the hub pass). Stack: Streamlit, scikit-learn, PyTorch (CPU), numpy, plotly, Azure OpenAI (gpt-4o deployment), tiktoken. Numbers: digit classifiers 98-99% on the sklearn test split; Tiny GPT 0.8M parameters, roughly 4 to 6 steps/s on CPU; averaged over 10 seeds on the cliff, SARSA about 27 vs Q-learning about 2 online reward (single runs are noisy); 84.8% on 20 newsgroups (6 categories, re-verified: 3,511 train / 2,338 test posts); MobileNetV2 3.5M parameters. LLM calls capped (default 150 per process, tiny max_tokens). If you want to say "in a day", confirm it against your own timeline before recording; the script keeps the claim as the working title only.

## Chapters (YouTube timestamps)
- 0:00 Cold open: the hub with 16 apps
- 0:35 Who I am and the deal: built with Claude Code
- 1:30 The stack
- 2:30 Tour 1: LLMs, RAG and security (01, 02, 03, 05, 08, 11, 12, 15)
- 4:15 Tour 2: classic ML and explainability (06, 13, 14)
- 5:30 Tour 3: deep learning from scratch (04, 07, 16)
- 6:45 Tour 4: RL and evolution (09, 10)
- 7:30 Shipping: hub, run_all, smoke test, cost control
- 8:30 Lessons learned
- 9:30 What's next + CTA

## Title options
1. I built 16 AI/ML projects in a day with an AI pair-programmer
2. 16 AI projects, one AI pair-programmer: what worked and what didn't
3. From LLM security to a tiny GPT: my 16-project AI portfolio (built with Claude Code)

## Thumbnail text (max 4 words)
"16 AI PROJECTS. 1 DAY." (alt: "16 PROJECTS, 1 DAY")

## Voice-over script (about 1,400 words)

### [0:00] Cold open (35 s)
This is a hub page. Sixteen buttons, sixteen working AI and machine learning apps. One teaches a neural network to draw its own decision boundary. One trains a tiny GPT live until gibberish turns into Shakespeare-ish text. One lets you try to hack a chatbot. [pause] I built all of these in about a day. Not alone: I had an AI pair-programmer, Claude Code, and I'm going to be honest throughout this video about exactly what that means. The narration you're hearing is AI-generated too. Let me show you what's here, what I learned, and where it fell short.

### [0:35] The deal (55 s)
I'm learning in public, and this channel is the notebook. The rule I set for these projects: each one is a single Python file you can read in one sitting. Each one should have a hook in the first three seconds: something you can see or play with, not a slide of equations.

How I worked with Claude Code: I picked the idea and the shape, it wrote most of the code, and I ran everything and decided what to keep. It also wrote tests, but I reviewed what they actually check. Where it got something wrong, and it did, I'll tell you. I'd call it pairing, not autopilot.

All sixteen apps together are only about fifteen hundred lines of Python. That matters, because small enough to read means small enough to learn from.

### [1:30] The stack (60 s)
The stack is deliberately boring. Streamlit for every interface, because one file gives you sliders, charts and buttons. scikit-learn for the classic machine learning. numpy, for when I want to write a neural network by hand. PyTorch on the CPU, for the transformer and the image model. plotly for the interactive charts. tiktoken to see text the way GPT sees it. And Azure OpenAI, a GPT-4o deployment, for the apps that need a language model.

Two cost rules. First, the LLM apps use tiny calls with small token limits, and the code has a hard cap on calls per run. Second, more than half of the projects need no API at all: they run entirely on your laptop CPU. No GPU, no Docker.

### [2:30] Tour 1: LLMs, RAG and security (105 s)
First group: language models. The Prompt Arena pits two prompting styles against each other with a judge that scores both orderings, to cancel out position bias. Prompt Injection Lab is a Gandalf-style game with five defence levels, then an automated red-team heat map. My honest finding: GPT-4o is robust, so mostly only level one leaks, and the grid is mostly green. I left it that way because it's the real result.

The Semantic Map shows embeddings on a 2D map and answers questions with retrieval. A caveat: I only had a chat deployment, so the embeddings are computed locally with character n-grams. The map clusters by wording rather than true meaning. Spot the Hallucination hides one lie among five facts; 20 Questions plays both directions; the Debate Arena has two debaters and a judge.

Token X-ray shows text as coloured tokens, with cost, and explains why a language model can't reliably count the letters in a word. And the new Prompt Gym gives you six levels where Python checks the model's answer: exactly ten words, strict JSON, no intro line.

### [4:15] Tour 2: classic ML and explainability (75 s)
Second group: classic machine learning, which still does a lot of the work in the real world. Draw a Digit lets you sketch a number while an SVM, a neural net, a random forest and k-nearest neighbours vote. They score 98 to 99 percent on the held-out digits, but trained on tiny eight-by-eight images, they often misread a messy drawing. That disagreement is the demo.

Clustering Lab walks K-means step by step, then runs four algorithms over five datasets. K-means cuts the moons in half; DBSCAN gets them right.

Explainable Text AI is my favourite of the three. A TF-IDF logistic regression gets 84.8 percent on unseen newsgroup posts, and it highlights which words pushed toward the answer and which pulled away. Not a black box.

### [5:30] Tour 3: deep learning (75 s)
Third group: deep learning, built rather than just used. The Neural Net Playground is backpropagation written in numpy; you watch the decision boundary bend as it trains.

The Tiny GPT Trainer is a character-level transformer with about 0.8 million parameters, trained live on Shakespeare with PyTorch on the CPU, at roughly six steps per second. You watch the output go from random characters to something that looks like a play. It's not smart. It's educational.

And CNN X-ray runs MobileNetV2 and uses Grad-CAM to paint the pixels behind each guess. A banana gets ninety-five percent; a cat is split between tiger cat and tabby at twenty-two and thirteen.

### [6:45] Tour 4: RL and evolution (45 s)
Fourth group: learning without labels. The RL Gridworld runs Q-learning and SARSA side by side on a cliff. Q-learning learns the risky edge path, SARSA the safe one, and averaged over ten seeds, SARSA scored an online reward of about 27 versus about 2 for Q-learning, because the risky path keeps falling off during training. And Evolving Rockets uses a genetic algorithm: rockets steer around obstacles to a target, and you scrub through the generations. One level, the zig-zag, doesn't get solved on some seeds. That's by design.

### [7:30] Shipping (60 s)
The skill people skip is shipping. So there is a hub page that links to everything, a `run_all` script that starts every app on its own port, and a smoke test that runs each app headlessly and fails if any of them throws an error. All sixteen apps and the hub pass that test.

There's cost control too: the LLM wrapper counts calls and refuses past the cap, and the key lives in an environment file that is never committed. Nothing in these videos shows it.

### [8:30] Lessons learned (60 s)
Five lessons.

One: scope tiny. A single file per idea forces you to cut until only the interesting part is left.

Two: choose a hook first. If I couldn't say what you'd see in three seconds, I changed the idea.

Three: test what the AI wrote. Tooling changed under us: one canvas package was broken on this version of Streamlit, so the digit app has its own small component. The AI fixed it, but only because I ran it and saw it fail.

Four: be honest about results. A security lab where the bot mostly wins isn't a failure; it's a finding.

Five: an AI pair-programmer makes you faster at building and no faster at understanding. The understanding still has to come from you. That's why I'm making these videos.

### [9:30] Next + CTA (30 s)
Next up: an attention visualiser for the tiny GPT, real embeddings for the semantic map, and an agent with a visible thought log. Tell me in the comments which one you want first. Subscribe, and the code is linked below. Thanks for watching.

## Shot list
| Time | Screen | Code | Avatar |
|---|---|---|---|
| 0:00-0:35 | Hub page (http://localhost:8500) scrolling the 16 cards, quick cuts of each app | | Avatar for the last two sentences |
| 0:35-1:30 | | `wc -l` of the app files; repo tree | Avatar PiP |
| 1:30-2:30 | Logo-free text cards for each library (plain text, no brand artwork) | `requirements.txt` | Avatar PiP |
| 2:30-4:15 | Screen captures: 01 arena, 02 heat map, 03 map, 11 token chips, 15 gym | `common/llm.py` call cap | Avatar small |
| 4:15-5:30 | 06 voting on a drawn digit, 13 showdown grid, 14 highlighted words | | Avatar small |
| 5:30-6:45 | 04 boundary bending, 07 text improving, 16 banana heat map | | Avatar small |
| 6:45-7:30 | 09 side-by-side policies, 10 generations scrub | | Avatar small |
| 7:30-8:30 | Terminal: `python run_all.py`, `python smoke_test.py` output | `run_all.py` | Avatar PiP |
| 8:30-9:30 | Five text cards, one per lesson | | Avatar full screen |
| 9:30-10:00 | End card | | Avatar full screen |

Recording notes: do not show `.env`. Keep Azure calls under budget by reusing footage. Capture only apps that were really run.

## Description
I built 16 AI and ML demo apps with an AI pair-programmer (Claude Code): LLM games and prompt-injection security, embeddings and RAG, classic ML, a neural network and a tiny GPT from scratch, Grad-CAM, reinforcement learning, evolutionary algorithms, and a hub with a smoke test to ship it all.

Stack: Streamlit, scikit-learn, PyTorch (CPU), numpy, plotly, Azure OpenAI, tiktoken.
Built with Claude Code. The narration is AI-generated. No GPU needed; more than half the projects make no API calls.

Chapters: see timestamps above.
Code: link to the repo (add before upload).

## Tags
ai projects, machine learning projects, claude code, ai pair programming, streamlit, scikit-learn, pytorch, llm, prompt injection, reinforcement learning, genetic algorithm, explainable ai, portfolio

## Pinned comment
Which of the 16 should get its own deep-dive video? Reply with a number or a name. Reminder: the apps were built with Claude Code and the narration is AI-generated; if I got something wrong, tell me and I'll pin the correction.
