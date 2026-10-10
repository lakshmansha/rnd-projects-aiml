"""RL Gridworld: Q-learning vs SARSA learning side by side. Scrub through training to watch the policy appear. No API calls."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="RL Gridworld", page_icon="🎮", layout="wide")
st.title("🎮 RL Gridworld: Q-learning vs SARSA")
st.caption("S = start, G = goal, ^ = cliff (-100, back to start), # = wall, every step costs -1. Nobody tells the agents the rules; they learn by trying.")

LAYOUTS = {
    "Cliff walking": ["............", "............", "............", "S^^^^^^^^^^G"],
    "Lava maze": ["S...#.....", ".##.#.###.", ".#..#...#.", ".#.^^.#.#.", ".#.##.#...", "...#..#.#G", ".#...^^.#."],
    "Two doors": ["S.........", "..........", "^^^^#^^^^^", "^^^^#^^^^^", "....G.....", ".........."],
}
ARROWS, MOVES = "↑→↓←", [(-1, 0), (0, 1), (1, 0), (0, -1)]
GOAL_R, STEP_R, CLIFF_R = 50.0, -1.0, -100.0


class Grid:
    def __init__(self, rows):
        self.rows, self.H, self.W = rows, len(rows), len(rows[0])
        find = lambda ch: [(r, c) for r in range(self.H) for c in range(self.W) if rows[r][c] == ch]
        self.start, self.goal = find("S")[0], find("G")[0]
        self.cliff, self.wall = set(find("^")), set(find("#"))

    def step(self, s, a):
        r, c = s[0] + MOVES[a][0], s[1] + MOVES[a][1]
        if not (0 <= r < self.H and 0 <= c < self.W) or (r, c) in self.wall:
            r, c = s
        if (r, c) in self.cliff:
            return self.start, CLIFF_R, False
        if (r, c) == self.goal:
            return (r, c), GOAL_R, True
        return (r, c), STEP_R, False


def train(env, algo, episodes, alpha, gamma, eps, seed=0):
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.H, env.W, 4))
    pick = lambda s: rng.integers(4) if rng.random() < eps else int(np.argmax(Q[s]))
    marks = set(np.unique(np.geomspace(1, episodes, 40).astype(int)))
    snaps, rewards = {0: Q.copy()}, []
    for ep in range(1, episodes + 1):
        s, a, total = env.start, pick(env.start), 0.0
        for _ in range(300):
            s2, r, done = env.step(s, a)
            a2 = pick(s2)
            target = r if done else r + gamma * (Q[s2][a2] if algo == "SARSA" else Q[s2].max())
            Q[s][a] += alpha * (target - Q[s][a])
            s, a, total = s2, a2, total + r
            if done:
                break
        rewards.append(total)
        if ep in marks:
            snaps[ep] = Q.copy()
    return snaps, rewards


def greedy_path(env, Q):
    s, path = env.start, [env.start]
    for _ in range(60):
        s, _, done = env.step(s, int(np.argmax(Q[s])))
        path.append(s)
        if done or len(path) > 2 and s == path[-2]:
            break
    return path


def draw(env, Q, title, show_path):
    V = Q.max(2).astype(float)
    for (r, c) in env.wall | env.cliff:
        V[r, c] = np.nan
    fig = go.Figure(go.Heatmap(z=V, colorscale="RdYlGn", showscale=False, xgap=2, ygap=2, zmid=-20))
    for r in range(env.H):
        for c in range(env.W):
            if (r, c) in env.wall:
                txt, col = "▇", "#333"
            elif (r, c) in env.cliff:
                txt, col = "☠", "#b00"
            elif (r, c) == env.goal:
                txt, col = "G", "#000"
            elif (r, c) == env.start and not Q.any():
                txt, col = "S", "#000"
            elif Q[r, c].any():
                txt, col = ARROWS[int(np.argmax(Q[r, c]))], "#111"
            else:
                txt, col = ("S" if (r, c) == env.start else ""), "#000"
            fig.add_annotation(x=c, y=r, text=txt, showarrow=False, font=dict(size=22, color=col))
    if show_path and Q.any():
        p = greedy_path(env, Q)
        fig.add_trace(go.Scatter(x=[c for _, c in p], y=[r for r, _ in p], mode="lines+markers",
                                 line=dict(color="royalblue", width=4), marker=dict(size=7), showlegend=False))
    fig.update_yaxes(autorange="reversed", visible=False, scaleanchor="x")
    fig.update_xaxes(visible=False)
    fig.update_layout(title=title, height=380, margin=dict(t=40, b=0, l=0, r=0))
    return fig


with st.sidebar:
    layout = st.selectbox("World", list(LAYOUTS))
    episodes = st.select_slider("Training episodes", [100, 300, 1000, 3000], 1000)
    alpha = st.select_slider("Learning rate α", [0.05, 0.1, 0.3, 0.5], 0.3)
    gamma = st.select_slider("Discount γ", [0.5, 0.9, 0.95, 0.99], 0.95)
    eps = st.select_slider("Exploration ε", [0.0, 0.05, 0.1, 0.2, 0.3], 0.1)
    show_path = st.checkbox("Show greedy path", True)

env = Grid(LAYOUTS[layout])
key = (layout, episodes, alpha, gamma, eps)
if st.session_state.get("key") != key:
    with st.spinner("Training both agents..."):
        st.session_state.runs = {a: train(env, a, episodes, alpha, gamma, eps) for a in ("Q-learning", "SARSA")}
    st.session_state.key = key
runs = st.session_state.runs

marks = sorted(runs["Q-learning"][0])
ep = st.select_slider("⏪ Scrub through training: episode", marks, value=marks[-1])
cols = st.columns(2)
for col, algo in zip(cols, runs):
    snaps, rewards = runs[algo]
    col.plotly_chart(draw(env, snaps[ep], f"{algo} after {ep} episodes", show_path), width="stretch")
    k = max(1, episodes // 50)
    smooth = np.convolve(rewards, np.ones(k) / k, mode="valid")
    col.caption(f"Avg reward over last {k} training episodes: **{smooth[-1]:.1f}**")

fig = go.Figure()
for algo in runs:
    r = runs[algo][1]
    k = max(5, episodes // 40)
    fig.add_scatter(y=np.convolve(r, np.ones(k) / k, mode="valid"), name=algo)
fig.update_layout(height=300, title="Reward while learning (moving average)", yaxis_title="reward / episode", xaxis_title="episode")
st.plotly_chart(fig, width="stretch")
st.info("Try **Cliff walking** with ε = 0.1: Q-learning learns the risky shortest path along the cliff edge, "
        "but while exploring it keeps falling in. SARSA accounts for its own exploration and takes the safe route.")
