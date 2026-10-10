# Short: 15 Prompt Gym (30 s, 9:16)

**Title:** Can you make GPT write exactly 10 words? (under 60 chars)
**Hashtags:** #PromptEngineering #GPT #LLM #Python #Shorts

## Voice-over (about 75 words)
**[0-3s, hook]** "Can you make GPT reply with exactly ten words? Harder than it sounds."
**[3-11s, what you see]** "It's a prompt gym. Six levels. You write the prompt, GPT answers, and plain Python code checks the result. No vibes, just pass or fail."
**[11-19s, surprising moment]** "Level four: summarise in exactly ten words. A lazy prompt fails, and the checker tells me how many words I really got."
**[19-27s, insight]** "Be specific, state the format, say what not to add. Then it passes."
**[27-30s, CTA]** "Built with Claude Code. Follow for more AI and ML builds."

## On-screen text
- 0-3s: "EXACTLY 10 WORDS?"
- 3-11s: "You prompt. Python grades."
- 11-19s: "Not yet: word count shown" (overlay the real count shown on screen)
- 19-27s: "Specific prompt = pass"
- 27-30s: "Follow for more AI/ML builds"

## Exact actions to record (http://localhost:8515, viewport 540x960; about 2 Azure calls, keep within budget)
1. Sidebar shows "Levels cleared 0 / 6". In the "Level" selectbox choose "Level 4 · Exact length".
2. In "Your prompt" type a lazy prompt (e.g. "Summarise this.") and click "Run". Red box shows "Your output had N words, need 10" (use whatever N appears).
3. Replace it with a strict prompt (e.g. "Summarise the INPUT in exactly 10 words. Output only the summary, no preamble.") and click "Run". If the green "Passed!" box appears, show it and the sidebar tick. If not, record again or show the retry honestly.
4. The stars caption says first try = three stars, up to 3 tries = two, more = one; this will be two stars here.

## Description
Prompt Gym: six levels (single word, sentiment, strict JSON, exact length, format discipline, persona + constraint) where you write the prompt, GPT answers at temperature 0 and Python checkers grade it. Built with Claude Code and Streamlit using Azure OpenAI. Narration is AI-generated.
