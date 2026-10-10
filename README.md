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
| 6 | `06-digit-classifier` | Draw a digit on a canvas; SVM, neural net, random forest and k-NN (trained live on sklearn digits) vote - no API calls |
| 7 | `07-tiny-gpt` | Train a real transformer (0.8M params, PyTorch CPU) from scratch and watch gibberish turn into Shakespeare-ish text |
| 8 | `08-twenty-questions` | AI 20 Questions: guess GPT's secret, or GPT tries to read your mind |
| 9 | `09-rl-gridworld` | Q-learning vs SARSA learn a cliff-walking world side by side; scrub through training (no API calls) |
| 10 | `10-evolving-rockets` | A genetic algorithm evolves rockets that dodge obstacles to hit a target; scrub through generations (no API calls) |

## Run
```
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu   # only for 07
streamlit run 01-llm-arena/app.py
streamlit run 02-prompt-injection-lab/app.py
streamlit run 03-semantic-map/app.py
streamlit run 04-neural-playground/app.py
streamlit run 05-spot-the-hallucination/app.py
streamlit run 06-digit-classifier/app.py
streamlit run 07-tiny-gpt/app.py
streamlit run 08-twenty-questions/app.py
streamlit run 09-rl-gridworld/app.py
streamlit run 10-evolving-rockets/app.py
```
