# 03 Semantic Map - 30s Short (9:16)

**Title:** I turned 60 sentences into a map of meaning (<60)
**App:** `03-semantic-map`. Needs embeddings + one tiny chat call per question. Record one or two questions.

## Voice-over (~76 words)
**Hook (0-3s):** "This map shows how an AI understands meaning."

**Beat 1 (3-11s) what you see:** "Sixty sentences on six topics, each turned into a vector, squashed to two dimensions. Same topic, same cluster. Nobody told it the topics."

**Beat 2 (11-19s) surprise:** "Now I ask: why does bread rise? A gold star lands right inside the cooking cluster, with dotted lines to the sentences it found."

**Beat 3 (19-27s) insight:** "Those are the nearest neighbours. Feed them to the model as context and you get a grounded answer. That's RAG."

**CTA (27-30s):** "Built with Claude Code, narrated by AI. Follow for more AI/ML builds."

## On-screen text
- 0-3s: "How AI sees meaning"
- 3-11s: "60 sentences, 6 topics, 1 map"
- 11-19s: "Ask: why does bread rise?"
- 19-27s: "Nearest neighbours -> RAG answer"
- 27-30s: "Follow for more AI/ML builds"

## Actions to record
1. Page loads with the title "Semantic Map"; hold on the coloured scatter (topics: Space, Cooking, Machine Learning, Football, Personal Finance, Ocean Life). Sidebar "Projection" radio = `t-SNE`. Hover one dot to show its sentence.
2. Click the "Ask something" text box, type `Why does bread rise?` (the app's own placeholder), press Enter.
3. Show the gold "query" star and dotted lines; then the "Retrieved" column (similarity score, topic, sentence) and the "RAG answer" column.
4. Optional 2s: switch "Projection" to `PCA` to show the clusters smear; "Top-k results" slider (1-8, default 3).
Note: the star sits at the similarity-weighted centroid of its top-k neighbours (an approximation, not a true projection of the query).

## Description
Every sentence becomes an embedding; similar meanings land close together. Ask a question and the app retrieves the nearest sentences and answers using only that context (RAG). 60 sentences, 6 topics, t-SNE or PCA. Built with Claude Code. Narration is AI-generated.

## Hashtags
#AI #Embeddings #RAG #MachineLearning #DataViz
