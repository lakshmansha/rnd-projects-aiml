# 14 Explainable Text AI - Full video (~7 min)

## Titles (pick one)
1. An AI That Shows Which Words Made Its Decision (Explainable ML)
2. Why Did the Classifier Say That? TF-IDF + Logistic Regression Explained
3. Opening the Black Box: See Every Word's Vote

**Thumbnail text (<=4 words):** WHY DID IT SAY THAT?

**Tags:** explainable ai, interpretable machine learning, tf-idf, logistic regression, text classification, scikit-learn, python, streamlit, machine learning, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Runs locally with scikit-learn on the 20 newsgroups dataset, no API calls. Type a sentence that fools it and tell me what it said.

**Description:**
A classic text classifier that shows which words drove each decision, trained live on real newsgroup posts. I built it with Claude Code and the narration is AI-generated. The app is one file and runs locally.

Recording note: the model is TF-IDF plus logistic regression, trained on 3,511 posts from six 20 Newsgroups categories and tested on 2,338 unseen posts (headers, footers and quotes removed): accuracy 84.8%. The Space example is predicted Space at 100% confidence, Hockey at 99%. The "Tricky" example (rocket engine, car, puck, hockey player) comes out Hockey 53%, Cars 46%. In the confusion matrix on the test set the three biggest error cells are Medicine posts labelled Cars (40), Space posts labelled Cars (38) and Politics posts labelled Cars (32).

## Voice-over

### [0:00] Cold open
[SCREEN: the app.] Here is a sentence about a shuttle, an orbit and a telescope. A classifier says: Space, one hundred percent confident. That alone isn't very useful. What I want to know is why. So the app highlights every word: green words push towards the answer, and red words push away. [SCREEN] Then I give it a sentence designed to confuse it, about a rocket engine, a car and a hockey puck. Watch the prediction wobble, and watch which words are voting for what. I built this with Claude Code, and the narration is AI-generated.

### [0:50] Black boxes and glass boxes
Deep neural networks are very good at text, but it is hard to say why they gave a particular answer. This app uses an older technique on purpose, because it can be explained completely.

The pipeline has two parts. TF-IDF turns a text into numbers: each word gets a score that is high when the word is frequent in this text and rare across the whole collection. Then logistic regression learns one weight per word for each topic. Positive weights mean the word is evidence for that topic. To classify a text, add up the evidence. Because the model is just a sum, you can read off every word's contribution.

### [2:00] Training
The data is a real dataset called twenty newsgroups: old internet discussion posts, labelled by the group they were posted in. I picked six groups: space, hockey, graphics, cars, medicine and politics, which here is the gun politics group.

```python
vec = TfidfVectorizer(stop_words="english", sublinear_tf=True, min_df=3, max_features=30000)
Xtr = vec.fit_transform(tr.data)
clf = LogisticRegression(C=10, max_iter=1000).fit(Xtr, tr.target)
pred = clf.predict(vec.transform(te.data))
```

Stop words like the and of are dropped, and words that appear in fewer than three posts are ignored. The vectoriser learns the vocabulary and the weights on thirty-five hundred training posts. Then the model predicts the separate test set of twenty-three hundred posts it has never seen. The app caches all this, so it only trains once. The accuracy on those unseen posts is shown in the sidebar: eighty-four point eight percent.

### [3:30] Where the highlights come from
This is the explanation itself.

```python
order = np.argsort(-p)
diff = clf.coef_[order[0]] - clf.coef_[order[1]]
contrib = {}
for w in set(re.findall(r"[a-z']+", text.lower())):
    if w in vocab:
        contrib[w] = diff[vocab[w]] * x[0, vocab[w]]
```

Take the top two topics for this text. For every word that the model knows, look at the difference between its weight for the winner and for the runner-up, and multiply by the word's TF-IDF value in this text. A positive number means the word pushed towards the winner, and a negative number means it pushed towards the runner-up. That number sets the colour and the strength of each highlight, and the eight biggest go in the table.

### [5:00] Live demo
[SCREEN: app.] The Space example. The biggest pushes are orbit, moon, launch, NASA and shuttle, in that order. The model is a hundred percent sure, and the reason is visible: five strong space words, and nothing pulling the other way.



[SCREEN] I click the Hockey example. Game, playoff, Bruins, win and scored carry it, and the prediction is Hockey with ninety-nine percent confidence.



[SCREEN] Now the tricky one: the new rocket engine has more horsepower than any car and could hit a puck faster than a hockey player. The model says Hockey, but only with fifty-three percent, and Cars has forty-six. And now we can see why. The word car pushes towards Cars with a strength of nearly three, and engine pushes the same way. Against that, hockey pushes towards Hockey even harder, and puck and player add to it. The model isn't confused in a mysterious way. It is a close vote between two clusters of words.



[SCREEN]

### [6:30] What each topic's words are
[SCREEN: second tab.] The second tab shows the highest weighted words for each topic, which the model worked out on its own. For Space: space, orbit, NASA, moon, launch, earth, spacecraft, shuttle. Nobody told it that. These come purely from which words show up in which group.



[SCREEN]

### [7:10] Where it gets confused
[SCREEN: third tab.] The confusion matrix shows, for each real topic, what the model predicted. Bright diagonal cells are correct answers. The app's own caption says mistakes are mostly between related topics like Space and Medicine, but in my run the biggest error cells are different. The largest are Medicine posts labelled Cars, forty of them, then Space posts labelled Cars, thirty-eight, and Politics posts labelled Cars, thirty-two. Why Cars absorbs so many mistakes, I haven't investigated.



[SCREEN]

### [7:50] What I take from it
Being able to see the reasons changes how you trust a model. For the easy examples, the right words carry the decision. For the tricky one, you can see the argument. And when I looked at the errors, I found something I wouldn't have guessed: most of the biggest mistakes land on Cars.

### [8:20] Honest limits
Eighty-four point eight percent on six topics is decent, not great. The data is old internet posts from the nineties, so the model knows that language, not modern text. The word contributions explain this particular model, which is a simple linear one; they don't explain a neural network, and they ignore word order and negation, so not good would count the same as good. The colours compare only the top two topics, not all six. I built this with Claude Code, and I read and ran the code, but read it yourself too.

### [9:00] What to build next
Next I'd let you train on your own labelled text, add a negation test, and put the same sentence through a neural model so you can compare the two explanations.

The code is in the description, with no API key and no cost. If you enjoyed seeing inside the model, follow for more AI and ML builds, and tell me which sentence should try to fool it next.
