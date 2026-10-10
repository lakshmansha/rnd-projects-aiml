"""Evolving Rockets: a genetic algorithm breeds rockets that learn to dodge obstacles and hit a target. No API calls."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Evolving Rockets", page_icon="🚀", layout="wide")
st.title("🚀 Evolving Rockets")
st.caption("Each rocket's DNA is a list of thrust directions. Best rockets breed, children mutate, repeat. Nobody programs the route.")

W, T = 100.0, 140
START, TARGET, TR = np.array([50.0, 6.0]), np.array([50.0, 92.0]), 5.0
LEVELS = {
    "Open sky": [],
    "Wall": [(20, 40, 80, 46)],
    "Gap": [(0, 40, 14, 47), (30, 40, 100, 47)],
    "Zig-zag": [(0, 32, 62, 38), (38, 60, 100, 66)],
}


def simulate(dna, obstacles):
    """dna: (N, T, 2) thrusts. Returns paths (N, T, 2), reached(N), crashed(N), steps_to_reach(N)."""
    N = len(dna)
    pos, vel = np.tile(START, (N, 1)), np.zeros((N, 2))
    paths = np.zeros((N, T, 2))
    alive, reached, when = np.ones(N, bool), np.zeros(N, bool), np.full(N, T)
    crashed = np.zeros(N, bool)
    for t in range(T):
        vel = np.clip(vel + dna[:, t], -2.2, 2.2)
        pos = np.where(alive[:, None], pos + vel, pos)
        paths[:, t] = pos
        hit = (pos < 0).any(1) | (pos > W).any(1)
        for x0, y0, x1, y1 in obstacles:
            hit |= (pos[:, 0] > x0) & (pos[:, 0] < x1) & (pos[:, 1] > y0) & (pos[:, 1] < y1)
        arrive = np.linalg.norm(pos - TARGET, axis=1) < TR
        newly = alive & arrive & ~reached
        when[newly], reached[newly] = t, True
        crashed |= alive & hit & ~arrive
        alive &= ~(hit | arrive)
    return paths, reached, crashed, when


def fitness(paths, reached, crashed, when):
    d = np.linalg.norm(paths - TARGET, axis=2).min(1)  # closest approach over the flight
    f = 100 / (1 + d) ** 1.2
    f = np.where(crashed, f * 0.4, f)
    return np.where(reached, 200 + (T - when), f)


def evolve(level, pop, gens, mut, seed):
    rng = np.random.default_rng(seed)
    obs = LEVELS[level]
    ang = rng.uniform(0, 2 * np.pi, (pop, T))
    dna = np.stack([np.cos(ang), np.sin(ang)], -1) * 0.35
    hist = []
    for g in range(gens):
        paths, reached, crashed, when = simulate(dna, obs)
        fit = fitness(paths, reached, crashed, when)
        order = np.argsort(-fit)
        hist.append(dict(paths=paths[order].astype(np.float32), fit=fit[order], reached=int(reached.sum()),
                         crashed=int(crashed.sum())))
        n_el = max(2, pop // 10)
        new = [dna[order[:n_el]]]
        pool = order[:pop // 2]
        pa, pb = rng.choice(pool, pop - n_el), rng.choice(pool, pop - n_el)
        cut = rng.integers(10, T - 10, pop - n_el)[:, None, None]
        child = np.where(np.arange(T)[None, :, None] < cut, dna[pa], dna[pb])
        m = rng.random(child.shape[:2]) < mut
        a = rng.uniform(0, 2 * np.pi, m.shape)
        child[m] = (np.stack([np.cos(a), np.sin(a)], -1) * 0.35)[m]
        dna = np.concatenate(new + [child])
    return hist


with st.sidebar:
    level = st.selectbox("Level", list(LEVELS), index=2)
    pop = st.select_slider("Population", [30, 60, 100, 200], 100)
    gens = st.select_slider("Generations", [20, 40, 80, 150], 80)
    mut = st.select_slider("Mutation rate", [0.005, 0.01, 0.02, 0.05, 0.1], 0.02)
    seed = st.number_input("Random seed", 0, 999, 1)

key = (level, pop, gens, mut, seed)
if st.session_state.get("key") != key:
    with st.spinner("Evolving..."):
        st.session_state.hist, st.session_state.key = evolve(level, pop, gens, mut, int(seed)), key
hist = st.session_state.hist

g = st.slider("⏪ Generation", 1, len(hist), len(hist)) - 1
h = hist[g]
fig = go.Figure()
for x0, y0, x1, y1 in LEVELS[level]:
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, fillcolor="#444", line_width=0)
fig.add_shape(type="circle", x0=TARGET[0] - TR, y0=TARGET[1] - TR, x1=TARGET[0] + TR, y1=TARGET[1] + TR, fillcolor="gold", line_color="orange")
for p in h["paths"][1:]:
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines", line=dict(color="rgba(80,120,200,0.18)", width=1.5), showlegend=False, hoverinfo="skip"))
best = h["paths"][0]
fig.add_trace(go.Scatter(x=best[:, 0], y=best[:, 1], mode="lines", line=dict(color="#e8590c", width=4), name="best rocket"))
fig.add_trace(go.Scatter(x=[START[0]], y=[START[1]], mode="markers+text", text=["🚀"], textfont=dict(size=22), showlegend=False))
fig.update_xaxes(range=[0, W], visible=False)
fig.update_yaxes(range=[0, W], visible=False, scaleanchor="x")
fig.update_layout(height=620, margin=dict(t=10, b=0, l=0, r=0), plot_bgcolor="#f6f8fb", legend=dict(x=0.01, y=0.99))

left, right = st.columns([3, 2])
left.plotly_chart(fig, width="stretch")
with right:
    c1, c2, c3 = st.columns(3)
    c1.metric("Generation", g + 1)
    c2.metric("Reached target", f"{h['reached']}/{pop}")
    c3.metric("Crashed", h["crashed"])
    curve = go.Figure()
    curve.add_scatter(y=[x["fit"][0] for x in hist], name="best")
    curve.add_scatter(y=[x["fit"].mean() for x in hist], name="average")
    curve.add_vline(x=g, line_dash="dot")
    curve.update_layout(height=320, title="Fitness over generations", margin=dict(t=40, b=0), xaxis_title="generation")
    st.plotly_chart(curve, width="stretch")
    first = next((i + 1 for i, x in enumerate(hist) if x["reached"]), None)
    st.info(f"First rocket reached the target in generation **{first}**." if first else "No rocket reached the target. Try more generations or a higher mutation rate.")
