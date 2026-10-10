# Routine plan: build a BATCH of 5-6 Shorts in one run, you approve, then schedule them on YouTube and Instagram

Decisions (2026-10-11, from the user): runs on **the user's PC (Windows Task Scheduler)**; posting mode **render -> user approves -> upload**. Nothing is ever posted without an approval.

## UPDATE 2026-10-11: batch mode (replaces the daily loop below)
The user wants **5-6 shorts built in one shot, then scheduled** (not one per day). So:
- One run (e.g. every Sunday) builds/stages **6 shorts** and writes a `SCHEDULE.md` with one publish time per day (default 19:00 local, Mon-Sat).
- You review the 6 previews once, approve the batch, and the posts are **scheduled** (YouTube "Schedule" / API `publishAt`; Instagram via Meta Business Suite scheduler or Graph API) so nothing else is needed for the week.
- Built now: `tools/stage_batch.py [count] [start_date] [hour]` + `content/queue.json`. First batch (06, 09, 07, 10, 02, 16) is staged in `content/_outbox/batch_2026-10-12/`, all passing the quality gate (format, 20-35 s, audio, no long silence).
- Stage B (new projects) becomes "build 6 new tiny projects in one run" weekly; the 16 existing shorts cover the first ~3 batches (6 + 6 + 4).
- The remaining text below describes the per-item pieces; read "daily" as "per batch".

## The loop (one run per day)

```
Task Scheduler (e.g. 18:00)
  -> tools/daily_short.py
       1. pick the next item from content/queue.json
       2. produce the short (stage A: already rendered v2 files; stage B: build a new project, see below)
       3. stage it in content/_outbox/<date>_<NN>/ : short_v2.mp4, title.txt, youtube.txt, instagram.txt, thumb.png, checks.txt
       4. run the quality gate (below); if it fails, mark "needs_fix" and notify instead of staging
       5. notify the user (Windows toast + a one-line summary in content/_outbox/LATEST.md)
  user reviews the preview (30 s) and approves
  -> tools/post.py approve <id>
       - YouTube: Data API upload (vertical, <=60 s, #Shorts in the description) as public or scheduled
       - Instagram: Reel via Meta Graph API, or manual upload from the outbox (see "Instagram options")
       - moves the item to content/_posted/ and records URLs in content/queue.json
```

## Stage A: the first 16 days (no new building)
The 16 shorts already exist (`out/short_v2.mp4`, order in `UPLOAD_PLAN.md`). The routine only stages the next one each day. This is cheap, reliable and lets you test the posting path before anything fancy.

## Stage B: a new short every day after that
New shorts need a new tiny project each day. The routine runs Claude Code headless on your PC with a fixed prompt (like the one that built this repo):
1. Take the next idea from `content/ideas.md` (backlog, you can edit it; I will seed 30 ideas).
2. Build `NN-name/app.py` (Streamlit, free to run, strong visual in the first 3 s, no API calls unless the idea needs one).
3. Test headless (`smoke_test.py`), commit.
4. Write `short.md`, `record.py`, record with `tools/make_short.py`, build with `tools/make_short2.py`.
5. Stage in the outbox like Stage A.
Cost: tokens for one small project per day plus <= 8 Azure calls only if the idea is an LLM one. A `MAX_DAILY_AZURE_CALLS` cap and a "stop if over budget" rule are part of the script.

## Quality gate before anything is staged (automatic)
- Video 1080x1920, 20-35 s, has audio, no silent frames > 1.5 s (ffmpeg checks).
- Frames extracted at 5 points; no Streamlit error box / "Connection error" text (OCR-free check: pixel colour of the red error banner, plus the recorder's own exception log).
- Voice text contains no numbers that are not in a `facts.json` the run produced from the real app output.
- No `.env`, API key, email or the personal photo in any frame (the recorder only opens the local demo app; the key is never rendered).
- Captions in the lower third; the follow line only on the end card.

## Posting details (what I need from you)
### YouTube (automatic, recommended)
One-time setup (about 15 min): Google Cloud project -> enable "YouTube Data API v3" -> OAuth consent screen (External, add yourself as a test user) -> create an OAuth Desktop client -> download `client_secret.json` into `secrets/` (git-ignored). First run opens a browser to authorise the **Watch It Learn brand channel**. After that uploads are automatic. Default quota covers about 6 uploads per day. Note: a new unverified API project may force uploads to be *private* until it passes Google's audit; if that happens we upload as private and you flip to public in one tap, or we switch to the manual path.

### Instagram options (pick one later)
1. **Manual with help (works today, zero setup):** the outbox gets a ready caption in your clipboard-friendly file; you post the Reel from your phone (I can copy the file to your phone via a shared folder or email-to-self). Takes about 1 minute a day.
2. **Meta Graph API (automatic):** needs the Instagram account switched to Professional, a Facebook Page linked to it, a Meta developer app with `instagram_content_publish`, a long-lived token (refreshed about every 60 days), and the video at a **public URL** when publishing (we would upload to a free host such as a temporary Cloudflare R2/S3 link, or YouTube is not accepted). More setup and more things that can break.
3. **Meta Business Suite scheduler (manual but batchable):** upload 7 days at once from a browser and schedule them. Good fallback.
My recommendation: **YouTube automatic + Instagram manual (option 1) for the first 2 weeks**, then add the Graph API only if the account is growing.

## Components to build (in order)
| # | Item | Needs you? |
|---|---|---|
| 1 | `content/queue.json` + `tools/daily_short.py` (stage A: stage next short in the outbox, toast) | no |
| 2 | Quality gate script | no |
| 3 | Windows Task Scheduler registration (`schtasks`, runs `daily_short.py` at 18:00) | one approval |
| 4 | `tools/post.py` YouTube upload + `approve` command | Google OAuth client file |
| 5 | Instagram helper (outbox caption file; optional Graph API later) | Meta app only if automatic |
| 6 | `content/ideas.md` (30 ideas) + headless Claude Code build prompt (Stage B) | no |
| 7 | Dry-run for 3 days in "stage only" mode, then switch posting on | you review |

## Guardrails
- Nothing is posted without your approval (command or a reply). No auto-post mode unless you later ask for it.
- Every generated claim is checked against the app's real output; AI-narration disclosure stays in every description.
- Credentials live only in `secrets/` and `.env` (git-ignored); never printed.
- Azure usage is capped per day; the routine stops and tells you if the cap is hit.
- If the PC is off at the set time, the task runs at next start (Task Scheduler "run as soon as possible after a missed start").
