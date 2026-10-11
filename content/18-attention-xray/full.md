# 18 Attention X-ray - Full video (~8 min)

## Titles (pick one)
1. I Looked Inside a GPT: Where Does Each Attention Head Look?
2. Attention Explained With a Real Model (Not a Diagram)
3. The First Thing a Transformer Learns: Look at the Previous Letter

**Thumbnail text (<=4 words):** INSIDE A GPT

**Tags:** attention, transformer, self-attention, gpt, interpretability, visualization, python, pytorch, streamlit, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. All numbers come from the tiny character-level GPT in this repo (project 18 reads the model from project 07) and run on a laptop CPU with no API calls. Which head would you want to inspect next?

**Description:**
A tiny GPT (about 0.8M parameters) reads Shakespeare and I plot every attention head of every layer. I built it with Claude Code and the narration is AI-generated.

Recording note: the measured numbers are averages over 200 random 64-character windows of the training text: layer 1 head 2 puts 99% of its attention on the previous character, head 1 puts 97% on the character two back, head 4 puts 78% and head 3 puts 59% on the previous character. In layer 4 no head puts more than about 21% on itself, the previous character or the one before that. The model was trained for 2,000 steps (final batch loss 1.40).

## Voice-over

### [0:00] Cold open
This is a tiny GPT reading a line of Shakespeare. And this grid shows where each of its attention heads is looking while it reads. [SCREEN: app, layer one.] Look at this one: a perfect diagonal, just under the main one. Every character is looking at the character right before it. And this head looks exactly two characters back. Nobody programmed that. The model worked it out by itself from predicting the next letter. In this video I'll show you how I pulled these maps out of a real transformer, what each layer turns out to do, and where this kind of picture stops being trustworthy. I built this with Claude Code, and the narration is AI-generated.

### [0:50] Why it matters
You've probably seen the famous diagram: a sentence, with lines of different thickness connecting the words. That's attention. But most of those pictures are drawn by hand, or from huge models you can't run yourself.

Here the model is small enough to train in a few minutes on a laptop CPU, and we can look at every single head. It's the same mechanism as the big models: every character produces a query, every earlier character offers a key, and the match between them decides how much information flows. The heatmap is just that matching score, after softmax, for every pair.

One thing that makes it causal: a character may only look backwards, never forwards. That's why every map is a triangle.

### [2:00] Getting the attention out
This project reuses the model from project seven, so there is no new architecture. Its attention layer is PyTorch's MultiheadAttention, and by default the model asks it not to return the weights. To look inside, I run the blocks myself and ask for them.

```python
@torch.no_grad()
def x_ray(ids):
    idx = torch.tensor([ids])
    x = model.tok(idx) + model.pos(torch.arange(idx.size(1)))
    maps = []
    for b in model.blocks:
        T = x.size(1)
        h = b.ln1(x)
        out, w = b.attn(h, h, h, attn_mask=b.mask[:T, :T], need_weights=True, average_attn_weights=False)
        maps.append(w[0].numpy())
        x = x + out
        x = x + b.mlp(b.ln2(x))
    probs = model.head(model.ln(x))[0].softmax(-1).numpy()
    return maps, probs
```

It's the same forward pass as before, with two changes: need_weights is true, and average_attn_weights is false, so I get one map per head instead of one averaged map. For each of the four layers I keep an array of heads by positions by positions. At the end, the same head layer gives me the probability of every possible next character.

The model itself was trained a bit longer than in project seven: two thousand steps with a decaying learning rate, saved to a three megabyte file, so the app loads instantly.

### [4:00] What the heads do
[SCREEN: app, layer one, all heads.] Layer one. Head two: a sharp diagonal. Averaged over two hundred random windows of Shakespeare, it puts ninety-nine percent of its attention on the previous character. Head one does the same trick, two characters back, ninety-seven percent. Heads three and four are looser: they mostly look one back, fifty-nine and seventy-eight percent, and spread the rest over earlier text.

So the very first thing this transformer learned is to build its own short window: for every position, it copies in what the one or two previous characters were. That's exactly the information a next-character predictor needs first.

[SCREEN: layer two.] Layer two is less tidy. Several heads still lean on the previous character, but they spread weight over the last few positions. [SCREEN: layer four.] By layer four, the simple diagonals are gone, and some maps show bright vertical stripes: many characters looking at the same few earlier places. No head puts more than about twenty-one percent on itself, the previous character, or the one before that. That doesn't mean they're useless. It means they're doing something that isn't a simple offset, and a heatmap can't tell me what those places have in common.

### [5:45] From attention to a prediction
[SCREEN: bottom of the app.] Below the map there's a slider for a character position. For that character I show how much it attends to each earlier one, and what the model predicts comes next.

[SCREEN]

After "ROMEO:", the model predicts a newline with one hundred percent probability. It has seen that speaker format thousands of times. [SCREEN]

After "doth teac", it predicts the letter h, again at ninety-nine percent. That's the model finishing a word it knows.

[SCREEN]

At other places it's honestly unsure. After "he doth te", it says l at thirty-six percent and a at thirty-three percent: the real word, teach, starts with the second one. This is a small model, and uncertainty like that is normal and visible.

### [7:00] Honest limits
Now the part that matters. An attention map is a clue, not an explanation. Later layers mix information from every head, and the weights don't tell you how much a value actually changes the output. A head that attends strongly to a character may be doing little with it.

The numbers here are averages over a modest sample of Shakespeare windows, and one trained model with one seed. A different training run would have different heads. And the model only knows characters from the training text, so unusual characters get skipped in the app.

I built this with Claude Code, and I ran the measurements myself, but please treat the percentages as examples from this one model.

### [7:50] What to build next
Next I'd like to track how these heads appear during training, so you can watch the previous-character head form. I'd also like to try knocking one head out and measuring how much worse the predictions get, which is a much better test than just looking at a heatmap.

The code is in the description. No API key, no cost. If you enjoyed looking inside a GPT, follow for more AI and ML builds, and tell me which head to investigate next.
