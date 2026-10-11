"""Train the Tiny GPT from project 07 for longer (2000 steps) and save weights.pt (about 3 MB) for the attention X-ray.  Usage: python 18-attention-xray/train.py"""
import sys
import time
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "07-tiny-gpt"))
from model import CharData, TinyGPT  # noqa: E402

STEPS, CTX, D, LAYERS, HEADS, LR = 2000, 64, 128, 4, 4, 3e-3
text = (HERE.parent / "07-tiny-gpt" / "data" / "shakespeare.txt").read_text(encoding="utf-8")[:1_200_000]
torch.manual_seed(0)
data = CharData(text)
model = TinyGPT(len(data.chars), ctx=CTX, d=D, layers=LAYERS, heads=HEADS)
opt = torch.optim.AdamW(model.parameters(), lr=LR)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, STEPS, eta_min=3e-4)
t0 = time.time()
for s in range(1, STEPS + 1):
    x, y = data.batch(CTX, 32)
    _, loss = model(x, y)
    opt.zero_grad(); loss.backward(); opt.step(); sched.step()
    if s % 100 == 0:
        print(f"step {s}/{STEPS} loss {loss.item():.3f} ({s / (time.time() - t0):.1f} steps/s)", flush=True)
torch.save(dict(state=model.state_dict(), chars=data.chars, cfg=dict(ctx=CTX, d=D, layers=LAYERS, heads=HEADS), final_loss=loss.item(), steps=STEPS), HERE / "weights.pt")
print("saved", HERE / "weights.pt")
