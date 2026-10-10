# 08 AI 20 Questions - 30s Short (9:16)

**Title (<60):** Can GPT read my mind in 20 questions?
**Description:** Think of anything. GPT asks yes/no questions to guess it, or you guess its secret. Built with Claude Code in Streamlit. Narration is AI-generated. Code: rnd-projects-aiml, project 08.
**Hashtags:** #AI #GPT #20Questions #Streamlit #ClaudeCode

## Voice-over (~75 words)
(0-3s) Can an AI read your mind in twenty questions?
(3-11s) I built this with Claude Code. I switch the sidebar to "GPT guesses your secret", think of something, and just answer Yes, No or Sometimes.
(11-19s) Watch the progress bar count down. Each question tries to split the possibilities in half, like a binary search.
(19-27s) When it's sure, it makes a guess and I press Correct or Nope. The other mode flips it: you grill GPT about its secret.
(27-30s) Follow for more AI/ML builds.

## Timeline and on-screen text
| Time | On screen text | Action to record |
|---|---|---|
| 0-3s | "Think of anything." | App title "AI 20 Questions", sidebar "Who guesses?" visible |
| 3-11s | "Answer: Yes / No / Sometimes" | Sidebar radio -> "GPT guesses your secret". Click "▶ Start game". GPT's first question appears; click "Yes" |
| 11-19s | "20 -> 0 questions left" | Click "No" / "Sometimes" on 2-3 more questions; show the progress bar text "N questions left" falling |
| 19-27s | "It makes a guess" | When GPT shows a guess, click "✅ Correct!" (success message "GPT read your mind in N questions 🧠") or "❌ Nope" |
| 27-30s | "Follow for more AI/ML builds" | End card |

Notes: think of a fixed object beforehand (e.g. "umbrella") so answers are quick. Keep to ~6-8 Azure calls total. Do not state the result before recording; narrate what actually happens (if GPT fails, change line 3 to "...and this time it lost").
