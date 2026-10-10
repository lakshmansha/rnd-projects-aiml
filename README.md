# AI/ML Showcase - 3 demo projects for YouTube

Chat uses the Azure OpenAI deployment from `.env` (see `.env.example`). No Docker needed.
Calls are kept tiny (<=90 tokens) and capped per process by `MAX_LLM_CALLS` (default 150).
Embeddings are computed locally with hashing n-grams (no embedding deployment required).

| # | Project | Hook for the video |
|---|---------|--------------------|
| 1 | `01-llm-arena` | Two prompting styles of GPT fight; a judge (run in both orderings to cancel position bias) scores them; Elo leaderboard |
| 2 | `02-prompt-injection-lab` | Gandalf-style game: 5 defense levels, then an automated red-team heatmap |
| 3 | `03-semantic-map` | Watch embeddings cluster meaning on a 2D map, search drops a star, RAG answers |
| 4 | `04-neural-playground` | A neural net written from scratch in numpy; train it live and watch the decision boundary bend (no API calls) |
| 5 | `05-spot-the-hallucination` | Game: GPT hides one subtle lie among 5 facts; can you spot it? |

## Run
```
pip install -r requirements.txt
streamlit run 01-llm-arena/app.py
streamlit run 02-prompt-injection-lab/app.py
streamlit run 03-semantic-map/app.py
streamlit run 04-neural-playground/app.py
streamlit run 05-spot-the-hallucination/app.py
```
