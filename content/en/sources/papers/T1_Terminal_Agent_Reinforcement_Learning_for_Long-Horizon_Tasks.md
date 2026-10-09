---
title: "T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks"
arxiv_id: "2609.11042"
HF_URL: "https://huggingface.co/papers/2609.11042"
published: 2026-09-10
authors: "Junyao Yang, Yucheng Shi, Zhongzhi Li, Ruhan Wang, Zongxia Li, Haitao Mi, Leowei Liang"
locale: en
---

[한국어 버전](../../../ko/sources/papers/T1_Terminal_Agent_Reinforcement_Learning_for_Long-Horizon_Tasks.md)

# T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks

**Authors**: Junyao Yang, Yucheng Shi, Zhongzhi Li, Ruhan Wang, Zongxia Li, Haitao Mi, Leowei Liang · **Published**: Sep 10, 2026 · **arXiv**: [2609.11042](https://arxiv.org/abs/2609.11042) · **HuggingFace**: [https://huggingface.co/papers/2609.11042](https://huggingface.co/papers/2609.11042)

## Abstract

Agent usage is shifting toward long-horizon tasks such as coding and scientific discovery, among which terminal tasks are especially important. We introduce T1, a Mixture-of-Experts model of 122B total trained with reinforcement learning, operating a real shell in a cloud sandbox for up to 300+ tool-call turns per task, rewarded by executing each task's own verifier. We provide a comprehensive recipe: First, an aggressively warm-started to stabilize actor-critic training, with a dense process reward scoring trajectories by the absolute number of passing verifiers. Second, stable optimization through TITO construction, training on the exact sampled token identifiers with drift repair at turn boundaries, and rollout routing replay, recording the sampler's per-token expert choices at every MoE layer and replaying them during training. Third, fully out-of-distribution training corpus: isolated seeds and synthesized tasks disjoint from Terminal-Bench 2.1 ensures gains reflect genuine capability transfer over benchmark overfitting. Together, TITO and R3 cut the training-to-inference log-probability difference from 0.021 to 0.013, with exactly aligned zero token drift in the loss region. On Terminal-Bench 2.1, our post-train pipeline raises initial base model from 43.8% to T1 with 64.0% resolved. On Long-Horizon Terminal Bench, T1 reaches 27.9% and surpasses GPT-5.4 and GLM-5.1.

## Background and Problem Setup

Autonomous AI agents are increasingly tasked with executing complex, multi-step workflows in interactive software environments, particularly command-line shell interfaces (terminal environments). In these settings, an agent must execute shell commands, parse unstructured stdout/stderr feedback, adapt to errors, and sustain reasoning across hundreds of interaction turns.

Training large language models (LLMs) with reinforcement learning (RL) for long-horizon terminal environments presents severe technical challenges:
1. **Severe Off-Policy Drift and Unstable RL**: In multi-turn tool interaction, minute mismatches between rollout sampling and training forward passes (e.g., tokenization drift, floating-point discrepancies, or MoE expert routing variation) lead to rapid policy degradation and actor-critic instability.
2. **Sparse Reward Signals**: Final outcome rewards (pass/fail) become extremely sparse when task completion requires 100 to 300+ interaction turns, making exploration highly inefficient.
3. **Benchmark Overfitting**: Training on benchmark-adjacent trajectories leads models to memorize specific command structures or environment shortcuts rather than acquiring robust problem-solving capabilities.

To overcome these obstacles, T1 introduces a 122B Mixture-of-Experts (MoE) architecture trained with a specialized RL post-training pipeline designed specifically for long-horizon terminal interaction.

## Methodology

T1 combines architectural scaling, algorithmic training safeguards, and rigorous data separation into a unified reinforcement learning recipe.

### Model Architecture and Execution Sandbox
- **122B Mixture-of-Experts (MoE) Base**: T1 uses a 122B total parameter MoE model that selectively activates a subset of parameters per token, balancing computational efficiency with massive capacity.
- **Real Shell Cloud Sandbox**: During rollouts, the agent interacts directly with a real Linux shell executing inside isolated cloud sandboxes. Tasks allow up to **300+ tool-call turns** per episode.
- **Automated Programmatic Verifiers**: Every training and evaluation task is paired with dedicated programmatic verifier scripts that check file states, test suite results, and system conditions directly within the container.

### Stable RL Post-Training Recipe
1. **Aggressively Warm-Started Actor-Critic**: To avoid collapse in early RL training, the policy and value networks are warm-started with curated multi-turn terminal trajectories.
2. **Dense Process Reward Function**: Instead of relying solely on sparse terminal outcome rewards, T1 employs a dense process reward that evaluates intermediate environment states by scoring the absolute number of passing sub-verifiers at each interaction turn.
3. **TITO (Turn-by-Turn Token Identifier Tracking with Drift Repair)**: To prevent rollout-to-training mismatch across multi-turn shell sessions:
   - TITO records the exact sampled token IDs during environment interaction.
   - It performs explicit drift repair at tool-call and environment observation boundaries, guaranteeing exact alignment between the rollout token sequence and the loss calculation region.
4. **Rollout Routing Replay ($R^3$)**: In MoE architectures, dynamic expert routing during forward passes can differ between sampling and training. $R^3$ explicitly logs the per-token expert choices selected by the sampler at every MoE layer during the rollout, and enforces these exact routing decisions during backpropagation training.

### Out-of-Distribution Data Generation Pipeline
- **Synthesized Task Generation**: Training tasks are generated via isolated seed prompts and programmatic task synthesis entirely disjoint from public evaluation benchmarks.
- **Zero Benchmark Contamination**: By enforcing strict task and domain isolation between the training set and Terminal-Bench 2.1 / Long-Horizon Terminal Bench, performance gains reflect genuine capability transfer rather than benchmark memorization.

## Results

T1 was evaluated on standard and long-horizon terminal execution benchmarks:

- **Training Stability Metrics**:
  - Combined TITO and $R^3$ reduced the training-to-inference log-probability discrepancy from **0.021 to 0.013**.
  - Token drift within the policy loss region was reduced to **exactly zero**, enabling stable RL optimization over 300+ turns.

- **Terminal-Bench 2.1**:
  - Base Model: **43.8%** task resolution.
  - **T1 (Post-Trained)**: **64.0%** task resolution (**+20.2 percentage points** gain).

- **Long-Horizon Terminal Bench**:
  - T1 achieved **27.9%** success rate.
  - Outperformed proprietary frontier models including **GPT-5.4** and **GLM-5.1** on multi-turn terminal execution.

## Limitations and Open Questions

- **Infrastructure Overhead**: Operating real Linux shell sandboxes for thousands of parallel RL rollout workers up to 300 turns per episode demands substantial cloud compute and container orchestration infrastructure.
- **Verifier Design Complexity**: The quality of the dense process reward depends heavily on fine-grained, robust verifier scripts. Creating automated, un-hackable verifiers for arbitrary open-ended coding or system tasks remains non-trivial.
- **Compute at Test Time**: Long-horizon execution requires significant inference latency when tasks exceed 100+ command turns, highlighting the need for parallel search or context pruning during rollouts.

## Relevance to Software Engineers

For software engineers building autonomous coding agents, shell automation systems, or RL pipelines, T1 provides essential practical insights:

1. **Exact Rollout-Training Alignment for MoE Agents**: When training MoE models with RL, dynamic routing shifts between sampling and training will degrade policy gradient updates. Implementing fixed routing logs ($R^3$) and exact token identifier alignment (TITO) is critical for training stability.
2. **Real Environment Execution vs. Mock Simulators**: Synthetic state transitions cannot replace real shell interactions. Executing rollouts in lightweight, isolated Linux containers with real verifiers is required for robust tool-use generalization.
3. **Dense Sub-Verifier Design**: When designing automated tasks or benchmark evaluations, break down completion checks into granular sub-verifiers. Process rewards based on incremental verifier pass counts drastically improve RL sample efficiency.
4. **Long-Horizon Scaling**: Modern terminal agents can sustain coherence across 300+ interaction turns when trained with drift-repaired turn boundaries, proving that multi-step system administration and debugging can be automated end-to-end.
