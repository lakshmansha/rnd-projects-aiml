# 18 Attention X-ray: Short

**Title (<60):** I looked inside a GPT: where does each head look?
**Hook:** "A tiny GPT is reading Shakespeare, and I can see where each attention head looks."
**Facts (measured on 200 random 64-character windows of the training text):** layer 1 head 2 puts 99% of its attention on the previous character; head 1 puts 97% on the character two back; head 4 78% and head 3 59% on the previous one; by layer 4 no head exceeds about 21% on itself, the previous or the one before.
**Description:** A character-level GPT (about 0.8M parameters, trained 2,000 steps) reads a line of Shakespeare and every attention head of every layer is plotted. Built with Claude Code; narration is AI-generated.
**Hashtags:** #Transformer #Attention #GPT #MachineLearning #Python
