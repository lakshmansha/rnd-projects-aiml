# Decisions

## 2026-10-10 Video pipeline spike (passed)
- **Voice:** `edge-tts` (pip), voice `en-US-AndrewNeural`; works online, much better than Windows SAPI (David/Zira are the fallback). Description discloses AI narration.
- **Footage:** Playwright + Chromium `record_video` (webm), viewport 540x960 for shorts, 1920x1080 for full. Open apps with `?embed=true` to hide the Deploy toolbar. Note: on this machine Python's `/tmp` is `D:\tmp`.
- **Avatar:** Pillow circular crop of photo (face is in top ~40%), added as PiP via ffmpeg overlay.
- **Docker/Ollama:** not needed; all non-LLM apps are free, so LLM-app recordings use a handful of Azure calls.
- Sample images for project 16 are Wikimedia Commons (500px thumbnails; fetch needs a User-Agent).
