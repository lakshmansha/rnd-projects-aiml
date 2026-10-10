# Short: Evolving Rockets (30s, 9:16)

**Title:** 100 rockets, zero programming: they evolve a route
**Hashtags:** #GeneticAlgorithm #Evolution #MachineLearning #Python #BuiltWithClaude

## Voice-over (~75 words, first person)
[0-3s HOOK] "Generation one: a hundred rockets, and ninety-nine crash."

[Beat 1, ~8s] "I built this with Claude Code. Each rocket's DNA is just a list of random thrusts. The best ones breed, the children mutate."

[Beat 2, ~8s] "Now watch me scrub through generations. By generation six, the first rocket slips through the gap and hits the target. Nobody programmed that route."

[Beat 3, ~8s] "The insight: selection plus a little mutation finds a path you never wrote. By generation eighty, most rockets make it."

[CTA, 3s] "Follow for more AI and ML builds."

## On-screen text
- 0-3s: "99 of 100 crash"
- Beat 1: "DNA = a list of thrusts"
- Beat 2: "Gen 6: first rocket arrives"
- Beat 3: "Nobody programmed the route"
- CTA: "Follow for more AI/ML builds"

## Recording actions (real app controls, port 8510)
1. Sidebar defaults: **Level** = "Gap", **Population** 100, **Generations** 80, **Mutation rate** 0.02, **Random seed** 1.
2. Drag the "⏪ Generation" slider to 1: metrics show Generation 1 and Crashed 99. Hold 2s on the tangled blue paths.
3. Drag the slider right slowly; pause at 6 where the blue info box reads "First rocket reached the target in generation 6."
4. Drag to 80: orange best-rocket path through the gap, "Reached target" 78/100. Show the "Fitness over generations" curve.
5. Optional teaser: switch **Level** to "Zig-zag" (first success generation 11, only 41/100 reach at 80 generations).

## Fact notes (verified headlessly, defaults, seed 1)
- Gap: generation 1 crashed 99/100; first reach generation 6; generation 80: 78 reached, 22 crashed.
- Zig-zag: first reach generation 11; generation 80: 41 reached, 59 crashed.

## Description
A genetic algorithm breeds rockets that dodge obstacles and hit a target. DNA is a list of thrust directions; the fittest breed, children mutate, repeat. By generation 6 the first rocket reaches the target, with no route ever programmed. Built with Claude Code (Python, numpy, Streamlit). Narration is AI-generated.
