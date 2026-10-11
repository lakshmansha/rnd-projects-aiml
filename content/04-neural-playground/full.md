# 04 Neural Net Playground - Full video (~6 min)

## Titles (pick one)
1. I Wrote a Neural Network From Scratch and Watched It Learn (numpy only)
2. Backpropagation Explained With a Live Decision Boundary
3. Why Your Neural Network Can't Learn This (Too Small)

**Thumbnail text (<=4 words):** TOO SMALL TO LEARN

**Tags:** neural network from scratch, backpropagation, numpy, decision boundary, python, streamlit, machine learning, deep learning, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. The network is plain numpy, no framework and no API calls. Try the spiral with hidden layers "3" and tell me the accuracy you get.

**Description:**
A neural network written from scratch in numpy, trained live while you watch its decision boundary bend. I built it with Claude Code and the narration is AI-generated. The network code is about thirty lines.

Recording note: numbers are from the app's own run on the Spiral dataset with tanh, learning rate 0.3 and 1500 epochs: hidden layers 8,8 reached 98.0% accuracy (loss 0.116); hidden layer 2 reached 57.0% (loss 0.656). Accuracy is measured on the same 300 training points, not on held-out data.

## Voice-over

### [0:00] Cold open
Two spirals, one orange and one blue, wound around each other. [SCREEN: press Train.] A neural network I wrote from scratch has to draw a line between them. Watch the boundary: at first it is almost flat, then it starts to bend, and after fifteen hundred steps it wraps around the spiral with ninety-eight percent accuracy. Then I'll shrink the network to two neurons and show you what happens. I built this with Claude Code, and the narration is AI-generated.

### [0:40] What a decision boundary is
A classifier takes a point and answers one question: orange or blue. The decision boundary is the border between those two answers. The coloured background in this chart is the network's opinion at every position, and the dots are the real data.

A straight line cannot separate a spiral. To separate it, the boundary has to curve and curve again. That curving comes from stacking layers, and it is the reason deep networks exist.

I wanted to watch that happen, step by step, with nothing hidden inside a library. So the whole network is numpy.

### [1:40] The network
Here is the forward pass.

```python
def forward(self, X):
    A = [X]
    for k, (W, b) in enumerate(zip(self.W, self.b)):
        z = A[-1] @ W + b
        A.append(1 / (1 + np.exp(-z)) if k == len(self.W) - 1 else self.f(z))
    return A
```

Each layer multiplies its input by a weight matrix, adds a bias, and applies an activation function. In the hidden layers the activation is tanh, which squashes numbers into a range from minus one to one. That squashing is what makes the layers more than one big linear map. The last layer uses a sigmoid, so the output is a probability between zero and one: how likely is this point to be orange.

With the default setting the shape is two inputs, two hidden layers of eight neurons, and one output. The weights start as small random numbers, so at the start the network knows nothing.

### [3:00] Backpropagation
Learning means nudging the weights so the answers get less wrong. This is the backward pass.

```python
def step(self, X, y, lr):
    A = self.forward(X)
    d = (A[-1] - y[:, None]) / len(X)  # sigmoid + BCE gradient
    for k in reversed(range(len(self.W))):
        gW, gb = A[k].T @ d, d.sum(0)
        if k:
            d = (d @ self.W[k].T) * self.df(A[k])
        self.W[k] -= lr * gW
        self.b[k] -= lr * gb
```

First we run the forward pass and measure the error at the output. With a sigmoid output and binary cross-entropy loss, that error is simply the prediction minus the label. Then we walk backwards through the layers. At each layer we work out how much each weight contributed to the error, which is the gradient, and we subtract a small multiple of it. The multiple is the learning rate. To pass the error further back, we multiply by the transposed weights and by the derivative of the activation. That one line, repeated layer by layer, is backpropagation.

Every step uses all three hundred points at once, so this is plain full-batch gradient descent.

### [4:30] Live demo
[SCREEN: app.] I pick the Spiral dataset, hidden layers eight comma eight, tanh, learning rate zero point three, and fifteen hundred epochs. I press Train. [SCREEN] The chart redraws about forty times during training, so you can watch the boundary bend and the loss fall. [SCREEN] At the end the app reports fifteen hundred epochs, accuracy ninety-eight point zero percent, and a loss of zero point one one six. The loss curve on the right fell from about zero point seven to about zero point one, with a few spikes along the way, and the boundary now follows both arms of the spiral.

Now the experiment. I change the hidden layers from eight comma eight to just two. That means a single hidden layer with two neurons. [SCREEN] Same data, same learning rate, same fifteen hundred epochs. [SCREEN] This time the result is fifty-seven percent accuracy, with a loss of zero point six five six. That is barely better than guessing, and the boundary stays almost straight. The loss curve dropped quickly at the start and then crawled, never getting anywhere near the other run.

### [5:45] What I take from it
More training would not rescue the small network. Two neurons can only combine two straight lines into a gentle bend, and that shape simply cannot describe a spiral. The limit is capacity, not effort. On the other side, more layers and more neurons give the boundary the freedom to curve, which is what the bigger network used.

### [6:15] Honest limits
This is a toy. The accuracy numbers are measured on the same three hundred points the network trained on, so they say how well it fitted the data, not how well it would do on new points. I used one dataset, one random seed for the weights, and one learning rate for the comparison. A different seed could land a few points away, and the two neuron result in particular could change. I built this with Claude Code and I read and ran the code, but read it yourself too.

### [6:50] What to build next
Next I'd add a held-out test set so you can watch overfitting happen, and show each neuron's own output so you can see what the hidden layers actually learn. Dropout and weight decay would be good additions too.

The code is in the description, with no API key and no cost. If you enjoyed watching a boundary bend, follow for more AI and ML builds, and tell me which dataset I should add.
