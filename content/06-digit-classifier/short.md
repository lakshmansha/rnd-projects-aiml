# 06 Draw a Digit - 30s Short (9:16)

**Title (<60):** I drew a digit and 4 ML models voted on it
**Description:** Four classic ML models (SVM, neural net, random forest, k-NN) trained live on 1,797 tiny 8x8 images, then judge your drawing. No API calls. Built with Claude Code. Narration is AI-generated. Code: rnd-projects-aiml, project 06.
**Hashtags:** #MachineLearning #Python #Streamlit #sklearn #ClaudeCode

## Voice-over (~75 words)
(0-3s) Four AI models just voted on my handwriting.
(3-11s) I built this with Claude Code. It trains an SVM, a neural net, a random forest and k-NN on tiny eight by eight digit images, right when the app starts.
(11-19s) I draw a seven, lift the mouse, and the app shrinks it to eight by eight pixels. That blurry blob is all the models ever see.
(19-27s) Each one votes, and the majority wins. On held-out test data they score about 98 to 99 percent.
(27-30s) Follow for more AI/ML builds.

## Timeline and on-screen text
| Time | On screen text | Action to record |
|---|---|---|
| 0-3s | "4 models. 1 digit. Vote." | App "Draw a Digit" loaded; show "Test accuracy (unseen data)" table |
| 3-11s | "Trained live on 1,797 images" | Hover the accuracy table (SVM (RBF), Neural net (MLP), Random forest, k-NN (k=5)) |
| 11-19s | "What the models see: 8x8" | Draw a big "7" on the canvas under "Draw here"; release mouse. "What the models see" 8x8 image and "Majority vote" metric appear |
| 19-27s | "~98-99% on unseen data" | Pan to the grouped bar chart "Each model's opinion" and the line "SVM (RBF) -> 7 ..." |
| 27-30s | "Follow for more AI/ML builds" | End card; optionally click "🧹 Clear" first |

Note: measured headlessly with the app's own split/augmentation (random_state=0): SVM 99.8%, k-NN 98.4%, random forest 98.2%, MLP 98.0% on the 450 test images.
