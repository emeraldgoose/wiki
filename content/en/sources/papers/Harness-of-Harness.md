---
title: "Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement"
description: HuggingFace Daily Papers — 2026-09-01 — 
tags: [source, paper, huggingface, arxiv, ai-engineering]
locale: en
arxiv_id: 2609.01481
---

# Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement

**arXiv**: 2609.01481 | **Published**: 2026-09-01 | **Organization**:  | **Submitted by**: taesiri | **Upvotes**: 10

**Authors**: Paper authors (arXiv: 2609.01481),

 Haoyang Yan, Min-le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu

## Abstract

This paper studies autonomous software development, in which LLM-based coding agents transform high-level requirements into complete, functional, and usable software systems without human intervention. We introduce Harness-of-Harness (HoH), a framework that enables coding agents to continually improve software during autonomous development. HoH operates on existing coding-agent harnesses, and organizes their executions into iterative planning-coding-testing loops. To sustain improvement across loops, HoH balances repair with capability growth, scopes development into small and verifiable increments, separates implementation-time testing from independent evaluation, and constrains verifiable outputs rather than prescribing agent workflows. It progressively exposes deliverables, role-specific tools, and skills, encourages reuse rather than recreation, and maintains versioned project histories. On GameCraft-Bench, FrontierSWE, and ProgramBench, three harness-model pairs (Codex with GPT-5.5, OpenCode with DeepSeek-V4-Pro, and Pi with MiniMax-M3), HoH consistently outperforms the corresponding standalone harnesses, achieving an average relative gain of 52.25 percent and a maximum gain of 82.86 percent after three iterations. In a multi-day deployment with more than 70 iterations, HoH autonomously develops a first-person-shooter game, featuring a coherent storyline, fully implemented core mechanics, human-playable experience, polished visuals and integrated audio. Github: https://github.com/Flesymeb/HarnessOfHarness Project Page: https://flesymeb.github.io/HarnessOfHarness/

## Key Contributions

- **Novel methodology** for [specific contribution]
- **Key insight** that addresses [problem]
- **Implementation details** relevant to software engineering,



## Methodology

- **Architecture**: [describe model architecture or framework]
- **Algorithms**: [key algorithms used]
- **Key equations/choices**: [important mathematical or computational choices]



## Results

- **Key results**: [main experimental findings with numbers]
- **Baseline comparisons**: [comparison with existing methods]
- **Reproducibility**: [whether results can be reproduced]



## Relevance to Software Engineers

- [To be filled: practical implications for SW engineers]

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.01481
- HuggingFace: https://huggingface.co/papers/2609.01481
