---
title: Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall
description: HuggingFace Daily Papers — 2026-09-01 — Meta
tags: [source, paper, huggingface, meta]
locale: en
arxiv_id: 2609.01532
---

# Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall

**arXiv**: 2609.01532 | **Published**: 2026-09-01 | **Organization**: Meta | **Submitted by**: Jacqueline He | **Upvotes**: 1

**Authors**: Paper authors (arXiv: 2609.01532),

 Jacqueline He, Howard Yen, Shuyue Stella Li, Margaret Li, Hanqing Zeng, Yinglong Xia, Benyu Zhang, Zhuokai Zhao, Qiang Zhang, Pang Wei Koh, Luke Zettlemoyer, Wen-tau Yih

## Abstract

Logit-based knowledge distillation (KD) is used to train smaller language models (LMs) via supervision from stronger teachers, but whether its benefits are consistent across training stages remains unclear. Through controlled experiments, we find that forward Kullback-Leibler (KL) distillation--the standard KD formulation--with post-trained teachers behaves fundamentally differently during mid-training, an intermediate phase of self-supervised learning on curated corpora. Surprisingly, while forward KD simultaneously improves reasoning and factual recall during pre-training relative to standard next-token prediction (NTP), it instead slows factual recall acquisition during mid-training despite continued reasoning gains. We trace this stage dependence to an asymmetry in teacher confidence across data domains and the student's evolving knowledge state: teachers are more confident on procedural than knowledge-intensive data, while students acquire low-entropy factual knowledge earlier in training. To mitigate this imbalance, we propose Switch Distillation, a simple mid-training objective that distills on tokens where the teacher is confident, using teacher predictive entropy as a lightweight routing signal, and otherwise falls back to cross-entropy. Switch Distillation consistently outperforms existing distillation objectives across teacher sizes. Relative to standard NTP, it achieves 1.61-1.71x the reasoning performance and 1.13-1.19x the knowledge and commonsense performance while preserving 96.7-96.8% of factual recall. Crucially, these benefits persist after post-training: Switch Distillation closes the factual recall gap while maintaining 1.25-1.32x and 1.13-1.20x gains in reasoning and knowledge and commonsense, respectively.

## Key Contributions

- **Novel methodology** for [specific contribution]
- **Key insight** that addresses [problem]
- **Implementation details** relevant to software engineering,



## Methodology

- **Architecture**: [describe model architecture or framework]
- **Algorithms**: [key algorithms used]
- **Key equations/choices**: [important mathematical or computational choices]



## Results

- **Key results**: [main experimental findings with numbers]
- **Baseline comparisons**: [comparison with existing methods]
- **Reproducibility**: [whether results can be reproduced]



## Relevance to Software Engineers

- [To be filled: practical implications for SW engineers]

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.01532
- HuggingFace: https://huggingface.co/papers/2609.01532
