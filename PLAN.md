# PLAN: finish the build, then script and produce the videos

Written 2026-10-10 before the user left for cricket (back after ~10 PM). The user will clear the session and say "start".
**Rule: this file is the source of truth. After every step, tick the box in `content/PROGRESS.md`, commit, and continue. If credit runs out, resume from the first unticked box.**

## Standing rules from the user
- **Docker works again** (Docker 29.8, ~6 GB RAM, confirmed 2026-10-10 evening): it MAY be used, e.g. an Ollama container for free local LLM calls (`qwen2.5:1.5b` / `llama3.2:3b`, plus `all-minilm` or `nomic-embed-text` for real embeddings) so recordings and the new project cost no Azure credit. **Azure OpenAI is also allowed** (root `.env`). Keep Azure calls VERY low (`MAX_LLM_CALLS` cap, small `max_tokens`). Never print or show the key or `.env`. If Docker fails again, fall back to Azure.
- Commit each finished piece (small commits, trailer line as required by the harness).
- "Keep going, don't ask." Make sensible decisions, write them down in `content/DECISIONS.md`.
- **Avatar photo (provided):** `D:\Research\Source\rnd-projects-aiml\photo\profile.JPG` (22 MB portrait: blue suit, glasses; the face is in the upper-middle of the frame, roughly the top 40%). The user permits using it as an avatar, and said "if the photo is complicated, leave it". The `photo/` folder is git-ignored: never commit it. Make a downscaled copy at `content/_assets/avatar.png` (also git-ignored) for use.
- **Never upload or publish to YouTube or any social platform.** The user will push the content tomorrow.
- Sub-agents are allowed (use them for parallel script writing; each writes only to its own folder).

## Phase 0: Re-orient (5 min)
1. Read `HANDOFF.md`, this file, `git log --oneline | head`.
2. Check that the Streamlit apps are running (`python run_all.py`, ports 8501-8515, hub 8500). Two old background tasks (an Arena server and a torchvision install) were stopped when the session ended: confirm `pip show torchvision` and restart servers as needed.
3. Create `content/PROGRESS.md` (checklist of everything below) and `content/DECISIONS.md`.

## Phase 1: Finish what's left in the build
0. (Optional, ~15 min) Restore a `docker-compose.yml` with an Ollama service, pull `qwen2.5:1.5b` and an embedding model, and add an `LLM_PROVIDER=ollama` option in `common/llm.py`, so project 03 gets real embeddings and recordings can run at zero Azure cost. Azure stays the default fallback.
1. **Project 16: CNN X-ray** (`16-cnn-xray/app.py`): upload or webcam image -> MobileNetV2 (ImageNet) top-5 + Grad-CAM heatmap overlay. Weights: `torchvision.models.mobilenet_v2(weights=IMAGENET1K_V2)`. Sample images in `16-cnn-xray/samples/` (dog.jpg may already exist; use free/public-domain images only). Test headlessly, add to `hub/app.py` (port 8516), README, `run_all` picks it up automatically.
2. Update `HANDOFF.md`, commit.
3. Quick smoke script `smoke_test.py` that runs every app via `streamlit.testing.v1.AppTest` and reports exceptions. Fix whatever breaks.

## Phase 2: Scripts (no video yet), per project, in `content/<NN-name>/`
For each of the 16 projects write:
- `short.md`: **30-second YouTube Short (9:16)**: 0-3 s hook line, 3 beats of ~8 s each (what you see, the surprising moment, the insight), 3 s call to action ("follow for more AI/ML builds"). ~75 words of voice-over. Include on-screen text lines, the exact in-app actions to record, title (<60 chars), description, 5 hashtags.
- `full.md`: **~10-minute video** (about 1,400 words voice-over) for the 6 flagship projects only (see list). Structure: cold-open hook (30 s) -> why it matters -> build walkthrough with code highlights (what the architecture is, key 20 lines) -> live demo -> insights and "what surprised me" -> limits/honest caveats -> what to build next + CTA. Include chapter timestamps, a shot list (screen / code / avatar), title options (3), thumbnail text (<=4 words), description, tags, pinned comment.
- Flagship 10-minute videos: **06 Draw a Digit, 07 Tiny GPT Trainer, 09 RL Gridworld (SARSA vs Q-learning), 10 Evolving Rockets, 02 Prompt Injection Lab, 16 CNN X-ray.** Plus one **channel-intro / skills-showcase video** (`content/_showcase/full.md`): "I built 16 AI/ML projects in a day with an AI pair-programmer": the stack, the range of skills (LLMs/RAG/security, classic ML, deep learning from scratch, RL, evolutionary algorithms, explainability, shipping), lessons learned. Tone: friendly, first person as the user, honest about the AI help (the user writes "built with Claude Code").
- Facts must come from the code and real test results (e.g. SARSA 28.6 vs Q-learning 11.0 average reward on the cliff; 98-99% digit accuracy on sklearn test split; 84.8% on 20 newsgroups; Tiny GPT 0.8M params, ~6 steps/s on CPU). Never invent numbers; re-run the app if unsure.
- Use sub-agents here: one per 4-5 projects, each told to read the app code, run it headlessly if needed, and write only its own `content/` folders. Review and fix their output.

## Phase 3: Produce the videos (shorts first, then full)
Pipeline (decide in `DECISIONS.md` after a 10-minute spike; prefer reliability over fancy):
1. **Voice-over:** text-to-speech from the script (try `edge-tts` or Windows SAPI via PowerShell `System.Speech`; no voice cloning of the user without them asking). Add disclosure line in the description: "narration is AI-generated".
2. **Screen footage:** primary = **scripted browser capture** (Playwright + Chromium `record_video`, or the Chrome extension for interactions, viewport 540x960 for shorts and 1920x1080 for full), because it is repeatable and unattended. Fallback = **OBS** (installed at `C:\Program Files\obs-studio\bin\64bit\obs64.exe`; control via obs-websocket on port 4455 with `obsws-python`, only if the user has enabled it). `ffmpeg` is on PATH (WinGet) for cutting, scaling, subtitles and muxing.
3. **Avatar:** keep it simple: crop the face from `photo/profile.JPG` into a circular picture-in-picture (bottom corner, ~220 px) with a ring that pulses to the audio level (Pillow + ffmpeg). Optional upgrade only if a spike takes under 20 min: a Docker image for a talking-head model (SadTalker / Wav2Lip); it is CPU-only here so probably too slow, so skip it otherwise. No face-swap. If anything about the photo is complicated, drop the avatar, use screen + voice only, and log that in `DECISIONS.md`.
4. **Assembly:** ffmpeg: footage + voice-over + burned-in captions (SRT) + title card + end card. Shorts: 1080x1920, <=30 s. Full: 1920x1080, ~10 min, chapters in the description.
5. Outputs in `content/<NN-name>/out/` (git-ignore the large `.mp4`; commit scripts, SRTs, thumbnails). Keep an `INDEX.md` listing every file with duration and status.
6. Order: all 16 shorts -> the showcase video -> the 6 flagship full videos. After each finished video: tick PROGRESS, commit.
7. **Quality gate on every video:** watch a few frames (extract with ffmpeg and view), check audio length matches the script, no `.env`/key/email/other-person content on screen, no copyrighted music (use none, or generate a quiet synthetic bed).

## Phase 4: Something new and catchy, then repeat
After everything above is done, build **one new, very catchy project** (pick from: attention visualiser for the Tiny GPT; "AI plays a game" such as a DQN/neuroevolution Flappy Bird or Snake that learns live; draw-and-guess with a CNN; LLM tool-using agent with visible thoughts). Prefer one with a strong visual hook in the first 3 seconds and low or zero Azure cost. Then run Phases 1-3 for it (build, test, commit, short + full script, video).

## Budget and resumption
- Azure: recordings of LLM apps should use <50 calls in total; reuse recorded footage.
- If the session credit runs out: stop cleanly after a commit. On resume, read `PLAN.md` and `content/PROGRESS.md` and continue at the first unticked item.
- Daily checkpoint: when the user returns (~10 PM) give a short status: what is done, where the videos are (`content/INDEX.md`), what needs their eyes (photo path, voice choice, anything skipped and why).
