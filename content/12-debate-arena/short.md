# Short: AI Debate Arena (30s, 9:16)

**Title:** I made two AIs debate pineapple on pizza
**Hashtags:** #AI #GPT4o #Debate #Streamlit #BuiltWithClaude

## Voice-over (~75 words, first person)
[0-3s HOOK] "Two AIs argue about pineapple on pizza. A third one judges."

[Beat 1, ~8s] "I built this with Claude Code. Before the debate, I rate how much I agree. Then a pro bot and a con bot trade short, punchy arguments."

[Beat 2, ~8s] "Then the judge scores both on logic, evidence, persuasion, clarity and rebuttal, and a radar chart shows the winner."

[Beat 3, ~8s] "The real test: I rate my opinion again. Did the bots move me? The app shows my shift in points."

[CTA, 3s] "Follow for more AI and ML builds."

## On-screen text
- 0-3s: "AI vs AI: pineapple on pizza"
- Beat 1: "Pro vs Con, 60 words max"
- Beat 2: "Judge scores 5 criteria"
- Beat 3: "Did they change YOUR mind?"
- CTA: "Follow for more AI/ML builds"

## Recording actions (real app controls, port 8512; calls Azure GPT-4o, 2 rounds = 5 small calls, record one take)
1. "Motion" dropdown = "Pineapple belongs on pizza." Set the "Before the debate" slider (e.g. 4).
2. "Rounds" slider = 2. Click "🔥 Start debate" (spinners "Round 1: Pro is thinking...").
3. Scroll the green (Pro) and red (Con) chat bubbles as they appear.
4. "⚖️ Verdict": radar chart, **Winner**, **Pro total**, **Con total**, and the judge's one-sentence reason.
5. Move the "After the debate" slider; the **Your shift** metric shows e.g. "+2 points".

## Fact notes
- Calls per debate = 2 x rounds + 1 (app caption). Debater replies are capped at 60 words (prompt) and the judge runs at temperature 0. Scores vary per run: read them off the screen; do not pre-script numbers.

## Description
Two GPT debaters argue a motion, a GPT judge scores them on logic, evidence, persuasion, clarity and rebuttal with a radar chart, and the app measures whether the debate changed your mind. Built with Claude Code (Python, Streamlit, Azure OpenAI). Narration is AI-generated.
