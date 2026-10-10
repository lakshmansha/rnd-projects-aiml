"""Prompt Arena: pit two prompting styles of the same LLM against each other, a judge picks winners, Elo tracks it."""
import json
import random
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402

STATE = Path(__file__).parent / "elo.json"
PROMPTS = [
    "Explain recursion to a 10-year-old in 3 sentences.",
    "Give me a one-line Python function that reverses a string.",
    "Why is the sky blue? Keep it under 50 words.",
    "Write a haiku about debugging at 2am.",
    "What is the difference between a list and a tuple in Python?",
    "Summarise what a neural network is in two sentences.",
    "Give three tips for a first YouTube video.",
    "Is 91 a prime number? Explain briefly.",
]
K = 32
STYLES = {
    "Concise": "Answer in the fewest words that are still correct.",
    "Step-by-step": "Think step by step, briefly, then give the answer.",
    "ELI5": "Explain like the reader is 5 years old, using a simple analogy.",
    "Pirate": "Answer correctly, but talk like a pirate.",
    "Expert": "Answer like a senior engineer: precise, technical, no fluff.",
}


def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {"elo": {}, "history": []}


def save(s):
    STATE.write_text(json.dumps(s, indent=1))


def update_elo(elo, a, b, score_a):
    ra, rb = elo.get(a, 1000.0), elo.get(b, 1000.0)
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    elo[a] = ra + K * (score_a - ea)
    elo[b] = rb + K * ((1 - score_a) - (1 - ea))


def judge(judge_model, prompt, ans_1, ans_2):
    """Ask the judge once. Returns 1, 2 or 0 (tie / unparseable)."""
    msg = [{"role": "system", "content": "You are a strict impartial judge. Reply ONLY with JSON: "
            '{"winner": 1} or {"winner": 2} or {"winner": 0} for a tie.'},
           {"role": "user", "content": f"Question: {prompt}\n\n[Answer 1]\n{ans_1}\n\n[Answer 2]\n{ans_2}\n\n"
            "Which answer is more correct, clear and concise?"}]
    text, _ = llm.chat(msg, temperature=0, max_tokens=10, json_mode=True)
    try:
        return int(json.loads(text).get("winner", 0))
    except Exception:
        return 0


def battle(model_a, model_b, judge_model, prompt):
    ans_a, ta = llm.chat([{"role": "system", "content": STYLES[model_a]}, {"role": "user", "content": prompt}], max_tokens=90)
    ans_b, tb = llm.chat([{"role": "system", "content": STYLES[model_b]}, {"role": "user", "content": prompt}], max_tokens=90)
    # Judge twice with swapped positions to cancel position bias; disagreement = tie.
    v1 = judge(judge_model, prompt, ans_a, ans_b)
    v2 = judge(judge_model, prompt, ans_b, ans_a)
    a_pts = (v1 == 1) + (v2 == 2)
    b_pts = (v1 == 2) + (v2 == 1)
    score_a = 1.0 if a_pts > b_pts else 0.0 if b_pts > a_pts else 0.5
    return dict(prompt=prompt, a=model_a, b=model_b, ans_a=ans_a, ans_b=ans_b,
                time_a=round(ta, 1), time_b=round(tb, 1), score_a=score_a)


st.set_page_config(page_title="Prompt Arena", page_icon="🥊", layout="wide")
st.title("🥊 Prompt Arena")
st.caption("Two prompting styles of GPT fight, a judge scores both orderings, Elo does the rest.")

models = list(STYLES)

state = load()
with st.sidebar:
    st.header("Setup (prompting styles)")
    a = st.selectbox("Fighter A", models, index=0)
    b = st.selectbox("Fighter B", models, index=min(1, len(models) - 1))
    j = None  # judge is the same gpt deployment
    st.caption("Each battle = 2 answers + 2 judge calls (4 tiny API calls).")
    n = st.slider("Battles to run", 1, 5, 2)
    if st.button("Reset leaderboard"):
        save({"elo": {}, "history": []})
        st.rerun()

custom = st.text_input("Custom prompt (optional)")
if st.button("⚔️ Fight!", type="primary"):
    prompts = [custom] if custom else random.sample(PROMPTS, min(n, len(PROMPTS)))
    for p in prompts:
        with st.status(f"Round: {p}", expanded=True) as status:
            r = battle(a, b, j, p)
            update_elo(state["elo"], a, b, r["score_a"])
            state["history"].append(r)
            save(state)
            c1, c2 = st.columns(2)
            c1.markdown(f"**{a}** ({r['time_a']}s)\n\n{r['ans_a']}")
            c2.markdown(f"**{b}** ({r['time_b']}s)\n\n{r['ans_b']}")
            verdict = {1.0: f"🏆 {a} wins", 0.0: f"🏆 {b} wins", 0.5: "🤝 Draw"}[r["score_a"]]
            status.update(label=f"{p} → {verdict}", state="complete")

st.subheader("Leaderboard")
if state["elo"]:
    df = pd.DataFrame(sorted(state["elo"].items(), key=lambda x: -x[1]), columns=["model", "elo"])
    st.plotly_chart(px.bar(df, x="model", y="elo", color="model", text=df["elo"].round(0)), use_container_width=True)
    hist = pd.DataFrame(state["history"])
    st.caption(f"{len(hist)} battles recorded")
else:
    st.info("No battles yet - hit Fight!")
