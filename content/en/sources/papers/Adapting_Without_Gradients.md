---
title: "Adapting Without Gradients: Affine Statistics Transport and What Its Certificate Can Tell You"
description: HuggingFace Daily Papers — 2026-08-31 — Talan
tags: [source, paper, huggingface, talan, machine-learning]
locale: en
arxiv_id: 2609.00374
---

# Adapting Without Gradients: Affine Statistics Transport and What Its Certificate Can Tell You

**arXiv**: 2609.00374 | **Published**: 2026-08-31 | **Organization**: Talan | **Submitted by**: Salim Khazem | **Upvotes**: 4

**Authors**: Salim Khazem, Ibrahim Mohamed Serouis

## Abstract

Test-time adaptation (TTA) typically assumes that model parameters can be updated at inference time. This assumption is restrictive for inference-only accelerators, frozen or third-party models, and memory-constrained deployments, and standard BatchNorm-based TTA configurations may also become inactive on architectures without BatchNorm. We study adaptation when the learned model must remain frozen. We introduce CASTER, a gradient-free method that stores source class statistics in a discriminative subspace, estimates a class-shared affine transformation from target-batch moments, and analytically transports the source class distributions before classification. CASTER requires no backward pass, optimizer state, or stored source feature bank. Across four backbones and seven datasets, it outperforms k-NN on identical frozen features in 27 of 28 backbone-dataset settings while retaining a median of 18x less state. Affine transport is not always reliable. On ImageNet-C, where batches contain only 64 samples for 1000 classes, unconditional transport loses 21.2 top-1 points. We therefore introduce an empirical residual-to-margin transportability certificate. Across 307 evaluation cells, every transport losing more than 10 points has certificate value above 3.9, although benign and destructive regimes are not perfectly separated. Gating converts an average -3.35-point effect of unconditional transport into a +1.69-point gain, and performance remains within 0.3 points of the best threshold over a broad threshold range. Finally, we show that this certificate is mechanism-specific: when applied to Tent, it accepts only 4.3% of updates and preserves 0.6% of Tent's available gain. These results position CASTER as a lightweight adaptation mechanism for frozen-model deployment, together with an explicit account of when its safety signal is informative and when it is not.

## Key Contributions

- Introduce CASTER, a gradient-free test-time adaptation method for frozen models
- Store source class statistics in a discriminative subspace
- Estimate class-shared affine transformation from target-batch moments
- Analytically transport source class distributions before classification
- Require no backward pass, optimizer state, or stored source feature bank
- Outperform k-NN in 27 of 28 backbone-dataset settings with 18x less state

## Methodology

CASTER stores source class statistics in a discriminative subspace. Estimates class-shared affine transformation from target-batch moments. Analytically transports source class distributions before classification. No backward pass, optimizer state, or stored source feature bank required. Transportability certificate gates unreliable updates.

## Results

Outperforms k-NN on identical frozen features in 27 of 28 backbone-dataset settings. Retains median of 18x less state than conventional TTA. On ImageNet-C with 64 samples/1000 classes, unconditional transport loses 21.2 top-1 points. Certificate gating converts -3.35 point effect to +1.69 point gain. Performance within 0.3 points of best threshold over broad range. Applied to Tent: accepts only 4.3% of updates, preserves 0.6% of available gain.

## Relevance to Software Engineers

For SW engineers, CASTER provides a practical gradient-free adaptation mechanism that works with frozen or third-party models - a common constraint in production deployments. The 18x reduction in state memory is significant for resource-constrained environments. The transportability certificate offers a reliable gating mechanism to determine when adaptation should occur, addressing the key TTA problem of uncertainty about whether adaptation will help or hurt. The mechanism-specific gating (e.g., 4.3% acceptance rate for Tent) provides a general framework for adaptive system design. This is directly applicable to any system needing online model adaptation without retraining or parameter updates.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.00374
- HuggingFace: https://huggingface.co/papers/2609.00374
