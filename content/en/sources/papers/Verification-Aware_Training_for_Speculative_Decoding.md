---
title: Verification-Aware Training for Speculative Decoding
description: HuggingFace Daily Papers — 2026-08-31 — NAVER AI Lab
tags: [source, paper, huggingface, naver-ai-lab]
locale: en
arxiv_id: 2608.30135
---

# Verification-Aware Training for Speculative Decoding

**arXiv**: 2608.30135 | **Published**: 2026-08-31 | **Organization**: NAVER AI Lab | **Submitted by**: Geonmo Gu | **Upvotes**: 5

**Authors**: Paper authors (arXiv: 2608.30135),

 Geonmo Gu, Byeongho Heo, HeeJae Jun, Yoohoon Kang, Sangmin Lee, Sangdoo Yun, Dongyoon Han

## Abstract

Speculative decoding accelerates large language model inference by using a draft model to generate candidate tokens, which are verified by the target model in a single forward pass. Verification proceeds sequentially and discards every position from the first rejection onward, yet existing draft training relies on token-level imitation of the target with a fixed per-position weighting that reflects neither property. We introduce Verification-Aware Training (VAT), a plug-in framework that simulates verification at every training step and turns the resulting accept and reject patterns into supervision. VAT consists of two components: (i) a verification head, a lightweight jointly trained binary classifier that supervises the draft model on whether each position survives sequential verification; (ii) verification-adaptive weighting, which replaces the fixed weighting schedule by keeping full weight up to each sample's first rejection point and re-anchoring the decay to start there. VAT modifies only the training objective, so it can be layered on top of existing methods without changing the draft architecture, the target model, or the inference procedure. Applied to EAGLE-3 and DFlash on Qwen3-4B, Qwen3-8B, and LLaMA-3.1-8B, VAT improves average acceptance length by up to 11.4% and wall-clock speedup by up to 8.7%, with consistent gains across math, code, and chat benchmarks. Code will be available at https://github.com/naver-ai/vat

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

- arXiv: https://arxiv.org/abs/2608.30135
- HuggingFace: https://huggingface.co/papers/2608.30135
