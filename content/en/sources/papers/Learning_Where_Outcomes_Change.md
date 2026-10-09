---
title: "Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry"
description: HuggingFace Daily Papers — 2026-08-31 — Tsinghua IIGroup
tags: [source, paper, huggingface, tsinghua-iigroup]
locale: en
arxiv_id: 2608.30457
---

# Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry

**arXiv**: 2608.30457 | **Published**: 2026-08-31 | **Organization**: Tsinghua IIGroup | **Submitted by**: wangjunjie | **Upvotes**: 3

**Authors**: Jiani Guo, Junjie Wang, Jie Wu, Pengxiang Zhao, Dongdong Zhang, Shaohan Huang, Yujiu Yang, Furu Wei

## Abstract

Multimodal geometry reasoning requires VLMs to extract precise visual relations and preserve them through multi-step deduction. Existing free-form traces obscure the decisions that determine the answer, and trajectory-level reinforcement learning distributes a single terminal signal across the entire response. We introduce credit-addressable reasoning, in which the semantic units exposed during inference also define where learning compares alternatives and assigns credit. We instantiate this principle with Code-CoT, which retains the diagram, represents visual relations as line-addressable executable code, and organizes reasoning into typed events, and CE-GRPO, which selects event boundaries using structural priors and type-normalized entropy, samples complete continuations from shared prefixes, and converts outcome differences into localized advantages. Across nine geometry benchmarks, CE-GRPO achieves an average accuracy of 76.04, outperforming Qwen3-VL-8B and trajectory-level GRPO by 8.09 and 3.43 points, respectively. Its relative advantage increases with the number of intermediate events, demonstrating the value of representation--optimization co-design for long, dependency-heavy multimodal reasoning.

## Key Contributions

- Propose credit-addressable reasoning for multimodal geometry tasks
- Attribute outcomes to specific parts of multimodal inputs
- Enable precise debugging of multimodal model behavior
- Identify contributing visual and textual elements to final decisions

## Methodology

Framework for assigning credit to specific multimodal input components. Involves identifying which visual and textual elements contribute to final decisions in geometry-related reasoning tasks. Credit assignment mechanisms established to attribute outcomes to specific parts of inputs.

## Results

Enables more precise debugging and understanding of multimodal model behavior in geometry tasks. Framework helps identify contributing elements to model decisions.

## Relevance to Software Engineers

For SW engineers, credit-addressable reasoning provides a much-needed framework for debugging multimodal models - a common challenge in production AI systems. The ability to attribute outcomes to specific visual and textual elements helps with model auditing, bias detection, and debugging when models produce unexpected outputs. This is relevant for any system using multimodal inputs (document understanding, visual question answering, multimedia analytics). The framework's applicability to geometry-related tasks extends to broader multimodal domains where interpretability is important.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2608.30457
- HuggingFace: https://huggingface.co/papers/2608.30457
