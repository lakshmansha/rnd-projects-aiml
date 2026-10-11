# 11 Token X-ray - Full video (~6 min)

## Titles (pick one)
1. What ChatGPT Actually Sees: Tokens, Explained With a Live Tool
2. Why LLMs Can't Count Letters (and Why Hindi Costs More)
3. I Built an X-ray for Text: See Tokens Like GPT Does

**Thumbnail text (<=4 words):** CHATGPT CAN'T SPELL

**Tags:** tokens, tokenization, tiktoken, gpt-4o, llm, context window, python, streamlit, machine learning, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The app only runs the tiktoken tokenizers locally, no API calls. Paste a sentence in your language and tell me how many tokens it takes.

**Description:**
An X-ray for text: see how GPT's tokenizers split any sentence into tokens, what that costs, and why it breaks letter counting. I built it with Claude Code and the narration is AI-generated. The app is one file and runs locally.

Recording note: all counts below come from the app itself (tiktoken, o200k_base vs cl100k_base, default price $2.50 per million input tokens): "How many r's are in strawberry?" is 8 tokens in both vocabularies, with " strawberry" as one token; the number sentence is 21 and 21; the four-language greeting is 21 vs 41; the emoji line is 16 vs 21; the code line is 24 and 24. The tokenizers are real; the app does not run any model.

## Voice-over

### [0:00] Cold open
Ask a chatbot how many r's are in strawberry, and for years the answer was a coin flip. Here is why. [SCREEN: the app.] This is that exact question, as the model actually receives it. The coloured chips are tokens. Look at the word strawberry: it is a single chip. The model never sees the letters s, t, r, a, w. It sees one unit, and it has to remember how that unit is spelled. I built this tool with Claude Code, and the narration is AI-generated.

### [0:45] What a token is
Language models don't read characters and they don't read words. They read tokens: chunks of text from a fixed vocabulary. A token can be a whole word, part of a word, a space, a number fragment, or a single symbol.

Why chunks? Because it's a compromise. Characters would make every text very long. Whole words would need a gigantic vocabulary and couldn't handle new words. Chunks sit in between.

And tokens are the unit of everything practical. You pay per token. The context window is measured in tokens. And what the model can and cannot do with spelling and arithmetic follows from how the text was chopped up.

### [2:00] How the tool works
The tokenizers themselves come from an open-source library called tiktoken, which OpenAI publishes. The app doesn't call any API.

```python
def split(enc, s):
    ids = enc.encode(s)
    return ids, [enc.decode_single_token_bytes(i) for i in ids]
```

Encoding turns the text into a list of integer IDs. Then each ID is turned back into the bytes it stands for, so we can show the piece of text behind it. Those integers are all the model ever gets.

```python
chips = "".join(
    f'<span style="background:{COLORS[i % len(COLORS)]};...>'
    f'{html.escape(show(p))}</span>'
    for i, (t, p) in enumerate(zip(ids, pieces)))
```

To draw them, each piece becomes a little coloured span, cycling through six colours so neighbouring tokens are easy to tell apart. Hover over a chip and you see its ID. The app does this for two vocabularies at once: o200k, used by the GPT-4o family, and cl100k, used by GPT-4 and GPT-3.5.

### [3:15] Strawberry
[SCREEN: the strawberry example.] The sentence How many r's are in strawberry has thirty-one characters and comes out as eight tokens, in both vocabularies. How, many, r, an apostrophe s, are, in, strawberry, and the question mark.



[SCREEN: open Token IDs.]

Open the token IDs and you see the real thing: just a list of integers. The word strawberry is one of them. To count its r's, the model can't look at letters, because there aren't any. It has to have learned the spelling of that token from its training text. That is a harder job, and the reason letter counting went wrong.



[SCREEN]

### [4:15] Numbers
[SCREEN: Numbers example.] Now numbers. The year two thousand twenty-four becomes the pieces two zero two and four. The long number one two three four five six seven eight nine zero one two three is chopped into one two three, four five six, seven eight nine, zero one two, and three. Pi is split too. So the model sees a number as a sequence of three-digit chunks, and which chunk boundaries you get depends on where the number starts. That is one reason arithmetic is awkward for language models.



[SCREEN]

### [5:00] Languages
[SCREEN: Other languages.] This is the same greeting, hello world, in English, Hindi, Japanese, Arabic and Russian. Sixty-three characters. On the newer o200k vocabulary it is twenty-one tokens.



[SCREEN]

Now I switch to the older cl100k vocabulary. The same text is forty-one tokens, almost double. The newer vocabulary was trained to cover more languages efficiently. The older one splits non-English text into many small pieces.



[SCREEN]

For you that means two things. Text in some languages costs more, because you pay per token, and it uses up more of the context window. The comparison between the two vocabularies shows it is a design choice, and that the newer one improved on it.

### [6:00] Emoji and the cost panel
[SCREEN: Emoji example.] Emoji are another case. Pizza and robot, plus a person with a skin tone and a laptop, come out as sixteen tokens on the new vocabulary and twenty-one on the old one. Each emoji is stored as several bytes, and the tokenizer splits them into byte fragments, so a single emoji can take two or three tokens.



[SCREEN]

At the bottom, the app turns the count into money. At the default price of two dollars fifty per million input tokens, a short line like this costs a tiny fraction of a cent. It adds up only at scale, and it scales with tokens, not characters.

### [6:50] What surprised me
That the answer to the strawberry question isn't about intelligence at all. It is about the input format. The model isn't bad at counting; it never saw the letters. Also how much the vocabulary matters: the same greeting costs about half as many tokens with the newer tokenizer.

### [7:20] Honest limits
This tool shows tokenisation only. It doesn't run a model, so it can't prove why a given model fails at a given task; it shows what the input looks like. It supports two OpenAI vocabularies. Other model families, like Claude, Llama or Gemini, use different tokenizers and would split the same text differently, and I have not compared them. The cost panel uses a price you can edit, not a live price list. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [7:55] What to build next
Next I'd add more tokenizers side by side, so you can compare several model families on the same sentence, and show the token IDs next to the chips. A context-window meter would also be a good addition.

The code is in the description, with no API key and no cost. If this changed how you see a chatbot's mistakes, follow for more AI and ML builds, and tell me what text I should put through the x-ray.
