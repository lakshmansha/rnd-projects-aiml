"""Attention X-ray: see which earlier characters each attention head of the Tiny GPT (project 07) looks at. No API calls."""
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import torch
from plotly.subplots import make_subplots

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "07-tiny-gpt"))
from model import TinyGPT  # noqa: E402

st.set_page_config(page_title="Attention X-ray", page_icon="🔬", layout="wide")
st.title("🔬 Attention X-ray")
st.caption("A real character-level transformer (the Tiny GPT from project 7, trained 2,000 steps on Shakespeare). "
           "Each cell shows how much one character (row) looks back at an earlier character (column) when the model reads your text.")

WEIGHTS = HERE / "weights.pt"
if not WEIGHTS.exists():
    st.error("weights.pt is missing. Run `python 18-attention-xray/train.py` first (about 6 minutes on a CPU).")
    st.stop()


@st.cache_resource(show_spinner="Loading the trained model...")
def load():
    ck = torch.load(WEIGHTS, map_location="cpu", weights_only=False)
    m = TinyGPT(len(ck["chars"]), **ck["cfg"])
    m.load_state_dict(ck["state"])
    return m.eval(), ck["chars"], ck


model, chars, ck = load()
stoi = {c: i for i, c in enumerate(chars)}


@torch.no_grad()
def x_ray(ids):
    """Forward pass that keeps every block's attention weights: list of (heads, T, T) arrays, plus next-char probabilities."""
    idx = torch.tensor([ids])
    x = model.tok(idx) + model.pos(torch.arange(idx.size(1)))
    maps = []
    for b in model.blocks:
        T = x.size(1)
        h = b.ln1(x)
        out, w = b.attn(h, h, h, attn_mask=b.mask[:T, :T], need_weights=True, average_attn_weights=False)
        maps.append(w[0].numpy())
        x = x + out
        x = x + b.mlp(b.ln2(x))
    probs = model.head(model.ln(x))[0].softmax(-1).numpy()
    return maps, probs


def show(c):
    return {"\n": "↵", " ": "·"}.get(c, c)


default = "ROMEO:\nO, she doth teach the torches to burn bright"
text = st.text_area("Text to read (up to 64 characters; characters the model never saw are skipped)", default, height=80)
text = "".join(c for c in text if c in stoi)[:ck["cfg"]["ctx"]]
if len(text) < 4:
    st.info("Type at least four characters.")
    st.stop()
ids = [stoi[c] for c in text]
maps, probs = x_ray(ids)
labels = [show(c) for c in text]
T = len(text)

c1, c2 = st.columns([1, 3])
layer = c1.radio("Layer", list(range(1, len(maps) + 1)), horizontal=True) - 1
view = c1.radio("Show", ["All 4 heads", "One head, large"])
head = c1.radio("Head", list(range(1, maps[0].shape[0] + 1)), horizontal=True) - 1 if view == "One head, large" else None

tick = dict(tickmode="array", tickvals=list(range(T)), ticktext=labels, tickfont=dict(size=11))
if head is None:
    fig = make_subplots(rows=2, cols=2, subplot_titles=[f"Layer {layer + 1}, head {h + 1}" for h in range(4)], horizontal_spacing=0.06, vertical_spacing=0.12)
    for h in range(4):
        fig.add_trace(go.Heatmap(z=maps[layer][h], colorscale="Viridis", showscale=False, zmin=0, zmax=1), row=h // 2 + 1, col=h % 2 + 1)
        fig.update_xaxes(**tick, row=h // 2 + 1, col=h % 2 + 1)
        fig.update_yaxes(**tick, autorange="reversed", row=h // 2 + 1, col=h % 2 + 1)
    fig.update_layout(height=720, margin=dict(t=40, b=0))
else:
    fig = go.Figure(go.Heatmap(z=maps[layer][head], colorscale="Viridis", zmin=0, zmax=1, colorbar=dict(title="attention")))
    fig.update_xaxes(**tick, title="looks at (earlier character)")
    fig.update_yaxes(**tick, autorange="reversed", title="reading (this character)")
    fig.update_layout(height=720, margin=dict(t=10, b=0), title=f"Layer {layer + 1}, head {head + 1}")
c2.plotly_chart(fig, width="stretch")
c2.caption("Measured on 200 random 64-character Shakespeare windows (average attention): layer 1 head 2 puts 99% on the previous character, "
           "head 1 puts 97% on the character two back, head 4 puts 78% on the previous one. By layer 4 no head puts more than about 21% on itself, the previous character or the one before that.")

st.subheader("What does one character look at, and what does the model predict next?")
pos = st.slider("Character position", 0, T - 1, min(T - 1, 20), format="%d")
left, right = st.columns(2)
row = maps[layer].mean(0)[pos] if head is None else maps[layer][head][pos]
bar = go.Figure(go.Bar(x=list(range(T)), y=row, marker_color=["#e8590c" if i == pos else "#4c6ef5" for i in range(T)]))
bar.update_layout(height=300, margin=dict(t=30, b=0), title=f"Layer {layer + 1}: attention from '{show(text[pos])}' (orange) to every earlier character",
                  xaxis=dict(tickmode="array", tickvals=list(range(T)), ticktext=labels), yaxis_title="attention")
left.plotly_chart(bar, width="stretch")
top = np.argsort(-probs[pos])[:5]
right.write(f"After **'{text[:pos + 1][-12:].replace(chr(10), '↵')}'** the model's top guesses for the next character:")
for i in top:
    right.progress(float(probs[pos][i]), text=f"'{show(chars[i])}'  {probs[pos][i]:.1%}")
if pos + 1 < T:
    right.caption(f"Actual next character in your text: '{show(text[pos + 1])}'")
st.caption("Attention is not a full explanation of what the model does: later layers mix information in ways these maps cannot show. "
           "Treat them as clues, not proofs.")
