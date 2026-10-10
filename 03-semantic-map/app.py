"""Semantic Map: see how embeddings organise meaning, then ask questions with RAG."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import llm  # noqa: E402

st.set_page_config(page_title="Semantic Map", page_icon="🗺️", layout="wide")
st.title("🗺️ Semantic Map")
st.caption("Every sentence becomes a vector; similar meanings land close together. Search drops a ⭐ on the map.")


@st.cache_data(show_spinner="Embedding corpus...")
def build(docs_json):
    docs = json.loads(docs_json)
    vecs = np.array(llm.embed([d["text"] for d in docs]))
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


def project(vecs, method):
    if method == "PCA":
        return PCA(n_components=2, random_state=0).fit_transform(vecs)
    return TSNE(n_components=2, perplexity=min(15, len(vecs) - 1), random_state=0, init="pca").fit_transform(vecs)


docs = json.loads((Path(__file__).parent / "corpus.json").read_text())
up = st.sidebar.file_uploader("Add your own .txt (one sentence per line)", type="txt")
if up:
    lines = [l.strip() for l in up.getvalue().decode().splitlines() if l.strip()]
    docs += [{"id": len(docs) + i, "topic": "Yours", "text": l} for i, l in enumerate(lines)]
method = st.sidebar.radio("Projection", ["t-SNE", "PCA"])
k = st.sidebar.slider("Top-k results", 1, 8, 3)

vecs = build(json.dumps(docs))
xy = project(vecs, method)
df = pd.DataFrame(docs).assign(x=xy[:, 0], y=xy[:, 1])

q = st.text_input("Ask something", placeholder="e.g. Why does bread rise?")
fig = px.scatter(df, x="x", y="y", color="topic", hover_name="text", hover_data={"x": False, "y": False})
fig.update_traces(marker=dict(size=11))
fig.update_layout(height=560, xaxis_visible=False, yaxis_visible=False)

if q:
    qv = np.array(llm.embed([q])[0])
    qv /= np.linalg.norm(qv)
    sims = vecs @ qv
    top = np.argsort(-sims)[:k]
    # Place the query on the 2D map at the similarity-weighted centroid of its neighbours.
    w = np.maximum(sims[top], 0) + 1e-6
    qxy = (xy[top] * w[:, None]).sum(0) / w.sum()
    fig.add_scatter(x=[qxy[0]], y=[qxy[1]], mode="markers+text", text=["⭐ query"], textposition="top center",
                    marker=dict(size=22, color="gold", line=dict(width=2, color="black")), name="query")
    for i in top:
        fig.add_scatter(x=[qxy[0], xy[i, 0]], y=[qxy[1], xy[i, 1]], mode="lines",
                        line=dict(color="gray", dash="dot"), showlegend=False, hoverinfo="skip")
    st.plotly_chart(fig, use_container_width=True)

    ctx = [docs[i]["text"] for i in top]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Retrieved")
        for i in top:
            st.write(f"**{sims[i]:.2f}** · _{docs[i]['topic']}_ · {docs[i]['text']}")
    with col2:
        st.subheader("RAG answer")
        with st.spinner("Generating..."):
            ans, secs = llm.chat(
                [{"role": "system", "content": "Answer using ONLY the context. If it is not there, say you don't know. Be brief."},
                 {"role": "user", "content": "Context:\n- " + "\n- ".join(ctx) + f"\n\nQuestion: {q}"}],
                temperature=0.2, max_tokens=80)
        st.write(ans)
        st.caption(f"{secs:.1f}s")
else:
    st.plotly_chart(fig, use_container_width=True)
