# 12 AI Debate Arena - Full video (~8 min)

## Titles (pick one)
1. I Made Two AIs Debate and a Third One Judge (Pineapple on Pizza)
2. AI vs AI Debate: Can an LLM Judge Be Trusted?
3. Tabs vs Spaces, Settled by AI? (Live Debate and Judge)

**Thumbnail text (<=4 words):** AI VS AI DEBATE

**Tags:** llm debate, llm as a judge, gpt-4o, azure openai, prompt engineering, streamlit, python, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Each debate is five small calls to GPT-4o on Azure (four speeches and one judge). Which motion should I put on trial next?

**Description:**
Two GPT debaters argue a motion, a judge scores both on five criteria, and you record whether they changed your mind. I built it with Claude Code and the narration is AI-generated. The app is one file.

Recording note: two real debates, two rounds each (five small LLM calls per debate). Pineapple belongs on pizza: Pro won, 40 to 36; I set my opinion to 4 beforehand and 5 afterwards. Tabs are better than spaces: Con won, 44 to 42; I set 7 beforehand and 6 afterwards. The opinion numbers are mine, as one viewer's reaction, not data. The same model plays all three roles (Pro, Con and judge), so two debates say nothing about whether the judge is fair or biased.

## Voice-over

### [0:00] Cold open
[SCREEN: a debate.] Two debaters, one motion: pineapple belongs on pizza. The green side argues for it, and the red side argues against, each in a few punchy sentences, and each answering the other's last point. [SCREEN] Then a judge scores them on five criteria and picks a winner, and finally the app asks you one question: did that change your mind? I built this with Claude Code, and the narration is AI-generated.

### [0:50] Why a debate
Models are good at producing a case for any side. That's useful, and it is also a little worrying, because the argument sounds confident whether or not it's right. A debate makes that visible: ask for both sides and you see two confident cases for opposite conclusions.

Then there's the second question, which matters more in practice: who judges? Using a language model as a judge is a common way to evaluate other models, so I wanted a small, visible example of what that looks like, with all the scores on screen.

### [1:50] The debaters
Each speech is one small call.

```python
stance = "FOR" if side == "Pro" else "AGAINST"
msgs = [{"role": "system", "content": f"You are a sharp competitive debater arguing {stance} the motion: '{topic}'. "
         "In 2-3 punchy sentences (max 60 words): make your strongest new point and directly rebut the opponent's last point. "
         "No pleasantries, no repeating yourself."},
        {"role": "user", "content": (f"Debate so far:\n{history}\n\n" if history else "") + f"Round {round_no}. Your turn."}]
return llm.chat(msgs, temperature=0.9, max_tokens=110)[0]
```

The system prompt gives the stance, asks for a new point plus a rebuttal of the opponent's last one, and bans pleasantries. The user message carries the debate so far, so each side can answer what the other said. Temperature is zero point nine, so the speeches vary from run to run, and the limit is a hundred and ten tokens, which keeps each speech short. In a debate of two rounds, that is four speeches.

### [3:10] The judge
```python
text, _ = llm.chat([
    {"role": "system", "content": "You are an impartial debate judge. Score each side 1-10 on logic, evidence, persuasion, clarity, rebuttal. "
     'Reply ONLY JSON: {"pro": {"logic": n, ...}, "con": {"logic": n, ...}, "winner": "pro"|"con", "reason": "one sentence"}.'},
    {"role": "user", "content": f"Motion: {topic}\n\n{transcript}"}], temperature=0, max_tokens=220, json_mode=True)
```

The judge gets the whole transcript and has to return JSON: a one to ten score for each side on logic, evidence, persuasion, clarity and rebuttal, a winner, and a one-sentence reason. The temperature is zero, so the judge is as steady as it gets. The app then draws the scores as a radar chart.

One more feature: before the debate you move a slider for how much you agree with the motion, and after the debate you move it again. The app shows your shift.

### [4:20] Debate one: pineapple
[SCREEN: setup.] The motion is: pineapple belongs on pizza. Two rounds.

[SCREEN] Before the debate I set my own opinion to four out of ten, slightly against. Then I press Start.

[SCREEN] Pro opens: the sweetness contrasts with salty toppings like ham. And there is a clever move: tomatoes are a fruit, so why is pineapple out of bounds? Con answers that tomato's acidity complements a pizza while pineapple overwhelms it, and asks: would chocolate syrup belong too?

[SCREEN] In round two, Pro calls the chocolate syrup point a strawman, because ham pairs with pineapple and syrup doesn't. Con replies that pineapple hijacks the palate, and calls it, in its words, a sugar tsunami in a savory ecosystem.

[SCREEN] The judge scores Pro forty and Con thirty-six, and picks Pro. The reason it gives: Pro made stronger arguments about the balance and evolution of flavors, and countered Con's points about disruption.

[SCREEN] Did they change my mind? I read the tomatoes point and thought it was good, even if it's a classic debating trick.

[SCREEN] I move my slider from four to five. Plus one point. A tiny shift.

### [6:30] Debate two: tabs against spaces
[SCREEN: setup.] Second motion, one every programmer has an opinion on: tabs are better than spaces.

[SCREEN] This time I set my opinion to seven: I lean towards tabs. Start.

[SCREEN] Pro argues that tabs save file size and let each person pick their own indentation width. Con says that fractures collaboration, because code looks different in every editor, while spaces look the same everywhere.

[SCREEN] In round two, Pro says consistency comes from agreeing on a standard, and tab widths are customizable. Con replies that a custom width creates an illusion of alignment, and that spaces are a pixel-perfect standard that tabs can never guarantee.

[SCREEN] The judge scores Con forty-four and Pro forty-two. Con wins, narrowly. The reason: stronger evidence and rebuttal about universal consistency.

[SCREEN] Did it change my mind?

[SCREEN] A bit: I move from seven to six. Minus one point.

### [8:30] What I noticed
Both debates ended close: four points apart in one, two in the other. The judge didn't give anyone a landslide. And the judge's one-sentence reasons mostly echo the winning side's main argument.

Also, the radar charts overlap a lot. With totals between thirty-six and forty-four out of fifty, every criterion averages between seven and nine, so the numbers look precise but say little about why one side won.

### [9:10] Honest limits
Two debates prove nothing about whether the judge is fair. The same model plays Pro, Con and the judge, so it may favour its own style. Pro always speaks first, which could matter, and I didn't test it: one debate went to each side, which is too little to say anything. The scores are one sample at temperature zero from one prompt; a different wording could shift them. And my opinion shifts, plus one and minus one, are just one person's reaction. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:55] What to build next
Next I'd swap the sides to test for position bias, use a different model as the judge, and run each motion many times to see how often the winner flips. A human vote next to the AI judge would be good too.

The code is in the description, with no key needed beyond your own Azure setup. If you liked this, follow for more AI and ML builds, and tell me which motion should be on trial next.
