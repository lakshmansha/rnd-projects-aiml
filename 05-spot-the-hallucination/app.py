"""Spot the Hallucination: GPT mixes one subtle falsehood into true facts. Can you find it?"""
import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402

TOPICS = ["Space", "Human body", "World history", "Programming", "Animals", "Geography", "Physics", "Food science"]

st.set_page_config(page_title="Spot the Hallucination", page_icon="🕵️")
st.title("🕵️ Spot the Hallucination")
st.caption("LLMs state falsehoods as confidently as facts. One of these 5 statements is fake. Find it.")

ss = st.session_state
ss.setdefault("score", 0)
ss.setdefault("rounds", 0)
ss.setdefault("round", None)
ss.setdefault("answered", False)
ss.setdefault("hit", False)

topic = st.sidebar.selectbox("Topic", TOPICS)
st.sidebar.metric("Score", f"{ss.score} / {ss.rounds}")
st.sidebar.caption("1 small Azure call per round.")


def new_round():
    text, _ = llm.chat(
        [{"role": "system", "content": 'Reply ONLY with JSON: {"statements": [5 short strings], "fake_index": 0-4, '
          '"truth": "one-sentence correction of the fake one"}. Exactly 4 statements must be true; 1 must be '
          "subtly but definitely false (plausible-sounding, with a wrong number, name or cause)."},
         {"role": "user", "content": f"Topic: {topic}. Surprising but well-established facts. Random seed: {id(object())}"}],
        temperature=1.0, max_tokens=350, json_mode=True)
    ss.round, ss.answered = json.loads(text), False


if st.button("🎲 New round", type="primary") or ss.round is None:
    try:
        new_round()
    except Exception as e:  # content filter / bad JSON / network
        st.error(f"Could not start a round: {e}")
        st.stop()

r = ss.round
choice = st.radio("Which one is the hallucination?", range(5), format_func=lambda i: r["statements"][i],
                  index=None, disabled=ss.answered)
if choice is not None and not ss.answered:
    ss.answered, ss.hit = True, choice == r["fake_index"]
    ss.rounds += 1
    ss.score += int(ss.hit)
    st.rerun()  # refresh the sidebar score
if ss.answered:
    fake = r["statements"][r["fake_index"]]
    (st.success if ss.hit else st.error)("🎯 Caught it!" if ss.hit else f"Fooled! The fake was: “{fake}”")
    st.info(f"Truth: {r['truth']}")
