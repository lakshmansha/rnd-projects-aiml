# Full video: 16 CNN X-ray (about 10 min)

Facts used (all from app.py or real runs): MobileNetV2 with IMAGENET1K_V2 weights, 3.5M parameters, 1,000 ImageNet classes, 224x224 centre crop, Grad-CAM on `model.features`. Sample results: banana 95%; cat = tiger cat 22% / tabby 13%; Labrador 20%; pizza 19% vs frying pan 18%. No API calls.

## Chapters (YouTube timestamps)
- 0:00 Cold open: 95% banana
- 0:30 Why you should care how a model decides
- 1:45 What a CNN and Grad-CAM are, in one picture
- 3:00 The build: the key 20 lines
- 5:00 Live demo: banana, cat, Labrador, pizza
- 7:15 What surprised me
- 8:30 Honest limits
- 9:15 What I'll build next + thanks

## Title options
1. I made a neural network show me where it's looking (Grad-CAM)
2. Is it a cat? What the AI actually looks at, in 20 lines of PyTorch
3. X-raying a neural network: 95% banana, 22% cat

## Thumbnail text (max 4 words)
"WHERE AI LOOKS" (alt: "X-RAY AN AI")

## Voice-over script (about 1,400 words)

### [0:00] Cold open (30 s)
This neural network is ninety-five percent sure this photo is a banana. Nice. But here is the question that bugged me: where did it look to decide that? Was it the banana? The background? The table? [pause] In the next ten minutes I will open the box, and you will see, pixel by pixel, what a real image classifier pays attention to. And I will show you the exact twenty lines of code that make it possible. [pause] I'm going to be upfront: I built this with Claude Code as my pair programmer, and the narration you hear is AI-generated. Everything you see running is real.

### [0:30] Why it matters (75 s)
Image models are everywhere: phone cameras, medical scans, self-driving cars. And almost all of them give you the same kind of answer: a label and a confidence number. "Banana, ninety-five percent." That number tells you nothing about why.

Why does that matter? Because models can be right for the wrong reason. A famous example is a classifier that learned to spot a husky by the snow in the background. It looks accurate right up until you show it a husky on grass.

So before I trust a model, I want to see its evidence. The technique I'm using is called Grad-CAM. It takes the model's own gradients, the signal it uses to learn, and turns them into a heat map. Red means "these pixels pushed the decision hard". Blue means "barely mattered". It does not need to retrain anything, and it works on almost any convolutional network.

### [1:45] The idea in one minute (75 s)
Here's the whole idea. A convolutional network, a CNN, slides small filters over the picture. Early layers find edges. Later layers find textures, then parts, then objects. By the last convolutional layer you have a stack of feature maps, each one answering a question like "is there something curved and yellow here?" at every location.

Then the network collapses those maps into a score for each of its one thousand classes. The question Grad-CAM asks is simple: for the class I care about, say banana, how much does each feature map contribute? We find out with the gradient. Take the banana score, ask how it changes if each feature map changes, and average that over the whole map. That average is a weight. Multiply each feature map by its weight, add them up, throw away the negative bits, and stretch the result back to the size of the photo. That is your heat map.

The model here is MobileNetV2, trained on ImageNet. It has about three and a half million parameters, small enough to run on my laptop CPU with no graphics card and no API calls at all.

### [3:00] The build (120 s)
The app is one Python file with Streamlit. Loading the model is two lines: I ask torchvision for MobileNetV2 with the ImageNet weights, and put it in eval mode. Streamlit caches it so it loads once.

Now the heart of it. Here is the real function:

```python
def gradcam(model, x, cls=None):
    feats = {}
    h = model.features.register_forward_hook(lambda m, i, o: feats.update(a=o))
    try:
        x = x.clone().requires_grad_(True)
        logits = model(x)
        probs = logits.softmax(1)[0]
        cls = int(probs.argmax()) if cls is None else cls
        grads, = torch.autograd.grad(logits[0, cls], feats["a"])
    finally:
        h.remove()
    w = grads.mean(dim=(2, 3), keepdim=True)
    cam = F.relu((w * feats["a"]).sum(1, keepdim=True))
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)[0, 0].detach().numpy()
    cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-9)
    return probs.detach().numpy(), cam, cls
```

Let me walk through it. First, a forward hook on `model.features`. That's a little spy that grabs the output of the last convolutional block, the feature maps, while the image goes through.

Then I run the model and take the softmax, which gives the probabilities. If you didn't tell me which class to explain, I use the winner.

The key line is `torch.autograd.grad`. It asks: how does the score for my class change with respect to those feature maps? That is the gradient.

Next, `grads.mean` over the height and width: one weight per feature map. Multiply the weights into the maps, sum, and apply ReLU, because I only care about evidence in favour of the class. Interpolate up to two hundred and twenty-four pixels, and normalise to zero-to-one. And that's it. Roughly twenty lines.

Notice the `cls` argument. It lets me ask "show me where you looked for the second-best guess", which turns out to be the most fun part of the demo.

The rest of the app is small: a function that blends red-to-blue colour into the photo with a strength slider, a top-five list, and an input chooser for samples, uploads or the webcam.

### [5:00] Live demo (135 s)
Let's run it. Sample: banana. The left image is what the network really sees: a two-hundred-twenty-four pixel centre crop, because that's what it was trained on. In the middle, the Grad-CAM overlay. Banana, ninety-five percent, and the red sits right on the fruit. That's what I hoped for.

I'll drag the heatmap strength slider to make the overlay stronger. Same evidence, easier to see.

Now the cat. The top guess is tiger cat at twenty-two percent, and the next is tabby at thirteen. Not very confident, because ImageNet has several kinds of cat and they overlap. Watch what happens when I pick the second guess in "Explain which guess?". The heat moves. For tabby, it highlights different pixels than for tiger cat. Two answers, two different sets of evidence.

Next, the dog. Labrador, around twenty percent. Again, much lower than the banana. I'll pick the runner-up and again the map changes.

And the pizza. Pizza gets nineteen percent, and a frying pan gets eighteen. That is basically a coin flip. If I click on the frying pan, the heat map shows which pixels support that wrong-but-close answer (describe what you actually see on screen when recording). The point: a one-point gap means the model genuinely can't separate them.

You can also upload your own photo, or use the webcam. I'd encourage you to try it with something weird.

### [7:15] What surprised me (75 s)
Three things surprised me.

One: confidence is low in a lot of normal cases. Only the banana was above ninety percent. The cat, the Labrador and the pizza all came out under twenty-three percent. Because ImageNet splits the world into very fine categories, probability gets shared among neighbours. Low confidence does not mean wrong; it often means "several right answers".

Two: the runner-up has its own evidence. The heat map for the second guess lives in different pixels. A single number hides that completely.

Three: how little code it took. The whole explanation technique is about twenty lines.

And a bonus I should be honest about: a heat map looks convincing, and that is a risk. It looks like an explanation, but it's a coarse picture, because the last block's feature map is small and then stretched up.

### [8:30] Honest limits (45 s)
Let me be straight about the limits. Grad-CAM is low resolution; it tells you roughly where, not exactly which pixel. It explains this model's gradients, not the model's "thoughts".

The network only knows one thousand ImageNet classes. Show it something else, a drawing, a person, a spoon in a weird light, and it will still pick one of the thousand and sometimes sound sure about it. The app says that in a caption, and I think it's the most important line in it.

Also, I only tried a handful of sample photos, so don't read my percentages as a benchmark. They are what this model produced on these four images.

And yes, I wrote this with Claude Code. I read and ran the code, but I would call myself the director, not the sole author.

### [9:15] Next + CTA (45 s)
What next? Ideas on my list: an attention visualiser for the tiny GPT I built earlier, so we can do the same X-ray for language; swapping in a bigger network and comparing heat maps; and a bias demo showing the husky-on-snow failure on purpose.

If you enjoyed this, I built sixteen AI and ML projects like it and the code is in the description. Subscribe, and tell me in the comments which photo I should feed it. Thanks for watching.

## Shot list
| Time | Screen | Code | Avatar |
|---|---|---|---|
| 0:00-0:30 | Screen: banana sample with Grad-CAM, zoom on red area | | Avatar full screen for "I'll open the box", then PiP |
| 0:30-1:45 | Slide/B-roll: husky-on-snow concept (generated graphic, no stock photos of real people) | | Avatar PiP |
| 1:45-3:00 | Animated diagram: feature maps -> weights -> heat map (simple slides) | | Avatar PiP |
| 3:00-5:00 | | Code editor: `gradcam` function highlighted line by line; then `heat()` and `load()` briefly | Avatar small PiP |
| 5:00-7:15 | Screen: app at 1920x1080, banana -> slider -> cat (switch guess) -> dog -> pizza (pan) | | Avatar hidden in demo, back for reactions |
| 7:15-8:30 | Screen: top-5 bars side by side; text overlays of percentages | | Avatar PiP |
| 8:30-9:15 | Screen: the "1,000 ImageNet classes" caption | | Avatar full screen |
| 9:15-10:00 | End card with 2 video suggestions | | Avatar full screen |

Recording note: all photos are the repo's own `16-cnn-xray/samples/*.jpg` (banana, cat, dog, pizza). Check frames for no private content before upload.

## Description
I open the black box of an image classifier. A real MobileNetV2 (ImageNet, 3.5M parameters) guesses what is in a photo, and Grad-CAM, about 20 lines of PyTorch, paints the pixels that drove each guess. We try a banana (95%), a cat (tiger cat 22%, tabby 13%), a Labrador (20%) and a pizza (19% vs frying pan 18%).

Built with Claude Code (AI pair programmer). The narration is AI-generated. No API calls; runs on CPU.

Chapters: see timestamps above.
Code: link to the repo (add before upload).
More builds: 16 AI/ML demos in this series.

## Tags
grad-cam, explainable ai, pytorch, mobilenetv2, computer vision, cnn, deep learning, image classification, streamlit, claude code, xai, machine learning

## Pinned comment
Which photo should I feed it next? Reply with something weird (a drawing, a meme, your pet) and I'll run it and show the heat map. Also: narration is AI-generated and the app was built with Claude Code, so if you spot a mistake, tell me and I'll pin the correction.
