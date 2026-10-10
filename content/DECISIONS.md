# Decisions

## 2026-10-10 Video pipeline spike (passed)
- **Voice:** `edge-tts` (pip), voice `en-US-AndrewNeural`; works online, much better than Windows SAPI (David/Zira are the fallback). Description discloses AI narration.
- **Footage:** Playwright + Chromium `record_video` (webm), viewport 540x960 for shorts, 1920x1080 for full. Open apps with `?embed=true` to hide the Deploy toolbar. Note: on this machine Python's `/tmp` is `D:\tmp`.
- **Avatar:** Pillow circular crop of photo (face is in top ~40%), added as PiP via ffmpeg overlay.
- **Docker/Ollama:** not needed; all non-LLM apps are free, so LLM-app recordings use a handful of Azure calls.
- Sample images for project 16 are Wikimedia Commons (500px thumbnails; fetch needs a User-Agent).
- SARSA/Q-learning numbers: the 28.6 vs 11.0 caption was a single noisy run; scripts use 10-seed averages (~27 vs ~2). Tiny GPT measured ~4 steps/s.
- 2026-10-10 user feedback: NO avatar overlay on shorts (looked bad); captions go in the lower third. Avatar dropped for full videos too unless asked.
- 2026-10-10 user feedback on shorts: voice good, small voice corrections to match the screen; add a catchy intro + follow call. Channel name chosen: **Watch It Learn** (check handle availability: ideas @watchitlearn.ai / @watchitlearn). Intro style: 1.5s branded title card (spoken "Watch It Learn") + end card "Follow for daily AI builds". Originals (`out/short.mp4`) are KEPT; new renders are `out/short_v2.mp4`.
