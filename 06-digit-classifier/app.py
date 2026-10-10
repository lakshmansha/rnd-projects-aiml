"""Draw-a-Digit: train four classic ML models on the sklearn digits set, then test them on your own drawing.
No API calls. The drawing canvas is a tiny inline Streamlit v2 component (no extra package)."""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.ndimage import shift, zoom
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

st.set_page_config(page_title="Draw a Digit", page_icon="✏️", layout="wide")
st.title("✏️ Draw a Digit")
st.caption("Four classic ML models, trained live on 1,797 tiny 8×8 images. Draw a digit and watch them vote.")

SIZE = 56  # canvas is downsampled to 56x56 in the browser, then to 8x8 here

CANVAS_JS = """
export default function ({ parentElement, setStateValue }) {
  const cv = parentElement.querySelector('#cv'), ctx = cv.getContext('2d');
  const reset = () => { ctx.fillStyle = '#000'; ctx.fillRect(0, 0, cv.width, cv.height); };
  reset();
  ctx.lineWidth = 20; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#fff';
  let down = false;
  const pos = e => { const r = cv.getBoundingClientRect();
    return [(e.clientX - r.left) * cv.width / r.width, (e.clientY - r.top) * cv.height / r.height]; };
  const send = () => {
    const s = document.createElement('canvas'); s.width = s.height = %d;
    const c = s.getContext('2d'); c.imageSmoothingEnabled = true; c.drawImage(cv, 0, 0, %d, %d);
    const d = c.getImageData(0, 0, %d, %d).data, out = [];
    for (let i = 0; i < d.length; i += 4) out.push(d[i]);
    setStateValue('img', out);
  };
  cv.onpointerdown = e => { down = true; cv.setPointerCapture(e.pointerId); ctx.beginPath(); const [x, y] = pos(e);
    ctx.moveTo(x, y); ctx.lineTo(x + 0.1, y + 0.1); ctx.stroke(); };
  cv.onpointermove = e => { if (!down) return; const [x, y] = pos(e); ctx.lineTo(x, y); ctx.stroke(); };
  cv.onpointerup = () => { down = false; send(); };
  parentElement.querySelector('#clr').onclick = () => { reset(); setStateValue('img', null); };
}
""" % (SIZE, SIZE, SIZE, SIZE, SIZE)

canvas = st.components.v2.component(
    "digit_canvas",
    html='<canvas id="cv" width="280" height="280"></canvas><br><button id="clr">🧹 Clear</button>',
    css="canvas{border:3px solid #888;border-radius:10px;touch-action:none;cursor:crosshair;width:280px;height:280px}"
        "button{margin-top:8px;padding:6px 14px;border-radius:8px;cursor:pointer}",
    js=CANVAS_JS)


def augment(X, y):
    """Shift each 8x8 image by 1px in 4 directions: 5x data, much more robust to hand-drawn offsets."""
    Xs, ys = [X], [y]
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        Xs.append(np.array([shift(im.reshape(8, 8), (dy, dx), cval=0).ravel() for im in X]))
        ys.append(y)
    return np.vstack(Xs), np.concatenate(ys)


@st.cache_resource(show_spinner="Training 4 models...")
def train():
    d = load_digits()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.25, random_state=0, stratify=d.target)
    Xa, ya = augment(Xtr, ytr)
    models = {
        "SVM (RBF)": SVC(gamma=0.001, C=10, probability=True, random_state=0),
        "Neural net (MLP)": MLPClassifier((64, 32), max_iter=400, random_state=0),
        "Random forest": RandomForestClassifier(200, random_state=0, n_jobs=-1),
        "k-NN (k=5)": KNeighborsClassifier(5),
    }
    acc = {}
    for n, m in models.items():
        m.fit(Xa, ya)
        acc[n] = m.score(Xte, yte)
    return models, acc


def to_8x8(img):
    """Crop to the ink, fill the 8x8 box like the dataset does (bbox-centred; a centre-of-mass shift hurt top-heavy digits like 7), scale to the dataset's 0-16 range."""
    a = np.array(img, dtype=float).reshape(SIZE, SIZE) / 255
    ys, xs = np.where(a > 0.15)
    if len(ys) == 0:
        return None
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    f = 8 / max(a.shape)
    a = zoom(a, f, order=1)
    out = np.zeros((8, 8))
    h, w = a.shape
    out[(8 - h) // 2:(8 - h) // 2 + h, (8 - w) // 2:(8 - w) // 2 + w] = a[:8, :8]
    return np.clip(out / out.max() * 16, 0, 16)


models, acc = train()
left, right = st.columns([1, 2])
with left:
    st.subheader("Draw here")
    res = canvas(key="digit", on_img_change=lambda: None)
    st.caption("Tip: draw big, one digit, like a dot-matrix display.")
    st.subheader("Test accuracy (unseen data)")
    st.dataframe(pd.Series(acc, name="accuracy").sort_values(ascending=False).to_frame().style.format("{:.1%}"))

with right:
    img = res.img if res else None
    x = to_8x8(img) if img else None
    if x is None:
        st.info("👈 Draw a digit 0-9 and lift the mouse.")
    else:
        probs = {n: m.predict_proba(x.reshape(1, -1))[0] for n, m in models.items()}
        votes = {n: int(p.argmax()) for n, p in probs.items()}
        final = pd.Series(votes).value_counts().idxmax()
        c1, c2 = st.columns([1, 2])
        c1.subheader("What the models see")
        c1.image(np.kron(x / 16, np.ones((20, 20))), clamp=True, caption="8×8 input")
        c1.metric("Majority vote", final)
        c2.subheader("Each model's opinion")
        df = pd.DataFrame(probs, index=range(10)).reset_index().melt("index", var_name="model", value_name="p")
        fig = px.bar(df, x="index", y="p", color="model", barmode="group", labels={"index": "digit", "p": "probability"})
        fig.update_layout(xaxis=dict(dtick=1), height=340, margin=dict(t=10))
        c2.plotly_chart(fig, width="stretch")
        st.write("  ".join(f"**{n}** → {v}" for n, v in votes.items()))
