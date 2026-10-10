"""CNN X-ray: MobileNetV2 (ImageNet) top-5 predictions + a Grad-CAM heatmap showing WHERE the network looked. No API calls."""
from pathlib import Path

import numpy as np
import streamlit as st
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms

st.set_page_config(page_title="CNN X-ray", page_icon="🩻", layout="wide")
st.title("🩻 CNN X-ray")
st.caption("Upload a photo. A real neural network (MobileNetV2, 3.5M parameters, 1,000 ImageNet classes) guesses what it is, "
           "and Grad-CAM paints the pixels it actually looked at.")

SAMPLES = Path(__file__).parent / "samples"
W = models.MobileNet_V2_Weights.IMAGENET1K_V2
PREP = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


@st.cache_resource(show_spinner="Loading MobileNetV2...")
def load():
    m = models.mobilenet_v2(weights=W).eval()
    return m, W.meta["categories"]


def gradcam(model, x, cls=None):
    """Grad-CAM on the last conv block: weight each feature map by its mean gradient, ReLU, upsample."""
    feats = {}
    h = model.features.register_forward_hook(lambda m, i, o: feats.update(a=o))
    try:
        x = x.clone().requires_grad_(True)
        logits = model(x)
        probs = logits.softmax(1)[0]
        cls = int(probs.argmax()) if cls is None else cls
        grads, = torch.autograd.grad(logits[0, cls], feats["a"])
    finally:
        h.remove()
    w = grads.mean(dim=(2, 3), keepdim=True)
    cam = F.relu((w * feats["a"]).sum(1, keepdim=True))
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)[0, 0].detach().numpy()
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-9)
    return probs.detach().numpy(), cam, cls


def heat(img, cam, alpha):
    r = np.clip(cam * 2, 0, 1)
    g = np.clip(cam * 2 - 0.5, 0, 1) * np.clip(2 - cam * 2, 0, 1)
    b = np.clip(1 - cam * 2, 0, 1)
    color = np.stack([r, g, b], -1)
    base = np.asarray(img, dtype=float) / 255
    return (base * (1 - alpha * cam[..., None]) + color * alpha * cam[..., None]).clip(0, 1)


model, cats = load()
st.sidebar.header("Image")
names = sorted(p.name for p in SAMPLES.glob("*.jpg"))
src = st.sidebar.radio("Source", ["Sample", "Upload", "Webcam"], horizontal=True)
img = None
if src == "Sample" and names:
    img = Image.open(SAMPLES / st.sidebar.selectbox("Sample", names)).convert("RGB")
elif src == "Upload":
    f = st.sidebar.file_uploader("Photo", type=["jpg", "jpeg", "png"])
    img = Image.open(f).convert("RGB") if f else None
elif src == "Webcam":
    f = st.camera_input("Take a photo")
    img = Image.open(f).convert("RGB") if f else None
alpha = st.sidebar.slider("Heatmap strength", 0.2, 1.0, 0.7, 0.05)

if img is None:
    st.info("Pick a sample, upload a photo, or use the webcam.")
    st.stop()

x = PREP(img).unsqueeze(0)
probs, cam, top = gradcam(model, x)
order = np.argsort(probs)[::-1][:5]
crop = transforms.CenterCrop(224)(transforms.Resize(256)(img))

pick = st.radio("Explain which guess?", [f"{cats[i]} ({probs[i]:.0%})" for i in order], horizontal=True)
cls = int(order[[f"{cats[i]} ({probs[i]:.0%})" for i in order].index(pick)])
if cls != top:
    _, cam, _ = gradcam(model, x, cls)

a, b, c = st.columns(3)
a.image(crop, caption="What the network sees (224x224 centre crop)", width="stretch")
b.image(heat(crop, cam, alpha), caption=f"Grad-CAM for '{cats[cls]}': red = decisive pixels", width="stretch")
with c:
    st.subheader("Top 5 guesses")
    for i in order:
        st.write(f"**{cats[i]}**")
        st.progress(float(probs[i]), text=f"{probs[i]:.1%}")
st.caption("Tip: switch the guess to a wrong class (e.g. the runner-up) and watch the heatmap move to different pixels. "
           "It only knows 1,000 ImageNet classes: show it something else and it will still pick one with confidence.")
