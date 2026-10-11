# 06 Draw a Digit - Full video (~10 min)

## Titles (pick one)
1. I Drew a Digit and 4 ML Models Voted On It
2. Classic Machine Learning Still Works (Live Demo)
3. Why Can 99% Accurate Models Still Misread You?

**Thumbnail text (<=4 words):** 99% ACCURATE... BUT?

**Tags:** machine learning, scikit-learn, digit classifier, SVM, random forest, k-NN, MLP, handwritten digits, streamlit, python, data augmentation, claude code, ai project

**Pinned comment:** Built with Claude Code; narration is AI-generated. Everything here is from the real repo (rnd-projects-aiml, project 06) and runs with no API calls. Draw a nasty digit and tell me which model you think wins!

**Description:**
Four classic ML models train live on 1,797 tiny 8x8 digit images, then vote on a digit you draw. No API calls, runs on a laptop. I built it with Claude Code and the narration is AI-generated.
Chapters:
00:00 Cold open
00:35 Why this matters
01:45 How it's built
05:00 Live demo
07:00 What surprised me
08:30 Honest limits
09:20 What to build next

## Chapters and shot list
| Time | Chapter | Shot |
|---|---|---|
| 0:00 | Cold open | Screen: draw a digit, bar chart appears. Avatar overlay in corner |
| 0:35 | Why it matters | Avatar full frame, then slide of an 8x8 digit grid |
| 1:45 | Build walkthrough | Code: `train()`, `augment()`, `to_8x8()`, the vote lines in app.py, highlighted piece by piece |
| 5:00 | Live demo | Screen: app, draw 7, 3, a sloppy 4, then "🧹 Clear" |
| 7:00 | Surprises | Screen: accuracy table; code comment in `to_8x8` |
| 8:30 | Limits | Avatar + screen of a misread drawing (record one if it happens) |
| 9:20 | Next + CTA | Avatar, end card |

Recording note: all numbers below were re-measured headlessly using the app's own split (test_size=0.25, random_state=0, stratified), 1,347 train / 450 test images, 6,735 after augmentation. Test accuracy: SVM 99.8%, k-NN 98.4%, random forest 98.2%, MLP 98.0%. Confirm against the table on screen when recording and read what is shown.

## Voice-over (~1,400 words)

### 0:00 Cold open
Four different AI models are about to look at my handwriting, and they are going to vote on what I wrote. [SCREEN: draw a 7, lift the mouse.] That blurry blob is what they actually see: an eight by eight grid of pixels. Sixty-four numbers. From that, a support vector machine, a small neural network, a random forest and a nearest-neighbour model each give an answer. Most of the time they agree. Sometimes they don't, and that is where it gets interesting. I'm going to show you how I built this, and why a few lines of unglamorous preprocessing mattered more than the choice of model.

### 0:35 Why it matters
Quick honesty first: I built this with Claude Code, and the narration you're hearing is AI-generated. The code, though, is real and short, and I'll show it.

Why does a digit classifier matter in a world of giant language models? Because it is the cleanest place to understand what machine learning actually is. You have examples with labels. You pick a model. You fit it. You test it on data it has never seen. That loop is the same for the biggest models in the world; it is just easier to see here.

The dataset is the scikit-learn digits set: one thousand seven hundred and ninety-seven images, each eight by eight pixels, with values from zero to sixteen. That is tiny, which is the point. The app trains four models when it starts, on a laptop CPU, with no GPU and no API calls.

There is also a trap hiding in benchmark numbers. A model that scores ninety-nine percent on a test split can still stumble on your own handwriting. Understanding why is the real lesson of this video.

### 1:45 Build walkthrough
The app is one file, about a hundred and twenty lines, in Streamlit. Three pieces matter: training, a bit of augmentation, and converting your drawing into something the models can read.

First, training. This is the function, cached so it only runs once:

```python
@st.cache_resource(show_spinner="Training 4 models...")
def train():
    d = load_digits()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.25, random_state=0, stratify=d.target)
    Xa, ya = augment(Xtr, ytr)
    models = {
        "SVM (RBF)": SVC(gamma=0.001, C=10, probability=True, random_state=0),
        "Neural net (MLP)": MLPClassifier((64, 32), max_iter=400, random_state=0),
        "Random forest": RandomForestClassifier(200, random_state=0, n_jobs=-1),
        "k-NN (k=5)": KNeighborsClassifier(5),
    }
```

We hold out a quarter of the images, four hundred and fifty of them, as a test set. Stratify means each digit appears in the same proportion in both halves. Then four models, all from scikit-learn, all trained on the same data. The accuracy table in the app is computed on that held-out quarter, never on the training images.

Second, augmentation. Hand-drawn digits are not perfectly centred, so I shift every training image by one pixel in four directions:

```python
def augment(X, y):
    Xs, ys = [X], [y]
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        Xs.append(np.array([shift(im.reshape(8, 8), (dy, dx), cval=0).ravel() for im in X]))
        ys.append(y)
    return np.vstack(Xs), np.concatenate(ys)
```

That turns one thousand three hundred and forty-seven training images into six thousand seven hundred and thirty-five. Five times the data, for free, and the models become less sensitive to exactly where you put the digit.

Third, the bridge between your mouse and the model. The browser canvas is downsampled to fifty-six by fifty-six, and then Python reduces that to eight by eight:

```python
def to_8x8(img):
    a = np.array(img, dtype=float).reshape(SIZE, SIZE) / 255
    ys, xs = np.where(a > 0.15)
    if len(ys) == 0:
        return None
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    f = 8 / max(a.shape)
    a = zoom(a, f, order=1)
    out = np.zeros((8, 8))
    h, w = a.shape
    out[(8 - h) // 2:(8 - h) // 2 + h, (8 - w) // 2:(8 - w) // 2 + w] = a[:8, :8]
    return np.clip(out / out.max() * 16, 0, 16)
```

Read it top to bottom. Find where the ink is. Crop to the bounding box. Scale so the longer side is eight pixels. Centre it in an eight by eight box. Then stretch the brightness to the dataset's zero to sixteen range. Each step exists to make my drawing look like the training images.

Finally the vote. Each model gives probabilities for the ten digits, we take each model's top pick, and the most common answer is the majority vote:

```python
probs = {n: m.predict_proba(x.reshape(1, -1))[0] for n, m in models.items()}
votes = {n: int(p.argmax()) for n, p in probs.items()}
final = pd.Series(votes).value_counts().idxmax()
```

Three lines. That's an ensemble.

The drawing canvas itself is a small inline Streamlit component written in JavaScript, so there is no extra package to install. When you lift the mouse, it sends the pixels back to Python.

### 5:00 Live demo
[SCREEN: app.] Here's the app. On the left, the canvas and the accuracy table. On unseen data, when I ran the same split and augmentation headlessly, the SVM scored ninety-nine point eight percent, k-nearest-neighbours ninety-eight point four, the random forest ninety-eight point two, and the neural net ninety-eight point zero. So all four are in the ninety-eight to ninety-nine percent range.

Let me draw a seven. Big, one digit, like a dot-matrix display, as the tip says. [Draw, release.] There's the eight by eight view, the majority vote, and on the right a bar chart of each model's probability for each digit. On this drawing the SVM and k-nearest-neighbours both said seven, while the neural net and the random forest both said five. That is a two-two split, and the app showed seven. Keep that in mind, because I come back to it in the limits.

Now a three. [Draw.] The SVM, the forest and k-nearest-neighbours say three. The neural net says eight, with near certainty. The majority wins, but the dissenter was confident, and that is worth noticing.

Now let me be mean and draw a messy four with an open top. [Draw.] The SVM, the neural net and the forest say four. k-nearest-neighbours says one. The majority vote gives one answer, but the chart tells you how confident each model was. That's the difference between a prediction and a prediction you should trust.

The cropping step enlarges any digit to fill the box, so size matters little, but shape does.

### 7:00 What surprised me
Three things.

One: the preprocessing mattered more than the model. A comment in the code says it directly: centring by centre of mass hurt top-heavy digits like seven, so I centre by the bounding box instead. That's the kind of thing you only learn by drawing digits and watching them get misread.

Two: simple models are very good here. A k-nearest-neighbours classifier, which essentially remembers the training images and looks for the closest ones, scores about ninety-eight percent. A neural network is not better on a dataset this small.

Three: the accuracy table is a statement about the test set, not about you. All four models score high on dataset images, but your hand-drawn digit comes from a different distribution. Augmentation narrows that gap; it does not close it.

### 8:30 Honest limits
Let me be straight about what this is not. It is eight by eight pixels, so it is a toy compared with real handwriting recognition. Some drawings will be misread, especially digits with unusual shapes or strokes that blur together at that resolution. I have not measured accuracy on my own drawings across many samples, so I won't claim a number for it; the ninety-eight to ninety-nine percent figure is for the held-out part of the dataset only. The majority vote has no sophisticated tie-break, so a two-two split is close to arbitrary. And the models use a fixed random seed, so you're seeing one run, not an average.

I also built this with an AI assistant. I ran the code and checked the numbers, but you should read it yourself before trusting it.

### 9:20 What to build next
If you want to take this further: swap the classic models for a small convolutional network and compare. There is a CNN project in the same repository. You could also collect your own drawings, label them, and measure real accuracy, which would be a more honest benchmark than the table.

All the code is in the repository linked below, no API key needed. If this was useful, follow for more AI and ML builds, and tell me in the comments which digit fooled your models.
