"""Flappy Evolution: a population of tiny neural nets learns to play a Flappy-style game by neuroevolution. No API calls."""
import time

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="Flappy Evolution", page_icon="🐦", layout="wide")
st.title("🐦 Flappy Evolution")
st.caption("Each bird is a tiny neural net (4 inputs, 6 hidden, 1 output). Nobody teaches it to play: the best birds breed, children mutate, repeat.")

W, H, BX, GAP, PIPE_W, SPEED, GRAV, FLAP, MAX_STEPS = 480, 360, 90, 100, 52, 3.4, 0.5, -6.4, 1200
SP = 150  # pixels between pipes


def course(seed, n=400):
    """Gap-centre heights for n pipes (one every SP px); same seed = same course."""
    return np.random.default_rng(seed).uniform(H / 2 - 75, H / 2 + 75, n)


def init_pop(n, rng):
    return [(rng.normal(0, 1, (4, 6)), np.zeros(6), rng.normal(0, 1, (6, 1)), np.zeros(1)) for _ in range(n)]


def think(net, x):
    w1, b1, w2, b2 = net
    return float(np.tanh(np.tanh(x @ w1 + b1) @ w2 + b2)[0])


def run_generation(pop, seed, draw=None):
    """Play every bird on the same course. Returns fitness (steps survived) per bird; calls draw(state) for live frames."""
    gaps = course(seed)
    n = len(pop)
    y, vy, alive, fit = np.full(n, H / 2), np.zeros(n), np.ones(n, bool), np.zeros(n)
    for step in range(MAX_STEPS):
        scroll = step * SPEED
        k = max(0, int(np.ceil((scroll + BX - PIPE_W - 250) / SP)))   # first pipe whose right edge is still ahead of the birds
        px = 250 + k * SP - scroll
        gc = gaps[k]
        for i in np.flatnonzero(alive):
            x = np.array([(gc - y[i]) / H * 2, y[i] / H - 0.5, vy[i] / 8, (px - BX) / 250])
            if think(pop[i], x) > 0:
                vy[i] = FLAP
        vy[alive] += GRAV
        y[alive] += vy[alive]
        hit = (y < 0) | (y > H) | ((px < BX + 12) & (px + PIPE_W > BX - 12) & (np.abs(y - gc) > GAP / 2 - 8))
        alive &= ~hit
        fit[alive] += 1
        if draw and step % 3 == 0:
            draw(step, scroll, gaps, y.copy(), alive.copy())
        if not alive.any():
            break
    return fit


def frame(scroll, gaps, y, alive):
    im = Image.new("RGB", (W, H), (112, 200, 236))
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - 8, W, H), fill=(222, 184, 120))
    for k in range(int(scroll // SP), int(scroll // SP) + 4):
        px = 250 + k * SP - scroll
        if -PIPE_W < px < W and k < len(gaps):
            g = gaps[k]
            d.rectangle((px, 0, px + PIPE_W, g - GAP / 2), fill=(76, 175, 80), outline=(40, 110, 45), width=3)
            d.rectangle((px, g + GAP / 2, px + PIPE_W, H), fill=(76, 175, 80), outline=(40, 110, 45), width=3)
    for yi, a in zip(y, alive):
        if a:
            d.ellipse((BX - 9, yi - 9, BX + 9, yi + 9), fill=(255, 214, 10, 255), outline=(180, 120, 0))
    return im


def next_gen(pop, fit, mut, rng):
    order = np.argsort(-fit)
    elite = [pop[i] for i in order[:max(2, len(pop) // 10)]]
    pool = [pop[i] for i in order[:max(4, len(pop) // 3)]]
    kids = []
    while len(elite) + len(kids) < len(pop):
        a, b = rng.choice(len(pool), 2)
        kid = []
        for pa, pb in zip(pool[a], pool[b]):
            mask = rng.random(pa.shape) < 0.5                          # crossover: mix weights from two parents
            c = np.where(mask, pa, pb)
            c = c + (rng.random(c.shape) < mut) * rng.normal(0, 0.5, c.shape)   # mutation
            kid.append(c)
        kids.append(tuple(kid))
    return elite + kids


with st.sidebar:
    n = st.select_slider("Birds per generation", [20, 40, 60, 100, 150], 60)
    gens = st.select_slider("Generations to run", [5, 10, 20, 40], 20)
    mut = st.select_slider("Mutation rate", [0.05, 0.1, 0.2, 0.4], 0.2)
    seed = st.number_input("Random seed", 0, 999, 1)
    live = st.checkbox("Show the game live", True)

go = st.button("🚀 Evolve", type="primary")

screen, chart = st.columns([3, 2])
slot, info, chart_slot = screen.empty(), screen.empty(), chart.empty()
if go:
    rng = np.random.default_rng(int(seed))
    pop, scores = init_pop(n, rng), []
    for g in range(1, gens + 1):
        def draw(step, scroll, gaps, y, alive):
            if live:
                slot.image(frame(scroll, gaps, y, alive), width="stretch")
                info.markdown(f"**Generation {g}** · alive: {int(alive.sum())}/{n} · distance: {int(scroll)} px · best so far: {int(max(scores)) if scores else 0}")
                time.sleep(0.01)
        fit = run_generation(pop, int(seed), draw)
        scores.append(float(fit.max()))
        chart_slot.line_chart(pd.DataFrame({"best steps survived": scores}), height=320)
        pop = next_gen(pop, fit, mut, rng)
        if fit.max() >= MAX_STEPS:
            info.success(f"Generation {g}: a bird survived all {MAX_STEPS} steps. The population has learned to play.")
            break
    st.session_state.scores = scores
else:
    slot.info("Press **Evolve**. Generation 1 crashes almost at once; watch how fast it learns.")
    if "scores" in st.session_state:
        chart_slot.line_chart(pd.DataFrame({"best steps survived": st.session_state.scores}), height=320)
