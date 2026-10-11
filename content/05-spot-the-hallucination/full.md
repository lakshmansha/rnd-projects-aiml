# 05 Spot the Hallucination - Full video (~7 min)

## Titles (pick one)
1. Can You Spot the AI's Lie? 5 Facts, 1 Hallucination (I Got Fooled)
2. GPT Mixes One Fake Fact Into Four True Ones: Play Along
3. Why AI Hallucinations Are So Hard to Spot (Live Game)

**Thumbnail text (<=4 words):** FOOLED BY GPT

**Tags:** ai hallucination, llm, gpt-4o, azure openai, streamlit, python, prompt engineering, fact checking, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The game calls GPT-4o through Azure (one small call per round). Which of the four rounds fooled you? Round 2 got me.

**Description:**
GPT writes five statements, four true and one subtly false, and you have to find the hallucination. I built it with Claude Code and the narration is AI-generated. The app is one file and uses one small LLM call per round.

Recording note: four rounds played live (four LLM calls in total), topics Space, Programming, Human body and Geography. The picks were mine, made by reading the statements and using what I already knew; I did not look anything up. Result: 3 of 4 found. The Space fake (Venus rotates faster than Earth, in 243 days), the Human-body fake (every cell replaced every 7 years) and the Geography fake (Russia spans three continents) were caught. In the Programming round I picked the Ruby statement and the fake was the one about time.sleep() precision. That "truth" the app displayed is itself shaky, because Python's time.sleep() accepts fractional seconds. The app has no fact-checking: GPT writes both the fake and the correction.

## Voice-over

### [0:00] Cold open
[SCREEN: round one.] Five statements about space. Four are true, and one is a hallucination, made up by GPT and written to sound just as confident as the rest. Which one is fake? Take a moment and read them. I'll tell you which one I picked, and whether I was right. I built this game with Claude Code, and the narration is AI-generated.

### [0:40] Why a game
Language models state false things in exactly the same tone as true things. There is no warning light. That is the real danger of a hallucination: it doesn't look any different.

So instead of explaining it, I wanted you to feel it. GPT is asked to produce five short statements on a topic, four true and one subtly false: plausible, with a wrong number, name or cause. You choose the one you think is fake, and the app reveals the answer and a correction.

### [1:50] How it works
The whole game is one prompt.

```python
text, _ = llm.chat(
    [{"role": "system", "content": 'Reply ONLY with JSON: {"statements": [5 short strings], "fake_index": 0-4, '
      '"truth": "one-sentence correction of the fake one"}. Exactly 4 statements must be true; 1 must be '
      "subtly but definitely false (plausible-sounding, with a wrong number, name or cause)."},
     {"role": "user", "content": f"Topic: {topic}. Surprising but well-established facts. Random seed: {id(object())}"}],
    temperature=1.0, max_tokens=350, json_mode=True)
```

The system prompt asks for a strict JSON object: five statements, the position of the fake one, and a one-sentence correction. JSON mode makes the model return something the app can parse. The temperature is high, one, so every round is different, and I add a random number to the prompt so the same topic doesn't repeat. Each round is one small call, capped at three hundred and fifty tokens.

And this is the part that matters for later: GPT writes the fake, GPT chooses which one is fake, and GPT writes the correction. Nothing in the app checks any of it.

```python
choice = st.radio("Which one is the hallucination?", range(5), format_func=lambda i: r["statements"][i],
                  index=None, disabled=ss.answered)
if choice is not None and not ss.answered:
    ss.answered, ss.hit = True, choice == r["fake_index"]
    ss.rounds += 1
    ss.score += int(ss.hit)
```

The rest is a radio button. You click, the app compares your choice to the fake index, and updates the score.

### [3:30] Round one: space
[SCREEN: round one.] The statements. The Sun contains more than ninety-nine point eight percent of the mass of the solar system. Titan has a dense atmosphere of nitrogen and methane. The Great Red Spot on Jupiter is a storm that has lasted over three hundred and fifty years. Pluto was reclassified as a dwarf planet in two thousand six. And Venus rotates faster than Earth, completing a rotation every two hundred and forty-three Earth days.

The last one contradicts itself. Two hundred and forty-three days for one rotation is much slower than Earth's one day, not faster. I pick that one.

[SCREEN] Caught it. The correction says Venus rotates slower than Earth. This one was easy, because the statement fights itself.

### [4:30] Round two: programming
[SCREEN: round two.] I switch the topic to programming. Python's sleep function halts execution at millisecond precision. JavaScript's triple equals is a type-safe comparison. Git was created by Linus Torvalds for the Linux kernel. Fortran, the first high-level language, appeared in nineteen fifty-seven. And Ruby was designed to run exclusively on Unix-based systems.

Ruby sounds the most suspicious to me, since I know it runs on Windows today, but the statement says originally. So I pick Ruby.

[SCREEN] Fooled. The fake was the sleep statement. The correction says Python's sleep works at second precision by default, not millisecond. And this is where it gets interesting, because that correction is shaky too. Python's time dot sleep accepts a floating point number of seconds, so you can sleep for fractions of a second. The app showed me a fake, and a correction that is also not quite right. That's the thing I mentioned: GPT wrote both, and nothing checks them.

### [6:00] Rounds three and four
[SCREEN: round three.] Human body. The brain has about eighty-six billion neurons. Ears never stop growing. The heart beats around a hundred thousand times a day. Every single cell in your body is replaced every seven years. And humans have over six hundred lymph nodes. The seven-year claim is a famous myth, and I pick it.

[SCREEN] Correct. Not every cell is replaced; some neurons last a lifetime.

[SCREEN: round four.] Geography. The Amazon discharges more water than the next seven rivers combined. Lake Superior is the largest freshwater lake by area. Mount Everest grows about four millimetres a year. The Sahara covers over nine million square kilometres. And Russia spans three continents: Europe, Asia and North America. That last one is wrong, Russia spans two.

[SCREEN] Correct again.

### [7:20] The score
[SCREEN: the sidebar.] The sidebar says three out of four. But look at how I got there: two of my three hits were statements that contradicted themselves or repeated a famous myth, and the round I lost was the one where the fake was a small, technical detail that sounded fine. The better the lie, the closer it is to a fact you half remember.

### [7:50] What surprised me
That the game is hard for the reason I expected, and also for a reason I didn't. The expected one: a plausible detail is nearly impossible to spot without checking. The surprise: the app's own answer key can be wrong. A fake and its correction both come from the same model. So the lesson isn't only that GPT hallucinates. It's that asking GPT to check GPT doesn't fix it.

### [8:30] Honest limits
Four rounds is a tiny sample, so my three out of four tells you nothing about how hard the game is in general. I used my own knowledge and didn't look anything up, and I'm not a typical player. The statements, the fake, and the correction all come from one model, with no fact-checking, so the app can be wrong about what's true. Some rounds may contain a statement that is also false by accident. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:10] What to build next
Next I'd add a second step that checks each answer against a source, a difficulty setting, and a leaderboard so you can compare your score with other people.

The code is in the description. It costs one small LLM call per round. If you were fooled by round two like I was, follow for more AI and ML builds, and tell me which statement got you.
