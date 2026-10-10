---
title: Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation
description: HuggingFace Daily Papers — 2026-08-25 — Kakao Corp.
tags: [source, paper, huggingface, kakao-corp., machine-learning]
locale: en
source_url: "https://arxiv.org/abs/2608.24293"
arxiv_id: 2608.24293
---

# Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation

**arXiv**: 2608.24293 | **Published**: 2026-08-25 | **Organization**: Kakao Corp. | **Submitted by**: lee | **Upvotes**: 11

**Authors**: Yeonkyeong Lee, Hyunsung Go, Jongmin Kim, Sewoong Lim, Donghoon Lee

## Abstract

Latent diffusion models have emerged as a dominant framework for high-fidelity image and video synthesis, operating in compact latent spaces with variational autoencoders (VAEs) to enhance computational efficiency without compromising visual quality. However, conventional VAEs are suboptimal for video data as they employ fixed compression ratios that cannot adapt to the varying complexity of spatio-temporal content. We present KATok (Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation), a transformer-based VAE that incorporates an adaptive token selector which is jointly learned with latent tokens. By evaluating each token's content-richness as keep-or-drop probability, the token selector effectively discards uninformative tokens, naturally allowing data-dependent compression. Applying adaptive tokenization to diffusion models may cause spatial misalignment, as token dropping can disturb the original spatio-temporal structure. To alleviate this issue, we propose two position-prediction strategies: cascaded and joint generation, to ensure spatial consistency. We empirically show that our model achieves strong reconstruction and generation quality at a state-of-the-art compression ratio. Further analysis on video data reveals that this improvement is primarily achieved by reducing spatio-temporal redundancy and removing uninformative tokens, as supported by both quantitative and qualitative results.

## Key Contributions

- **KATok**: transformer-based VAE with an adaptive token selector jointly learned with latent tokens; each token's content-richness is scored as a keep-or-drop probability, giving data-dependent compression instead of a fixed ratio
- **Two position-prediction strategies** for spatial consistency after token dropping: cascaded generation vs joint generation
- **Claim**: strong reconstruction and generation quality at a state-of-the-art compression ratio, attributed to reduced spatio-temporal redundancy and removal of uninformative tokens

## Methodology

A transformer VAE where the token selector is trained jointly with latent tokens: per-token drop probabilities from content-richness, then position prediction (cascaded or joint) to repair the spatio-temporal structure disturbed by dropping. The resulting tokenizer is plugged into video diffusion models. Which strategy wins, and under what resolution/motion regime, is reported in the full text — not the abstract.

## Results

The arXiv abstract reports **no numeric metrics** (no compression ratio, no PSNR/FVD-style scores, no baseline table), only the qualitative claim above. Do not cite numbers from this page; verify in the full text (PDF, v2 2026-08-27):

- Stated: SOTA compression ratio with strong reconstruction/generation quality
- Stated mechanism: gains from spatio-temporal redundancy reduction + uninformative-token removal, supported by quantitative and qualitative results (in-paper only)

## Caveats

This summary is abstract-based: the paper's evidence lives in the PDF body. Before reusing KATok, check the full-text tables for the actual ratio, datasets, baselines, and which position-prediction strategy (cascaded vs joint) the ablations favor.

## Relevance to Software Engineers

For SW engineers, this work introduces adaptive tokenization techniques that can be applied to improve efficiency of diffusion-based image/video generation. The keep-or-drop probability mechanism offers a data-dependent compression approach that reduces computational cost while maintaining quality. The position-prediction strategies (cascaded/joint generation) provide frameworks for maintaining spatial consistency when tokens are dropped, relevant for any system dealing with multi-resolution or multi-scale data representations.

## Related Concepts

- [Transformer](../../concepts/machine-learning/transformer.md)
- [Attention](../../concepts/machine-learning/attention.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2608.24293
- arXiv HTML: https://arxiv.org/html/2608.24293
- HuggingFace: https://huggingface.co/papers/2608.24293
- Scope: abstract-based; quantitative tables are PDF-only (v2 2026-08-27)
