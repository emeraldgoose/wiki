---
title: "DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection"
description: HuggingFace Daily Papers — 2026-08-31 — SpatialAxiom
tags: [source, paper, huggingface, spatialaxiom, machine-learning]
locale: en
source_url: "https://arxiv.org/abs/2608.30209"
arxiv_id: 2608.30209
---

# DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection

**arXiv**: 2608.30209 | **Published**: 2026-08-31 | **Organization**: SpatialAxiom | **Submitted by**: hongyuyang | **Upvotes**: 2

**Authors**: Paper authors (arXiv: 2608.30209),

 Yuyang Hong, Jinhui Guo, Jiaqi Gu, Lubin Fan, Ruixiang Wang, Kun Ding, Yue Wu, Shiming Xiang, Jieping Ye

## Abstract

Visual instruction tuning is crucial for advancing the vision-language alignment and instruction-following capabilities of Vision-Language Models (VLMs). However, identifying optimal subsets under a fixed ratio constraint from rapidly expanding datasets remains a significant bottleneck. While existing methods largely depend on distribution diversity or heuristic filtering, they often overlook the internal coherence within individual samples. To bridge this gap, we propose Data Intrinsic Consistency (DIC), a self-scoring metric designed to quantify the sample-level inter-component consistency. DIC consists of two modules: Visual Information Consistency (VIC), evaluating the alignment between visual content and instructions, and Response Information Consistency (RIC), assessing response coherence relative to the instruction. Building upon DIC, we introduce Data Intrinsic Consistency Selection (DICS), an adaptive data selection method that optimizes the trade-off between high intra-sample consistency and global distributional diversity under varying data budgets. Extensive experiments demonstrate that DICS consistently outperforms state-of-the-art methods across diverse dataset scales and model architectures, surpassing full-dataset fine-tuning while using only 25% of the LLaVA-1.5-665K data. We further curate DICS-6M, a 6M-sample multi-modal instruction corpus that enables the largest-scale visual instruction selection study to date; remarkably, DICS reaches 94.52\% of the official InternVL3-8B-Instruct performance using less than 25\% of its reported training data. Code can be seen at https://github.com/cqu-student/DICS

## Key Contributions

- **DIC (Data Intrinsic Consistency)**: self-scoring metric for intra-sample coherence — VIC (visual content ↔ instruction alignment) + RIC (response coherence relative to instruction)
- **DICS selection**: adaptively trades high intra-sample consistency against global distributional diversity under varying data budgets, instead of relying on diversity/heuristics alone
- **DICS-6M**: 6M-sample multimodal instruction corpus enabling the largest-scale visual-instruction selection study to date

## Methodology

Score every sample with DIC (VIC + RIC), then select under a fixed ratio constraint balancing top-consistency samples with distribution coverage. Evaluated across dataset scales and model architectures.

## Results

| Finding | Number |
|---|---|
| vs full-dataset fine-tuning | surpasses it with **25%** of LLaVA-1.5-665K data |
| vs official InternVL3-8B-Instruct | **94.52%** of its performance with **<25%** of reported training data |
| Generality | consistently beats SOTA selection across scales and architectures |

## Relevance to Software Engineers

When instruction-tuning VLMs on a data budget, filter by intra-sample consistency (does the response actually cohere with the instruction and image?), not just diversity. 25%-of-data beating full-data fine-tuning is a direct training-cost lever. Code: https://github.com/cqu-student/DICS

## Related Concepts

- [Embeddings](../../concepts/machine-learning/embedding.md)
- [Transformer](../../concepts/machine-learning/transformer.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2608.30209
- HuggingFace: https://huggingface.co/papers/2608.30209
- Scope: abstract-based; per-scale tables are in the full text
