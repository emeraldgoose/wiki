---
title: "DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory"
description: HuggingFace Daily Papers — 2026-09-01 — LongCat
tags: [source, paper, huggingface, longcat]
locale: en
source_url: "https://arxiv.org/abs/2609.00768"
arxiv_id: 2609.00768
---

# DiagEvo: Diagnosis-Guided Self-Evolution via Hierarchical Error Memory

**arXiv**: 2609.00768 | **Published**: 2026-09-01 | **Organization**: LongCat | **Submitted by**: dingyi | **Upvotes**: 14

**Authors**: Paper authors (arXiv: 2609.00768),

 Xincheng Wei, Yifan Ding, Yoshua Li, Dongsheng Ma, Rongxiang Weng, Xunliang Cai, Wenjian Ding, Yao Zhang

## Abstract

Self-play is an effective paradigm for language-model self-evolution, but without guidance, solver performance can plateau or decline across rounds. Unguided methods steer question generation with signals such as difficulty, learnability, or diversity. These signals keep questions challenging and varied but do not specify which unresolved reasoning weaknesses later rounds should target. Guided methods obtain direction from external task resources, including human examples, document corpora, or specified difficulty targets, and therefore rely on task information supplied outside the self-play loop. We show that the needed direction can instead be derived from the solver's own failure history. We introduce DiagEvo, whose diagnostician extracts recurring error causes from this history and stores them in a hierarchical error-cause memory. The memory groups related causes under skill nodes and tracks each as Active or Mastered according to self-consistency on targeted questions. The challenger uses these states and recurrence counts to balance cause-targeted generation with free exploration. Double-confidence filtering retains intermediate-difficulty questions only when the most common solver answer has a clear vote lead. DiagEvo derives its curriculum from information produced during self-play, without external task resources. With the default 4B diagnostician, DiagEvo outperforms every baseline in mean accuracy across all nine benchmarks for each of the three solvers: Qwen3-4B, Qwen3-8B, and OctoThinker-8B. On Qwen3-8B, it reaches 72.3% mean accuracy across five mathematical reasoning benchmarks, 4.5 percentage points above R-Zero. Its mean accuracy across all nine benchmarks is 57.4%, 1.1 percentage points above DARC. Ablations show that the hierarchical error-cause memory and double-confidence filtering both contribute to these gains.

## Key Contributions

- **Failure-history-derived direction**: instead of difficulty/learnability/diversity signals or external task resources, DiagEvo's diagnostician extracts recurring error causes from the solver's own failure history into a hierarchical error-cause memory (skill nodes; each cause tracked Active/Mastered by self-consistency on targeted questions)
- **Challenger** balances cause-targeted generation with free exploration using memory states and recurrence counts
- **Double-confidence filtering**: keeps intermediate-difficulty questions only when the most common solver answer has a clear vote lead

## Methodology

Self-play loop with a default 4B diagnostician: diagnose → hierarchical memory → targeted + exploratory question generation → filtered solving → memory update. No external task resources. Evaluated on three solvers (Qwen3-4B, Qwen3-8B, OctoThinker-8B) across nine benchmarks.

## Results

| Finding | Number |
|---|---|
| Mean accuracy, all 9 benchmarks × all 3 solvers | best of every baseline |
| Qwen3-8B, 5 math benchmarks | **72.3%** (+4.5 pp over R-Zero) |
| Qwen3-8B, all 9 benchmarks | **57.4%** (+1.1 pp over DARC) |
| Ablations | hierarchical memory and double-confidence filtering both contribute |

## Relevance to Software Engineers

For self-improving LM pipelines, mine the failure log — not just difficulty scores — and track error causes as a stateful memory (active vs mastered). Gate training questions on answer-consensus margin. The pattern ports to any agentic self-play loop (coding, tool use) where unguided rounds plateau.

## Related Concepts

- [LLM Training](../../concepts/ai-engineering/llm-training.md)
- [Transformer](../../concepts/machine-learning/transformer.md)

## References

- arXiv: https://arxiv.org/abs/2609.00768
- HuggingFace: https://huggingface.co/papers/2609.00768
- Scope: abstract-based; per-benchmark tables are in the full text
