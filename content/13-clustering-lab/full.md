# 13 Clustering Lab - Full video (~7 min)

## Titles (pick one)
1. Watch K-means Think, Step by Step (and Where It Fails)
2. K-means vs DBSCAN vs GMM: Which Clustering Algorithm Wins?
3. Why K-means Fails on This Data (Live Comparison)

**Thumbnail text (<=4 words):** K-MEANS FAILS HERE

**Tags:** clustering, k-means, dbscan, gaussian mixture, unsupervised learning, scikit-learn, python, streamlit, machine learning, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Runs locally with scikit-learn, no API calls. Which dataset would you add to the grid?

**Description:**
K-means step by step, then four clustering algorithms on five datasets. I built it with Claude Code and the narration is AI-generated. The app is one file and runs locally.

Recording note: K-means numbers are from the app (Blobs, k=3, seed 0): the loop converged after 9 assignment steps and the within-cluster distance fell 450.1, 224.4, 183.3, 171.2, 167.7, 167.1. The elbow-chart inertias for k = 1 to 9 are 600, 314, 167, 140, 117, 99, 87, 75, 68. The accuracy scores for the algorithm comparison (adjusted Rand index against the true groups, 1.0 is perfect) were computed offline with the same generators and settings and are not shown in the app: Moons with k=2: K-means 0.46, single-linkage 1.00, DBSCAN 0.99; Circles with k=2: K-means 0.00, single-linkage 1.00, DBSCAN 0.86 (it found three clusters). The comparison grid in the app uses k=2 by default.

## Voice-over

### [0:00] Cold open
Here are three clouds of points, and no labels at all. [SCREEN: the app.] I drag the slider back to the start, and now watch the black crosses. Each step, every point joins its nearest cross, and then every cross moves to the middle of its points. Step by step, the crosses settle, and after nine steps nothing moves any more: that's K-means. But the second half of this video is about the places where it breaks. I built this with Claude Code, and the narration is AI-generated.

### [0:45] Unsupervised learning
In supervised learning you give the model examples with answers. In unsupervised learning there are no answers, and the algorithm has to find structure on its own. Clustering means finding groups of similar points.

K-means is the classic way to do it. You choose how many groups you want, called k, and the algorithm finds k centres. It's fast, it's simple, and it's usually the first thing people try. But it carries a hidden assumption about the shape of the groups, and that's what the second tab tests.

### [1:45] K-means in code
The whole algorithm is a short loop.

```python
rng = np.random.RandomState(int(seed))
cent = X[rng.choice(len(X), k, replace=False)]
steps = []  # (centroids, labels)
for _ in range(15):
    lab = np.argmin(((X[:, None] - cent[None]) ** 2).sum(2), 1)
    steps.append((cent.copy(), lab))
    new = np.array([X[lab == j].mean(0) if (lab == j).any() else cent[j] for j in range(k)])
    if np.allclose(new, cent):
        break
    cent = new
```

First, pick k of the points at random as the starting centres. That seed is a setting in the app, because a different start can give a different answer. Then loop. The first line computes the distance from every point to every centre and takes the nearest: that's the assignment step. The next line moves each centre to the mean of the points assigned to it, which is the update step. If no centre moved, we've converged and stop. I keep every step in a list so the slider can scrub through them.

### [3:00] Live demo
[SCREEN: app.] This is the Blobs dataset with three clusters. At the start the three crosses are three random points. The number on the right is the within-cluster distance: the total squared distance from each point to its own centre. At iteration zero it is four hundred and fifty. K-means is trying to make that number small.

[SCREEN] I step forward one iteration at a time. The crosses jump towards the middle of their groups, and the distance falls: two hundred and twenty-four, then one hundred and eighty-three, one hundred and seventy-one, then one sixty-eight. The improvements get smaller each time. The distance stops changing at about the fifth step, and the loop stops after nine, with the app marking it converged.

[SCREEN] The final distance is one hundred and sixty-seven. K-means never makes it worse, but it only finds a local optimum, so a different seed can end somewhere different.

### [4:30] Choosing k
[SCREEN: the elbow chart.] There's one more thing: how do you choose k? The app has an elbow chart that runs K-means for k from one to nine and plots the final distance. It falls from six hundred at k equals one to three hundred and fourteen at two and to one sixty-seven at three. After three, it keeps falling, but slowly, so the bend, the elbow, is at three. That matches how this data was generated.

### [5:15] The showdown
The second tab runs four algorithms on five datasets, all at once. K-means, a Gaussian mixture, which fits ellipses, agglomerative clustering with single linkage, which merges close neighbours, and DBSCAN, which grows clusters from dense regions.

```python
algos = {"K-means": lambda X: KMeans(k2, n_init=5, random_state=0).fit_predict(X),
         "Gaussian mixture": lambda X: GaussianMixture(k2, random_state=0).fit_predict(X),
         "Agglomerative": lambda X: AgglomerativeClustering(k2, linkage="single").fit_predict(X),
         "DBSCAN": lambda X: DBSCAN(eps=eps, min_samples=5).fit_predict(X)}
```

[SCREEN: the grid.] Each row is a dataset, each column an algorithm.

### [6:00] Reading the grid
[SCREEN] Look at the Moons row. Two interleaved half circles. K-means cuts straight through the middle instead, because it only knows how to draw round groups around a centre. The agglomerative and DBSCAN columns follow the curves. I also computed a score offline, the adjusted Rand index, where one is perfect. For the moons, K-means scores zero point four six, while single linkage gets one point zero and DBSCAN zero point nine nine.

[SCREEN] The circles are worse for K-means: a ring around a smaller ring has no useful straight cut, and its score is zero, which is no better than chance. DBSCAN does well, though its score is zero point eight six, because with this setting it splits the data into three clusters, and the grey points are the ones it calls noise. On the stretched blobs, which are tilted ellipses, K-means only knows round shapes, while the Gaussian mixture can model tilted ones.

[SCREEN] On the uniform noise row there are no real groups at all, and most of the algorithms still carve it into pieces. Clustering will happily return an answer, whether or not there is anything to find.

### [7:15] What I take from it
Every algorithm hides an assumption about what a cluster looks like: round, elliptical, dense, or connected. When your data matches it you win, and when it doesn't, you get a confident wrong answer. So plot your data first.

### [7:45] Honest limits
This is two-dimensional toy data, which is much friendlier than real data with dozens of columns. I used default-ish settings: a fixed k of two on the comparison tab, one DBSCAN radius, and single linkage only. The scores I quoted were computed offline with the same generators and are not shown in the app, and I only ran one random seed. I built this with Claude Code, and I read and ran the code, but you should read it yourself too.

### [8:25] What to build next
Next I'd let you upload your own CSV, add a silhouette score so you can judge clusters without true labels, and let you tune each algorithm's settings.

The code is in the description, with no API key and no cost. If you liked watching K-means think, follow for more AI and ML builds, and tell me which dataset should break an algorithm next.
