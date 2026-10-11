# 08 AI 20 Questions - Full video (~8 min)

## Titles (pick one)
1. I Played 20 Questions Against GPT (Both Directions)
2. Can GPT Read My Mind? 20 Questions With an LLM
3. How an LLM Plays 20 Questions: Host and Guesser

**Thumbnail text (<=4 words):** CAN GPT READ MINDS?

**Tags:** 20 questions, llm game, gpt-4o, azure openai, streamlit, python, prompt engineering, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The game calls GPT-4o through Azure with one small call per question. What would you think of to beat it?

**Description:**
Two games in one: you guess GPT's secret, or you think of something and GPT tries to read your mind. I built it with Claude Code and the narration is AI-generated. The app is one file and uses about one tiny LLM call per question.

Recording note: one game in each direction, played live (about two dozen small calls). Mode A: the secret was an octopus from the Animal list; my questions were "Is it bigger than a dog?" (Sometimes), "Can it fly?" (No), "Does it live in water?" (Yes), "Does it have feathers?" (No), "Does it have eight arms?" (Yes), "Is it an octopus?" (Yes): solved in 6 questions. Mode B: I thought of a stapler and answered honestly; GPT asked 17 questions and then guessed "stapler". I wrote the app, so I know the animal list, which makes mode A easier for me than for a viewer. These are single games, not a benchmark.

## Voice-over

### [0:00] Cold open
[SCREEN: a game.] GPT has a secret animal. I get to ask yes or no questions, and I have twenty. [SCREEN] Six questions later: "Yes, it was octopus." Then we swap. [SCREEN: the second game.] I think of an object, and now GPT has to work out what's in my head. [SCREEN] After seventeen questions it says: stapler. It was right. I built this with Claude Code, and the narration is AI-generated.

### [0:50] Two games, one app
Twenty questions is a nice test for language models because it needs two different skills. When the model is the host, it has to hold a secret and answer honestly without giving it away. When the model is the guesser, it has to ask questions that actually narrow things down.

The app lets you play both. In the first mode, you guess. In the second, you think of something and GPT guesses. Each question is about one tiny call to GPT-4o on Azure, with a limit of about sixty tokens, so a game costs very little.

### [1:50] The host
The secret never goes to the player. It's picked in Python from a list for each category: animals, objects, places, food, tech. And it lives in the app's memory, not in the chat.

```python
def ask_json(system, user, max_tokens=60):
    text, _ = llm.chat([{"role": "system", "content": system}, {"role": "user", "content": user}],
                       temperature=0.3, max_tokens=max_tokens, json_mode=True)
    return json.loads(text)
```

Every question goes to a small helper that asks GPT for strict JSON, at a low temperature of zero point three, so the answers are steady.

```python
r = ask_json(f"You are the host of 20 Questions. The secret is '{secret}'. Reply ONLY JSON "
             '{"answer": "Yes|No|Sometimes|Irrelevant", "correct": true|false}. "correct" is true only if the user\'s '
             f"message is a direct guess that names '{secret}' (or a clear synonym). Never reveal the secret.", q)
```

The host prompt tells GPT the secret, limits its answers to four words, Yes, No, Sometimes or Irrelevant, and asks it to flag a correct guess in a separate field. The app, not the model, decides when the game is won. And the prompt says never reveal the secret.

### [3:10] Live: you guess
[SCREEN: the start screen.] The category is Animal, and the app picked a secret that I can't see.

[SCREEN] My first question: is it bigger than a dog? The host says: Sometimes. That's honest, since some of the animals vary a lot in size, but it also tells me a yes or no question about size isn't always clean.

[SCREEN] Can it fly? No.

[SCREEN] Does it live in water? Yes. So now I'm looking at something that doesn't fly and lives in water.

[SCREEN] Does it have feathers? No. That rules out the birds.

[SCREEN] Does it have eight arms? Yes. There aren't many animals with eight arms.

[SCREEN] Is it an octopus? Yes.

[SCREEN] The app says: Yes, it was octopus, you got it in six questions. I should be honest that I wrote this app, so I know roughly what's on the animal list, and that makes it easier for me than for you.

### [5:10] The guesser
The other direction is harder for the model. It has no secret to look at, only the history of questions and answers.

```python
r = ask_json("You are playing 20 Questions and must guess what the human is thinking of. Ask ONE smart yes/no question "
             "that splits the remaining possibilities, or make a final guess when confident. Reply ONLY JSON "
             '{"type": "question"|"guess", "text": "..."}.' + (" This is your LAST turn: you must guess." if last else ""),
             f"Questions so far:\n{hist}", max_tokens=50)
```

Each turn, the app sends the whole history, and GPT replies with either a question or a final guess. The prompt asks for a smart question that splits the remaining possibilities. On the last turn it's forced to guess. The app shows buttons for Yes, No or Sometimes, or Correct and Nope when GPT guesses.

### [6:20] Live: GPT guesses
[SCREEN: the start screen.] I think of an object on my desk. I'm not telling you what it is yet.

[SCREEN] GPT's first question is: is it a living thing? No. The next three questions are good ones: is it man-made, yes; is it larger than a microwave, no; is it an electronic device, no.

[SCREEN] Then it asks if it's commonly found in a household. For a stapler I answered Sometimes. Then personal care, which is no, entertainment, no, and work or productivity, yes.

[SCREEN] Is it a tool for writing or drawing? No. Cooking? No. An office or workspace? Yes. Used for organizing or storing? Sometimes. Made of plastic? Sometimes, since a stapler can be plastic, metal or both.

[SCREEN] On a desk? Yes. Holding or displaying paper? Sometimes. Cutting or modifying paper? Sometimes. Then: primarily used for fastening or attaching things together? Yes.

[SCREEN] And now it guesses. Stapler. I press Correct.

[SCREEN] The app says: GPT read your mind in seventeen questions.

### [8:30] What I noticed
The guesser starts well, with questions that cut the field in half, living or not, man-made or not, big or small. But in the middle it wandered. Within a few turns it asked about personal care, entertainment and cooking, when a better question would have used what it already knew: not electronic, used for work, found in offices. It still got there, but it used seventeen questions of twenty. I'd expect a good human player to need fewer, though I haven't measured that.

And the host side showed something else: the Sometimes answer. Real questions are often vague, and the host has to choose.

### [9:10] Honest limits
This was one game in each direction, so it says nothing about how good GPT is at twenty questions in general. In the guessing game I picked the object myself, a stapler, which is a common thing, and my Sometimes answers were my own judgments. In the host game, the animal list is short and I wrote it, so it's easier for me than for a new player. The host is also just a language model: it can answer wrongly, and the app has no way to check. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:55] What to build next
Next I'd add a scoreboard, harder categories, and a mode where the host also has to give a hint. And I'd measure how many questions GPT needs across many objects, rather than one.

The code is in the description, with no key needed beyond your own Azure setup. If you enjoyed this, follow for more AI and ML builds, and tell me what I should think of next.
