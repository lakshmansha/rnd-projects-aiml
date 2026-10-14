# Handoff for the next session (written 2026-10-15)

Start here. Older history is in `HANDOFF.md` (sessions 1 to 5), `content/PROGRESS.md`, `content/FULL_VIDEOS.md`.

## 1. Where things stand

**Project:** 18 small AI/ML Streamlit demos for the **Watch It Learn** channel (repo `D:\Research\Source\rnd-projects-aiml`, public at https://github.com/lakshmansha/rnd-projects-aiml, MIT, topics and README done, `origin/main` is up to date). Each project has a short (`content/<NN>-*/out/short_v2.mp4`, 1080x1920) and a long video (`content/<NN>-*/out/full.mp4`, 1920x1080, AI voice). Videos are git-ignored; scripts, SRTs, chapters, thumbnails are committed.

**YouTube (done, scheduled).** Channel: https://www.youtube.com/@watchitlearn (channel id `UCDaF27zZ2ExcyyHRtr1uDxA`). All 18 shorts and all 18 long videos are uploaded with titles, descriptions, tags (long videos), custom thumbnails (long videos), "not made for kids" and the AI-content label. Every item is **Scheduled to go public at 7:00 PM IST, one project per day, short and long video together**:

| Date (2026) | # | Project | Date | # | Project |
|---|---|---|---|---|---|
| Oct 15 | 06 | digit-classifier | Oct 25 | 13 | clustering-lab |
| Oct 16 | 09 | rl-gridworld | Oct 26 | 14 | explainable-text-ai |
| Oct 17 | 07 | tiny-gpt | Oct 27 | 05 | spot-the-hallucination |
| Oct 18 | 10 | evolving-rockets | Oct 28 | 15 | prompt-gym |
| Oct 19 | 02 | prompt-injection-lab | Oct 29 | 12 | debate-arena |
| Oct 20 | 16 | cnn-xray | Oct 30 | 01 | llm-arena |
| Oct 21 | 17 | flappy-evolution | Oct 31 | 03 | semantic-map |
| Oct 22 | 18 | attention-xray | Nov 1 | 08 | twenty-questions |
| Oct 23 | 04 | neural-playground | | | |
| Oct 24 | 11 | token-xray | | | |

Each short's description links to its long video. Scheduling is server-side, so the PC does not need to be on. The long videos are private until their slot (YouTube turns an unlisted video into "private before publishing" when scheduled).

**Instagram (@watchitlearn), not scheduled yet.** The account exists, is Professional, logged in on the user's Chrome, and linked in Meta Business Suite. The bio says "YouTube: youtube.com/@watchitlearn" (plain text). Everything needed to post is in `content/_instagram/`: 18 numbered `.mp4` files (`01_2026-10-15_06-digit-classifier.mp4` ...), a matching `.txt` caption, and a `_cover.jpg` (1080x1920) per Reel. `content/INSTAGRAM_QUEUE.md` has the same list with captions.

## 2. Open items, in priority order

1. **Instagram Reels (user task, time critical).** Schedule all 18 at 7:00 PM IST on the date in each filename, tick the AI label, paste the caption. Reel 01 must be scheduled before 7 PM on Oct 15. Use Meta Business Suite (Create Reel, Add video, Share step, Schedule) or the Instagram app (Reel, Advanced settings, Schedule). Why not automated: Instagram web has **no schedule option** (Share posts immediately), and Business Suite's "Add video" opens a native file picker that the browser tool cannot reach.
2. **Clickable bio link (user task, phone only).** Instagram app, Edit profile, Links, add `https://www.youtube.com/@watchitlearn`. Instagram web cannot edit links.
3. **Pinned comments on YouTube.** Not posted. Text is in `content/PUBLISH_SHEET.md` (long videos) and "Which project should I build next? The full walkthrough is linked in the description." for shorts. Post and pin after each video is public.
4. **Verify the first live day.** On Oct 15 evening confirm the first short and long video (#06) actually went public and the link inside the short works. Check Studio's Content list for any item stuck in "Scheduled" after its time or flagged by a copyright or policy check.
5. **Instagram caption links.** Captions say "Full video on YouTube (link in bio)". Once the clickable bio link exists this is accurate.
6. Optional: `requirements.txt` says torch is "only project 07", but 16 and 18 use it too; the `README` quick start already says so correctly.
7. Optional next content: new projects from `content/ideas.md` (30 ideas), the weekly batch routine in `content/ROUTINE_PLAN.md`, and a Task Scheduler job (needs the user's OK).

## 3. Files that matter

- `content/PUBLISH_SHEET.md`: paste-ready YouTube text (titles, descriptions, tags, pinned comments) for all 18 long videos and 18 shorts. Regenerate with `python tools/publish_sheet.py [--links content/links.json --out PUBLISH_SHEET_LINKED.md]`.
- `content/links.json` and `content/PUBLISH_SHEET_LINKED.md`: the real unlisted YouTube URLs; **git-ignored on purpose**, they exist only on the user's PC. Do not commit them while any video is unlisted.
- `content/_thumbs/NN.jpg`: 1280x720 long-video thumbnails (`python tools/make_thumbs.py [NN]`).
- `content/_instagram/`: Reel files, captions, covers (git-ignored mp4/jpg copies of the shorts).
- `tools/make_full.py <NN>`: builds a long video from `content/<NN>-*/full.md` + `video.py` (helpers added in session 4: `CROPS`, `TRIM`, `--record-as TAG`).
- `HANDOFF.md`, `content/FULL_VIDEOS.md`: pipeline details and honesty notes per video.

## 4. How the publishing was done (reusable, and its traps)

- The user bulk-uploaded the 17 long videos by hand (the Chrome upload tool caps files at about 10 MB; those are 10 to 20 MB). Everything else was done by driving YouTube Studio in the user's logged-in Chrome (`mcp__claude-in-chrome__*`). Shorts (3 to 7 MB) were uploaded through the tool with `file_upload`.
- Pattern that worked: a tiny local HTTP server served each video's title/description/tags as JSON (CORS on) so page JavaScript could `fetch` them and fill the Studio fields with `document.execCommand('insertText')`. Selectors: title `#title-textarea #textbox`, description `#description-textarea #textbox`, kids radio `[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]`, AI label `[name=VIDEO_HAS_ALTERED_CONTENT_YES]`, tags `#tags-container input` (end with a comma), schedule date `#datepicker-trigger`, time input `ytcp-datetime-picker input`. The visibility editor on an existing video opens via `[aria-label="Edit video visibility status"]`.
- Traps hit: (a) the extension disconnects now and then mid-batch; re-check the page state before repeating; (b) fixed click coordinates drift when the dialog shows a "processing" banner, so I used JS to focus the date and time fields; one short (#07) was first scheduled at 12:00 AM and fixed; (c) file names must be unique when bulk-uploading (they were all `full.mp4`, hence `content/_upload/NN-name.mp4`); (d) Python `write_text` on Windows rewrites `\n` as `\r\n`: pass `newline="\n"` (a bad commit was fixed in `2874d92`); (e) `git commit` messages must end with the two attribution lines from the session reminder.
- Time zone in Studio is the browser's local zone (GMT+05:30). All times are 7:00 PM there.

## 5. Decisions and rules to keep

- Never publish, post or upload without the user's explicit approval for that action; scheduling and posting were each approved explicitly. Do not click OAuth consent screens (for example "Continue with Instagram" on Business Suite) without asking.
- Keep Azure OpenAI use tiny (the `.env` key is never printed or committed; checked in git history before the repo was made public).
- Videos must say narration is AI-generated, and scripts report real recorded numbers with honest limits.
- A duplicate draft "18 attention xray" existed; the user deleted it.
- Local-only state: unlisted links, `.env`, the personal photo (`photo/`), generated videos.

## 6. Quick commands

```
git pull / git log --oneline | head          # repo is clean and pushed (origin/main)
python run_all.py                            # all apps on ports 8501-8518, hub on 8500
python tools/make_full.py <NN> [--record]    # rebuild a long video
python tools/publish_sheet.py                # regenerate the publish sheet
python tools/make_thumbs.py [NN]             # regenerate thumbnails
```
