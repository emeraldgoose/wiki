---
title: SHAPE of Chain-of-Thought in Math Reasoning
description: HuggingFace Daily Papers — 2026-06-28 — Seoul National University
tags: [source, paper, huggingface, seoul-national-university, machine-learning]
locale: en
source_url: "https://arxiv.org/abs/2608.28600"
arxiv_id: 2608.28600
---

# SHAPE of Chain-of-Thought in Math Reasoning

**arXiv**: 2608.28600 | **Published**: 2026-06-28 | **Organization**: Seoul National University | **Submitted by**: Minjae Oh | **Upvotes**: 27

**Authors**: Paper authors (arXiv: 2608.28600),

 Jonghyun Song, Sangjun Song, Minjae Oh, Haesung Pyun, Sungsik Lee, Yohan Jo

## Abstract

Large language models (LLMs) achieve strong performance on mathematical reasoning benchmarks, yet the mathematically meaningful skills underlying their reasoning remain underexplored. We introduce SHAPE, a framework that analyzes Chain-of-Thought (CoT) trajectories through two lenses developed in mathematics education: (1) semantic spaces: the model's evolving mathematical interpretations of a problem (e.g., algebraic, geometric), and (2) heuristics: the specific mathematical actions taken within those spaces (e.g., simplifying the problem, working backward). We first use SHAPE to analyze the reasoning patterns of various models. Our findings reveal that the mathematical heuristics employed by a model better explain final answer correctness than traditional CoT features. Furthermore, models are likely to reach correct solutions by concentrating their reasoning effort within a few semantic spaces rather than exploring many disparate ones -- a pattern consistent with human behavior. Next, we utilize the SHAPE lens to evaluate whether post-training truly enhances mathematical proficiency. We find that reinforcement learning induces mode-seeking in heuristic usage. Lastly, we post-train LLMs by promoting diverse heuristics and demonstrate its effectiveness in improving accuracy. Overall, SHAPE provides a theoretically-grounded diagnostic framework for decoding LLM reasoning and offers a new path toward post-training LLMs for math reasoning. The code for our model is available at https://github.com/holi-lab/SHAPE-of-CoT

## Key Contributions

- **SHAPE**: analyzes CoT trajectories through two mathematics-education lenses — (1) semantic spaces (the model's evolving interpretations: algebraic, geometric, …) and (2) heuristics (actions within spaces: simplifying, working backward, …)
- **Descriptive finding**: the heuristics a model uses explain final-answer correctness better than traditional CoT features; correct solutions concentrate effort in few semantic spaces (human-like), rather than exploring many
- **Post-training finding**: RL induces mode-seeking in heuristic usage
- **Intervention**: post-training that promotes diverse heuristics improves accuracy

## Methodology

SHAPE lens applied to reasoning patterns of various models (pattern analysis), then to evaluating whether post-training truly enhances math proficiency, then as a training signal (diversity promotion).

## Results

Qualitative-structural results (no single headline number in the abstract): heuristic profiles beat CoT features at explaining correctness; concentration-beats-breadth pattern; RL mode-seeking diagnosis; diverse-heuristic training helps. Check the paper body for per-model tables.

## Relevance to Software Engineers

When debugging math reasoning, log *heuristics and semantic spaces*, not just CoT length — they predict correctness. If RL post-training plateaus, check for heuristic mode collapse and explicitly reward heuristic diversity. Code: https://github.com/holi-lab/SHAPE-of-CoT

## Related Concepts

- [LLM Training](../../concepts/ai-engineering/llm-training.md)
- [Transformer](../../concepts/machine-learning/transformer.md)
- [Attention](../../concepts/machine-learning/attention.md)

## References

- arXiv: https://arxiv.org/abs/2608.28600
- HuggingFace: https://huggingface.co/papers/2608.28600
- Scope: abstract-based; per-model analyses are in the full text
