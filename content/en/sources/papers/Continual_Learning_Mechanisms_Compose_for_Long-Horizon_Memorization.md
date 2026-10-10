---
title: "Continual Learning Mechanisms Compose for Long-Horizon Memorization"
description: "Composing continual-learning mechanisms (anchors x low-rank allocation) lifts 100-task retention from 1.2% to 34.9%"
published: 2026-09-07
arxiv_id: "2609.06986"
url: "https://arxiv.org/abs/2609.06986"
authors: ["Zheyuan Zhang", "Alvin Zhang", "Daniel Khashabi", "Tianmin Shu"]
tags: [source, paper, machine-learning]
locale: en
---

# Continual Learning Mechanisms Compose for Long-Horizon Memorization

## Abstract

Language models may need to internalize information that arrives over time and retain it through many subsequent updates. To study this challenge, the authors introduce **long-horizon memorization**: a model learns 100 query-answer tasks through continual supervised fine-tuning (SFT) without retaining earlier training examples or receiving task identifiers at inference. Sequential updates cause catastrophic forgetting, and no single continual-learning mechanism evaluated maintains strong retention at this horizon. The hypothesis: mechanisms addressing complementary sources of forgetting compose more effectively than any one alone. Compositions are organized along two design dimensions — **anchors** (what prior information each update preserves: data, function, weight) and **low-rank allocation rules** (where successive updates are retained across LoRA adapters). Tested on three newly constructed 100-task memorization datasets with task-level successive halving to search the combinatorial space plus a factorial experiment for individual and interaction effects, the best method (all three anchors + merged LoRA) ranks top-3 on all datasets and raises average final retention from **1.2%** under naive sequential fine-tuning to **34.9%** — a 28-fold improvement. The data anchor and merged LoRA give the largest average gains and interact super-additively on all three datasets.

## Background & Problem Setup

Prompting and retrieval keep new information outside parameters — it must be re-supplied every time. The paper asks whether repeated parameter updates can instead build durable memory inside the model. The setting is domain-incremental continual SFT: 100 tasks in sequence, each a set of query-answer pairs with the same QA interface and vocabulary throughout, no raw earlier examples retained, no task ID at test time. The metric is recall of the training queries after all later tasks (final retention), plus memory half-life (tasks until retention halves). This isolates associative retention from transfer or heterogeneous downstream-task performance measured by prior continual-LM benchmarks (TRACE, TemporalWiki, CITB) and from targeted-edit metrics of sequential model-editing work (GRACE and follow-ups showing repeated edits weaken earlier ones). Classical catastrophic forgetting (McCloskey & Cohen; French; EWC; SI) is the enemy: each new task's gradient step overwrites prior associations.

## Methodology

**Design space.** Anchors specify what evidence of earlier tasks an update must preserve; low-rank allocation specifies the LoRA capacity each task uses and how updates persist:

- **Data anchor — unconditional generative replay**: the model trained up to the last task generates pseudo-samples of earlier data unconditionally (no stored examples carried forward; cf. Shin et al., LAMOL). Constant memory in tasks.
- **Function anchor — previous-state self-distillation**: the frozen post-task-(t−1) model acts as teacher; the student matches its output distributions (KL) on current-task inputs (cf. Learning without Forgetting). Constant memory.
- **Weight anchors — importance regularization**: Synaptic Intelligence (SI) and online EWC penalize movement in parameters important to earlier tasks (one reference + one diagonal importance/Fisher tensor per trainable tensor, discarded after each task). Constant memory.
- **Shared LoRA**: one rank-r adapter reused across all tasks (vanilla baseline allocation).
- **Merged LoRA** (cf. ReLoRA): each task's update is folded into the dense weights, then a fresh rank-r adapter is initialized — cumulative change becomes effectively higher-rank over time. Constant memory.
- **O-LoRA / sequential OSRM**: per-task subspaces with overlap penalties or feature-derived initialization (linear-in-tasks storage; included for comparison).

**Datasets (three × 100 tasks)**: arbitrary symbol associations (pure memorization stress test), LLM-generated fictional facts (LLM-QA), and natural questions filtered from public QA sets (Real-QA: TriviaQA, SQuAD, ARC, OpenBookQA, MedMCQA sources). Training covers the full question+answer token sequence (no prefix masking, matching deployment where no question prefix is available); replay seeds are masked.

**Search & analysis**: task-level successive halving (borrowed from hyperparameter search) prunes the large composition space cheaply for preliminary evidence; a factorial experiment then quantifies main and interaction effects rigorously.

## Results

- **Composition beats the best single mechanism everywhere** (Figure 1 memory-lifetime curves, 3-seed means): naive sequential SFT ends at 1.2% average final retention; the best individual mechanism reaches only 8.1%.
- **Best method — all three anchors + merged LoRA** — is the only factorial composition ranking top-3 on every dataset, at 34.9% average final retention (28× naive).
- **Factorial attribution**: the data anchor and merged LoRA are the largest individual contributors, and their interaction is **super-additive** on all three datasets — replayed pseudo-data plus fresh-per-task capacity reinforce each other.
- **Ablations over allocation rules** confirm merged LoRA's edge over shared LoRA and show O-LoRA/OSRM variants are competitive but pay linear storage cost.
- **Code/data**: project page compose-cl.github.io, repo github.com/cozheyuanzhangde/compose-cl, dataset cozzyde/long-horizon-memorization on the Hub.

## Limitations & Open Questions

- **Memorization, not generalization**: evaluation replays training queries; a model can retain an association yet fail its paraphrase. No claim about generalization to new formulations.
- **General capability still degrades**: Appendix E.9 shows substantial accuracy loss on held-out general benchmarks (MATH/MMLU-style) after 100 tasks even for the best method — preserving broad ability while banking associations remains open.
- **100-task horizon and QA-only interface**: longer horizons, mixed task formats, and interleaved pretraining-scale updates are untested; importance estimates (SI/Fisher) may misfire under distribution shift.

## Relevance to SW Engineers

For teams continually fine-tuning deployed models (support bots absorbing new products, coding assistants tracking new APIs), the takeaway is architectural: **don't pick one anti-forgetting trick — compose a replay signal with a capacity policy**. Concretely, unconditional generative replay costs no example storage (privacy-friendly) and merged-LoRA folding is a two-line training-loop change with constant memory — the pair that super-adds in this study. Track final retention over a growing task suite (not just latest-task accuracy) and report memory half-life; expect general-capability regression to need separate mitigation (mixing in pretraining data or scheduled merges). Extends `concepts/ai-engineering/llm-training.md` and `concepts/machine-learning/knowledge-distillation.md`.

## References

- Paper: https://arxiv.org/abs/2609.06986 (HTML: https://arxiv.org/html/2609.06986)
- Project: https://compose-cl.github.io/ — Code: https://github.com/cozheyuanzhangde/compose-cl — Data: https://huggingface.co/datasets/cozzyde/long-horizon-memorization
- LoRA (Hu et al. 2022); ReLoRA (Lialin et al. 2024); O-LoRA (Wang et al. 2023); EWC (Kirkpatrick et al. 2017); SI (Zenke et al. 2017); LwF (Li & Hoiem 2017); DER (Buzzega et al. 2020)
