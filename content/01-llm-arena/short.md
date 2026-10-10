# 01 Prompt Arena - 30s Short (9:16)

**Title:** Two AI prompts fight. A judge picks the winner. (<60)
**App:** `01-llm-arena` (Streamlit, "Prompt Arena"). Record with 2 to 3 battles only (4 tiny API calls each).

## Voice-over (~76 words)
**Hook (0-3s):** "Which prompt style wins: pirate, or expert?"

**Beat 1 (3-11s) what you see:** "This is Prompt Arena. Same model, two prompting styles. I pick Fighter A and Fighter B, press Fight, and each style answers the same question."

**Beat 2 (11-19s) the surprise:** "Then a judge scores both answers, twice, with the order swapped, so position bias cancels out. If it disagrees with itself, it's a draw."

**Beat 3 (19-27s) the insight:** "Elo ranks the winners. Starting from a thousand, one win over an equal moves you just sixteen points. Rankings need many battles."

**CTA (27-30s):** "Built with Claude Code, narrated by AI. Follow for more AI/ML builds."

## On-screen text
- 0-3s: "Pirate vs Expert: who wins?"
- 3-11s: "Same model. Different prompt style."
- 11-19s: "Judge runs TWICE, order swapped"
- 19-27s: "Elo: +16 for a win vs an equal"
- 27-30s: "Follow for more AI/ML builds"

## Actions to record (real controls)
1. Sidebar "Setup (prompting styles)": Fighter A = `Pirate`, Fighter B = `Expert` (options: Concise, Step-by-step, ELI5, Pirate, Expert).
2. Slider "Battles to run" = 2. (Leave "Custom prompt (optional)" empty.)
3. Click the "Fight!" button (primary). Let the status boxes show the two columns of answers and the "wins / Draw" label.
4. Scroll to "Leaderboard": the Elo bar chart with rounded Elo labels and the "N battles recorded" caption.
Do not click "Reset leaderboard" on camera unless you want a clean chart first.

## Description
Same LLM, two prompting styles, one judge. Prompt Arena makes both styles answer, asks a judge twice with positions swapped to cancel position bias (disagreement counts as a tie), and tracks results with Elo (K=32, start 1000). Built with Claude Code. Narration is AI-generated.

## Hashtags
#AI #LLM #PromptEngineering #Streamlit #BuildInPublic
