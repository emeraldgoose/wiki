---
title: "From Production Traffic to Post-Training: Building a Self-Hosted LLM That Covers the Corporate Request Mix"
description: HuggingFace Daily Papers — 2026-09-01 — T-Tech
tags: [source, paper, huggingface, t-tech]
locale: en
arxiv_id: 2609.01572
---

# From Production Traffic to Post-Training: Building a Self-Hosted LLM That Covers the Corporate Request Mix

**arXiv**: 2609.01572 | **Published**: 2026-09-01 | **Organization**: T-Tech | **Submitted by**: Alex Medvedev | **Upvotes**: 31

**Authors**: Olga Tsymboi, Dmitrii Stoianov, Ramil Latypov, Danil Taranets, Daniil Dryabin, Mikhail Gashkov, Viktor Zelenkovskiy, Aleksandr Fida, Gleb Alektorov, Nikita Gulyakov, Arthur Babkin, Aleksandr Medvedev, Pavel Gein, Anatolii Potapov

## Abstract

Data-residency constraints force enterprises to self-host LLMs, but continuous adoption of newer models without decommissioning their predecessors expands the serving fleet, fragmenting a finite GPU pool. We consolidate traffic from over 200 internal applications onto a single model by closing quality gaps identified through production error analysis along three axes: instruction following, function-calling, and internal task distribution. Quality is tracked by offline benchmarks stratified to production traffic and scored by deterministic verifiers or calibrated LLM judges. Rather than optimising all objectives jointly, which introduces cross-domain reward interference, we train a separate GRPO expert per axis and merge them via two-stage SLERP. Each expert's reward exposes a distinct failure mode, namely semantic collapse, over-calling, and verbosity hacking, each requiring a domain-specific fix. In non-reasoning mode the recipe surpasses a {sim}7times larger by total parameters baseline on the in-house Arena with 69.6 to 65.8, instruction following with 0.85 to 0.83, and function-calling with 0.79 to 0.77, while lifting general dialogue benchmarks. The model absorbs 50% of platform traffic, 116M requests per month, at a fraction of the serving cost.

## Key Contributions

- Consolidate 200+ internal applications onto a single self-hosted LLM model
- Three-axis quality analysis: instruction following, function-calling, internal task distribution
- Train separate GRPO expert per axis to address distinct failure modes
- Merge experts via two-stage SLERP to combine complementary strengths
- Achieve ~7x smaller model matching larger baseline performance on in-house Arena
- Serve 50% of platform traffic (116M requests/month) at fraction of serving cost

## Methodology

Production error analysis across 200+ internal apps along three axes. Separate GRPO expert training per axis (instruction following, function-calling, task distribution). Two-stage SLERP merging of experts. Offline benchmarks with deterministic verifiers and calibrated LLM judges. Quality tracking stratified to production traffic distribution.

## Results

~7x smaller model matches larger baseline on in-house Arena (69.6 vs 65.8). Instruction following 0.85 to 0.83, function-calling 0.79 to 0.77 improvements. General dialogue benchmarks lifted. 50% platform traffic absorption (116M requests/month) at fraction of serving cost.

## Relevance to Software Engineers

For SW engineers, this work demonstrates a practical approach to consolidating multiple LLM serving endpoints into a single model. The GRPO expert training per quality axis and SLERP merging technique provides a framework for improving model capabilities without proportional cost increases. The 7x size reduction while matching performance is particularly relevant for GPU-constrained environments. The three-axis quality framework (instruction following, function-calling, task distribution) offers a practical methodology for incremental model improvement. The 116M requests/month throughput at reduced cost is directly applicable to large-scale deployment scenarios.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.01572
- HuggingFace: https://huggingface.co/papers/2609.01572
