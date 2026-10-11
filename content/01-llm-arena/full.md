# 01 Prompt Arena - Full video (~8 min)

## Titles (pick one)
1. Prompting Styles Fight: Which One Does an AI Judge Prefer? (Elo Leaderboard)
2. I Made GPT Fight Itself: Concise vs Expert vs Pirate (Judge + Elo)
3. How to Compare Prompts With an LLM Judge (and Why It Misleads)

**Thumbnail text (<=4 words):** PIRATE VS EXPERT

**Tags:** prompt engineering, llm as a judge, elo rating, gpt-4o, azure openai, streamlit, python, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Each battle is four small calls to GPT-4o on Azure (two answers, two judge calls). Which prompting style would you enter?

**Description:**
Two prompting styles of the same model answer the same question, a judge picks the better answer, and an Elo leaderboard keeps score. I built it with Claude Code and the narration is AI-generated. The app is one file.

Recording note: two fights played live, starting from an empty leaderboard (four small calls per battle, 20 calls in all). Fight 1, Concise vs Expert, three battles: reverse a string (identical answers, draw), is 91 prime (Concise won; 21 words against 50), summarise a neural network (Concise won; 40 words against 52). Result: Concise 1030.5, Expert 969.5. Fight 2, Pirate vs Step-by-step, two battles: why is the sky blue (Step-by-step won) and reverse a string (Step-by-step won). Result: Step-by-step 1030.5, Pirate 969.5. The prompts are drawn at random by the app. The two fights never involved the same pair, so ratings from different fights are not comparable. The judge's instructions ask for the answer that is most correct, clear and concise, so it favours short answers by design.

## Voice-over

### [0:00] Cold open
[SCREEN: a battle.] The same question, answered in two different prompting styles. On the left: concise. On the right: expert. Same model, same question; only the system prompt differs. [SCREEN] A judge decides which answer is better, twice, with the order swapped, and an Elo rating keeps score, like in chess. I built this with Claude Code, and the narration is AI-generated.

### [0:50] The idea
When people argue about prompts, they usually argue about taste: be concise, think step by step, explain it like I'm five. This app turns that into a tournament. Each fighter is not a different model but a different instruction to the same model. Five styles are available: concise, step by step, ELI5, pirate and expert.

The scoring is also not a human's opinion. A second call to the same model acts as the judge. That's convenient, and it's also a trap, which I'll come back to.

### [1:50] A battle in code
Each battle is four small calls.

```python
def battle(model_a, model_b, judge_model, prompt):
    ans_a, ta = llm.chat([{"role": "system", "content": STYLES[model_a]}, {"role": "user", "content": prompt}], max_tokens=90)
    ans_b, tb = llm.chat([{"role": "system", "content": STYLES[model_b]}, {"role": "user", "content": prompt}], max_tokens=90)
    # Judge twice with swapped positions to cancel position bias; disagreement = tie.
    v1 = judge(judge_model, prompt, ans_a, ans_b)
    v2 = judge(judge_model, prompt, ans_b, ans_a)
    a_pts = (v1 == 1) + (v2 == 2)
    b_pts = (v1 == 2) + (v2 == 1)
    score_a = 1.0 if a_pts > b_pts else 0.0 if b_pts > a_pts else 0.5
```

The two answers come from the same question with two different system prompts, each limited to ninety tokens. Then the judge is called twice. Language-model judges tend to prefer whichever answer comes first, so the second call swaps the order. If the judge picks the same fighter both times, that fighter wins the battle. If its choice flips with the order, the battle is a draw.

```python
msg = [{"role": "system", "content": "You are a strict impartial judge. Reply ONLY with JSON: "
        '{"winner": 1} or {"winner": 2} or {"winner": 0} for a tie.'},
       {"role": "user", "content": f"Question: {prompt}\n\n[Answer 1]\n{ans_1}\n\n[Answer 2]\n{ans_2}\n\n"
        "Which answer is more correct, clear and concise?"}]
```

The judge sees only the question and the two answers, not which style wrote them. It must reply with a tiny JSON object. Notice the last line: the judge is asked for the answer that is more correct, clear and concise. So conciseness is part of the rules from the start.

### [3:50] Elo
```python
def update_elo(elo, a, b, score_a):
    ra, rb = elo.get(a, 1000.0), elo.get(b, 1000.0)
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    elo[a] = ra + K * (score_a - ea)
    elo[b] = rb + K * ((1 - score_a) - (1 - ea))
```

Everyone starts at one thousand. Before a battle the formula computes how likely each side was to win, based on the rating gap. After the battle, each rating moves by thirty-two times the difference between the actual result and that expectation. Beating an equal is worth sixteen points. A draw between equals changes nothing. An upset moves the ratings further.

### [4:40] Fight one: concise against expert
[SCREEN: setup.] Fighter A is concise, fighter B is expert, three battles, starting from an empty leaderboard.

[SCREEN] I press Fight. Each battle takes a few seconds.

[SCREEN] Three results. The leaderboard is still empty, but the rows are in.

[SCREEN] Battle one: write a one-line Python function that reverses a string. Both fighters give the same code, a lambda with a slice, so the judge can't separate them and it's a draw. Concise and expert are the same here.

[SCREEN] Battle two: is ninety-one prime? Concise answers in twenty-one words: not prime, seven times thirteen. Expert gives fifty words, with a definition of a prime number first. Both are correct, and the judge picks concise.

[SCREEN] Battle three: summarise a neural network in two sentences. Both do, but the expert version is longer, fifty-two words against forty, with more technical terms. Concise wins again.

[SCREEN] Final ratings: concise one thousand and thirty and a half, expert nine hundred and sixty-nine and a half. A draw and two wins.

### [6:30] Fight two: pirate against step-by-step
[SCREEN: setup.] Second fight: pirate against step-by-step, two battles.

[SCREEN] Press Fight again.

[SCREEN] Two results.

[SCREEN] Battle one: why is the sky blue, in under fifty words. The pirate says: arrr, matey, the sky be blue because of sunlight scatterin', and ends with: science be magic. Step-by-step gives a clean explanation with the word Rayleigh scattering. Step-by-step wins.

[SCREEN] Battle two: the string-reversing function again. The pirate's answer wraps the code in pirate talk, and step-by-step adds a sentence explaining the slice. Step-by-step wins again.

[SCREEN] The leaderboard now shows four bars. Step-by-step at one thousand thirty and a half, pirate at nine hundred sixty-nine and a half.

### [8:10] What I noticed
In every battle that wasn't a draw, the shorter or cleaner answer won, even when both were correct. That's not surprising once you've read the judge prompt: it asks for correct, clear and concise. So what this arena measures is not which style is best, but which style this judge, with this instruction, likes. If I changed the judge's last line to ask for the most detailed answer, the ranking could flip.

The other thing is the draw. The first battle shows that when the question is simple, the styles collapse into the same answer.

### [8:50] Honest limits
Five battles is far too few to rank anything: the ratings are one sample each, and the prompts are drawn at random, so another run gives different questions. The two fights never put the same pair together, so concise at one thousand thirty and a half and step-by-step at one thousand thirty and a half were never compared, and the numbers on the shared leaderboard are not comparable across fights. The same model answers and judges, so it may favour its own style. The ninety token limit can also cut a long answer off, and I haven't checked whether it did here. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:40] What to build next
Next I'd run every pair against each other, use a different model as the judge, let you edit the judge's instruction, and add a human vote next to the AI's.

The code is in the description, with no key needed beyond your own Azure setup. If you enjoyed this, follow for more AI and ML builds, and tell me which style should enter next.
