# 15 Prompt Gym - Full video (~8 min)

## Titles (pick one)
1. I Tried a Prompt Engineering Gym: 6 Levels, Python Checks Your Prompt
2. Why "Say banana" Fails: Prompt Engineering Levels With Auto-Grading
3. 6 Prompt Challenges GPT Fails at First (And How I Fixed Each)

**Thumbnail text (<=4 words):** SAY BANANA. FAIL.

**Tags:** prompt engineering, gpt-4o, azure openai, llm, structured output, json, python, streamlit, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Every attempt is one small call to GPT-4o on Azure at temperature 0, and Python (not an AI) checks the answer. Which level would you add?

**Description:**
A gym for prompt writing: six levels with strict, automatically checked requirements. I built it with Claude Code and the narration is AI-generated. The app is one file and uses one small LLM call per attempt.

Recording note: I played all six levels live and cleared them in 10 attempts: Level 1 (one word) took 2, Level 2 (sentiment) 2, Level 3 (JSON) 2, Level 4 (exactly 10 words) 1, Level 5 (3 short bullets) 2, Level 6 (Spanish with exclamation marks) 1. The stars add up to 14 of 18. The video footage is a second, identical run of the same ten prompts so that the verdicts stay in frame; the pass or fail result was the same for every attempt, although the exact wording of a failed answer can differ slightly between runs. This is one person's prompts on one model, not a benchmark.

## Voice-over

### [0:00] Cold open
[SCREEN: level one.] The goal: make the model reply with the single word banana. Lowercase, no punctuation, nothing else. I type the obvious prompt: say banana. [SCREEN] And the model replies: capital B, banana, exclamation mark, and a banana emoji. A person would call that a pass. A program would not. In this video I go through six levels like that, where Python, not a human, decides whether the answer is acceptable. I built this with Claude Code, and the narration is AI-generated.

### [0:50] Why a gym
Writing a prompt feels like writing a message to a person, but when the output feeds into other code, the rules change. A parser needs valid JSON. A form field needs one word. A layout needs exactly three lines. And then good enough is not good enough.

So this app turns prompt writing into something you can practise and score. Each level has a goal, a piece of input text that's added to your prompt automatically, and a checker written in Python. You write a prompt, GPT answers at temperature zero, so the answers are as repeatable as it gets, and the checker says pass or fail. You get stars: three for passing on the first try, two for up to three tries, and one after that.

### [2:00] How the checking works
Each level has a small checking function. Here is the one for the JSON level.

```python
def chk_json(out):
    d = j(out)
    ok = sorted(d) == ["city", "date", "person"] and {p.lower() for p in d["person"]} == {"priya", "tom"} \
        and d["city"].lower() == "paris" and "5" in str(d["date"]) and "may" in str(d["date"]).lower()
    return ok, "Need exactly keys person (list: Priya, Tom), city, date (5 May)." if not ok else "Valid and correct."
```

It parses the output as JSON, then checks the exact keys, the exact people, the city and the date. If the text isn't valid JSON, the parser fails, and the attempt fails.

```python
user = prompt + (f"\n\nINPUT:\n{lv['data']}" if lv["data"] else "")
out, _ = llm.chat([{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user}],
                  temperature=0, max_tokens=120)
ok, note = lv["check"](out)
```

When you press Run, your prompt and the level's input go to the model with a generic system message. The output goes straight to the level's checker. Nothing in between helps you. And the answer is capped at a hundred and twenty tokens, which matters for the later levels.

### [3:30] Level one: one word
[SCREEN: level one.] The goal is the single word banana.

[SCREEN] My first prompt was: say banana.

[SCREEN] The model said: Banana, exclamation mark, banana emoji. Not yet. The checker shows exactly what it received.

[SCREEN] So I get strict. Reply with exactly one word, banana. Lowercase only, no punctuation, no emoji, nothing else.

[SCREEN] That passes on the second try. Two stars. Every constraint I add maps to one thing the first answer got wrong: the capital letter, the exclamation mark and the emoji.

### [4:40] Level two: sentiment
[SCREEN: level two.] Classify a review as positive, negative or mixed, and reply with one lowercase word. The review loves the movie but hates the popcorn and the seats.

[SCREEN] My first prompt: what is the sentiment of this review?

[SCREEN] The model got it right. It said the sentiment is mixed, and then explained why. And the checker still says no, because I asked for a single word and got a paragraph. Right answer, wrong format.

[SCREEN] Second try: classify the sentiment as positive, negative or mixed, and answer with only that one lowercase word.

[SCREEN] Passed. The fix was to list the allowed labels and to say only.

### [5:40] Level three: strict JSON
[SCREEN: level three.] Extract a person list, a city and a date from a sentence, as valid JSON with no markdown fences.

[SCREEN] My first prompt asked for JSON with keys person, city and date.

[SCREEN] The JSON is correct, but it's wrapped in markdown code fences, three backticks and the word json. Humans like that. A parser doesn't, and the checker tells me to remove the fences.

[SCREEN] Second prompt: return only valid JSON, say that person is a list, and don't use code fences or commentary.

[SCREEN] Passed. Notice that I never had to tell the model what the right answer was; I only had to describe the shape of the output.

### [6:40] Level four: exactly ten words
[SCREEN: level four.] Summarise a sentence about a bicycle path in exactly ten words.

[SCREEN] My prompt was: summarise the text in exactly ten words.

[SCREEN] The model wrote: City council approves river bike path to reduce traffic, pollution. That is ten words, and the level passes on the first try. I want to be careful here: language models are known to be unreliable at counting, and one lucky pass doesn't show that this prompt works in general.

### [7:30] Level five: three short bullets
[SCREEN: level five.] Three bullets, each at most six words, with no intro and no outro. The topic is why sleep matters for students.

[SCREEN] My first prompt: write three short bullet points about the topic below.

[SCREEN] The model gave three bullets, but each was a full sentence with a bold heading, much longer than six words. The checker counts words per line, so that fails.

[SCREEN] Second prompt: exactly three markdown bullets starting with a dash, each at most six words, no introduction and no closing line.

[SCREEN] Passed. The word short in my first prompt meant something to me, but not to the checker. The fix was to give a number.

### [8:30] Level six: Spanish with exclamation marks
[SCREEN: level six.] Translate a greeting into Spanish, and end every sentence with an exclamation mark.

[SCREEN] My prompt: translate the text into Spanish and end every sentence with an exclamation mark.

[SCREEN] The model gave: Buenos días, and then, I would like a coffee please, with Spanish exclamation marks around both sentences. It passed on the first try, three stars.

### [9:10] The scoreboard
[SCREEN: the sidebar.] All six levels cleared, in ten attempts. Fourteen stars out of eighteen. Four levels needed a second try, and in each case the first failure told me exactly what to add.

### [9:40] What I learned
The pattern was the same each time. A short, natural prompt gets a helpful, human answer, with a friendly extra bit. And the checker wants the machine answer. The fix was never a clever trick. It was to name the format, the allowed values, the limits, and what to leave out. Failures were also my best feedback: the checker prints what it received, so each failed attempt tells you what to change.

### [10:15] Honest limits
This is one person's prompts, on one model, once. A different model, or even a different day, could pass the first try on levels where I failed, or the other way round. Level four passed on the first try, which tells us little about counting. The checkers are my own, and they accept some answers a human would reject and the other way round. For example, the Spanish check looks for the word buen and exclamation marks, nothing deeper. The model also gets only a hundred and twenty tokens. And the footage in this video is a second, identical run of the same ten prompts, so the verdicts stay on screen; each attempt had the same pass or fail result in both runs. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [11:00] What to build next
Next I'd add levels with few-shot examples, a level where the model has to refuse something, and a leaderboard with the fewest attempts. And I'd run the same prompts against several models to see which ones need fewer constraints.

The code is in the description, with no key needed beyond your own Azure setup. If you want to try a level, follow for more AI and ML builds, and tell me what the next one should be.
