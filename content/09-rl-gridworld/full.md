# Full video: RL Gridworld, Q-learning vs SARSA (~10 min)

## Titles (pick one)
1. Two AIs, One Cliff: Why the Safe Learner Wins
2. I Built Reinforcement Learning From Scratch (No Libraries)
3. Q-learning vs SARSA: The Cliff Problem, Explained Visually

**Thumbnail text (max 4 words):** "SAFE BEATS SHORT" (alt: "CLIFF: AI FALLS")

## Chapters
- 0:00 Cold open: the agent that keeps falling
- 0:30 Why reinforcement learning matters
- 1:30 The world and the rules
- 2:45 The 20 lines that learn
- 5:00 Live demo
- 7:15 What surprised me
- 8:15 Honest limits
- 9:00 What to build next + CTA

## Voice-over (about 1,400 words, first person, friendly)

### 0:00 Cold open (30s)
**[SCREEN: Cliff walking, both heatmaps at episode 1, blue paths wandering. Then slider dragged to the end.]**

Two AI agents. One cliff. Every time they step off the edge, they lose a hundred points and get thrown back to the start. Nobody told them where the cliff is. Nobody told them the rules. They only get a score. And look at what happens: one of them learns the shortest path, right along the edge, and keeps falling in. The other one takes a longer, safer road, and scores higher. Same maths, almost. One tiny difference. By the end of this video you'll see exactly where it hides, in a single line of code. I'm going to be upfront: I built this whole thing with Claude Code, and I'll show you what I learned from reading it.

### 0:30 Why it matters (1 min)
**[AVATAR full frame, then cut to a slide: "Supervised: given answers. RL: given a score."]**

Most machine learning you hear about is supervised: here are a million examples with the right answers, copy them. Reinforcement learning is different. There are no right answers. There's an agent, a world, and a reward signal. The agent tries something, sees what happens, and slowly figures out what works. That's how game-playing agents are trained, how robots learn to walk, and it's a big part of how language models get tuned to follow instructions.

The tricky part is exploration. To find good actions, the agent has to sometimes do random things. But random things near a cliff are expensive. And that tension, between trying new stuff and not dying, is exactly what this demo shows.

### 1:30 The world (1 min 15s)
**[SCREEN: the caption at top of the app, then the sidebar. Hover the World dropdown.]**

The world is a small grid. S is the start, G is the goal, the skull cells are the cliff. Every step costs minus one, so wandering is punished. Reaching the goal pays fifty. The cliff costs minus a hundred and sends you back to the start. In the code that's literally one line of constants:

**[CODE: line 16]** `GOAL_R, STEP_R, CLIFF_R = 50.0, -1.0, -100.0`

The agent's only knowledge is a table called Q. For every cell and each of the four moves, up, right, down, left, it stores a number: how good do I think this move is from here? It starts at all zeros. Learning is just nudging those numbers.

I also added three worlds. The classic Cliff walking, a Lava maze, and Two doors. We'll mostly use the cliff.

### 2:45 The code (2 min 15s)
**[SCREEN: code editor, train() function, highlight lines as I speak.]**

Here's the whole learning loop. I'll read it, because it's short enough to read.

**[CODE: 09-rl-gridworld/app.py, lines 37-56, shown in full]**

```python
def train(env, algo, episodes, alpha, gamma, eps, seed=0):
    rng = np.random.default_rng(seed)
    Q = np.zeros((env.H, env.W, 4))
    pick = lambda s: rng.integers(4) if rng.random() < eps else int(np.argmax(Q[s]))
    ...
    for ep in range(1, episodes + 1):
        s, a, total = env.start, pick(env.start), 0.0
        for _ in range(300):
            s2, r, done = env.step(s, a)
            a2 = pick(s2)
            target = r if done else r + gamma * (Q[s2][a2] if algo == "SARSA" else Q[s2].max())
            Q[s][a] += alpha * (target - Q[s][a])
            s, a, total = s2, a2, total + r
            if done:
                break
        rewards.append(total)
```

First, the Q table, all zeros. Then this pick function: with probability epsilon, a random move; otherwise the best move the table knows. That's exploration versus exploitation in one line. Epsilon is a slider in the sidebar, default point one, so one move in ten is random.

Then the loop. Take a step. See the reward and the new cell. Choose the next action. And now the key line, the target. The target is the reward I just got, plus gamma, the discount, times how good I think the next position is.

And here's the one tiny difference. For SARSA, "how good is the next position" means: the value of the action I'm actually going to take next, which might be a random clumsy one. For Q-learning it means: the value of the best action available there, as if I'd never be clumsy. Same line, a ternary, `Q[s2][a2]` versus `Q[s2].max()`.

The last line nudges the table: move the old estimate a fraction alpha toward the target. That's it. That's the whole algorithm. Twelve lines and a table.

I also snapshot the table at about forty points, spaced on a log scale, so the UI can let you scrub through training without retraining. That was a small design choice I liked: training runs once, scrubbing is instant.

One more helper: `greedy_path` follows the best move from the start until it reaches the goal, and that's the blue line you'll see.

### 5:00 Live demo (2 min 15s)
**[SCREEN: app, Cliff walking, ε = 0.1, 1000 episodes.]**

Okay, live. Cliff walking, a thousand episodes, epsilon point one. Both agents train when the page loads. I'll drag the scrub slider back to the beginning. Episode one: the heatmap is empty, there are no arrows, the agents know nothing.

Now I scrub forward. Watch the arrows appear near the goal first, the values spread backwards from the goal, like a ripple. Green is good, red is bad.

At the end, look at the blue paths. Q-learning goes along the edge of the cliff, the shortest route. SARSA goes up and around, longer but away from the edge. In my run, Q-learning's path was fourteen cells and SARSA's was eighteen.

Now scroll down to the reward chart. This is reward during learning, not after. SARSA's line sits above Q-learning's. I checked this headlessly across ten random seeds, averaging the last fifth of a thousand episodes: SARSA averaged around twenty-seven, Q-learning around two. The little caption under each heatmap is noisier, because it only averages twenty episodes, so don't trust it for a single run.

Here's the check that proves the idea. Set epsilon to zero, no random moves at all. Now both agents, when evaluated, walk the edge happily. In my test, both scored the same, thirty-eight. The cliff-edge path really is the best path. The difference only exists because of exploration.

### 7:15 What surprised me (1 min)
**[AVATAR with a lower-third: "Optimal is not the same as safe."]**

Two things surprised me. First, that Q-learning is not "worse". It learns the genuinely optimal path. If you turned off the random moves, it wins. It's just that while it's still exploring, it pays for that optimism. It's learning about a policy it isn't actually following.

SARSA learns the value of the policy it is really running, clumsiness included. So when your behaviour is risky, SARSA says: given that I'll sometimes stumble, stay away from the edge.

Second, this is a real lesson for real systems. If the thing you're training can't afford to fail while it learns, a robot, a trading bot, anything physical, the algorithm that accounts for its own mistakes might be the right choice.

### 8:15 Honest limits (45s)
**[SCREEN: Lava maze and Two doors worlds.]**

Let me be honest about the limits. This is a tiny grid with a lookup table. It doesn't scale to big worlds. That's why modern RL uses neural networks instead of a table.

And not every world works with the default settings. On the Lava maze, Q-learning reached the goal in my test, but SARSA did not in a thousand episodes. On Two doors, neither agent got through with the defaults; they just wandered until the step limit. I haven't tuned those, so you may need more episodes or a different epsilon. Also, one training run with one random seed is a single sample, so results wobble. And yes, Claude Code wrote most of this, and I checked the numbers by running the app's own functions, not by trusting the text in the info box.

### 9:00 What to build next + CTA (1 min)
**[AVATAR, then the hub page with project tiles]**

What would I build next? A deep Q-network, where the table is replaced by a neural net, so it can handle images. Or let you draw your own cliff. Or add a wind that randomly pushes the agent.

If you want to try this, the code is in the description, it runs with no API keys, no cost. If you enjoyed it, subscribe, because this is one of sixteen AI and ML builds I'm making. And tell me in the comments: would you rather have the safe agent or the fast one? Thanks for watching. The narration in this video is AI-generated, and the code was built with Claude Code.

## Shot list
| Time | Type | Content |
|---|---|---|
| 0:00 | Screen | Cliff walking, slider scrubbed 1 to 1000 |
| 0:20 | Avatar | Hook line ("one tiny difference") |
| 0:30 | Avatar + slide | Supervised vs RL graphic |
| 1:30 | Screen | Caption, sidebar, World dropdown |
| 1:50 | Code | Line 16 constants |
| 2:45 | Code | train() lines 37-56, highlight pick / target / update |
| 4:30 | Code | greedy_path (lines 59-66) |
| 5:00 | Screen | Live demo: scrub, paths, reward chart |
| 6:30 | Screen | Set ε to 0.0 and compare |
| 7:15 | Avatar | Insight lower-third |
| 8:15 | Screen | Lava maze, Two doors |
| 9:00 | Avatar + screen | Hub page and CTA |

## Description
Two reinforcement-learning agents, Q-learning and SARSA, learn to cross a cliff with no rules given. Same update rule, one tiny difference, very different behaviour: Q-learning takes the shortest, riskiest path; SARSA takes the safe one. I walk through the ~20 lines of numpy that do the learning, then demo the Streamlit app live.

Built with Claude Code (Python, numpy, Plotly, Streamlit). No API calls, free to run. Narration in this video is AI-generated.

Chapters: 0:00 Cold open | 0:30 Why RL matters | 1:30 The world | 2:45 The code | 5:00 Live demo | 7:15 What surprised me | 8:15 Honest limits | 9:00 What next

## Tags
reinforcement learning, q-learning, sarsa, cliff walking, machine learning, python, numpy, streamlit, ai explained, claude code, build with ai, rl tutorial

## Pinned comment
Which would you pick: the fast agent that sometimes falls, or the safe one that takes the long way round? Try ε = 0.0 vs 0.1 in the app and tell me what you see. (Narration is AI-generated; code built with Claude Code.)
