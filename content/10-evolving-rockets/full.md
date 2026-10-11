# Full video: Evolving Rockets, a genetic algorithm (~10 min)

## Titles (pick one)
1. I Evolved Rockets Until They Dodged Walls (No Programming)
2. 99 Rockets Crash. Then Evolution Kicks In.
3. Genetic Algorithms Explained With Rockets (Python)

**Thumbnail text (max 4 words):** "NOBODY PROGRAMMED THIS" (alt: "99 CRASH. EVOLVE.")

## Chapters
- 0:00 Cold open: 99 of 100 crash
- 0:30 Why evolution as an algorithm
- 1:30 DNA, physics and fitness
- 3:00 Selection, crossover, mutation (the code)
- 5:15 Live demo
- 7:15 What surprised me
- 8:15 Honest limits
- 9:00 What to build next + CTA

## Voice-over (about 1,400 words, first person, friendly)

### 0:00 Cold open (30s)
**[SCREEN: Gap level, generation 1: a tangle of blue lines, metric "Crashed 99". Then drag to generation 80.]**

A hundred rockets. Generation one: ninety-nine of them crash. They fly into walls, off the screen, nowhere near the target. 

[SCREEN]

Now watch. Generation six: the first rocket slips through the gap and hits the target. Generation eighty: most of them make it. And here's the part I love. Nobody programmed this route. There's no pathfinding. No map. Just random thrusts, a score, and a bit of evolution. I built this with Claude Code, and in the next ten minutes I'll show you every line that makes it work.

### 0:30 Why it matters (1 min)
**[AVATAR, then slide: "Try, score, keep the best, mix, mutate."]**

Genetic algorithms are one of the oldest ideas in AI, and they are still used for things like designing antennas, scheduling, and tuning parameters. The idea is borrowed from biology. You don't need to understand a problem. You just need a way to score a solution. Then you keep the better ones, combine them, add random changes, and repeat.

Compare that with the neural networks we usually talk about. They need gradients, which means a smooth, differentiable problem. Evolution works on anything you can score. Even a rocket flight path through a gap in a wall.

### 1:30 DNA, physics and fitness (1 min 30s)
**[SCREEN: code, simulate() and fitness()]**

First, what is a rocket's DNA? It's an array of shape, population by one hundred forty time steps by two. At each tick, the rocket gets a little push in x and y. That's the entire genome: a hundred and forty thrusts.

The physics is almost embarrassingly simple:

```python
vel = np.clip(vel + dna[:, t], -2.2, 2.2)
pos = np.where(alive[:, None], pos + vel, pos)
```

Add the thrust to velocity, cap the speed, move the rocket. And because it's numpy, all hundred rockets are simulated at once. There's no loop over rockets, just a loop over time. A rocket dies if it leaves the box, enters an obstacle rectangle, or reaches the target.

Now the important part: fitness. How do you score a rocket that crashed?

```python
d = np.linalg.norm(paths - TARGET, axis=2).min(1)  # closest approach over the flight
f = 100 / (1 + d) ** 1.2
f = np.where(crashed, f * 0.4, f)
return np.where(reached, 200 + (T - when), f)
```

The score is based on the closest the rocket ever got to the target, so rockets that crashed near the goal still beat rockets that wandered off. Crashing costs sixty percent of the score. And if you reach the target, you jump to over two hundred, plus a bonus for arriving earlier. That bonus is why later generations get faster, not just successful.

### 3:00 Selection, crossover, mutation (2 min 15s)
**[SCREEN: evolve() lines 49-71, highlight each step]**

Now the evolution step. Each generation: simulate, score, sort by fitness. Then build the next population.

```python
n_el = max(2, pop // 10)
new = [dna[order[:n_el]]]
pool = order[:pop // 2]
pa, pb = rng.choice(pool, pop - n_el), rng.choice(pool, pop - n_el)
cut = rng.integers(10, T - 10, pop - n_el)[:, None, None]
child = np.where(np.arange(T)[None, :, None] < cut, dna[pa], dna[pb])
m = rng.random(child.shape[:2]) < mut
a = rng.uniform(0, 2 * np.pi, m.shape)
child[m] = (np.stack([np.cos(a), np.sin(a)], -1) * 0.35)[m]
dna = np.concatenate(new + [child])
```

Line by line. 

[SCREEN]

Elitism: the top ten percent are copied unchanged, so we never lose our best rocket. 

[SCREEN]

Selection: parents are drawn at random from the top half. 

[SCREEN]

Crossover: pick a random cut point; the child takes its first thrusts from parent A and the rest from parent B. That's the np.where line, with the cut point broadcast across the whole population at once. 

[SCREEN]

Mutation: each thrust has a small chance, the mutation rate, default two percent, of being replaced with a fresh random direction. 

[SCREEN]

Finally stick elites and children together. That's the next generation.

That's the whole thing. I also store every generation's paths, sorted best first, which is why the UI can scrub through them.



[SCREEN]

One detail I like: the initial DNA is random directions of length point three five, so the first generation is basically a random walk. The first rocket to touch the target in my default run needs six generations.

### 5:15 Live demo (2 min)
**[SCREEN: app, Level = Gap, seed 1, 100 rockets, 80 generations, mutation 0.02]**

Here's the app. Level: Gap. Population a hundred, eighty generations, mutation point oh two, seed one. It evolves everything upfront, then I can scrub.



[SCREEN]

Generation one. Ninety-nine crashed. The faint blue lines are the population, the thick orange one is the best rocket. It's going nowhere useful.



[SCREEN]

I drag the generation slider. The cloud starts to lean upward. Around generation six the blue info box says "First rocket reached the target in generation six." Keep going and the cloud funnels through the gap.



[SCREEN]

Generation eighty: seventy-eight reached the target, twenty-two crashed, and the fitness chart on the right shows the best score climbing to around two hundred ninety-eight while the average catches up behind it.



[SCREEN]

Now change the level. Open sky: the first success is at generation two. Wall: six. Gap: six. Zig-zag, the hard one with two staggered walls: first success is generation eleven, and by generation eighty only forty-one of a hundred reach it. Those numbers are from my runs with the default settings and seed one. Change the seed and they move.

### 7:15 What surprised me (1 min)
**[AVATAR with lower-third: "Selection + noise = a route."]**

What surprised me was how fast it goes from nothing to something. The best fitness in generation one is below one, and then once a rocket reaches the target it jumps past two hundred. That jump comes from the reach bonus, which makes success worth far more than getting close.

Second, the mutation rate matters in a way that's very visible, and not the way I expected. On the Gap level, with three seeds each, point oh oh five had eighty-eight to ninety-two rockets arriving at generation eighty, the default point oh two had seventy to seventy-eight, and point one had only twenty-one to forty. Too much mutation keeps scrambling a good route. But on Zig-zag, the low rate got stuck on one seed, never reaching the target at all, so a little mutation helps when the problem is hard. Play with that slider rather than trusting me.

Third: the rockets don't plan. They just replay a fixed list of thrusts. If I moved the wall by a few pixels, the DNA would be wrong and they'd need to evolve again.

### 8:15 Honest limits (45s)
**[SCREEN: Zig-zag level, 41/100]**

Honest limits. This is a toy. The DNA is a fixed-length open-loop script, so the rocket doesn't sense anything. The Zig-zag level is hard, and on some seeds it doesn't get solved in eighty generations; the app tells you to try more generations. Everything is one run with one seed, so I'd treat my numbers as examples, not benchmarks. And I haven't compared this to smarter methods. A real controller would use sensors and a neural network. Also, I built this with Claude Code, and I verified the generation numbers by running the app's own functions headlessly.

### 9:00 What to build next + CTA (1 min)
**[AVATAR, then hub page]**

Next I want to evolve a neural network instead of a list of thrusts, so rockets can react to obstacles. Or add moving obstacles. Or let you draw the walls with the mouse.

The code is in the description, it needs no API key and costs nothing to run. If you enjoyed this, subscribe, there are sixteen of these AI and ML builds. And in the comments: what would you evolve? The narration is AI-generated, and the app was built with Claude Code. Thanks for watching.

## Shot list
| Time | Type | Content |
|---|---|---|
| 0:00 | Screen | Gap level gen 1 to gen 80 scrub |
| 0:20 | Avatar | "Nobody programmed this route" |
| 0:30 | Avatar + slide | Try, score, keep, mix, mutate |
| 1:30 | Code | simulate() velocity/position lines |
| 2:15 | Code | fitness() four lines |
| 3:00 | Code | evolve() elitism/crossover/mutation block, highlight each line |
| 5:15 | Screen | Live demo: generation slider, info box at gen 6, fitness curve |
| 6:30 | Screen | Switch levels: Open sky, Wall, Gap, Zig-zag |
| 7:15 | Avatar | Insight lower-third; optionally show Mutation rate 0.005 vs 0.1 |
| 8:15 | Screen | Zig-zag with 41/100 |
| 9:00 | Avatar + screen | Hub page and CTA |

## Description
A genetic algorithm breeds rockets that dodge obstacles and hit a target. DNA is a list of thrust directions; the fittest breed, children mutate, repeat. 99 of 100 crash in generation 1, and the first rocket reaches the target in generation 6 on the Gap level. I walk through the numpy code for physics, fitness, crossover and mutation, then demo the Streamlit app.

Built with Claude Code (Python, numpy, Plotly, Streamlit). No API calls. Narration in this video is AI-generated.

Chapters: 0:00 Cold open | 0:30 Why evolution | 1:30 DNA, physics, fitness | 3:00 The evolution code | 5:15 Live demo | 7:15 What surprised me | 8:15 Honest limits | 9:00 What next

## Tags
genetic algorithm, evolutionary algorithm, machine learning, python, numpy, streamlit, ai explained, evolution simulation, claude code, build with ai, rockets

## Pinned comment
What should I evolve next: a neural-network pilot, moving walls, or something you suggest? Try the Zig-zag level and tell me how many generations it took you. (Narration is AI-generated; built with Claude Code.)
