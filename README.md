# AI/ML Showcase - 3 demo projects for YouTube

All run locally on CPU with small LLMs served from Docker (Ollama). No Azure.
Optional: set `LLM_PROVIDER=openai` + `OPENAI_API_KEY` in `.env` to use a GPT model instead.

| # | Project | Hook for the video |
|---|---------|--------------------|
| 1 | `01-llm-arena` | Two models fight; a judge (run in both orderings to cancel position bias) scores them; Elo leaderboard |
| 2 | `02-prompt-injection-lab` | Gandalf-style game: 5 defense levels, then an automated red-team heatmap |
| 3 | `03-semantic-map` | Watch embeddings cluster meaning on a 2D map, search drops a star, RAG answers |

## Run
```
docker compose up -d
docker exec ollama ollama pull qwen2.5:0.5b
docker exec ollama ollama pull qwen2.5:1.5b
docker exec ollama ollama pull all-minilm
pip install -r requirements.txt
streamlit run 01-llm-arena/app.py
streamlit run 02-prompt-injection-lab/app.py
streamlit run 03-semantic-map/app.py
```
Docker here has ~2 GB RAM, so models are tiny. Give Docker more RAM and pull `llama3.2:3b` for better answers.
