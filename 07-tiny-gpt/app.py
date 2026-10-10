"""Tiny GPT Trainer: train a transformer language model from scratch, live, and watch it learn to write."""
import time
from pathlib import Path

import pandas as pd
import streamlit as st
import torch

from model import CharData, TinyGPT

st.set_page_config(page_title="Tiny GPT Trainer", page_icon="🤖", layout="wide")
st.title("🤖 Tiny GPT Trainer")
st.caption("A real transformer (the same architecture as GPT), ~0.8M parameters, trained from scratch on your CPU. No API calls.")

ss = st.session_state
SHAKE = Path(__file__).parent / "data" / "shakespeare.txt"

with st.sidebar:
    st.header("Data")
    src = st.radio("Training text", ["Shakespeare", "Upload .txt"])
    text = SHAKE.read_text(encoding="utf-8") if src == "Shakespeare" else None
    if src == "Upload .txt":
        up = st.file_uploader("Plain text, >50 KB works best", type="txt")
        text = up.getvalue().decode("utf-8", "ignore") if up else None
    st.header("Model")
    layers = st.slider("Transformer layers", 1, 6, 4)
    d = st.select_slider("Embedding size", [32, 64, 128, 192], 128)
    ctx = st.select_slider("Context length", [32, 64, 128], 64)
    st.header("Training")
    steps = st.slider("Steps", 100, 1500, 600, 100)
    lr = st.select_slider("Learning rate", [3e-4, 1e-3, 3e-3, 6e-3], 3e-3)
    every = st.select_slider("Show a sample every N steps", [25, 50, 100, 200], 100)
    go = st.button("🚀 Train from scratch", type="primary", disabled=text is None)

if text is None:
    st.info("Upload a text file to train on.")
    st.stop()
if len(text) > 1_200_000:
    text = text[:1_200_000]

if go:
    torch.manual_seed(0)
    data = CharData(text)
    model = TinyGPT(len(data.chars), ctx=ctx, d=d, layers=layers, heads=4)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    st.write(f"**{sum(p.numel() for p in model.parameters()):,} parameters** · vocabulary of {len(data.chars)} characters · {len(text):,} characters of training text")
    bar, chart_slot = st.progress(0.0), st.empty()
    st.subheader("What the model writes as it learns")
    samples = st.container()
    losses, t0 = [], time.time()
    prompt = torch.tensor([data.encode("\n")])
    for s in range(1, steps + 1):
        model.train()
        x, y = data.batch(ctx, 32)
        _, loss = model(x, y)
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(loss.item())
        if s % 10 == 0:
            bar.progress(s / steps, text=f"step {s}/{steps} · loss {loss.item():.2f} · {s / (time.time() - t0):.1f} steps/s")
            chart_slot.line_chart(pd.Series(losses, name="loss"), height=220)
        if s == 1 or s % every == 0:
            model.eval()
            sample = data.decode(model.generate(prompt, 160, 0.8)[0].tolist())
            with samples:
                st.markdown(f"**Step {s}** (loss {loss.item():.2f})")
                st.code(sample, language=None)
    ss.model, ss.data = model.eval(), data
    st.success(f"Done in {time.time() - t0:.0f}s. Scroll down to generate with your model.")

if "model" in ss:
    st.divider()
    st.subheader("✍️ Generate with your trained model")
    c1, c2, c3 = st.columns([3, 1, 1])
    start = c1.text_input("Start of the text", "ROMEO:" if src == "Shakespeare" else "The ")
    temp = c2.slider("Temperature", 0.2, 1.5, 0.8, 0.1)
    n = c3.slider("Characters", 100, 800, 400, 50)
    if st.button("Generate"):
        ids = torch.tensor([ss.data.encode(start)])
        st.code(ss.data.decode(ss.model.generate(ids, n, temp, top_k=20)[0].tolist()), language=None)
    st.caption("Low temperature = safe and repetitive. High temperature = creative and chaotic.")
else:
    st.info("Press **Train from scratch** in the sidebar. Around 600 steps takes ~2 minutes on CPU, and you can watch gibberish turn into play-like text.")
