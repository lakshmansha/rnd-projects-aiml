# Short: 13 Clustering Lab (30 s, 9:16)

**Title:** K-means cuts this in half. This one doesn't. (under 60 chars)
**Hashtags:** #MachineLearning #Clustering #KMeans #Python #Shorts

## Voice-over (about 75 words)
**[0-3s, hook]** "Same data. Four algorithms. Only one gets it right."
**[3-11s, what you see]** "This is K-means, step by step. Every point joins its nearest cross, then each cross moves to the middle of its points. Drag the iteration slider and watch it settle."
**[11-19s, surprising moment]** "Now the showdown. On the moons and circles, K-means slices the shapes in half. DBSCAN follows the density and nails both."
**[19-27s, insight]** "Every algorithm assumes a shape. There's no best one, only the right one for your data."
**[27-30s, CTA]** "Built with Claude Code. Follow for more AI and ML builds."

## On-screen text
- 0-3s: "SAME DATA. 4 ALGORITHMS."
- 3-11s: "K-means: assign, move, repeat"
- 11-19s: "K-means cuts the moons in half" then "DBSCAN gets it"
- 19-27s: "Every algorithm assumes a shape"
- 27-30s: "Follow for more AI/ML builds"

## Exact actions to record (http://localhost:8513, viewport 540x960; no API calls)
1. Tab "K-means step by step" is open. Dataset = "Blobs", slider "k (number of clusters)" = 3.
2. Drag slider "Iteration" from 0 to its maximum slowly (crosses move, the "Within-cluster distance" metric drops, "Converged." appears in the caption).
3. Click tab "Algorithm showdown". Leave "Clusters (for algorithms that need k)" = 2 and "DBSCAN eps" = 0.3.
4. Scroll the 5x4 grid to the Moons and Circles rows; pause on the K-means column (split in half), then the DBSCAN column (grey points = noise).
5. Last second: the blue info box "No algorithm is best everywhere".

## Description
Watch K-means think step by step, then see four clustering algorithms (K-means, Gaussian mixture, Agglomerative, DBSCAN) tackle five datasets. Built with Claude Code using Streamlit and scikit-learn; no API calls. Narration is AI-generated.
