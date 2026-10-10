---
title: Verification-Aware Training for Speculative Decoding
description: HuggingFace Daily Papers — 2026-08-31 — NAVER AI Lab
tags: [source, paper, huggingface, naver-ai-lab]
locale: en
source_url: "https://arxiv.org/abs/2608.30135"
arxiv_id: 2608.30135
---

# Verification-Aware Training for Speculative Decoding

**arXiv**: 2608.30135 | **Published**: 2026-08-31 | **Organization**: NAVER AI Lab | **Submitted by**: Geonmo Gu | **Upvotes**: 5

**Authors**: Paper authors (arXiv: 2608.30135),

 Geonmo Gu, Byeongho Heo, HeeJae Jun, Yoohoon Kang, Sangmin Lee, Sangdoo Yun, Dongyoon Han

## Abstract

Speculative decoding accelerates large language model inference by using a draft model to generate candidate tokens, which are verified by the target model in a single forward pass. Verification proceeds sequentially and discards every position from the first rejection onward, yet existing draft training relies on token-level imitation of the target with a fixed per-position weighting that reflects neither property. We introduce Verification-Aware Training (VAT), a plug-in framework that simulates verification at every training step and turns the resulting accept and reject patterns into supervision. VAT consists of two components: (i) a verification head, a lightweight jointly trained binary classifier that supervises the draft model on whether each position survives sequential verification; (ii) verification-adaptive weighting, which replaces the fixed weighting schedule by keeping full weight up to each sample's first rejection point and re-anchoring the decay to start there. VAT modifies only the training objective, so it can be layered on top of existing methods without changing the draft architecture, the target model, or the inference procedure. Applied to EAGLE-3 and DFlash on Qwen3-4B, Qwen3-8B, and LLaMA-3.1-8B, VAT improves average acceptance length by up to 11.4% and wall-clock speedup by up to 8.7%, with consistent gains across math, code, and chat benchmarks. Code will be available at https://github.com/naver-ai/vat

## Key Contributions

- **Problem**: sequential verification discards everything from the first rejection on, but draft training uses fixed per-position imitation weights reflecting neither sequentiality nor rejection
- **VAT (Verification-Aware Training)**: plug-in that simulates verification every step — (i) verification head (lightweight joint binary classifier: does each position survive sequential verification?), (ii) verification-adaptive weighting (full weight up to each sample's first rejection, decay re-anchored there)
- **Compatibility**: training-objective-only change; layers onto existing methods without touching draft architecture, target model, or inference

## Methodology

Applied to EAGLE-3 and DFlash on Qwen3-4B, Qwen3-8B, and LLaMA-3.1-8B; evaluated on math, code, and chat benchmarks for acceptance length and wall-clock speedup.

## Results

| Finding | Number |
|---|---|
| Avg acceptance length | up to **+11.4%** |
| Wall-clock speedup | up to **+8.7%** |
| Generality | consistent gains across math/code/chat |

## Relevance to Software Engineers

If you serve LLMs with speculative decoding, VAT is a free upgrade — no inference change, just retrain the draft head with verification simulation. Weight supervision by survival, not position. Code forthcoming at https://github.com/naver-ai/vat

## Related Concepts

- [Speculative Decoding](../../concepts/ai-engineering/speculative-decoding.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)
- [Transformer](../../concepts/machine-learning/transformer.md)

## References

- arXiv: https://arxiv.org/abs/2608.30135
- HuggingFace: https://huggingface.co/papers/2608.30135
- Scope: abstract-based; per-model/bench tables are in the full text
