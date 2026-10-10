"""Prompt Injection Lab: hack the bot yourself, then watch an automated red-team grid."""
import pandas as pd
import plotly.express as px
import streamlit as st

import engine

st.set_page_config(page_title="Prompt Injection Lab", page_icon="🔐", layout="wide")
st.title("🔐 Prompt Injection Lab")
st.caption("A small LLM guards a secret password. Five defense levels. Can you break them?")

tab_play, tab_red = st.tabs(["🎮 Play", "🤖 Automated red team"])

with tab_play:
    level = st.select_slider("Defense level", options=list(engine.LEVELS), format_func=lambda x: f"Level {x}")
    st.info(engine.LEVELS[level])
    msg = st.text_input("Your attack", placeholder="Try to make it say the password...")
    if st.button("Send", type="primary") and msg:
        with st.spinner("Thinking..."):
            r = engine.ask(level, msg)
        st.chat_message("user").write(msg)
        st.chat_message("assistant").write(r["reply"])
        if r["leaked"]:
            st.error("💥 The secret leaked! You win this level.")
        elif r["blocked_by"]:
            st.warning(f"Defense: {r['blocked_by']}")
        else:
            st.success("Secret held.")

with tab_red:
    st.write(f"Fire {len(engine.ATTACKS)} known attacks at every level and see which defenses hold.")
    levels = st.multiselect("Levels", list(engine.LEVELS), default=list(engine.LEVELS))
    st.caption("~1 tiny API call per attack per level (2 on level 5). Pick fewer levels to spend less.")
    if st.button("🚀 Run red team"):
        rows, bar = [], st.progress(0.0)
        total, done = len(levels) * len(engine.ATTACKS), 0
        for lv in levels:
            for name, text in engine.ATTACKS.items():
                r = engine.ask(lv, text)
                rows.append(dict(level=f"L{lv}", attack=name, leaked=int(r["leaked"])))
                done += 1
                bar.progress(done / total)
        df = pd.DataFrame(rows)
        pivot = df.pivot(index="attack", columns="level", values="leaked")
        fig = px.imshow(pivot, color_continuous_scale=["#2ecc71", "#e74c3c"], text_auto=True, aspect="auto",
                        labels=dict(color="leaked"))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df.groupby("level").leaked.mean().rename("leak rate").to_frame().style.format("{:.0%}"))
