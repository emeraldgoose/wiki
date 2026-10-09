---
title: JIT-Agent — Paper Source (Full Body)
description: "JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution"
tags: [paper, source, huggingface, ai-engineering, agent-harness, harness-intelligence]
locale: en
---

# JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution

**arXiv**: 2608.25593 | **Authors**: National University of Singapore | **Project**: https://bingreeky.github.io/JIT-site/ | **GitHub**: https://github.com/bingreeky/JIT

## Full-Body Seminar Summary

### Problem
Agent capability ≠ model alone. The **agent harness** (memory management, planning strategy, action protocol, tool/skill orchestration) can dominate contribution of the underlying foundation model. Yet harness design is:
- Manual
- Task-specific
- Fundamentally unscalable

### Solution: JIT-Agent
A **harness intelligence model** trained to synthesize task-adaptive agent harnesses on-the-fly for arbitrary off-the-shelf agentic LLMs.

### Formalization: Agent Harness as Composable Artifact
**Four-module protocol** (fixed, machine-generatable):
1. **Memory Management** — what to remember, how to retrieve
2. **Planning Strategy** — how to decompose, sequence, reflect
3. **Action Protocol** — tool calling format, validation, error handling
4. **Tool/Skill Orchestration** — which tools, when, how to compose

### JIT-Agent Capabilities
1. **Synthesize**: Generate harness for given task at hand
2. **Repair**: Fix harnesses for stable/reliable execution
3. **Self-Evolve**: Distill performance signals from expanding archive of prior harness configurations

### Training
- Trained on diverse tasks + harness configurations
- Learns to customize harness per (model, task) pair
- Archive of prior harnesses provides compounding knowledge base

### Results

| Base Model | Benchmark | JIT-Agent Gain | Comparison |
|------------|-----------|----------------|------------|
| DeepSeek-V4-Flash | DeepSearchQA | **+9.1** | Surpasses GPT-5.6 |
| DeepSeek-V4-Flash | OdysseyBench | **+4.3** | Surpasses GPT-5.6 |
| GLM-5.2 | (multiple) | **up to +20.2** | Already strong model |
| Multi-scale families (DeepSeek V4, Mimo-V2.5, Qwen3.6) | Controlled eval | Consistent improvement | Performance-competitive with OpenCode, Claude Code |

### Key Insight
**Harness Intelligence** = trainable, transferable, compounding dimension of agent capability **orthogonal to model scaling**. JIT-Agent establishes harness generation as a learnable skill that improves across model families and tasks.

### Architecture
- JIT-Agent acts as "harness helper" — sits between user task and agentic LLM
- Generates harness config → agentic LLM executes with that harness
- Archive accumulates (task, harness, performance) tuples for self-evolution

### Related Concepts
- `concepts/ai-engineering/agent.md` (agent harness, memory/planning/action/tool modules)
- `guides/ai-engineering/build-agent.md` (harness configuration best practices)
- `concepts/ai-engineering/rag.md` (tool orchestration, memory management)
