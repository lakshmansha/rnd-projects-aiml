# 07 Tiny GPT Trainer - Full video (~10 min)

## Titles (pick one)
1. I Trained a GPT From Scratch on My CPU (Watch It Learn)
2. Build a Transformer in 70 Lines of PyTorch
3. From Gibberish to Shakespeare: A Tiny GPT Live

**Thumbnail text (<=4 words):** GIBBERISH TO SHAKESPEARE

**Tags:** GPT, transformer, pytorch, nanoGPT, language model, deep learning, train from scratch, shakespeare, character level, attention, streamlit, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The model is 818,176 parameters, trains on CPU, no API calls. Code is in the rnd-projects-aiml repo, project 07. What text would you train it on? Tell me below.

**Description:**
A real transformer language model (818,176 parameters at the default settings) trains from scratch on Shakespeare, live on a CPU, and you watch it learn to write. Built with Claude Code; narration is AI-generated.
Chapters:
00:00 Cold open
00:35 Why this matters
01:40 The model, in code
05:30 Live training demo
07:30 What surprised me
08:30 Honest limits
09:20 What to build next

## Chapters and shot list
| Time | Chapter | Shot |
|---|---|---|
| 0:00 | Cold open | Screen: sped-up training, samples stacking under "What the model writes as it learns" |
| 0:35 | Why it matters | Avatar full frame; simple slide "predict the next character" |
| 1:40 | Model walkthrough | Code: model.py `Block`, `TinyGPT.forward`, `generate`, `CharData.batch`; app.py training loop |
| 5:30 | Live demo | Screen: sidebar sliders, "🚀 Train from scratch", progress text, loss chart, samples; then Generate with Temperature sliders |
| 7:30 | Surprises | Screen: Step 1 vs later samples side by side |
| 8:30 | Limits | Avatar, screen of weak output |
| 9:20 | Next + CTA | Avatar, end card |

Verified headlessly with the repo code (default settings: context 64, embedding 128, 4 layers, 4 heads, batch 32, lr 3e-3): 818,176 parameters, 65-character vocabulary, 1,115,394 characters in data/shakespeare.txt, loss 4.31 at step 1 and 2.47 after 60 steps, about 4 steps/s on the build machine (an earlier run measured around 6 steps/s). Always read the steps/s and loss shown on screen during recording rather than my numbers. The app itself says 600 steps take about 2 minutes on CPU; speed up the footage and say so.

## Voice-over (~1,400 words)

### 0:00 Cold open
This is a GPT that knows nothing. Not a word of English. Not even that letters exist in a particular order. [SCREEN: press Train from scratch.] Step one: pure gibberish, random characters. Now watch what happens as the loss number drops. Letters start clumping into words. Words start taking the shape of lines. Character names with colons appear, then speeches. It never read a grammar book. It only ever practised one thing: guessing the next character. I'll show you the roughly seventy lines of PyTorch behind it, and then we'll train one live.

### 0:35 Why it matters
Before anything else: I built this with Claude Code, and the narration is AI-generated. The code and the training you'll see are real, and run on my own CPU.

Why build a tiny GPT when you can call a big one? Because the big ones can feel like magic, and a magic trick stops being scary once you've watched it assembled. The model in this app has the same ingredients as the systems behind chatbots: token embeddings, positional embeddings, stacked transformer blocks with self-attention, and a final layer that outputs a probability for every possible next token. The difference is scale. At the default settings this one has eight hundred and eighteen thousand, one hundred and seventy-six parameters. That is under a million.

It is also character-level. The vocabulary is just the sixty-five different characters that appear in the training text. No words, no tokenizer. That makes it simple, and it makes the learning stages easy to see.

### 1:40 The model, in code
Everything lives in model.py. Start with the block, the repeating unit of a transformer:

```python
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
```

Two things to notice. First, the mask. It's an upper-triangular matrix that blocks each position from looking at later positions. That is what makes the model causal: when it predicts the next character, it can only use the characters before it. Without that, training would be cheating. Second, the plus signs. The block adds its output to its input, a residual connection, which helps deep stacks train.

Now the full model:

```python
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
```

Characters become vectors, the position of each character is added, the stack of blocks mixes information, and the head turns the result back into one score per character in the vocabulary. The loss is cross-entropy: how surprised was the model by the true next character?

The training data is sliced in a very simple way:

```python
def batch(self, ctx, bs):
    ix = torch.randint(len(self.data) - ctx - 1, (bs,))
    x = torch.stack([self.data[i:i + ctx] for i in ix])
    y = torch.stack([self.data[i + 1:i + ctx + 1] for i in ix])
    return x, y
```

Pick random starting points, take a window as the input, and take the same window shifted by one as the answer. That is the whole supervision signal: every position is a tiny quiz where the answer is the next character.

And here is how it writes:

```python
@torch.no_grad()
def generate(self, idx, n, temperature=0.8, top_k=None):
    for _ in range(n):
        logits, _ = self(idx[:, -self.ctx:])
        logits = logits[:, -1] / max(temperature, 1e-4)
        if top_k:
            logits[logits < torch.topk(logits, top_k).values[:, [-1]]] = -float("inf")
        idx = torch.cat([idx, torch.multinomial(F.softmax(logits, -1), 1)], 1)
    return idx
```

Take the scores for the last position, divide by temperature, optionally keep only the top k, turn them into probabilities, and sample one character. Append it and repeat. Temperature is the creativity knob: low means safe and repetitive, high means adventurous and messy.

The training loop in the app is the standard four lines: get a batch, compute the loss, zero the gradients, backward, step, using the AdamW optimiser. The sidebar lets you change layers from one to six, the embedding size, the context length, the number of steps and the learning rate.

### 5:30 Live demo
[SCREEN: app.] The sidebar: training text is Shakespeare, or you can upload your own text file. Model settings: four layers, embedding size one hundred and twenty-eight, context sixty-four. Training: six hundred steps, learning rate three e minus three. I press Train from scratch. [SCREEN: footage sped up.]

First it reports the parameter count, vocabulary and the size of the text: over a million characters of Shakespeare. The progress bar shows the step, the loss, and steps per second. [Read the real values shown.] When I checked this on the build machine, the loss started around four point three, which is roughly what you'd expect from guessing among sixty-five characters at random, and fell to about two point five within the first sixty steps.

Now the part I love: the section called "What the model writes as it learns". Step one is noise. A few hundred steps in, there are real-looking words and line breaks and speaker names. It isn't coherent, but the shape is unmistakably a play.

When training finishes, scroll down to generate. I type "ROMEO:" as the start, and keep temperature at zero point eight. [Click Generate.] Now low temperature, zero point two: the text gets calmer, and starts repeating itself. High, one point four: wilder words, more nonsense. Same model, same weights, only the sampling changes.

### 7:30 What surprised me
First, how early the structure appears. Before the model gets the words right, it learns the layout: capital letters after line breaks, names followed by colons. Structure is cheap; meaning is expensive.

Second, how much temperature changes the personality of the same model. People often blame the model for being boring or erratic when it is the sampling setting.

Third, how small this is. Under a million parameters, no GPU, a minute or two of training for a first impression. Everything you need to understand the core mechanism fits in one short file.

### 8:30 Honest limits
Let me be clear about what this model is not. It won't write coherent Shakespeare. At this size and with this little training it produces text that looks like a play but doesn't make sense. It only has a context window of up to a hundred and twenty-eight characters, so it can't remember anything earlier. It is character-level, which is slower to learn than word-level models. I haven't compared it against other architectures or tuned anything systematically, so don't read any particular loss number as a benchmark. Speed depends on your CPU; I measured between roughly four and six steps per second on mine across runs. And a language model trained on a single book will repeat that book's style and quirks, so if you upload text, expect it to echo it.

And again: I built this with an AI assistant. I ran it and checked the figures, but read the code yourself.

### 9:20 What to build next
Here are the obvious next steps. Visualise the attention weights, so you can see which earlier characters each position looks at. That's on my list. Train on your own writing, using the upload option. Try a word-level tokenizer. Or scale layers and embedding size up and measure what changes in the loss.

All the code is in the repo linked in the description, no API key needed. If you enjoyed watching a GPT go from gibberish to something play-shaped, follow for more AI and ML builds, and tell me what text you'd feed it.
