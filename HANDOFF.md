# Handoff: AI/ML YouTube demo projects

Date: 2026-10-10 · Location: `D:\Research\Source\rnd-projects-aiml` · Git: local repo, one commit per project.

## What this is
A collection of 16 small Streamlit apps for YouTube demos on AI/ML. Each is a single `app.py` (project 02 also has `engine.py`, project 07 has `model.py`). Shared code is in `common/llm.py`.

## How to run
```
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu    # only project 07
python run_all.py            # all apps on ports 8501-8515, hub at http://localhost:8500
python run_all.py 4 6        # only projects 04 and 06
```
Port = 8500 + project number.

## What was built (all tested headlessly with Streamlit AppTest; 06 also driven in real Chrome)
| # | Project | Type | Azure cost |
|---|---------|------|-----------|
| 01 | Prompt Arena: GPT prompting styles fight, judge scores both orderings, Elo | LLM game | ~4 calls/battle |
| 02 | Prompt Injection Lab: 5 defense levels, manual play + automated red-team heatmap | LLM security | ~1 call/attack |
| 03 | Semantic Map: embeddings on a 2D map + RAG answer | embeddings + RAG | 1 call/search |
| 04 | Neural Net Playground: numpy backprop, live decision boundary | build a model | none |
| 05 | Spot the Hallucination: find the lie among 5 GPT facts | LLM game | 1 call/round |
| 06 | Draw a Digit: SVM / MLP / RF / k-NN vote on your drawing (custom canvas component) | classic ML | none |
| 07 | Tiny GPT Trainer: 0.8M-param char transformer trained live on Shakespeare (PyTorch CPU) | build a model | none |
| 08 | AI 20 Questions (both directions) | LLM game | 1 call/question |
| 09 | RL Gridworld: Q-learning vs SARSA, scrub through training | RL | none |
| 10 | Evolving Rockets: genetic algorithm, scrub through generations | evolutionary | none |
| 11 | Token X-ray: tiktoken colour chips, cost, why LLMs can't count letters | LLM education | none |
| 12 | AI Debate Arena: 2 debaters + judge radar chart + "did it change your mind" | LLM | 2×rounds+1 calls |
| 13 | Clustering Lab: K-means step-by-step + 4 algorithms x 5 datasets | classic ML | none |
| 14 | Explainable Text AI: TF-IDF classifier highlighting the words behind each decision | classic ML | none |
| 15 | Prompt Gym: 6 prompt-writing levels graded by Python checkers | LLM game | 1 call/attempt |
| 16 | CNN X-ray: MobileNetV2 top-5 + Grad-CAM heatmap (sample/upload/webcam) | deep learning | none |

Also: `hub/app.py` (landing page linking everything), `run_all.py`, `README.md`.

## Configuration and decisions (read before changing things)
- **LLM = Azure OpenAI**, read from the root `.env` (gitignored, never committed): `AZURE_OPENAI_API_KEY`, `_ENDPOINT`, `_DEPLOYMENT` (gpt-4o), `_API_VERSION`. `.env.example` has the template. Only a **chat** deployment exists.
- **Cost control:** every call is small (`max_tokens` 3-350), and `common/llm.py` has a per-process cap `MAX_LLM_CALLS` (default 150, set in `.env` to change). The user asked for "very low" usage.
- **Docker was abandoned.** The first plan was Ollama in Docker, but Docker Desktop was unstable (and only ~2 GB RAM), and the user then said to use Azure. `docker-compose.yml` was removed. No project needs Docker.
- **Embeddings are local** hashing char-n-grams (`common/llm.embed`), because there is no Azure embedding deployment. Consequence: project 03's map clusters by wording, not true meaning. Adding an embedding deployment and switching `embed()` would improve it.
- **Azure content filter** may reject jailbreak-style prompts; project 02 treats that as "blocked by Azure content filter".
- **Streamlit is 1.65.** The `streamlit-drawable-canvas` package is broken on it, so project 06 uses its own inline v2 component. `use_container_width` is deprecated; code uses `width="stretch"`.
- **Downloads on first run:** 14 fetches 20newsgroups via scikit-learn (slow once, then cached in `~/scikit_learn_data`); 11 uses tiktoken vocab files; 07 needs `data/shakespeare.txt` (committed).

## Known limits
- 06: trained on 8x8 sklearn digits; messy or off-centre drawings are often misread (that disagreement is part of the demo). Only a "7" was tested by hand.
- 05: the "true" facts come from GPT itself, so a round can occasionally contain a wrong "fact".
- 10: the Zig-zag level is hard and unsolved on some seeds (by design; the UI suggests more generations).
- 02: GPT-4o is robust, so only level 1 (and sometimes 2) leaks. The red-team grid is mostly green, which is an honest result.
- Nothing has been screen-recorded or run through a full manual click-through except 06.

## What we can do next
1. **Finish 16 CNN X-ray** (Grad-CAM + webcam via `st.camera_input`).
2. **Attention visualiser** for project 07 (heatmap of what each head looks at).
3. **Real embeddings** for 03 (Azure embedding deployment) plus a "chat with your own PDF" mode.
4. **Overfitting / bias-variance lab** (polynomial degree slider, train vs test error).
5. **Self-consistency demo**: ask GPT a maths question 5 times and majority-vote (shows why sampling helps; ~30 calls).
6. **LLM agent demo**: tool-using agent (calculator + search over local docs) with a visible thought/action log.
7. **Polish for filming:** dark theme, bigger fonts (`.streamlit/config.toml`), a title card per app, record each with the Chrome GIF tool.
8. **Video plan:** best hooks are 06 (draw a digit), 07 (watch gibberish become Shakespeare), 09 (SARSA vs Q-learning cliff), 10 (rockets), 02 (hack the bot). 04 and 13 are good short explainers.
9. **Housekeeping:** add a simple smoke-test script that runs every app with AppTest; pin versions in `requirements.txt`.

---
# Session 2 handoff (2026-10-10/11): video production

## State at a glance
- **16 projects built**; `python smoke_test.py` passes all 16 apps + hub. Project 16 (CNN X-ray, MobileNetV2 + Grad-CAM) was added this session.
- **Scripts written**: `content/<NN-name>/short.md` (16), `full.md` for 02, 06, 07, 09, 10, 16, and `content/_showcase/full.md`. Facts re-verified (SARSA vs Q-learning is ~27 vs ~2 over 10 seeds, NOT 28.6 vs 11.0; Tiny GPT ~4 steps/s measured).
- **Shorts rendered**: all 16, two versions each: `out/short.mp4` (v1, kept) and `out/short_v2.mp4` (Watch It Learn electric intro + spoken end card + voice matched to the screen). Use v2. Videos are git-ignored; scripts are committed.
- **Channel**: name **Watch It Learn** (new YouTube Brand channel on existing Google account + new Instagram Creator account; handles to check: @watchitlearn, @watchitlearn.ai). Art in `content/_brand/`. Posting order/titles/captions in `content/UPLOAD_PLAN.md` (generated by `tools/upload_plan.py`).
- **First batch of 6 staged** (not uploaded): `content/_outbox/batch_2026-10-12/` = 06, 09, 07, 10, 02, 16, one per day 19:00 from Mon 12 Oct; see its `SCHEDULE.md`.
- **Nothing has been published anywhere.** Never upload without approval.

## Tools (all in `tools/`)
| tool | what |
|---|---|
| `make_short.py <NN>` | records the live app with Playwright (540x960), edge-tts voice, ffmpeg; needs the app running on port 8500+NN; reads `content/<proj>/record.py` (PORT, VOICE, CAPTIONS, prepare, actions); writes `out/short.mp4` + `out/raw.json` |
| `make_short2.py <NN>` | rebuilds `out/short_v2.mp4` from EXISTING raw footage (no re-record, no LLM calls): VOICE2/CAPTIONS2 from record.py, strips the spoken "Follow for more..." (end card says it), electric intro + outro cached in `content/_assets/` |
| `brand.py` | Pillow electric intro/outro frames + synthesized zap sound |
| `brand_assets.py` | profile picture + YouTube banner into `content/_brand/` |
| `upload_plan.py` | writes `content/UPLOAD_PLAN.md` |
| `stage_batch.py [count] [start] [hour]` | stages the next N shorts into `content/_outbox/batch_<date>/` with quality gate and `queue.json` |

## Decisions and user feedback (full log in `content/DECISIONS.md`)
- No avatar anywhere (user said it looked bad); captions in the lower third; follow call spoken once, on the end card; voice = edge-tts `en-US-AndrewNeural` (AI-narration disclosure in every description); electric intro approved ("looks nice").
- Routine plan (`content/ROUTINE_PLAN.md`): runs on the user's PC (Task Scheduler), **batch mode: build/stage 5-6 shorts in one run, user approves, then schedule** (YouTube Schedule / Meta Business Suite). Not built yet: Task Scheduler entry, quality-gate screen checks, YouTube API uploader (needs the user's Google OAuth client file in `secrets/`), Instagram (manual or Graph API), Stage B headless "build 6 new projects" run, `content/ideas.md`.
- Azure usage ran over the soft cap during short recording (~60-70 calls total; 08 alone ~20). Keep future LLM recordings to a few calls per project and reuse raw footage.

## Known flaws in the shorts (user may want fixes)
03 caption covers part of the retrieved list; 07 trained off-camera (clip scrolls a finished 300-step run); 10 and 09 have a few blank/greyed frames during Streamlit reruns; 01 started on a loading skeleton in v1 (v2 uses the same footage); 08's game never reaches a guess in the footage. Frames of the last rebuild were only checked on 16.

## Next steps (resume here)
1. User creates the accounts and checks the handle; user schedules batch 1 by hand (or does the Google OAuth setup so we can build the uploader).
2. Build the routine pieces in the order listed in `content/ROUTINE_PLAN.md` (queue exists; add screen checks, Task Scheduler, uploader).
3. Phase 3b/3c from `PLAN.md`: showcase video (`content/_showcase/full.md`) and the six 10-minute videos (06, 07, 09, 10, 02, 16). Reuse `tools/` (record at 1920x1080; no avatar).
4. Phase 4: a new catchy project (ideas in PLAN.md and HANDOFF "What we can do next"), then the whole pipeline again.
5. Optional: re-record/polish the flawed shorts above.

---
# Session 3 handoff (2026-10-11): long videos + project 17

- **Long-video builders:** `tools/make_showcase.py` (showcase, 7.3 min) and `tools/make_full.py <NN>` (flagships). `make_full` reads `content/<proj>/full.md` (voice-over; `[SCREEN]`, ```code blocks and `[Draw]` markers advance the visuals) and `content/<proj>/video.py` (PORT, CODE crops, SECTIONS, `record()` scenes, optional `FIT`/`QUERY`). One edge-tts clip per sentence decoded to wav, so captions and voice stay in sync. Outputs `content/<proj>/out/full.mp4` + committed `chapters.txt` / `full.srt` (shifted for the intro). See `content/FULL_VIDEOS.md`.
- **Built:** showcase, flagships 06, 07, 09, 10, 02, 16, and the new **17 Flappy Evolution** (neuroevolution, port 8517, hub + README + smoke test updated) with its short (`short_v2.mp4`) and full video. 17 is already in `content/UPLOAD_PLAN.md`, but not in the staged batch (`_outbox/batch_2026-10-12`).
- **Lessons:** mp3 duration from edge-tts headers is unreliable (decode to wav); Streamlit's sidebar select is `stSelectbox`, radio labels include the widget label as item 0; use `?embed=true` only when the sidebar is not needed; zoom the page (`html{zoom:.85}`) so tall plots fit 1600x860.
- **Honesty notes:** 02's red-team numbers (L1 50%, L2 25%, L3-L5 0%) are from one recorded run and the script says so; that recording used ~55 Azure calls.
- **Nothing is uploaded.** Next: user reviews the videos; then upload/schedule (see `content/ROUTINE_PLAN.md`, `content/INSTAGRAM_SETUP.md`), optional polish of blank Streamlit frames, more projects.

## Project 18 Attention X-ray (added later on 2026-10-11)
- `18-attention-xray/`: app (port 8518) shows every head of every layer of the Tiny GPT trained by `18-attention-xray/train.py` (2,000 steps, `weights.pt` 3.3 MB, committed). Measured on 200 random 64-char windows: L1H2 puts 99% on the previous char, L1H1 97% on the char two back, L1H4 78% / L1H3 59% on the previous; by layer 4 no head exceeds ~21% on itself/prev/prev-prev, and the maps show vertical stripes.
- Short (`content/18-attention-xray/out/short_v2.mp4`, 27 s) and full video (5.6 min) built with the same tools; added to hub, README (ports 8501-8518) and `content/UPLOAD_PLAN.md`.

---
# Session 4 handoff (2026-10-11): the missing 10 long videos

- **Done:** long videos for 04, 11, 13, 14 (local apps) and 01, 03, 05, 08, 12, 15 (LLM apps, played live against Azure with real results). All 18 projects now have a short and a long video. Table and notes in `content/FULL_VIDEOS.md`; per-project script, title options, tags, pinned comment and description in `content/<project>/full.md`.
- **How the LLM ones were recorded:** each `video.py` writes the on-screen state to a scratch folder after every turn and waits for my next input (question, prompt, answer), then types it into the real app. Scores and verdicts in the scripts are real (e.g. 05 got 3 of 4, 15 cleared all six levels in 10 attempts, 12 debates ended 40-36 and 42-44). 15's footage is a replay of the same ten prompts so the verdict stays in frame; its description says so.
- **Pipeline additions in `tools/make_full.py`:** `CROPS`, `TRIM`, `--record-as TAG` (see `content/FULL_VIDEOS.md`). Gotchas learnt: Streamlit text areas need Ctrl+Enter to commit before a button is enabled; chart updates that remount every frame paint blank in video (04 now sleeps 0.12 s per frame); marker sentences advance the picture on the *next* sentence, so put `[SCREEN]` before the sentence it should illustrate; scenes end on their last frame, so trim scenes whose recorder scrolls at the end.
- **App fixes made for the videos:** 04 (no per-frame key, short sleep), 15 (passed result stays visible after auto-advance).
- **Honest-note reminders:** 14's in-app caption says errors are mostly Space/Medicine, but the largest real error cells are posts labelled Cars; 03's embeddings are character hashes, not semantic; 05 and 08 were played by the author who knows the answer lists; 01's Elo values from different fights are not comparable.
- **Nothing is uploaded.** Next: user reviews the 10 new videos (watch at least the first minute and a few random points of each), then upload/schedule as in `content/ROUTINE_PLAN.md`; the 10 are not yet in the staged batches or `content/UPLOAD_PLAN.md`.

---
# Session 5 (2026-10-14): YouTube publishing
- Channel: https://www.youtube.com/@watchitlearn. Repo public: https://github.com/lakshmansha/rnd-projects-aiml (MIT, topics, README).
- 18 long videos uploaded with metadata + thumbnails (content/_thumbs), now SCHEDULED public at 7:00 PM IST, one per day, Oct 15 to Nov 1 2026, same day as the matching short (order in content/INSTAGRAM_QUEUE.md). 18 shorts scheduled the same way (7:00 PM IST). Each short links its long video.
- Not done: pinned comments (post after each goes public); Instagram Reels (manual or Meta Business Suite, see content/INSTAGRAM_QUEUE.md); delete the duplicate draft "18 attention xray" (id 7KUk3_B3sGQ) in Studio.
- Chrome upload tool limit ~10 MB per file; the videos were uploaded by the user by hand, metadata set by script through Studio. content/links.json and PUBLISH_SHEET_LINKED.md hold the real links and are git-ignored.

- **Full, current handoff: see `HANDOFF_NEXT.md` (written 2026-10-15).** It supersedes the short Session 5 notes above: all 36 YouTube videos are scheduled (7 PM IST daily, Oct 15 to Nov 1); the Instagram Reels still need to be scheduled by the user.
