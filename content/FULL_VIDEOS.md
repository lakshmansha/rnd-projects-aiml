# Long videos (1920x1080, Watch It Learn)

All built by `tools/make_full.py <NN>` (showcase: `tools/make_showcase.py`): AI voice (edge-tts), real app recordings and code from the repo, captions burned in, electric intro + spoken end card. Videos are git-ignored; scripts, SRTs and chapter lists are committed.

| Video | File | Length | Chapters / SRT |
|---|---|---|---|
| Showcase (16 projects) | `content/_showcase/out/showcase.mp4` | 7.3 min | `content/_showcase/out/` |
| 02-prompt-injection-lab | `content/02-prompt-injection-lab/out/full.mp4` | 11.4 min | `content/02-prompt-injection-lab/chapters.txt`, `full.srt` |
| 06-digit-classifier | `content/06-digit-classifier/out/full.mp4` | 7.6 min | `content/06-digit-classifier/chapters.txt`, `full.srt` |
| 07-tiny-gpt | `content/07-tiny-gpt/out/full.mp4` | 7.1 min | `content/07-tiny-gpt/chapters.txt`, `full.srt` |
| 09-rl-gridworld | `content/09-rl-gridworld/out/full.mp4` | 7.9 min | `content/09-rl-gridworld/chapters.txt`, `full.srt` |
| 10-evolving-rockets | `content/10-evolving-rockets/out/full.mp4` | 7.2 min | `content/10-evolving-rockets/chapters.txt`, `full.srt` |
| 16-cnn-xray | `content/16-cnn-xray/out/full.mp4` | 8.3 min | `content/16-cnn-xray/chapters.txt`, `full.srt` |
| 17-flappy-evolution (new) | `content/17-flappy-evolution/out/full.mp4` | 6.3 min | `content/17-flappy-evolution/chapters.txt`, `full.srt` |
| 18-attention-xray (new) | `content/18-attention-xray/out/full.mp4` | 5.5 min | `content/18-attention-xray/chapters.txt`, `full.srt` |

Notes:
- Each video's title options, description, tags and pinned comment are in `content/<project>/full.md`.
- 02's live numbers (L1 50%, L2 25%, L3-L5 0%) come from one recorded run; the script says so. 02 recording used ~55 Azure calls.
- Narration is AI-generated; every description must say so.
- Nothing has been uploaded.