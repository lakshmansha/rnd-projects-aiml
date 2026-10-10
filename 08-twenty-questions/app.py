"""AI 20 Questions: guess GPT's secret, or think of something and watch GPT try to read your mind."""
import json
import random
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402

SECRETS = {
    "Animal": ["penguin", "octopus", "giraffe", "kangaroo", "dolphin", "eagle", "elephant", "bee", "crocodile", "panda"],
    "Object": ["umbrella", "toothbrush", "bicycle", "microscope", "guitar", "clock", "refrigerator", "scissors", "telescope", "backpack"],
    "Place": ["Eiffel Tower", "Sahara Desert", "Taj Mahal", "Mount Everest", "Amazon River", "Great Wall of China", "Antarctica", "Niagara Falls"],
    "Food": ["pizza", "sushi", "chocolate", "banana", "popcorn", "pancake", "ice cream", "avocado"],
    "Tech": ["smartphone", "Wi-Fi router", "keyboard", "drone", "robot vacuum", "satellite", "Bitcoin", "neural network"],
}
MAX_Q = 20

st.set_page_config(page_title="AI 20 Questions", page_icon="❓")
st.title("❓ AI 20 Questions")
ss = st.session_state
mode = st.sidebar.radio("Who guesses?", ["You guess GPT's secret", "GPT guesses your secret"])
st.sidebar.caption("About 1 tiny Azure call per question.")


def reset(**kw):
    ss.game = dict(mode=mode, log=[], over=False, msg="", **kw)


def ask_json(system, user, max_tokens=60):
    text, _ = llm.chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                       temperature=0.3, max_tokens=max_tokens, json_mode=True)
    return json.loads(text)


# ---------- Mode A: the player guesses ----------
def play_user_guesses():
    g = ss.game
    st.write(f"I'm thinking of something in the category **{g['cat']}**. Ask yes/no questions, or make a guess!")
    for q, a in g["log"]:
        st.chat_message("user").write(q)
        st.chat_message("assistant").write(a)
    left = MAX_Q - len(g["log"])
    if g["over"]:
        (st.success if g["won"] else st.error)(g["msg"])
        return
    st.progress(left / MAX_Q, text=f"{left} questions left")
    q = st.chat_input("Is it bigger than a car?  /  Is it a penguin?")
    if not q:
        return
    secret = g["secret"]
    try:
        r = ask_json(f"You are the host of 20 Questions. The secret is '{secret}'. Reply ONLY JSON "
                     '{"answer": "Yes|No|Sometimes|Irrelevant", "correct": true|false}. "correct" is true only if the user\'s '
                     f"message is a direct guess that names '{secret}' (or a clear synonym). Never reveal the secret.", q)
    except Exception as e:
        st.error(f"Host error: {e}")
        return
    g["log"].append((q, r.get("answer", "Irrelevant")))
    if r.get("correct"):
        g.update(over=True, won=True, msg=f"🎉 Yes, it was **{secret}**! You got it in {len(g['log'])} questions.")
    elif len(g["log"]) >= MAX_Q:
        g.update(over=True, won=False, msg=f"Out of questions. It was **{secret}**.")
    st.rerun()


# ---------- Mode B: GPT guesses ----------
def gpt_turn():
    g = ss.game
    hist = "\n".join(f"Q: {q}\nA: {a}" for q, a in g["log"]) or "(no questions yet)"
    last = len(g["log"]) >= MAX_Q - 1
    r = ask_json("You are playing 20 Questions and must guess what the human is thinking of. Ask ONE smart yes/no question "
                 "that splits the remaining possibilities, or make a final guess when confident. Reply ONLY JSON "
                 '{"type": "question"|"guess", "text": "..."}.' + (" This is your LAST turn: you must guess." if last else ""),
                 f"Questions so far:\n{hist}", max_tokens=50)
    g["pending"] = r


def play_gpt_guesses():
    g = ss.game
    st.write("Think of any **object, animal, place or thing**. Don't tell me. Answer honestly!")
    for q, a in g["log"]:
        st.chat_message("assistant").write(q)
        st.chat_message("user").write(a)
    if g["over"]:
        (st.success if g["won"] else st.warning)(g["msg"])
        return
    if "pending" not in g:
        try:
            with st.spinner("Thinking..."):
                gpt_turn()
        except Exception as e:
            st.error(f"GPT error: {e}")
            return
    p = g["pending"]
    st.chat_message("assistant").write(p["text"])
    if p["type"] == "guess":
        c1, c2 = st.columns(2)
        if c1.button("✅ Correct!"):
            g.update(over=True, won=True, msg=f"GPT read your mind in {len(g['log'])} questions 🧠")
            st.rerun()
        if c2.button("❌ Nope"):
            g["log"].append((f"Is it {p['text']}", "No"))
            g.pop("pending")
            if len(g["log"]) >= MAX_Q:
                g.update(over=True, won=False, msg="GPT ran out of questions. You win! 🏆")
            st.rerun()
    else:
        cols = st.columns(3)
        for col, ans in zip(cols, ["Yes", "No", "Sometimes"]):
            if col.button(ans, width="stretch"):
                g["log"].append((p["text"], ans))
                g.pop("pending")
                if len(g["log"]) >= MAX_Q:
                    g.update(over=True, won=False, msg="GPT ran out of questions. You win! 🏆")
                st.rerun()
    st.progress((MAX_Q - len(g["log"])) / MAX_Q, text=f"{MAX_Q - len(g['log'])} questions left")


# ---------- router ----------
if "game" not in ss or ss.game["mode"] != mode:
    cat = st.selectbox("Category", list(SECRETS)) if mode.startswith("You") else None
    if st.button("▶ Start game", type="primary"):
        reset(cat=cat, secret=random.choice(SECRETS[cat]) if cat else None, won=False)
        st.rerun()
    st.stop()
if st.sidebar.button("🔄 New game"):
    del ss["game"]
    st.rerun()
(play_user_guesses if mode.startswith("You") else play_gpt_guesses)()
