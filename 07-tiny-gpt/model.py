"""A character-level GPT in ~70 lines of PyTorch (nanoGPT-style). Trains on CPU in a minute or two."""
import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, d, heads, ctx):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, heads, batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
        self.register_buffer("mask", torch.triu(torch.ones(ctx, ctx, dtype=torch.bool), 1))

    def forward(self, x):
        T = x.size(1)
        h = self.ln1(x)
        x = x + self.attn(h, h, h, attn_mask=self.mask[:T, :T], need_weights=False)[0]  # causal self-attention
        return x + self.mlp(self.ln2(x))


class TinyGPT(nn.Module):
    def __init__(self, vocab, ctx=64, d=128, layers=4, heads=4):
        super().__init__()
        self.ctx = ctx
        self.tok, self.pos = nn.Embedding(vocab, d), nn.Embedding(ctx, d)
        self.blocks = nn.Sequential(*[Block(d, heads, ctx) for _ in range(layers)])
        self.ln, self.head = nn.LayerNorm(d), nn.Linear(d, vocab, bias=False)

    def forward(self, idx, targets=None):
        x = self.tok(idx) + self.pos(torch.arange(idx.size(1)))
        logits = self.head(self.ln(self.blocks(x)))
        loss = None if targets is None else F.cross_entropy(logits.flatten(0, 1), targets.flatten())
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, n, temperature=0.8, top_k=None):
        for _ in range(n):
            logits, _ = self(idx[:, -self.ctx:])
            logits = logits[:, -1] / max(temperature, 1e-4)
            if top_k:
                logits[logits < torch.topk(logits, top_k).values[:, [-1]]] = -float("inf")
            idx = torch.cat([idx, torch.multinomial(F.softmax(logits, -1), 1)], 1)
        return idx


class CharData:
    def __init__(self, text):
        self.chars = sorted(set(text))
        self.stoi = {c: i for i, c in enumerate(self.chars)}
        self.data = torch.tensor([self.stoi[c] for c in text])

    def encode(self, s):
        return [self.stoi[c] for c in s if c in self.stoi] or [0]

    def decode(self, ids):
        return "".join(self.chars[i] for i in ids)

    def batch(self, ctx, bs):
        ix = torch.randint(len(self.data) - ctx - 1, (bs,))
        x = torch.stack([self.data[i:i + ctx] for i in ix])
        y = torch.stack([self.data[i + 1:i + ctx + 1] for i in ix])
        return x, y
