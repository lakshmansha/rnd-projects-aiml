# 04 Neural Playground - 30s Short (9:16)

**Title:** Watch a neural net learn a spiral, live (<60)
**App:** `04-neural-playground` (pure numpy, no API calls, free to record repeatedly).
Real numbers (seed 0, 300 points, noise 0.15, tanh, lr 0.3, 1500 epochs, measured by running the app's own MLP code headless): Spiral with `8,8` reaches 98.0% accuracy, loss 0.116. Spiral with `2` stays at 57.0% accuracy, loss 0.656. (Note: `2` means one hidden layer of 2 neurons.)

## Voice-over (~74 words)
**Hook (0-3s):** "Can a tiny network untangle this spiral?"

**Beat 1 (3-11s) what you see:** "It's a neural network I wrote from scratch in numpy. Two hidden layers of eight. I press Train and the decision boundary starts bending."

**Beat 2 (11-19s) surprise:** "It finds the spiral: ninety-eight percent accuracy. Now shrink it to two neurons. Same data, same training, fifty-seven percent. Barely better than a coin flip."

**Beat 3 (19-27s) insight:** "Depth and width are what let a boundary curve. Too little capacity, and no amount of training helps."

**CTA (27-30s):** "Built with Claude Code, narrated by AI. Follow for more AI/ML builds."

## On-screen text
- 0-3s: "Untangle the spiral"
- 3-11s: "Backprop from scratch, ~30 lines"
- 11-19s: "8,8 -> 98%   |   2 -> 57%"
- 19-27s: "Capacity decides what it can learn"
- 27-30s: "Follow for more AI/ML builds"

## Actions to record
1. Sidebar: Dataset = `Spiral` (it is the default, index 2), Noise = 0.15, Hidden layers = `8,8`, Activation = `tanh`, Learning rate = 0.3, Epochs = 1500 (all defaults).
2. Click "Train" (primary). The chart redraws about 40 times: left "Decision boundary" contour, right "Loss" curve, with the "Epoch / accuracy" metric. Capture the whole run (screen-record, speed up if slow).
3. Change "Hidden layers" to `2`, click "Train" again, capture the final ~57% accuracy.
4. Do NOT use `relu` on the spiral at these settings: it only reached 62% in my run, which would confuse the story. (Could be a bonus "relu isn't always better" short.)

## Description
A neural network written from scratch in numpy, trained live in the browser: watch the decision boundary bend. Spiral with two hidden layers of 8 neurons reached 98% accuracy; with a single 2-neuron hidden layer only 57% (same seed, data and settings). Built with Claude Code. Narration is AI-generated.

## Hashtags
#NeuralNetworks #MachineLearning #Numpy #DeepLearning #AI
