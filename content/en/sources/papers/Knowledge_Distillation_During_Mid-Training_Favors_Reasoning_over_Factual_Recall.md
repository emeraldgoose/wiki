---
title: Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall
description: HuggingFace Daily Papers — 2026-09-01 — Meta
tags: [source, paper, huggingface, meta, machine-learning]
locale: en
source_url: "https://arxiv.org/abs/2609.01532"
arxiv_id: 2609.01532
---

# Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall

**arXiv**: 2609.01532 | **Published**: 2026-09-01 | **Organization**: Meta | **Submitted by**: Jacqueline He | **Upvotes**: 1

**Authors**: Paper authors (arXiv: 2609.01532),

 Jacqueline He, Howard Yen, Shuyue Stella Li, Margaret Li, Hanqing Zeng, Yinglong Xia, Benyu Zhang, Zhuokai Zhao, Qiang Zhang, Pang Wei Koh, Luke Zettlemoyer, Wen-tau Yih

## Abstract

Logit-based knowledge distillation (KD) is used to train smaller language models (LMs) via supervision from stronger teachers, but whether its benefits are consistent across training stages remains unclear. Through controlled experiments, we find that forward Kullback-Leibler (KL) distillation--the standard KD formulation--with post-trained teachers behaves fundamentally differently during mid-training, an intermediate phase of self-supervised learning on curated corpora. Surprisingly, while forward KD simultaneously improves reasoning and factual recall during pre-training relative to standard next-token prediction (NTP), it instead slows factual recall acquisition during mid-training despite continued reasoning gains. We trace this stage dependence to an asymmetry in teacher confidence across data domains and the student's evolving knowledge state: teachers are more confident on procedural than knowledge-intensive data, while students acquire low-entropy factual knowledge earlier in training. To mitigate this imbalance, we propose Switch Distillation, a simple mid-training objective that distills on tokens where the teacher is confident, using teacher predictive entropy as a lightweight routing signal, and otherwise falls back to cross-entropy. Switch Distillation consistently outperforms existing distillation objectives across teacher sizes. Relative to standard NTP, it achieves 1.61-1.71x the reasoning performance and 1.13-1.19x the knowledge and commonsense performance while preserving 96.7-96.8% of factual recall. Crucially, these benefits persist after post-training: Switch Distillation closes the factual recall gap while maintaining 1.25-1.32x and 1.13-1.20x gains in reasoning and knowledge and commonsense, respectively.

## Key Contributions

- **Stage-dependence finding**: forward-KL distillation improves reasoning *and* factual recall in pre-training vs NTP, but during mid-training it keeps reasoning gains while *slowing* factual-recall acquisition
- **Mechanism**: teacher confidence asymmetry across domains (confident on procedural, less on knowledge-intensive) meets the student's state (low-entropy facts learned early)
- **Switch Distillation**: distill only where the teacher is confident (predictive-entropy routing), else fall back to cross-entropy; beats existing KD objectives across teacher sizes

## Methodology

Controlled experiments comparing forward KD vs standard next-token prediction in pre-training and mid-training (self-supervised learning on curated corpora), tracing confidence × knowledge-state interaction, then testing entropy-routed Switch Distillation through post-training.

## Results

| Finding | Number |
|---|---|
| Switch vs NTP: reasoning | **1.61–1.71x** |
| Switch vs NTP: knowledge & commonsense | **1.13–1.19x** |
| Factual recall preserved | **96.7–96.8%** |
| After post-training | gap closed; reasoning **1.25–1.32x**, knowledge **1.13–1.20x** retained |

## Relevance to Software Engineers

If you distill into small LMs mid-training, do not distill blindly — route by teacher entropy or you will tax factual recall. Switch Distillation is a two-line change (entropy gate + CE fallback) with 1.6x-class reasoning payoff that survives post-training.

## Related Concepts

- [Knowledge Distillation](../../concepts/machine-learning/knowledge-distillation.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)
- [Transformer](../../concepts/machine-learning/transformer.md)

## References

- arXiv: https://arxiv.org/abs/2609.01532
- HuggingFace: https://huggingface.co/papers/2609.01532
- Scope: abstract-based; teacher-size sweeps are in the full text
