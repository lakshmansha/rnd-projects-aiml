"""Explainable Text AI: a classic TF-IDF + logistic regression classifier that shows WHICH WORDS drove its decision. No API calls."""
import html
import re

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="Explainable Text AI", page_icon="🔍", layout="wide")
st.title("🔍 Explainable Text AI")
st.caption("Trained on real newsgroup posts. Unlike a black box, every prediction can be traced to individual words.")

CATS = {"sci.space": "Space", "rec.sport.hockey": "Hockey", "comp.graphics": "Graphics",
        "talk.politics.guns": "Politics", "rec.autos": "Cars", "sci.med": "Medicine"}
EXAMPLES = {
    "🚀 Space": "NASA announced the shuttle orbit launch will carry a new telescope to study the moon and distant planets.",
    "🏒 Hockey": "The goalie made 40 saves and the Bruins scored in overtime to win the playoff game.",
    "🚗 Cars": "My engine is leaking oil and the brakes squeal. Should I buy a new Toyota or fix the transmission?",
    "💊 Medicine": "The doctor prescribed antibiotics for the infection and said the patient's symptoms should improve.",
    "🎨 Graphics": "Which software can render 3D images and convert a bitmap file to a polygon mesh?",
    "😈 Tricky": "The new rocket engine has more horsepower than any car and could hit a puck faster than a hockey player.",
}


@st.cache_resource(show_spinner="Training on ~3,400 newsgroup posts...")
def train():
    kw = dict(categories=list(CATS), remove=("headers", "footers", "quotes"))
    tr, te = fetch_20newsgroups(subset="train", **kw), fetch_20newsgroups(subset="test", **kw)
    vec = TfidfVectorizer(stop_words="english", sublinear_tf=True, min_df=3, max_features=30000)
    Xtr = vec.fit_transform(tr.data)
    clf = LogisticRegression(C=10, max_iter=1000).fit(Xtr, tr.target)
    pred = clf.predict(vec.transform(te.data))
    names = [CATS[n] for n in tr.target_names]
    return vec, clf, names, float((pred == te.target).mean()), confusion_matrix(te.target, pred)


vec, clf, names, acc, cm = train()
vocab = vec.vocabulary_
st.sidebar.metric("Accuracy on unseen posts", f"{acc:.1%}")
st.sidebar.write("Categories: " + ", ".join(names))

if "txt" not in st.session_state:
    st.session_state.txt = EXAMPLES["🚀 Space"]
cols = st.columns(len(EXAMPLES))
for c, (label, t) in zip(cols, EXAMPLES.items()):
    if c.button(label, width="stretch"):
        st.session_state.txt = t
text = st.text_area("Write something (English)", key="txt", height=100)

tab1, tab2, tab3 = st.tabs(["🧠 Explain a prediction", "📖 What each topic's words are", "❌ Where it gets confused"])

with tab1:
    x = vec.transform([text])
    if x.nnz == 0:
        st.warning("No known words found. Try something about space, cars, hockey, graphics, medicine or politics.")
    else:
        p = clf.predict_proba(x)[0]
        k = int(p.argmax())
        left, right = st.columns([2, 3])
        left.metric("Prediction", names[k], f"{p[k]:.0%} confident")
        left.plotly_chart(px.bar(x=p, y=names, orientation="h", labels=dict(x="probability", y="")).update_layout(height=300, margin=dict(t=5)), width="stretch")
        # Per-word contribution = coefficient * tf-idf weight, toward the predicted class vs. the runner-up.
        order = np.argsort(-p)
        diff = clf.coef_[order[0]] - clf.coef_[order[1]]
        contrib = {}
        for w in set(re.findall(r"[a-z']+", text.lower())):
            if w in vocab:
                contrib[w] = diff[vocab[w]] * x[0, vocab[w]]
        mx = max((abs(v) for v in contrib.values()), default=1) or 1
        def chip(tok):
            v = contrib.get(tok.lower())
            if v is None:
                return html.escape(tok)
            a = min(1, abs(v) / mx)
            col = f"rgba(47,158,68,{0.15 + 0.7 * a})" if v > 0 else f"rgba(224,49,49,{0.15 + 0.7 * a})"
            return f'<span style="background:{col};color:#111;padding:1px 3px;border-radius:4px" title="{v:+.3f}">{html.escape(tok)}</span>'
        marked = " ".join(chip(t) for t in text.split())
        right.markdown(f"**Why {names[order[0]]}?** 🟩 pushes toward **{names[order[0]]}**, 🟥 pushes toward **{names[order[1]]}** (runner-up).", help="Contribution = (weight difference of the two classes) × TF-IDF value")
        right.markdown(f'<div style="line-height:2.1;font-size:1.1rem">{marked}</div>', unsafe_allow_html=True)
        top = sorted(contrib.items(), key=lambda kv: -abs(kv[1]))[:8]
        right.dataframe(pd.DataFrame(top, columns=["word", "push"]).assign(push=lambda d: d.push.round(3)), hide_index=True)

with tab2:
    pick = st.selectbox("Topic", names)
    i = names.index(pick)
    fnames = np.array(vec.get_feature_names_out())
    idx = np.argsort(-clf.coef_[i])[:20]
    st.plotly_chart(px.bar(x=clf.coef_[i][idx][::-1], y=fnames[idx][::-1], orientation="h", labels=dict(x="weight", y="")).update_layout(height=560), width="stretch")
    st.caption("These are the words the model learned on its own are most associated with this topic.")

with tab3:
    st.plotly_chart(px.imshow(cm, x=names, y=names, text_auto=True, color_continuous_scale="Blues", labels=dict(x="predicted", y="actual")).update_layout(height=520), width="stretch")
    st.caption("Bright off-diagonal cells are mistakes, usually between related topics such as Space and Medicine (both 'sci').")
