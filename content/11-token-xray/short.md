# Short: Token X-ray (30s, 9:16)

**Title:** What ChatGPT actually reads (it isn't letters)
**Hashtags:** #LLM #Tokenization #ChatGPT #AI #BuiltWithClaude

## Voice-over (~75 words, first person)
[0-3s HOOK] "ChatGPT can't see letters. Here's what it reads instead."

[Beat 1, ~8s] "I built this X-ray with Claude Code. Type any text and it splits into colored chips, each one a token."

[Beat 2, ~8s] "Now the surprise. The same greeting in Hindi, Japanese, Arabic and Russian takes twenty-one tokens on the newer GPT-4o vocabulary, and forty-one on the older one."

[Beat 3, ~8s] "The insight: models work on chunks, not letters, which is why counting letters is hard, and why some languages cost more."

[CTA, 3s] "Follow for more AI and ML builds."

## On-screen text
- 0-3s: "LLMs don't read letters"
- Beat 1: "Every chip = 1 token"
- Beat 2: "63 characters: 21 tokens vs 41 tokens"
- Beat 3: "Chunks, not letters"
- CTA: "Follow for more AI/ML builds"

## Recording actions (real app controls, port 8511)
1. App opens with the "🍓 Strawberry" text, "How many r's are in strawberry?". Show the colored chips on the "o200k_base · GPT-4o family" tab (8 tokens, 31 characters).
2. Click the "🌍 Other languages" example button. Chips multiply.
3. Read the **Tokens** metric: 21 on o200k_base. Click the "cl100k_base · GPT-4 / GPT-3.5" tab: 41.
4. Scroll to "What this means": the "Same text, different vocabulary" bar chart (21 vs 41) and the cost bullet.
5. Optional: click "🔢 Numbers" to show digits chopped into short pieces.

## Fact notes (verified headlessly with tiktoken)
- Strawberry sentence: 8 tokens in both vocabularies; " strawberry" is a single token in both, so the model never sees its letters. (The app text says "a few chunks"; narrate it as one chunk.)
- Multilingual example: 63 characters; 21 tokens (o200k_base) vs 41 (cl100k_base).
- Numbers example: 57 characters, 21 tokens in both.

## Description
Token X-ray shows text the way an LLM sees it: colored token chips, token counts, cost, and two GPT vocabularies side by side. Why letter-counting is hard and why some languages cost more. Built with Claude Code (Python, tiktoken, Streamlit), no API calls. Narration is AI-generated.
