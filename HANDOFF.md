# Handoff: AI/ML YouTube demo projects

Date: 2026-10-10 · Location: `D:\Research\Source\rnd-projects-aiml` · Git: local repo, one commit per project.

## What this is
A collection of 15 small Streamlit apps for YouTube demos on AI/ML. Each is a single `app.py` (project 02 also has `engine.py`, project 07 has `model.py`). Shared code is in `common/llm.py`.

## How to run
```
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu    # only project 07
python run_all.py            # all apps on ports 8501-8515, hub at http://localhost:8500
python run_all.py 4 6        # only projects 04 and 06
```
Port = 8500 + project number.

## What was built (all tested headlessly with Streamlit AppTest; 06 also driven in real Chrome)
| # | Project | Type | Azure cost |
|---|---------|------|-----------|
| 01 | Prompt Arena: GPT prompting styles fight, judge scores both orderings, Elo | LLM game | ~4 calls/battle |
| 02 | Prompt Injection Lab: 5 defense levels, manual play + automated red-team heatmap | LLM security | ~1 call/attack |
| 03 | Semantic Map: embeddings on a 2D map + RAG answer | embeddings + RAG | 1 call/search |
| 04 | Neural Net Playground: numpy backprop, live decision boundary | build a model | none |
| 05 | Spot the Hallucination: find the lie among 5 GPT facts | LLM game | 1 call/round |
| 06 | Draw a Digit: SVM / MLP / RF / k-NN vote on your drawing (custom canvas component) | classic ML | none |
| 07 | Tiny GPT Trainer: 0.8M-param char transformer trained live on Shakespeare (PyTorch CPU) | build a model | none |
| 08 | AI 20 Questions (both directions) | LLM game | 1 call/question |
| 09 | RL Gridworld: Q-learning vs SARSA, scrub through training | RL | none |
| 10 | Evolving Rockets: genetic algorithm, scrub through generations | evolutionary | none |
| 11 | Token X-ray: tiktoken colour chips, cost, why LLMs can't count letters | LLM education | none |
| 12 | AI Debate Arena: 2 debaters + judge radar chart + "did it change your mind" | LLM | 2×rounds+1 calls |
| 13 | Clustering Lab: K-means step-by-step + 4 algorithms x 5 datasets | classic ML | none |
| 14 | Explainable Text AI: TF-IDF classifier highlighting the words behind each decision | classic ML | none |
| 15 | Prompt Gym: 6 prompt-writing levels graded by Python checkers | LLM game | 1 call/attempt |

Also: `hub/app.py` (landing page linking everything), `run_all.py`, `README.md`.

## Configuration and decisions (read before changing things)
- **LLM = Azure OpenAI**, read from the root `.env` (gitignored, never committed): `AZURE_OPENAI_API_KEY`, `_ENDPOINT`, `_DEPLOYMENT` (gpt-4o), `_API_VERSION`. `.env.example` has the template. Only a **chat** deployment exists.
- **Cost control:** every call is small (`max_tokens` 3-350), and `common/llm.py` has a per-process cap `MAX_LLM_CALLS` (default 150, set in `.env` to change). The user asked for "very low" usage.
- **Docker was abandoned.** The first plan was Ollama in Docker, but Docker Desktop was unstable (and only ~2 GB RAM), and the user then said to use Azure. `docker-compose.yml` was removed. No project needs Docker.
- **Embeddings are local** hashing char-n-grams (`common/llm.embed`), because there is no Azure embedding deployment. Consequence: project 03's map clusters by wording, not true meaning. Adding an embedding deployment and switching `embed()` would improve it.
- **Azure content filter** may reject jailbreak-style prompts; project 02 treats that as "blocked by Azure content filter".
- **Streamlit is 1.65.** The `streamlit-drawable-canvas` package is broken on it, so project 06 uses its own inline v2 component. `use_container_width` is deprecated; code uses `width="stretch"`.
- **Downloads on first run:** 14 fetches 20newsgroups via scikit-learn (slow once, then cached in `~/scikit_learn_data`); 11 uses tiktoken vocab files; 07 needs `data/shakespeare.txt` (committed).

## Known limits
- 06: trained on 8x8 sklearn digits; messy or off-centre drawings are often misread (that disagreement is part of the demo). Only a "7" was tested by hand.
- 05: the "true" facts come from GPT itself, so a round can occasionally contain a wrong "fact".
- 10: the Zig-zag level is hard and unsolved on some seeds (by design; the UI suggests more generations).
- 02: GPT-4o is robust, so only level 1 (and sometimes 2) leaks. The red-team grid is mostly green, which is an honest result.
- Nothing has been screen-recorded or run through a full manual click-through except 06.

## In progress (not committed)
`16-cnn-xray/`: upload a photo -> MobileNetV2 (ImageNet) top-5 + Grad-CAM heatmap. `torchvision` (CPU) and the weights download were started; only `samples/dog.jpg` may exist. No `app.py` yet.

## What we can do next
1. **Finish 16 CNN X-ray** (Grad-CAM + webcam via `st.camera_input`).
2. **Attention visualiser** for project 07 (heatmap of what each head looks at).
3. **Real embeddings** for 03 (Azure embedding deployment) plus a "chat with your own PDF" mode.
4. **Overfitting / bias-variance lab** (polynomial degree slider, train vs test error).
5. **Self-consistency demo**: ask GPT a maths question 5 times and majority-vote (shows why sampling helps; ~30 calls).
6. **LLM agent demo**: tool-using agent (calculator + search over local docs) with a visible thought/action log.
7. **Polish for filming:** dark theme, bigger fonts (`.streamlit/config.toml`), a title card per app, record each with the Chrome GIF tool.
8. **Video plan:** best hooks are 06 (draw a digit), 07 (watch gibberish become Shakespeare), 09 (SARSA vs Q-learning cliff), 10 (rockets), 02 (hack the bot). 04 and 13 are good short explainers.
9. **Housekeeping:** add a simple smoke-test script that runs every app with AppTest; pin versions in `requirements.txt`.
