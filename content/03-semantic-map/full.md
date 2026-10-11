# 03 Semantic Map - Full video (~7 min)

## Titles (pick one)
1. How RAG Works: Embeddings, a Semantic Map and Grounded Answers
2. I Built a Map of Meaning (and Found Where Embeddings Fail)
3. RAG From Scratch: Retrieve, Then Answer Only From the Context

**Thumbnail text (<=4 words):** I DON'T KNOW (GOOD)

**Tags:** rag, retrieval augmented generation, embeddings, semantic search, tsne, pca, gpt-4o, azure openai, streamlit, python, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The map and search run locally; only the final answer uses one small call to GPT-4o on Azure. Which question would you ask it?

**Description:**
Sentences become points on a 2D map, a question lands on the map as a star, the closest sentences are retrieved, and GPT answers using only those. I built it with Claude Code and the narration is AI-generated. The app is one file plus a 60-sentence corpus.

Recording note: four real questions, one small LLM call each. "Why does bread rise?" retrieved the sourdough sentence (similarity 0.28) and answered from it. "How do I stop my savings losing value over time?" retrieved the inflation sentence (0.29) and the model said "I don't know", because that sentence says what inflation does, not how to stop it. "Which team won the most World Cups?" retrieved "The World Cup is held every four years" (0.35) and the model said "I don't know". "Who painted the Mona Lisa?" retrieved unrelated sentences and the model said "I don't know". Important: the embeddings here are local character n-gram hashing vectors, not a trained semantic model (no embedding model is deployed), so retrieval depends largely on shared wording, and the similarity scores are low (0.17 to 0.35).

## Voice-over

### [0:00] Cold open
[SCREEN: the answer.] Ask a question: why does bread rise? The app finds the sentence in a small collection that matches best, hands only that to GPT, and the answer comes back, grounded in it. [SCREEN] Underneath you can see exactly which sentences were retrieved, and how similar they were. I built this with Claude Code, and the narration is AI-generated. It's also a good example of when retrieval works, and of when the right answer is: I don't know.

### [0:50] The idea
Retrieval-augmented generation, or RAG, has two steps. First, retrieve: find the pieces of your own text that are relevant to the question. Second, generate: give only those pieces to the model and ask it to answer from them. The model doesn't have to know your documents; it only has to read the few sentences you hand over.

The first step depends on turning text into numbers. An embedding is a list of numbers that represents a piece of text, built so that similar texts get similar lists. Then finding relevant text becomes finding the closest points.

### [1:50] The embeddings
Here is the honest part. A proper embedding model has been trained to put similar meanings close together. I don't have one deployed in this project, only a chat model. So the vectors here come from a simpler, free method.

```python
_hasher = HashingVectorizer(n_features=1024, analyzer="char_wb", ngram_range=(3, 5), alternate_sign=False, norm="l2")


def embed(texts):
    """Local, free, stateless text vectors (character n-grams). No API call."""
    return _hasher.transform(texts).toarray().tolist()
```

Each text is chopped into overlapping chunks of three to five characters, which are hashed into a vector of a thousand and twenty-four numbers. Two sentences that share words or word pieces get similar vectors. That's useful, but it is not meaning: it measures shared spelling. Keep that in mind for everything that follows.

### [3:00] Searching and answering
```python
qv = np.array(llm.embed([q])[0])
qv /= np.linalg.norm(qv)
sims = vecs @ qv
top = np.argsort(-sims)[:k]
```

The question gets the same treatment. Then one matrix multiplication gives its similarity to all sixty sentences, and the top k, three by default, are taken. The star on the map is placed at the similarity-weighted centre of those neighbours, so you can see where the question lands.

```python
ans, secs = llm.chat(
    [{"role": "system", "content": "Answer using ONLY the context. If it is not there, say you don't know. Be brief."},
     {"role": "user", "content": "Context:\n- " + "\n- ".join(ctx) + f"\n\nQuestion: {q}"}],
    temperature=0.2, max_tokens=80)
```

And the generation step is a single call. The system prompt is the important part: answer using only the context, and if it isn't there, say you don't know. The retrieved sentences go in as the context.

### [4:00] The map
[SCREEN: the map.] These are sixty sentences, ten each on space, cooking, machine learning, football, personal finance and ocean life, projected down to two dimensions with t-SNE, which keeps close points close. The colours are the topics. And you can see the limitation straight away: the colours form loose neighbourhoods, not clean islands, because the vectors capture wording, not meaning.

[SCREEN] Switching to PCA, a simpler projection, gives a different picture, and a more squashed one. The projection is only a drawing; the retrieval itself happens in the original thousand-dimensional space.

### [5:00] Question one: bread
[SCREEN: typing.] I ask: why does bread rise?

[SCREEN] A star appears on the map, with dotted lines to the three nearest sentences.

[SCREEN] The best match is the sourdough sentence, with a similarity of zero point two eight: sourdough bread rises thanks to wild yeast and lactic acid bacteria. The other two are unrelated: one about diversification, one about overfitting, at zero point one seven. They are only there because I asked for three. The answer: bread rises because of wild yeast and lactic acid bacteria, which produce gases during fermentation. The last part, about gases, was not in the retrieved sentence, so even with a strict prompt the model added something from its own knowledge.

### [6:00] Question two: savings
[SCREEN: typing.] Next: how do I stop my savings losing value over time?

[SCREEN] The top result is the right sentence: inflation reduces the purchasing power of money over time, at zero point two nine. But the model answers: I don't know. And I think that's correct. The sentence explains the problem, not the solution, and the prompt said to use only the context.

### [6:50] Questions three and four
[SCREEN: typing.] Which team won the most World Cups?

[SCREEN] The closest sentence is: the World Cup is held every four years, at zero point three five. It's about the right topic, but it doesn't contain the answer, so the model says: I don't know.

[SCREEN: typing.] And a question that has nothing to do with the collection: who painted the Mona Lisa?

[SCREEN] The retrieved sentences are about paying off debt, the Mariana Trench and goalkeepers, and the answer is again: I don't know. Without the instruction to stay in the context, GPT would likely just answer from memory, and you wouldn't know whether the answer came from your documents.

### [8:00] What I noticed
Three of four answers were I don't know, and I found that reassuring rather than disappointing. Retrieval returned plausible but insufficient text, and the prompt made the model say so instead of guessing. The bread example also shows the opposite risk: a correct answer that leaks a bit of outside knowledge.

And the similarity scores are low even for a good match, zero point two eight, because character n-grams share little between a question and a statement.

### [8:40] Honest limits
Sixty sentences is tiny; real systems retrieve from thousands or millions of passages. The embeddings are character hashes, not a semantic model, so a question that doesn't share words with the right sentence can miss it entirely, and the map clusters by wording, not meaning. The top k is fixed, so weak matches get passed to the model as noise. I tried four questions, which says nothing about accuracy in general. And only the answer is generated by the model; the retrieval can't be better than the embeddings. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:30] What to build next
Next I'd switch to a real embedding model and compare the maps, add a similarity cut-off so weak matches are dropped, show which retrieved sentence the answer used, and let you upload longer documents.

The code is in the description. The map costs nothing to run, and the answer costs one small call. If you want to see the same app with real embeddings, follow for more AI and ML builds, and tell me what question I should ask it.
