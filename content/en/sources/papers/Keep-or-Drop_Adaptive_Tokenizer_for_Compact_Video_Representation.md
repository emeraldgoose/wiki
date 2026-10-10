---
title: Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation
description: HuggingFace Daily Papers — 2026-08-25 — Kakao Corp.
tags: [source, paper, huggingface, kakao-corp., machine-learning]
locale: en
arxiv_id: 2608.24293
---

# Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation

**arXiv**: 2608.24293 | **Published**: 2026-08-25 | **Organization**: Kakao Corp. | **Submitted by**: lee | **Upvotes**: 11

**Authors**: Yeonkyeong Lee, Hyunsung Go, Jongmin Kim, Sewoong Lim, Donghoon Lee

## Abstract

Latent diffusion models have emerged as a dominant framework for high-fidelity image and video synthesis, operating in compact latent spaces with variational autoencoders (VAEs) to enhance computational efficiency without compromising visual quality. However, conventional VAEs are suboptimal for video data as they employ fixed compression ratios that cannot adapt to the varying complexity of spatio-temporal content. We present KATok (Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation), a transformer-based VAE that incorporates an adaptive token selector which is jointly learned with latent tokens. By evaluating each token's content-richness as keep-or-drop probability, the token selector effectively discards uninformative tokens, naturally allowing data-dependent compression. Applying adaptive tokenization to diffusion models may cause spatial misalignment, as token dropping can disturb the original spatio-temporal structure. To alleviate this issue, we propose two position-prediction strategies: cascaded and joint generation, to ensure spatial consistency. We empirically show that our model achieves strong reconstruction and generation quality at a state-of-the-art compression ratio. Further analysis on video data reveals that this improvement is primarily achieved by reducing spatio-temporal redundancy and removing uninformative tokens, as supported by both quantitative and qualitative results.

## Key Contributions

- Present KATok, a transformer-based VAE with adaptive token selector for video representation
- Adaptive token selector evaluates each token's content-richness as keep-or-drop probability
- Two position-prediction strategies (cascaded and joint generation) ensure spatial consistency
- Achieves state-of-the-art compression ratio with strong reconstruction/generation quality

## Methodology

Transformer-based VAE with jointly learned adaptive token selector. Token drop probabilities computed per-token based on content-richness. Position-prediction strategies (cascaded/joint generation) maintain spatial consistency after token dropping. Trained on video diffusion models to achieve strong reconstruction and generation quality.

## Results

Strong reconstruction and generation quality at state-of-the-art compression ratio. Reduction of spatio-temporal redundancy and removal of uninformative tokens supported by quantitative and qualitative results.

## Relevance to Software Engineers

For SW engineers, this work introduces adaptive tokenization techniques that can be applied to improve efficiency of diffusion-based image/video generation. The keep-or-drop probability mechanism offers a data-dependent compression approach that reduces computational cost while maintaining quality. The position-prediction strategies (cascaded/joint generation) provide frameworks for maintaining spatial consistency when tokens are dropped, relevant for any system dealing with multi-resolution or multi-scale data representations.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2608.24293
- HuggingFace: https://huggingface.co/papers/2608.24293
