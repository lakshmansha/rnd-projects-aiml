"""AI Debate Arena: two GPT debaters argue, a judge scores them, and we measure whether they changed YOUR mind."""
import json
import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402

TOPICS = [
    "Pineapple belongs on pizza.",
    "AI will create more jobs than it destroys.",
    "Remote work is better than the office.",
    "Tabs are better than spaces.",
    "Cats make better pets than dogs.",
    "Social media does more harm than good.",
    "Homework should be abolished.",
]
CRITERIA = ["logic", "evidence", "persuasion", "clarity", "rebuttal"]

st.set_page_config(page_title="AI Debate Arena", page_icon="🎤")
st.title("🎤 AI Debate Arena")
st.caption("Two GPT debaters, one judge, and you. Each debate = 2×rounds + 1 tiny Azure calls.")

ss = st.session_state
topic = st.selectbox("Motion", TOPICS + ["(write your own)"])
if topic == "(write your own)":
    topic = st.text_input("Your motion", "Mondays should be banned.")
rounds = st.slider("Rounds", 1, 3, 2)
before = st.slider("Before the debate: do you agree with the motion? (0 = strongly disagree, 10 = strongly agree)", 0, 10, 5)


def say(side, history, round_no):
    stance = "FOR" if side == "Pro" else "AGAINST"
    msgs = [{"role": "system", "content": f"You are a sharp competitive debater arguing {stance} the motion: '{topic}'. "
             "In 2-3 punchy sentences (max 60 words): make your strongest new point and directly rebut the opponent's last point. "
             "No pleasantries, no repeating yourself."},
            {"role": "user", "content": (f"Debate so far:\n{history}\n\n" if history else "") + f"Round {round_no}. Your turn."}]
    return llm.chat(msgs, temperature=0.9, max_tokens=110)[0]


def judge(transcript):
    text, _ = llm.chat([
        {"role": "system", "content": "You are an impartial debate judge. Score each side 1-10 on logic, evidence, persuasion, clarity, rebuttal. "
         'Reply ONLY JSON: {"pro": {"logic": n, ...}, "con": {"logic": n, ...}, "winner": "pro"|"con", "reason": "one sentence"}.'},
        {"role": "user", "content": f"Motion: {topic}\n\n{transcript}"}], temperature=0, max_tokens=220, json_mode=True)
    return json.loads(text)


if st.button("🔥 Start debate", type="primary"):
    history, turns = "", []
    try:
        for r in range(1, rounds + 1):
            for side in ("Pro", "Con"):
                with st.spinner(f"Round {r}: {side} is thinking..."):
                    msg = say(side, history, r)
                history += f"{side}: {msg}\n"
                turns.append((side, r, msg))
        with st.spinner("The judge is deliberating..."):
            verdict = judge(history)
    except Exception as e:
        st.error(f"Debate failed: {e}")
        st.stop()
    ss.debate = dict(turns=turns, verdict=verdict, topic=topic, before=before)

d = ss.get("debate")
if d:
    st.header(f"Motion: {d['topic']}")
    for side, r, msg in d["turns"]:
        with st.chat_message("user" if side == "Pro" else "assistant", avatar="🟢" if side == "Pro" else "🔴"):
            st.markdown(f"**{side} · round {r}**  \n{msg}")
    v = d["verdict"]
    st.header("⚖️ Verdict")
    fig = go.Figure()
    for side, col in (("pro", "#2f9e44"), ("con", "#e03131")):
        vals = [v[side].get(c, 0) for c in CRITERIA]
        fig.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=CRITERIA + CRITERIA[:1], fill="toself", name=side.title(), line_color=col))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 10])), height=380, margin=dict(t=20, b=20))
    c1, c2 = st.columns([3, 2])
    c1.plotly_chart(fig, width="stretch")
    c2.metric("Winner", v["winner"].title())
    c2.metric("Pro total", sum(v["pro"].values()))
    c2.metric("Con total", sum(v["con"].values()))
    st.info(v["reason"])
    st.subheader("Did they change your mind?")
    after = st.slider("After the debate: do you agree with the motion?", 0, 10, d["before"], key="after")
    shift = after - d["before"]
    st.metric("Your shift", f"{shift:+d} points", delta=shift)
    if shift == 0:
        st.caption("Unmoved. Stubborn human, or the bots weren't convincing enough.")
