"""Token X-ray: see text the way an LLM sees it. No API calls."""
import html

import pandas as pd
import plotly.express as px
import streamlit as st
import tiktoken

st.set_page_config(page_title="Token X-ray", page_icon="🔬", layout="wide")
st.title("🔬 Token X-ray")
st.caption("LLMs never see letters or words, only token IDs. This is the text GPT actually reads.")

ENCODINGS = {"o200k_base": "GPT-4o family", "cl100k_base": "GPT-4 / GPT-3.5"}
EXAMPLES = {
    "🍓 Strawberry": "How many r's are in strawberry?",
    "🔢 Numbers": "The year 2024 and the number 1234567890123 and 3.14159265",
    "🌍 Other languages": "Hello world. नमस्ते दुनिया. こんにちは世界. مرحبا بالعالم. Привет мир.",
    "😀 Emoji": "I love pizza 🍕 and robots 🤖👩🏽‍💻",
    "💻 Code": "def fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)",
    "🤪 Weird words": "Supercalifragilisticexpialidocious SolidGoldMagikarp antidisestablishmentarianism",
    "␣ Whitespace": "Hello   world\t\ttabs   and     spaces",
}
COLORS = ["#ffd6d6", "#d6f0ff", "#e0ffd6", "#fff3c4", "#ead6ff", "#ffe0c2"]

if "text" not in st.session_state:
    st.session_state.text = EXAMPLES["🍓 Strawberry"]
cols = st.columns(len(EXAMPLES))
for c, (name, txt) in zip(cols, EXAMPLES.items()):
    if c.button(name, width="stretch"):
        st.session_state.text = txt
text = st.text_area("Type anything", key="text", height=110)
price = st.sidebar.number_input("Price per 1M input tokens ($)", 0.0, 50.0, 2.5, 0.5)


def split(enc, s):
    ids = enc.encode(s)
    return ids, [enc.decode_single_token_bytes(i) for i in ids]


def show(b):
    s = b.decode("utf-8", errors="replace")
    return s.replace(" ", "␣").replace("\n", "↵\n").replace("\t", "⇥") if s.strip() == "" or "\n" in s else s


rows = []
tabs = st.tabs([f"{k} · {v}" for k, v in ENCODINGS.items()])
for tab, name in zip(tabs, ENCODINGS):
    enc = tiktoken.get_encoding(name)
    ids, pieces = split(enc, text)
    rows.append(dict(encoding=name, tokens=len(ids), characters=len(text), chars_per_token=len(text) / max(1, len(ids))))
    with tab:
        chips = "".join(
            f'<span style="background:{COLORS[i % len(COLORS)]};color:#111;padding:2px 3px;margin:1px;border-radius:4px;'
            f'font-family:monospace;white-space:pre-wrap;display:inline-block" title="id {t}">{html.escape(show(p))}</span>'
            for i, (t, p) in enumerate(zip(ids, pieces)))
        st.markdown(chips or "_(empty)_", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Tokens", len(ids))
        m2.metric("Characters", len(text))
        m3.metric("Chars per token", f"{len(text) / max(1, len(ids)):.1f}")
        with st.expander("Token IDs"):
            st.code(str(ids), language=None)

st.subheader("What this means")
df = pd.DataFrame(rows)
c1, c2 = st.columns(2)
c1.plotly_chart(px.bar(df, x="encoding", y="tokens", color="encoding", text="tokens", title="Same text, different vocabulary").update_layout(showlegend=False, height=300), width="stretch")
best = df.tokens.min()
c2.markdown(f"""
- **Cost:** {best} tokens ≈ **${best * price / 1e6:.6f}** at ${price}/1M tokens. The same text costs {int(df.tokens.max())} tokens on the older vocabulary.
- **Why LLMs fumble letter-counting:** "strawberry" arrives as a few chunks, not 10 letters, so the model has to *remember* the spelling of each chunk.
- **Non-English is pricier:** compare the 🌍 example. Rare scripts split into many tokens, so they cost more and use up more of the context window.
- **Numbers split oddly:** long numbers are chopped into 1-3 digit pieces, one reason arithmetic is hard for LLMs.
""")
