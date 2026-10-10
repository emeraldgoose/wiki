---
title: "Dream-RSI: Recursive Self-Improvement through Evolving Worlds"
published: 2026-09-14
arxiv_id: "2609.14858"
url: "https://arxiv.org/abs/2609.14858"
authors: ["Tong Zheng", "and 16 other authors"]
tags: [source, paper, ai-engineering]
---

# Dream-RSI: Recursive Self-Improvement through Evolving Worlds

[KO version](../ko/sources/papers/Dream-RSI_Recursive_Self-Improvement_through_Evolving_Worlds.md)

## Abstract
As AI agents become participants in the development of their successors, they reshape both the production of intelligence and the role of human researchers. We introduce Dream-RSI, a framework for scalable and recursively self-improving exploration. A lightweight orchestration layer makes exploration explicit and programmable while leaving the underlying coding agent unchanged. Our key insight is that accumulated discovery history can serve as a replay simulator over the realized search space. By performing dreaming in the replay simulator constructed from historical discovery trees, Dream-RSI secures immediate, low-cost off-policy feedback to evaluate and refine exploration policies without invoking repetitive, expensive online evaluations. The improved policy is subsequently redeployed online to drive further discovery, continuously expanding the simulator pool in a self-improving loop. Across algorithm engineering, mathematical optimization, and GPU kernel engineering, Dream-RSI achieves competitive or improved discovery quality while substantially reducing discovery cost in several settings.

## Background & Problem Setup
Autonomous exploration in complex spaces (like GPU kernel optimization or algorithm design) usually faces a trade-off:
1. **Online Policy Optimization**: High-fidelity but extremely expensive and slow due to the need for repeated real-world executions (e.g., compiling and running kernels on hardware).
2. **Static Search**: Fast but limited by the quality of the initial policy and lacks a feedback loop for improvement.
The core problem is how to refine an exploration policy without paying the full cost of online evaluation for every trial.

## Methodology: The "Dreaming" Loop
Dream-RSI introduces a recursive loop that leverages historical data as a proxy for the real world.

1. **Discovery History as a Simulator**: The framework records all previous exploration attempts (the "discovery tree"). Instead of treating this as a log, Dream-RSI treats it as a **replay simulator**.
2. **Dreaming (Off-policy Evaluation)**: The agent "dreams" by simulating new exploration paths using the historical discovery tree. It evaluates potential moves based on whether similar paths in the past led to success or failure. This provides immediate, low-cost feedback.
3. **Policy Refinement**: The exploration policy is updated based on these "dreams." The agent learns which types of mutations or search directions are most promising.
4. **Online Redeployment**: The refined policy is deployed back into the real environment to perform actual discovery.
5. **Recursive Expansion**: New discoveries from the online phase are added back to the discovery history, expanding the simulator's fidelity and continuing the self-improvement loop.

## Results
- **Domains**: Tested in algorithm engineering, mathematical optimization, and GPU kernel engineering.
- **Efficiency**: Substantially reduced the discovery cost (compute/time) compared to pure online optimization.
- **Quality**: Achieved competitive or superior discovery quality, meaning it found better solutions than baselines while using fewer resources.

## Limitations & Open Questions
- **Simulator Drift**: If the discovery history is too sparse or biased, the "dreams" may not accurately reflect the real search space, leading to suboptimal policies.
- **Scaling to Novelty**: The replay simulator is naturally better at refining existing paths than discovering completely novel directions that have no historical precedent.

## Relevance to SW Engineers
For engineers working on performance optimization (like CUDA/Triton kernels), Dream-RSI suggests a **Data-Driven Optimization** approach. Instead of random trials or intuition-based tuning, one can build a "history of attempts" and use it to guide future searches. It demonstrates the power of **off-policy learning** in engineering: using past failures and successes to simulate future outcomes before committing expensive hardware resources.
