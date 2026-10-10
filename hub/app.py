"""Demo hub: one page linking to every project."""
import streamlit as st

st.set_page_config(page_title="AI/ML Demo Hub", page_icon="🎬", layout="wide")
st.title("🎬 AI/ML Demo Hub")
st.caption("Start everything with `python run_all.py`. Cost column: how much Azure OpenAI each demo uses.")

APPS = [
    (8501, "🥊 Prompt Arena", "Two GPT prompting styles fight; a judge + Elo decide", "GPT, ~4 calls/battle"),
    (8502, "🔐 Prompt Injection Lab", "Hack a bot guarding a password across 5 defense levels", "GPT, ~1 call/attack"),
    (8503, "🗺️ Semantic Map", "Embeddings on a 2D map + RAG answers", "GPT, 1 call/search"),
    (8504, "🧠 Neural Net Playground", "Backprop from scratch, watch the boundary bend", "none"),
    (8505, "🕵️ Spot the Hallucination", "Find the one lie among 5 GPT facts", "GPT, 1 call/round"),
    (8506, "✏️ Draw a Digit", "4 ML models vote on your hand-drawn digit", "none"),
    (8507, "🤖 Tiny GPT Trainer", "Train a transformer from scratch, watch it learn to write", "none"),
    (8508, "❓ AI 20 Questions", "Guess GPT's secret, or GPT guesses yours", "GPT, 1 call/question"),
    (8509, "🎮 RL Gridworld", "Q-learning vs SARSA on a cliff", "none"),
    (8510, "🚀 Evolving Rockets", "A genetic algorithm breeds smarter rockets", "none"),
    (8511, "🔬 Token X-ray", "See text the way an LLM sees it", "none"),
    (8512, "🎤 AI Debate Arena", "Two GPT debaters, a judge, and your changed mind", "GPT, 2×rounds+1 calls"),
    (8513, "🧩 Clustering Lab", "K-means step by step + algorithm showdown", "none"),
    (8514, "🔍 Explainable Text AI", "Which words drove the classifier's decision?", "none"),
    (8515, "🏋️ Prompt Gym", "Write prompts that pass strict automatic checks", "GPT, 1 call/attempt"),
]
cols = st.columns(3)
for i, (port, name, blurb, cost) in enumerate(APPS):
    with cols[i % 3].container(border=True):
        st.subheader(name)
        st.write(blurb)
        st.caption(f"Cost: {cost}")
        st.link_button("Open ↗", f"http://localhost:{port}", width="stretch")
