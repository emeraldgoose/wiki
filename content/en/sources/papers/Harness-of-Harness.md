---
title: "Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement"
description: HuggingFace Daily Papers — 2026-09-01 — 
tags: [source, paper, huggingface, arxiv, ai-engineering]
locale: en
source_url: "https://arxiv.org/abs/2609.01481"
arxiv_id: 2609.01481
---

# Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement

**arXiv**: 2609.01481 | **Published**: 2026-09-01 | **Organization**:  | **Submitted by**: taesiri | **Upvotes**: 10

**Authors**: Paper authors (arXiv: 2609.01481),

 Haoyang Yan, Min-le Su, Hangfan Zhang, Zhanhao Li, Chen Zhang, Shao Zhang, Yang Chen, Lei Bai, Shuyue Hu

## Abstract

This paper studies autonomous software development, in which LLM-based coding agents transform high-level requirements into complete, functional, and usable software systems without human intervention. We introduce Harness-of-Harness (HoH), a framework that enables coding agents to continually improve software during autonomous development. HoH operates on existing coding-agent harnesses, and organizes their executions into iterative planning-coding-testing loops. To sustain improvement across loops, HoH balances repair with capability growth, scopes development into small and verifiable increments, separates implementation-time testing from independent evaluation, and constrains verifiable outputs rather than prescribing agent workflows. It progressively exposes deliverables, role-specific tools, and skills, encourages reuse rather than recreation, and maintains versioned project histories. On GameCraft-Bench, FrontierSWE, and ProgramBench, three harness-model pairs (Codex with GPT-5.5, OpenCode with DeepSeek-V4-Pro, and Pi with MiniMax-M3), HoH consistently outperforms the corresponding standalone harnesses, achieving an average relative gain of 52.25 percent and a maximum gain of 82.86 percent after three iterations. In a multi-day deployment with more than 70 iterations, HoH autonomously develops a first-person-shooter game, featuring a coherent storyline, fully implemented core mechanics, human-playable experience, polished visuals and integrated audio. Github: https://github.com/Flesymeb/HarnessOfHarness Project Page: https://flesymeb.github.io/HarnessOfHarness/

## Key Contributions

- **Harness-of-Harness (HoH)**: operates on existing coding-agent harnesses, organizing executions into iterative planning–coding–testing loops that balance repair with capability growth
- **Design rules**: small verifiable increments, implementation-time testing separated from independent evaluation, constrained verifiable outputs instead of prescribed workflows, progressive exposure of deliverables/tools/skills, reuse over recreation, versioned project histories
- **Multi-day autonomy demo**: 70+ iterations building a playable first-person-shooter game (storyline, mechanics, visuals, audio)

## Methodology

Three harness–model pairs (Codex + GPT-5.5, OpenCode + DeepSeek-V4-Pro, Pi + MiniMax-M3) run HoH loops vs standalone harnesses on GameCraft-Bench, FrontierSWE, and ProgramBench.

## Results

| Finding | Number |
|---|---|
| Average relative gain over standalone harness | **+52.25%** after 3 iterations |
| Maximum gain | **+82.86%** |
| Consistency | gains across all three harness–model pairs |
| Endurance | coherent FPS game over 70+ autonomous iterations |

## Relevance to Software Engineers

Wrap your coding agent in an outer loop with versioned history, separate eval gates, and small increments — harness-level iteration beats single-shot generation. Constrain *outputs* (verifiable), not *workflows*. Links from the paper: https://github.com/Flesymeb/HarnessOfHarness, https://flesymeb.github.io/HarnessOfHarness/

## Related Concepts

- [Agent](../../concepts/ai-engineering/agent.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2609.01481
- HuggingFace: https://huggingface.co/papers/2609.01481
- Scope: abstract-based; per-bench tables are in the full text
