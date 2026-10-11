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
| 01-llm-arena (new) | `content/01-llm-arena/out/full.mp4` | 5.8 min | `content/01-llm-arena/chapters.txt`, `full.srt` |
| 03-semantic-map (new) | `content/03-semantic-map/out/full.mp4` | 6.3 min | `content/03-semantic-map/chapters.txt`, `full.srt` |
| 04-neural-playground (new) | `content/04-neural-playground/out/full.mp4` | 5.1 min | `content/04-neural-playground/chapters.txt`, `full.srt` |
| 05-spot-the-hallucination (new) | `content/05-spot-the-hallucination/out/full.mp4` | 6.2 min | `content/05-spot-the-hallucination/chapters.txt`, `full.srt` |
| 08-twenty-questions (new) | `content/08-twenty-questions/out/full.mp4` | 6.2 min | `content/08-twenty-questions/chapters.txt`, `full.srt` |
| 11-token-xray (new) | `content/11-token-xray/out/full.mp4` | 6.0 min | `content/11-token-xray/chapters.txt`, `full.srt` |
| 12-debate-arena (new) | `content/12-debate-arena/out/full.mp4` | 5.7 min | `content/12-debate-arena/chapters.txt`, `full.srt` |
| 13-clustering-lab (new) | `content/13-clustering-lab/out/full.mp4` | 5.7 min | `content/13-clustering-lab/chapters.txt`, `full.srt` |
| 14-explainable-text-ai (new) | `content/14-explainable-text-ai/out/full.mp4` | 5.6 min | `content/14-explainable-text-ai/chapters.txt`, `full.srt` |
| 15-prompt-gym (new) | `content/15-prompt-gym/out/full.mp4` | 7.4 min | `content/15-prompt-gym/chapters.txt`, `full.srt` |

Notes:
- Each video's title options, description, tags and pinned comment are in `content/<project>/full.md`.
- 02's live numbers (L1 50%, L2 25%, L3-L5 0%) come from one recorded run; the script says so. 02 recording used ~55 Azure calls.
- Narration is AI-generated; every description must say so.
- Nothing has been uploaded.
- All 18 projects now have a long video (the 8 above plus the 10 added in session 4: 01, 03, 04, 05, 08, 11, 12, 13, 14, 15).
- Session 4 videos with LLM calls were played live against Azure: the recorder writes the on-screen state to a scratch folder and waits for my next move (question, prompt, pick), so scores and verdicts in the script are what really happened. Rough Azure use: 01 about 40 calls (two takes), 03 4, 05 4, 08 about 30 (several takes), 12 10, 15 about 30 (an interactive take plus an identical replay of 10 prompts for framing).
- 15 Prompt Gym: the footage is a replay of the same ten prompts so the verdict stays in view; the description and the script say so.
- Helpers added to `tools/make_full.py`: `CROPS` (zoom into part of a scene), `TRIM` (use only the first N seconds of a scene), `--record-as TAG` (extra recording whose scenes override same-named ones, used for 08 mode A).
- App changes made for the videos: 04 draws without a per-frame key and sleeps 0.12 s per frame (the chart painted blank otherwise); 15 keeps showing a passed result after it auto-advances to the next level.
- Honest-note reminders: 14's caption claims errors cluster between related topics, but the real largest cells are posts labelled Cars; 03 uses character-hash embeddings (not semantic); 08 and 05 were played by the author, who knows the lists.
