---
title: StepGuard — Paper Source (Full Body)
description: "StepGuard: Learning Step-Level Guardrails with Scalable Supervision and Safety-Utility Balancing"
tags: [paper, source, huggingface, ai-engineering, agent-security, grpo]
locale: en
---

# StepGuard: Learning Step-Level Guardrails

**arXiv**: 2608.24777 | **Authors**: AI45Research et al. | **Code**: https://github.com/zheng977/StepGuard | **Weights**: https://huggingface.co/ninty-seven/StepGuard

## Full-Body Seminar Summary

### Problem
LLM-based agents interact with external environments via tool invocation, introducing security risks: file modification, information leakage, unauthorized actions. Existing guardrails evaluate completed trajectories — leaving **pre-execution step-level monitoring underexplored**.

### Solution: StepGuard
A **step-level guard model** that:
1. Audits completed agent trajectories
2. Checks tool actions **before execution**

### Training Pipeline

#### StepGen (Automatic Data Engine)
Generates safe/unsafe trajectory pairs with **same context but different actions at the risky step**. Enables contrastive learning at the exact decision point.

#### Balance-GRPO (Balanced Group Relative Policy Optimization)
Dynamically balances learning between safe/unsafe actions based on **observed accuracy**. Reduces both over-defense (false positives) and under-defense (false negatives).

### Architecture
- Step-level classifier on tool invocation
- Trained on StepGen-generated contrastive pairs
- Balance-GRPO for safety-utility tradeoff optimization

### Results
- **Highest average accuracy** among open-weight guard models
- Performance **comparable to GPT-5.4** (closed-source)
- On AgentDojo & AgentDyn benchmarks:
  - **77.3% reduction** in mean attack success rate (vs no-guard)
  - **Only 2.8 pp utility drop** (minimal over-defense)
- Model weights open: `ninty-seven/StepGuard` on HF

### Key Insight
Pre-execution step-level guarding + contrastive trajectory generation + balanced RL = strong security with minimal utility loss. Orthogonal to model scaling — can guard any agentic LLM.

### Related Concepts
- `concepts/ai-engineering/agent.md` (agent harness, tool invocation)
- `guides/ai-engineering/build-agent.md` (safe agent deployment)
