# Short: RL Gridworld (30s, 9:16)

**Title:** Two AIs, one cliff: only one plays it safe
**Hashtags:** #ReinforcementLearning #MachineLearning #Python #AI #BuiltWithClaude

## Voice-over (~75 words, first person)
[0-3s HOOK] "Two AI agents walk along a cliff. Only one learns to play it safe."

[Beat 1, ~8s] "I built this with Claude Code. Both agents start knowing nothing. Every step costs one point, the cliff costs a hundred. Watch the arrows appear as they learn."

[Beat 2, ~8s] "Here's the surprise. Q-learning hugs the cliff edge, the shortest path, and keeps falling in while it explores. SARSA takes the safe route up top."

[Beat 3, ~8s] "The insight: SARSA counts its own clumsy exploring, Q-learning doesn't. Safe beats short."

[CTA, 3s] "Follow for more AI and ML builds."

## On-screen text
- 0-3s: "Which AI survives the cliff?"
- Beat 1: "No rules given. Just trial and error."
- Beat 2: "Q-learning: shortest path, keeps falling"
- Beat 2b: "SARSA: the safe route"
- Beat 3: "Safe beats short"
- CTA: "Follow for more AI/ML builds"

## Recording actions (real app controls, port 8509)
1. Sidebar: **World** = "Cliff walking", **Training episodes** = 1000, **Exploration ε** = 0.1, **Show greedy path** ticked.
2. Main page: drag the "⏪ Scrub through training: episode" slider from the first mark to the last (about 5s, slow) while both heatmaps fill with arrows.
3. Pause at the end: blue greedy paths visible. Q-learning's path runs along the cliff-side rows (rows 2-3), SARSA's uses the upper rows.
4. Scroll to the "Reward while learning (moving average)" chart; hold 2s. SARSA's line sits above Q-learning's.
5. Optional cutaway: the blue info box ("Try Cliff walking with ε = 0.1...").

## Fact notes (verified headlessly with the app's own train())
- Final greedy paths at defaults: Q-learning 14 cells, rows 2-3 (next to the cliff); SARSA 18 cells, rows 0-3 (detours up).
- Reward while exploring, mean of last 20% of 1000 episodes over 10 seeds: SARSA about 27, Q-learning about 2. The on-screen "Avg reward" caption is noisy (seed 0, 1000 eps: SARSA 32.2 vs Q-learning 20.2), so say "SARSA scores higher while learning" and avoid reading out numbers.

## Description
Two reinforcement-learning agents, Q-learning and SARSA, learn to cross a cliff with no rules given. Q-learning finds the shortest path but keeps falling during training; SARSA takes the safer route. Built with Claude Code in Python + Streamlit, no API calls. Narration is AI-generated.
