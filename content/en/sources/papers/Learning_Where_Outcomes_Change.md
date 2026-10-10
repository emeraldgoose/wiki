---
title: "Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry"
description: HuggingFace Daily Papers — 2026-08-31 — Tsinghua IIGroup
tags: [source, paper, huggingface, tsinghua-iigroup]
locale: en
source_url: "https://arxiv.org/abs/2608.30457"
arxiv_id: 2608.30457
---

# Learning Where Outcomes Change:Credit-Addressable Reasoning for Multimodal Geometry

**arXiv**: 2608.30457 | **Published**: 2026-08-31 | **Organization**: Tsinghua IIGroup | **Submitted by**: wangjunjie | **Upvotes**: 3

**Authors**: Jiani Guo, Junjie Wang, Jie Wu, Pengxiang Zhao, Dongdong Zhang, Shaohan Huang, Yujiu Yang, Furu Wei

## Abstract

Multimodal geometry reasoning requires VLMs to extract precise visual relations and preserve them through multi-step deduction. Existing free-form traces obscure the decisions that determine the answer, and trajectory-level reinforcement learning distributes a single terminal signal across the entire response. We introduce credit-addressable reasoning, in which the semantic units exposed during inference also define where learning compares alternatives and assigns credit. We instantiate this principle with Code-CoT, which retains the diagram, represents visual relations as line-addressable executable code, and organizes reasoning into typed events, and CE-GRPO, which selects event boundaries using structural priors and type-normalized entropy, samples complete continuations from shared prefixes, and converts outcome differences into localized advantages. Across nine geometry benchmarks, CE-GRPO achieves an average accuracy of 76.04, outperforming Qwen3-VL-8B and trajectory-level GRPO by 8.09 and 3.43 points, respectively. Its relative advantage increases with the number of intermediate events, demonstrating the value of representation--optimization co-design for long, dependency-heavy multimodal reasoning.

## Key Contributions

- **Credit-addressable reasoning**: the semantic units exposed during inference (typed events) also define where learning compares alternatives and assigns credit — closing both the representation gap and the credit gap of trajectory-level RL
- **Code-CoT**: retains the diagram and represents visual relations as line-addressable executable Matplotlib code, organizing reasoning into typed events (`reference`, `auxiliary`, `coordinate`, `think`); each event is verifiable and branchable
- **CE-GRPO**: selects candidate event boundaries with a structural prior + type-normalized entropy, samples complete continuations from the shared prefix through the final answer, and converts terminal outcome differences into localized advantages (shared prefix excluded from loss; unanimous groups contribute no update)
- **Evidence**: 9 geometry benchmarks, average 76.04 (+8.09 over Qwen3-VL-8B, +3.43 over trajectory-level GRPO); margin over trajectory GRPO grows 3.77 points per additional intermediate event

## Methodology

Code-CoT is installed by SFT on 18,302 quality-controlled traces (diagram + perception code + plan + typed events + answer; visual encoder frozen), then refined by CE-GRPO. Ordinary and shared-prefix groups are mixed 1:1 under the same GRPO objective with a programmatic reward (correctness + action validity − repetition/answer-leakage penalties). Branching fixes image, question, and complete prefix, so updates apply only to the regenerated event and its downstream consequences.

## Results

| Comparison | Result |
|---|---|
| CE-GRPO average (9 benchmarks) | **76.04** |
| vs Qwen3-VL-8B backbone | **+8.09** (all 9 benchmarks improved) |
| vs trajectory-level GRPO | **+3.43** (+3.91 on validly terminated responses) |
| vs Code-CoT SFT | +6.49 |
| Dependency-heavy splits | GeoLaux-mini **+15.16**, MM-Math **+9.44** over trajectory GRPO |
| Event scaling | CE-GRPO margin **+3.77 points per additional event** (r=0.866) |
| Selector ablation | structure + entropy best (76.04, 4.73% unclosed); structure alone 74.26; entropy alone ≈ random |

Code-grounded training also narrows the MathVerse text-dominant–vision-only gap from 30.07 to 14.09. Full per-benchmark tables are in the paper (HTML version verified); protocol-constrained models must terminate with a non-empty `<answer>` block.

## Relevance to Software Engineers

For SW engineers, credit-addressable reasoning provides a much-needed framework for debugging multimodal models - a common challenge in production AI systems. The ability to attribute outcomes to specific visual and textual elements helps with model auditing, bias detection, and debugging when models produce unexpected outputs. This is relevant for any system using multimodal inputs (document understanding, visual question answering, multimedia analytics). The framework's applicability to geometry-related tasks extends to broader multimodal domains where interpretability is important.

## Related Concepts

- [LLM Training](../../concepts/ai-engineering/llm-training.md)
- [Transformer](../../concepts/machine-learning/transformer.md)
- [Attention](../../concepts/machine-learning/attention.md)

## References

- arXiv: https://arxiv.org/abs/2608.30457
- arXiv HTML (verified): https://arxiv.org/html/2608.30457
- HuggingFace: https://huggingface.co/papers/2608.30457
