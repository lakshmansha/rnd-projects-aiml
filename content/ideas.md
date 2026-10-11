# Project ideas for Watch It Learn (next builds)

Rule for every idea: one Streamlit file, a hook you can see in 3 seconds, runs on a laptop CPU, no or tiny API cost, and an honest limit.

## Games and "watch it learn" (strongest hooks)
1. **Snake neuroevolution**: same engine as 17, a snake that learns to eat food.
2. **DQN CartPole / LunarLander**: a small deep Q-network learning live, reward chart beside it.
3. **Tic-tac-toe MENACE**: matchboxes and beads as a learning machine, shown as bead counts.
4. **Connect-4 vs minimax**: depth slider, see how much search depth buys.
5. **Maze solver bake-off**: BFS, A*, Q-learning on the same maze.
6. **Evolving walkers**: stick figures learning to walk (simple physics).
7. **Pong self-play**: two tiny nets improving against each other.
8. **Traveling salesman**: genetic algorithm vs simulated annealing, animated route.

## Seeing inside models
9. **Attention over training**: watch the "previous character" head form during training (follow-up to 18).
10. **Head knock-out**: remove one head of the tiny GPT and measure the loss change.
11. **Embedding explorer**: word2vec trained on a small corpus, analogies and 2D map.
12. **Neuron activations in a CNN**: what each filter responds to (project 16 follow-up).
13. **Loss landscape**: 2D slice of the loss around trained weights.
14. **Saliency vs Grad-CAM**: compare explanation methods on the same image.

## Classic ML
15. **Overfitting lab**: polynomial degree slider, train vs test error, bias-variance.
16. **Decision tree builder**: split by split, with the Gini impurity shown.
17. **PCA playground**: rotate the axes, see variance explained, reconstruct digits.
18. **Gradient descent races**: SGD, momentum, Adam on a 2D surface.
19. **Naive Bayes spam filter**: which words push toward spam.
20. **Recommender from scratch**: matrix factorisation on movie ratings.

## LLM-based (tiny API use, or local)
21. **Self-consistency demo**: ask a maths question many times, majority vote (about 30 calls).
22. **Tool-using agent with a visible thought log**: calculator plus local-docs search.
23. **Prompt compression**: how few tokens keep the answer.
24. **LLM as judge bias check**: position and length bias, measured.
25. **Chat with your own PDF** (needs real embeddings; Docker Ollama or an Azure embedding deployment).

## Data and tools
26. **Time-series forecaster bake-off**: naive, ARIMA-like, small net.
27. **Anomaly detector**: isolation forest on streaming data.
28. **Image compression with k-means**: colour palette size slider.
29. **Audio spectrogram classifier**: whistle vs clap (microphone in browser).
30. **Handwriting to LaTeX toy**: draw, classify symbols (extension of project 6).
