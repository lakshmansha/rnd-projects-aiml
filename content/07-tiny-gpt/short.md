# 07 Tiny GPT Trainer - 30s Short (9:16)

**Title (<60):** I trained a tiny GPT from scratch on my CPU
**Description:** A real transformer (~0.8M parameters) learns Shakespeare live: watch gibberish turn into play-like text. No API calls. Built with Claude Code. Narration is AI-generated. Code: rnd-projects-aiml, project 07.
**Hashtags:** #GPT #Transformer #PyTorch #DeepLearning #ClaudeCode

## Voice-over (~75 words)
(0-3s) This GPT starts out knowing nothing. Watch it learn.
(3-11s) I built it with Claude Code: a real transformer, under a million parameters, training on Shakespeare on my CPU. I press Train from scratch.
(11-19s) Step one is pure gibberish. As the loss falls, you see letters, then words, then something shaped like a play.
(19-27s) It only ever predicts the next character. Everything else emerges from that.
(27-30s) Follow for more AI/ML builds.

## Timeline and on-screen text
| Time | On screen text | Action to record |
|---|---|---|
| 0-3s | "A GPT that knows NOTHING" | App "Tiny GPT Trainer" open, sidebar showing Data: Shakespeare |
| 3-11s | "818,176 parameters" | Click "🚀 Train from scratch" (default 4 layers, embedding 128, context 64, 600 steps). Text line "818,176 parameters · vocabulary of 65 characters..." appears |
| 11-19s | "Step 1 -> Step 100 -> Step 200" | Show the loss chart and the "What the model writes as it learns" samples stacking: "Step 1" gibberish, later samples more Shakespeare-like |
| 19-27s | "Just predicts the next character" | Scroll to samples; optionally show the sidebar sliders |
| 27-30s | "Follow for more AI/ML builds" | End card |

Notes: speed up the training footage in editing (the app says ~2 min for 600 steps). Re-verified headlessly: 818,176 parameters, 65-character vocabulary, loss 4.31 at step 1 and 2.47 at step 60, ~4 steps/s on this machine. Say "under a million parameters" in narration; do not read out steps/s unless it is visible on the progress bar.
