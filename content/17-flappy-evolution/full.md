# 17 Flappy Evolution - Full video (~8 min)

## Titles (pick one)
1. 60 AI Birds Learn to Play Flappy Bird With Zero Training
2. How a Neural Network Learns a Game Without Being Taught (Neuroevolution)
3. I Evolved a Flappy Bird AI in 100 Lines of Python

**Thumbnail text (<=4 words):** NOBODY TAUGHT THEM

**Tags:** neuroevolution, genetic algorithm, neural network, flappy bird ai, python, streamlit, numpy, machine learning, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Everything here runs on a laptop CPU, no API calls. Change the seed in the sidebar and tell me how many generations it took you.

**Description:**
Sixty tiny neural nets learn to play a Flappy-style game by evolution: no gradients, no training data, no teacher. I built it with Claude Code and the narration is AI-generated. The code is one file, about 120 lines.

Recording note: all numbers below are from the app's own run with the default settings (60 birds, mutation 0.2, seed 1): best steps survived per generation were 88, 99, 99, 485, 485, 485, 1062, 1200, so a bird flew the whole course in generation eight. Other seeds (checked headlessly with the same code): seed 2 needed 3 generations, seed 3 needed 7, seed 4 needed 8.

## Voice-over

### [0:00] Cold open
Sixty birds. Each one has a tiny brain with random weights, so none of them can fly. [SCREEN: press Evolve.] Watch generation one: they all crash within a second or two. Now watch the best score climb. By generation eight, one bird flies the entire course, through every pipe. Nobody taught it. There is no training data, no reward function in the usual sense, and no gradient descent. Just evolution. I'm going to show you the whole thing in about a hundred lines of Python, and I should say up front: I built it with Claude Code, and the narration is AI-generated.

### [0:40] Why it matters
Most of the neural networks you hear about learn by gradient descent. You show them examples, measure the error, and nudge the weights downhill. That needs a smooth, differentiable signal and lots of labelled examples.

But a game gives you something different. You don't have the right move for every frame. You only know how far the bird got. Neuroevolution uses that. Try a lot of random brains, keep the ones that got further, mix them, add some random changes, and repeat. It's the same idea as the rockets video, but now the thing being evolved is a neural network.

This is an old technique. Variants of it were used to evolve controllers for robots and to play games long before deep reinforcement learning became popular, and it still turns up when the problem can't be differentiated.

### [2:00] The game and the brain
The world is deliberately small. A bird sits at a fixed horizontal position. Gravity pulls it down every step. Each step the brain may flap, which sets its vertical speed upward. Pipes scroll past with a gap in each one. Hit a pipe, the floor or the ceiling and you are out. Your fitness is simply how many steps you survived.

Here is the course. Every generation plays the same sequence of gaps, so scores can be compared fairly:

```python
def course(seed, n=400):
    return np.random.default_rng(seed).uniform(H / 2 - 75, H / 2 + 75, n)
```



And here is the brain. It has four inputs: how far the bird is below or above the middle of the next gap, its own height, its vertical speed, and the distance to the next pipe. One hidden layer of six units, and a single output. If the output is above zero, flap.

```python
def think(net, x):
    w1, b1, w2, b2 = net
    return float(np.tanh(np.tanh(x @ w1 + b1) @ w2 + b2)[0])
```

That is the entire neural network: two matrix multiplications and two tanh functions. At the start every weight is a random number, so the bird's behaviour is random: some flap constantly and fly into the ceiling, some never flap and fall into the floor.

### [3:30] One generation
Here is the loop that plays a generation.

```python
for i in np.flatnonzero(alive):
    x = np.array([(gc - y[i]) / H * 2, y[i] / H - 0.5, vy[i] / 8, (px - BX) / 250])
    if think(pop[i], x) > 0:
        vy[i] = FLAP
vy[alive] += GRAV
y[alive] += vy[alive]
hit = (y < 0) | (y > H) | ((px < BX + 12) & (px + PIPE_W > BX - 12) & (np.abs(y - gc) > GAP / 2 - 8))
alive &= ~hit
fit[alive] += 1
```



For every bird that is still alive: build its four inputs, ask the brain, flap if it says so. Then gravity, then movement, then collision: a bird is out if it leaves the screen, or if it overlaps a pipe horizontally while being outside the gap vertically. Anyone still alive gets one more point. That's the whole game, and it plays all sixty birds at the same time.

### [5:00] Selection, crossover and mutation
Now the evolution step. Sort the birds by score, then build the next generation.

```python
order = np.argsort(-fit)
elite = [pop[i] for i in order[:max(2, len(pop) // 10)]]
pool = [pop[i] for i in order[:max(4, len(pop) // 3)]]
mask = rng.random(pa.shape) < 0.5
c = np.where(mask, pa, pb)
c = c + (rng.random(c.shape) < mut) * rng.normal(0, 0.5, c.shape)
```



The top ten percent are copied unchanged, so we never lose our best bird. The parents for everyone else come from the top third. For crossover, each weight in the child is copied from one parent or the other, chosen by a coin flip. For mutation, each weight has a chance, the mutation rate, of getting a random nudge. That's it: selection, crossover, mutation.

### [6:15] Live demo
[SCREEN: app.] I leave the defaults: sixty birds, twenty generations at most, mutation point two, seed one. I press Evolve. The app plays each generation live, with all the living birds drawn on top of each other. The counter shows how many are still alive, and the chart on the right shows the best score of each generation.



[SCREEN]

Generation one: the best bird survives only eighty-eight steps. Generations two and three barely improve. 

Then at generation four the best score jumps to four hundred and eighty-five, because a lucky child found how to get through the first few pipes. It stays there for two generations, then climbs to one thousand and sixty-two, and in generation eight a bird survives all twelve hundred steps, the full course. The app stops there and says the population has learned to play.



[SCREEN]

The shape of that chart is typical: flat for a while, then a jump. Evolution doesn't improve smoothly; it waits for a lucky combination and then keeps it.

### [7:15] What surprised me
How little the brain needs. Six hidden units were enough. And how much tuning the game itself took: my first version was so easy that a random bird already flew the whole course, and my second was so hard that nothing evolved. The final settings sit in between. Making the game fair mattered as much as the evolution code.

Also how much the seed matters. With the same settings, seed two solves it in three generations, seed three needs seven and seed four needs eight.

### [8:00] Honest limits
This is a toy. The course is the same every generation, so the birds learn this one sequence of gaps, not Flappy Bird in general; I haven't tested them on new courses. The score is capped at twelve hundred steps. The simulation is simplified: no real Flappy Bird physics, and the pipes are evenly spaced. And every number here comes from a handful of runs, so don't read them as a benchmark. I built this with Claude Code, and I read and ran the code, but you should read it yourself too.

### [8:40] What to build next
Next I'd generate a fresh course for every generation and see whether the brains generalise. I'd also like to add a second kind of obstacle, or let you draw the course. And a comparison with gradient-based reinforcement learning would be a good video.

The code is in the description, no API key, no cost. If you enjoyed watching birds learn, follow for more AI and ML builds, and tell me which game I should evolve next.
