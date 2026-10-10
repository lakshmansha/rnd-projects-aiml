# Short: 16 CNN X-ray (30 s, 9:16)

**Title:** What does an AI actually look at? Grad-CAM X-ray (under 60 chars)
**Hashtags:** #DeepLearning #ComputerVision #GradCAM #PyTorch #Shorts

## Voice-over (about 75 words)
**[0-3s, hook]** "This neural network is 95 percent sure it's a banana. Here's where it looked."
**[3-11s, what you see]** "A real MobileNetV2 guesses the photo, and Grad-CAM paints the pixels that mattered, red for decisive."
**[11-19s, surprising moment]** "Now the cat. Tiger cat, 22 percent. Tabby, 13. I switch to the runner-up and the heat moves to different pixels."
**[19-27s, insight]** "Even a guess that's wrong has a reason you can see."
**[27-30s, CTA]** "Built with Claude Code. Follow for more AI and ML builds."

## On-screen text
- 0-3s: "95% BANANA. Where did it look?"
- 3-11s: "Red = decisive pixels"
- 11-19s: "Tiger cat 22% / tabby 13%" then "Switch guess, heat moves"
- 19-27s: "Not a black box"
- 27-30s: "Follow for more AI/ML builds"

## Exact actions to record (http://localhost:8516, viewport 540x960; no API calls)
1. Sidebar "Source" = Sample, "Sample" = banana.jpg. Show the three columns: centre crop, Grad-CAM heatmap, "Top 5 guesses" (banana about 95%).
2. Drag sidebar slider "Heatmap strength" from 0.7 to 1.0 and back.
3. Select Sample = cat.jpg. Show the first option in "Explain which guess?" (tiger cat, 22%), then click the second (tabby, 13%); the heatmap changes.
4. End on the caption about 1,000 ImageNet classes.

## Description
CNN X-ray runs a real MobileNetV2 (ImageNet) on your photo and uses Grad-CAM to show which pixels drove each guess. Built with Claude Code using PyTorch and Streamlit; no API calls. Narration is AI-generated.
