---
title: "AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling"
description: HuggingFace Daily Papers — 2026-08-27 — ServiceNow-AI
tags: [source, paper, huggingface, servicenow-ai]
locale: en
source_url: "https://arxiv.org/abs/2608.26623"
arxiv_id: 2608.26623
---

# AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling

**arXiv**: 2608.26623 | **Published**: 2026-08-27 | **Organization**: ServiceNow-AI | **Submitted by**: Amit Kumar Saha | **Upvotes**: 16

**Authors**: Paper authors (arXiv: 2608.26623),

 Abhigya Verma, Amit Kumar Saha, Seganrasan Subramanian, Sai Harshitha Aluru

## Abstract

LLM judges are widely used to evaluate agentic tool-calling systems, yet their reliability on structured, dependency-driven workflows remains largely unexamined. We present AgentJudgeBench, the first benchmark to systematically study LLM-as-a-judge reliability for agentic tool-calling over workflow DAGs, as distinct from the broader LLM-as-a-judge task of open-ended text or preference evaluation. The benchmark comprises 3,808 instances spanning six DAG topologies and three difficulty tiers, evaluated with five generators (3B-70B open-weight models and GPT-5.4) and six judges (20B to frontier scale) under paired with- and without-ground-truth conditions. Judge alignment degrades monotonically with task difficulty, 1.5x faster without ground truth, and on hard queries without ground truth all six judges converge to a narrow 77-82% band regardless of scale, revealing a structural ceiling driven primarily by task difficulty, though its height is partly prompt-dependent for weaker generators, that model capacity alone cannot overcome. Ground-truth exposure is not uniformly beneficial: it reduces alignment for GPT-5.4 (1.5 pp) and Gemini-2.5-Pro (3.9 pp), consistent with over-anchoring. Among mitigation strategies, chain-of-thought reasoning and judge temperature both have negligible effect, while structured evaluation rubrics improve alignment by up to 6.5 pp but do not generalize uniformly across judge-generator pairs. With ground truth, QwQ-32B best matches the programmatic reference, while a human validation study identifies GPT-OSS-120B as the most human-aligned judge; without it, frontier judges lead only marginally within the shared ceiling. These results expose fundamental limitations of current LLM judges and yield practical guidelines for reliable evaluation in agentic systems.

## Key Contributions

- **First benchmark for LLM-as-a-judge on agentic tool-calling over workflow DAGs** — 3,808 instances across six DAG topologies and three difficulty tiers, separating judge reliability from open-ended text/preference evaluation
- **Paired with/without-ground-truth protocol**: five generators (3B–70B open-weight + GPT-5.4) × six judges (20B to frontier scale)
- **Structural ceiling finding**: judge alignment degrades monotonically with difficulty, 1.5x faster without ground truth; on hard queries without GT all six judges converge to 77–82% regardless of scale
- **Over-anchoring**: ground-truth exposure reduces alignment for GPT-5.4 (−1.5 pp) and Gemini-2.5-Pro (−3.9 pp)

## Methodology

Workflow DAGs at three difficulty tiers with paired ground-truth conditions. Judge–generator matrix evaluated against programmatic reference plus a human validation study. Mitigations tested: chain-of-thought, temperature, structured rubrics.

## Results

| Finding | Number |
|---|---|
| Difficulty degradation without GT | 1.5x faster than with GT |
| Hard queries, no GT (all 6 judges) | 77–82% band regardless of scale |
| GT over-anchoring | −1.5 pp (GPT-5.4), −3.9 pp (Gemini-2.5-Pro) |
| CoT reasoning / temperature | negligible effect |
| Structured rubrics | up to +6.5 pp, not uniform across pairs |
| Best with GT | QwQ-32B (programmatic match); GPT-OSS-120B most human-aligned |

## Relevance to Software Engineers

Do not trust LLM judges on hard multi-step tool-calling without ground truth — capacity does not break the ceiling. Budget for structured rubrics (+6.5 pp where they transfer) and paired GT/no-GT evaluation; watch for over-anchoring when showing judges the answer. QwQ-32B and GPT-OSS-120B are the reference points to beat.

## Related Concepts

- [Agent Evaluation](../../concepts/ai-engineering/agent-evaluation.md)
- [Agent](../../concepts/ai-engineering/agent.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2608.26623
- HuggingFace: https://huggingface.co/papers/2608.26623
- Scope: abstract-based; per-DAG tables are in the full text
