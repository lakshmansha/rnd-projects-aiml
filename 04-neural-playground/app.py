"""Neural Net Playground: a neural network written from scratch in numpy, trained live. No API calls."""
import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from sklearn.datasets import make_circles, make_moons

st.set_page_config(page_title="Neural Playground", page_icon="🧠", layout="wide")
st.title("🧠 Neural Net Playground")
st.caption("Backprop in ~30 lines of numpy. Watch the decision boundary bend as it learns.")


def spiral(n=300, noise=0.15, seed=0):
    r = np.random.RandomState(seed)
    t = np.linspace(0.3, 3.2 * np.pi, n // 2)
    a = np.c_[t * np.cos(t), t * np.sin(t)] / 9
    X = np.r_[a, -a] + r.randn(n, 2) * noise * 0.4
    return X, np.r_[np.zeros(n // 2), np.ones(n // 2)]


def xor(n=300, noise=0.15, seed=0):
    r = np.random.RandomState(seed)
    X = r.uniform(-1, 1, (n, 2))
    return X + r.randn(n, 2) * noise * 0.2, ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(float)


DATA = {"Moons": lambda n, s: make_moons(n, noise=s, random_state=0),
        "Circles": lambda n, s: make_circles(n, noise=s * 0.5, factor=0.4, random_state=0),
        "Spiral": lambda n, s: spiral(n, s), "XOR": lambda n, s: xor(n, s)}
ACT = {"tanh": (np.tanh, lambda a: 1 - a ** 2), "relu": (lambda z: np.maximum(0, z), lambda a: (a > 0).astype(float))}


class MLP:
    def __init__(self, sizes, act, seed=0):
        r = np.random.RandomState(seed)
        self.W = [r.randn(i, o) * np.sqrt(2 / i) for i, o in zip(sizes, sizes[1:])]
        self.b = [np.zeros(o) for o in sizes[1:]]
        self.f, self.df = ACT[act]

    def forward(self, X):
        A = [X]
        for k, (W, b) in enumerate(zip(self.W, self.b)):
            z = A[-1] @ W + b
            A.append(1 / (1 + np.exp(-z)) if k == len(self.W) - 1 else self.f(z))
        return A

    def step(self, X, y, lr):
        A = self.forward(X)
        d = (A[-1] - y[:, None]) / len(X)  # sigmoid + BCE gradient
        for k in reversed(range(len(self.W))):
            gW, gb = A[k].T @ d, d.sum(0)
            if k:
                d = (d @ self.W[k].T) * self.df(A[k])
            self.W[k] -= lr * gW
            self.b[k] -= lr * gb
        p = np.clip(A[-1][:, 0], 1e-7, 1 - 1e-7)
        return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))), float(np.mean((p > .5) == y))


with st.sidebar:
    ds = st.selectbox("Dataset", list(DATA), index=2)
    noise = st.slider("Noise", 0.0, 0.5, 0.15)
    hidden = st.text_input("Hidden layers", "8,8")
    act = st.radio("Activation", list(ACT), horizontal=True)
    lr = st.select_slider("Learning rate", [0.01, 0.03, 0.1, 0.3, 1.0], value=0.3)
    epochs = st.slider("Epochs", 100, 5000, 1500, 100)
    go_btn = st.button("▶ Train", type="primary")

X, y = DATA[ds](300, noise)
X = (X - X.mean(0)) / X.std(0)
g = np.linspace(-2.6, 2.6, 70)
gx, gy = np.meshgrid(g, g)
grid = np.c_[gx.ravel(), gy.ravel()]


def draw(net, losses, accs):
    zz = net.forward(grid)[-1][:, 0].reshape(gx.shape)
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], subplot_titles=("Decision boundary", "Loss"))
    fig.add_trace(go.Contour(x=g, y=g, z=zz, showscale=False, contours_coloring="heatmap", opacity=.65,
                             colorscale=[[0, "#4f8bf9"], [.5, "#f4f4f4"], [1, "#ff7a45"]], zmin=0, zmax=1), 1, 1)
    for c, col in ((0, "#1f4fbf"), (1, "#d9480f")):
        fig.add_trace(go.Scatter(x=X[y == c, 0], y=X[y == c, 1], mode="markers", showlegend=False,
                                 marker=dict(color=col, size=6, line=dict(width=1, color="white"))), 1, 1)
    fig.add_trace(go.Scatter(y=losses, mode="lines", showlegend=False, line=dict(color="#555")), 1, 2)
    fig.update_layout(height=480, margin=dict(t=40, b=10))
    return fig


try:
    sizes = [2] + [int(h) for h in hidden.split(",") if h.strip()] + [1]
except ValueError:
    st.error("Hidden layers must look like 8,8"); st.stop()

slot, info = st.empty(), st.empty()
if go_btn:
    net, losses, accs = MLP(sizes, act), [], []
    for e in range(1, epochs + 1):
        l, a = net.step(X, y, lr)
        losses.append(l); accs.append(a)
        if e % max(1, epochs // 40) == 0 or e == epochs:
            slot.plotly_chart(draw(net, losses, accs), use_container_width=True)
            time.sleep(0.12)  # give the browser time to paint each frame
            info.metric("Epoch / accuracy", f"{e} / {a:.1%}", f"loss {l:.3f}")
else:
    net0 = MLP(sizes, act)
    slot.plotly_chart(draw(net0, [], []), use_container_width=True)
    st.info("Pick a dataset and press **Train**. Try the Spiral with `8,8` vs a single layer `2`.")
