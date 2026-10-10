# Short: 14 Explainable Text AI (30 s, 9:16)

**Title:** Which words made the AI decide? It shows me. (under 60 chars)
**Hashtags:** #ExplainableAI #MachineLearning #NLP #Python #Shorts

## Voice-over (about 75 words)
**[0-3s, hook]** "Most AI can't tell you why it decided. This one highlights the exact words."
**[3-11s, what you see]** "I trained a simple classifier on real newsgroup posts. Type a sentence and it picks a topic, with green words pushing toward the answer."
**[11-19s, surprising moment]** "Now a trick sentence: rocket engine, horsepower, hockey puck. Red words pull toward the runner-up, so I can watch it argue with itself."
**[19-27s, insight]** "It's 84.8 percent accurate on posts it never saw, and when it's wrong, I can see why."
**[27-30s, CTA]** "Built with Claude Code. Follow for more AI and ML builds."

## On-screen text
- 0-3s: "WHY did the AI decide that?"
- 3-11s: "Green = pushes toward the answer"
- 11-19s: "Red = pulls toward the runner-up"
- 19-27s: "84.8% accuracy on unseen posts"
- 27-30s: "Follow for more AI/ML builds"

## Exact actions to record (http://localhost:8514, viewport 540x960; no API calls)
First load trains on 3,511 posts (and downloads the dataset once), so start recording after the "Training..." spinner is gone.
1. Click button "🚀 Space". Tab "🧠 Explain a prediction" shows the Prediction metric and green-highlighted words; hover one chip to show its +/- number.
2. Click button "😈 Tricky". Show the new prediction and confidence, the red vs green chips, and the table of the top 8 words ("word", "push").
3. Point at the sidebar metric "Accuracy on unseen posts" (84.8%).
4. Optional: tab "❌ Where it gets confused" for the confusion matrix.

## Description
A TF-IDF + logistic regression text classifier that highlights which words drove each decision. Trained on six 20 newsgroups categories, it scores 84.8% on the held-out test posts. Built with Claude Code using scikit-learn and Streamlit; no API calls. Narration is AI-generated.
