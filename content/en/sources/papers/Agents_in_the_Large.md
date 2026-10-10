---
title: "Agents in the Large: Perception-Centered Architecture for Persistent Agents"
description: HuggingFace Daily Papers — 2026-08-31 — Fudan University
tags: [source, paper, huggingface, fudan-university]
locale: en
source_url: "https://arxiv.org/abs/2608.30478"
arxiv_id: 2608.30478
---

# Agents in the Large: Perception-Centered Architecture for Persistent Agents

**arXiv**: 2608.30478 | **Published**: 2026-08-31 | **Organization**: Fudan University | **Submitted by**: Shichun Liu | **Upvotes**: 8

**Authors**: Paper authors (arXiv: 2608.30478),

 Shihan Dou, Haoxiang Jia, Shichun Liu, Feng Chen, Chenhao Huang, Yujiong Shen, Shaofan Liu, Jiayi Chen, Jiahang Lin, Honglin Guo, Qianyu He, Minghao Guo, Ziyi Ye, Pluto Zhou, Tao Gui, Qi Zhang, Xuanjing Huang

## Abstract

Cognitive language agents have achieved substantial progress by equipping language models with memory, tools, and decision-making procedures, enabling agents to reason and act in interactive environments. Existing frameworks largely cast these agents as systems for solving user-specified, bounded tasks. An increasingly important goal is for language agents to provide persistent assistance in long-lived settings where user needs, context, and service procedures persist and change, and to remain useful across the broad range of tasks that arise over time. Yet we still lack a framework to characterize persistent AI agents, organize existing work, and guide future development. To this end, we propose a Perception-Centered Architecture for Persistent Agents (Pera). Pera describes a persistent agent organized around perception and control components that continually perceive service-relevant signals from episodic task executions, internal context, and changes in the surrounding environment, and use these signals to construct lifecycle tasks. These tasks drive the ongoing operation and adaptation of the agent's service procedures. We use Pera to retrospectively organize recent work, examine a detailed case study, and offer forward-looking insights for building more capable persistent agents. Just as software engineering moved from programming in the small to programming in the large, Pera frames the evolution of language agents as an analogous architectural transition toward long-lived, adaptive intelligence systems.

## Key Contributions

- **Pera (Perception-Centered Architecture for Persistent Agents)**: organizes a long-lived agent around perception and control components that continually perceive service-relevant signals — from episodic task executions, internal context, and environment changes — and turn them into lifecycle tasks driving ongoing operation and adaptation
- **Retrospective organization** of recent work through the Pera lens plus a detailed case study and forward-looking guidance
- **Framing**: just as software engineering moved from programming-in-the-small to programming-in-the-large, language agents face an analogous transition toward long-lived, adaptive intelligence

## Methodology

Conceptual architecture paper (no benchmark table): defines persistent assistance as the target setting (needs, context, and procedures persist and change), derives lifecycle tasks from perceived signals, and uses Pera to re-describe existing systems and the case study.

## Results

No quantitative results — this is a framework/position contribution. Its testable content is the Pera decomposition (perception → lifecycle tasks → service-procedure adaptation) applied to the case study and prior work.

## Relevance to Software Engineers

If you operate agents across sessions (memory, changing procedures, recurring users), Pera gives a checklist: what signals are perceived, what lifecycle tasks they create, and how service procedures adapt. Design the perception loop first; bounded-task harnesses will not compose into persistent assistance by themselves.

## Related Concepts

- [Agent](../../concepts/ai-engineering/agent.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2608.30478
- HuggingFace: https://huggingface.co/papers/2608.30478
- Scope: framework paper; no benchmark numbers to cite
