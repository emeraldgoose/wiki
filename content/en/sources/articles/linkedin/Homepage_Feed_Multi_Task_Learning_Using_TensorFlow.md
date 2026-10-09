---
title: Homepage Feed Multi-Task Learning Using TensorFlow
description: LinkedIn's unified multi-task ranking model for homepage feed — shared representations, task towers, joint optimization
date: 2021-06-03
tags: [source, linkedin, feed, ranking, multi-task-learning, tensorflow]
locale: en
source_url: "https://www.linkedin.com/blog/engineering/feed/homepage-feed-multi-task-learning-using-tensorflow"
blog: linkedin
author: Ian Ackerman
---

# Homepage Feed Multi-Task Learning Using TensorFlow

Feed ranking must predict many member behaviors at once — clicks, likes, comments, shares, dwells, skips. This post describes LinkedIn's move from **separate per-behavior models** to a **unified multi-task deep learning framework in TensorFlow**, improving both serving efficiency and member engagement.

## Why multi-task: limits of one-model-per-behavior

- Each behavior model learned its own representation — duplicated compute in training and serving (one forward pass per model per request).
- Rare behaviors (comments, shares) had thin training signal in isolation; related-task signal went unused.
- Independent models could disagree with no principled fusion.

## Model: shared bottom + task towers

- **Shared bottom MLP** over member/item/context features learns a common representation capturing what generalizes across behaviors.
- **Task-specific towers** map the shared representation to each objective (click, like, comment, share, dwell…), with **joint optimization** of a weighted multi-task loss.
- MTL acts as implicit regularization: noisy sparse heads (shares) borrow structure from dense heads (clicks), while one forward pass amortizes serving cost across all heads.

## Handling task differences

- **Negative transfer** is the core risk: unrelated tasks pull the shared representation in conflicting directions. Task grouping and loss weighting keep dominant heads from hijacking gradients.
- This shared-bottom design is the direct ancestor of the later MMoE/GR evolution: the 2026 Generative Recommender keeps the same multi-task philosophy but replaces the shared bottom with a sequential transformer + per-task gating (passive vs. active tasks).

## Results and significance

- Consolidated serving footprint (one model instead of N) with better engagement than the per-task ensemble — the pattern that made MTL the default Feed ranking shape at LinkedIn for the following years.
- Conceptually superseded (not invalidated) by the LLM-retrieval + GR stack of 2026, which extends MTL with sequential history and semantic embeddings.

## Takeaways for SW engineers

1. Start MTL with shared-bottom; add gating (MMoE) only when task conflict is measured.
2. Watch loss scales across heads — normalize or weight so rare-task gradients survive.
3. One forward pass / many heads is primarily a serving-cost win that also regularizes.

## Related concepts

- `sources/articles/linkedin/Engineering_the_Next_Generation_of_LinkedIn_Feed.md` (GR + MMoE successor)
- `concepts/machine-learning/transformer.md`

## References

- Source: https://www.linkedin.com/blog/engineering/feed/homepage-feed-multi-task-learning-using-tensorflow
