"""Clustering Lab: watch K-means think step by step, then see which algorithm survives tricky data. No API calls."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Clustering Lab", page_icon="🧩", layout="wide")
st.title("🧩 Clustering Lab")
st.caption("Unsupervised learning: no labels, the algorithm finds the groups. Which one wins depends on the shape of the data.")


def make_data(name, n=300, seed=0):
    rng = np.random.RandomState(seed)
    if name == "Blobs":
        X = make_blobs(n, centers=3, cluster_std=1.0, random_state=seed)[0]
    elif name == "Moons":
        X = make_moons(n, noise=0.07, random_state=seed)[0]
    elif name == "Circles":
        X = make_circles(n, noise=0.05, factor=0.4, random_state=seed)[0]
    elif name == "Stretched blobs":
        X = make_blobs(n, centers=3, random_state=seed)[0] @ np.array([[0.6, -0.65], [-0.4, 0.85]])
    else:  # Uniform noise
        X = rng.rand(n, 2)
    return StandardScaler().fit_transform(X)


DATASETS = ["Blobs", "Moons", "Circles", "Stretched blobs", "Uniform noise"]
tab1, tab2 = st.tabs(["🐢 K-means step by step", "🥊 Algorithm showdown"])

with tab1:
    c1, c2, c3 = st.columns(3)
    ds = c1.selectbox("Dataset", DATASETS, key="d1")
    k = c2.slider("k (number of clusters)", 2, 8, 3)
    seed = c3.number_input("Random init seed", 0, 99, 0)
    X = make_data(ds)
    rng = np.random.RandomState(int(seed))
    cent = X[rng.choice(len(X), k, replace=False)]
    steps = []  # (centroids, labels)
    for _ in range(15):
        lab = np.argmin(((X[:, None] - cent[None]) ** 2).sum(2), 1)
        steps.append((cent.copy(), lab))
        new = np.array([X[lab == j].mean(0) if (lab == j).any() else cent[j] for j in range(k)])
        if np.allclose(new, cent):
            break
        cent = new
    it = st.slider("Iteration", 0, len(steps) - 1, len(steps) - 1)
    cent, lab = steps[it]
    inertia = sum(((X[lab == j] - cent[j]) ** 2).sum() for j in range(k))
    fig = px.scatter(x=X[:, 0], y=X[:, 1], color=lab.astype(str), color_discrete_sequence=px.colors.qualitative.Set2)
    fig.add_trace(go.Scatter(x=cent[:, 0], y=cent[:, 1], mode="markers", marker=dict(symbol="x", size=18, color="black", line=dict(width=2, color="white")), name="centroids"))
    fig.update_layout(height=520, showlegend=False, margin=dict(t=10))
    fig.update_yaxes(scaleanchor="x")
    left, right = st.columns([3, 1])
    left.plotly_chart(fig, width="stretch")
    right.metric("Iteration", it)
    right.metric("Within-cluster distance", f"{inertia:.1f}")
    right.caption("Each step: ① assign every point to its nearest ✕, ② move each ✕ to the centre of its points. Repeat until nothing moves." +
                  (" **Converged.**" if it == len(steps) - 1 else ""))
    with st.expander("Elbow chart: how do you choose k?"):
        ks = range(1, 10)
        inert = [KMeans(j, n_init=5, random_state=0).fit(X).inertia_ for j in ks]
        st.plotly_chart(px.line(x=list(ks), y=inert, markers=True, labels=dict(x="k", y="inertia")).update_layout(height=280), width="stretch")

with tab2:
    st.write("Same four algorithms on every dataset. K-means assumes round blobs, DBSCAN follows density, GMM fits ellipses, Agglomerative merges neighbours.")
    k2 = st.slider("Clusters (for algorithms that need k)", 2, 5, 2, key="k2")
    eps = st.slider("DBSCAN eps", 0.1, 0.6, 0.3, 0.05)
    algos = {"K-means": lambda X: KMeans(k2, n_init=5, random_state=0).fit_predict(X),
             "Gaussian mixture": lambda X: GaussianMixture(k2, random_state=0).fit_predict(X),
             "Agglomerative": lambda X: AgglomerativeClustering(k2, linkage="single").fit_predict(X),
             "DBSCAN": lambda X: DBSCAN(eps=eps, min_samples=5).fit_predict(X)}
    fig = make_subplots(rows=len(DATASETS), cols=len(algos), subplot_titles=[a if i == 0 else "" for i in range(len(DATASETS)) for a in algos],
                        horizontal_spacing=0.02, vertical_spacing=0.03)
    pal = px.colors.qualitative.Set2
    for r, name in enumerate(DATASETS, 1):
        X = make_data(name)
        for c, (an, fn) in enumerate(algos.items(), 1):
            lab = fn(X)
            colors = ["#999" if l == -1 else pal[l % len(pal)] for l in lab]
            fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(color=colors, size=4), showlegend=False), r, c)
            fig.update_xaxes(visible=False, row=r, col=c)
            fig.update_yaxes(visible=False, row=r, col=c)
        fig.add_annotation(x=-0.012, y=1 - (r - 0.5) / len(DATASETS), xref="paper", yref="paper", text=name, textangle=-90, showarrow=False)
    fig.update_layout(height=900, margin=dict(l=30, t=30, b=0, r=0))
    st.plotly_chart(fig, width="stretch")
    st.info("Notice: K-means cuts Moons and Circles in half (wrong shape assumption), while DBSCAN nails them but marks sparse points grey as noise. "
            "No algorithm is best everywhere.")
