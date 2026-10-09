---
title: Beyond Data Scaling — Paper Source (Full Body)
description: 'Beyond Data Scaling: Representation-Centric Continued Pre-training for Vision-Language-Action Models (StarVLA / VLAct)'
tags: [paper, source, huggingface, ai-engineering, robotics, vision-language-action, representation-learning]
locale: en
arxiv_id: 2608.27550
---

# Beyond Data Scaling: Representation-Centric Continued Pre-training for Vision-Language-Action Models

**arXiv**: 2608.27550 | **Published**: 2026-08-26 | **Organization**: StarVLA | **Project**: https://starvla.github.io/VLAct | **Backbone**: VLAct · Qwen3-VL-4B (`StarVLA/VLAct_Qwen3_Pretrain`)

**Authors**: Senqiao Yang, Chengyao Wang, Yuxin Chen, Zixuan Wang, Longxiang Tang, Haokun Gui, Jinhui Ye, Changsheng Lu, Xiaoyang Wu, Mingkang Zhu, Pengguang Chen, Shu Liu, Zhuotao Tian, Hengshuang Zhao, Bei Yu, Jiaya Jia

## Abstract

Vision-language-action (VLA) models are usually improved by scaling robot trajectory data, but robot data is scarce and costly to collect. Under a fixed robot-data budget, continued pre-training must turn limited trajectories into transferable visual-action knowledge rather than merely fit actions — making representation quality a central bottleneck. We propose VLAct, a VLA-oriented VLM backbone trained on broad, heterogeneous, multi-embodiment robot data before task-specific fine-tuning. VLAct preserves the broad VLM prior and encourages shared action semantics across embodiments through VLM-prior preservation, multi-head continuous action co-supervision, and a partially unified cross-embodiment action layout, while allowing task-specific action heads during fine-tuning. Results are obtained using fully open-source data and only a 16-GPU training setup, showing that representation-centric continued pre-training delivers highly competitive performance under a modest compute budget and is an important independent axis of VLA progress beyond data scaling.

## Key Contributions

- Frames VLA progress as representation quality, not just data volume: an independent axis beyond data scaling
- VLAct: a VLA-oriented VLM backbone (Qwen3-VL-4B based) continued-pretrained on broad, heterogeneous, multi-embodiment robot data
- Three continued-pretraining principles: preserve the VLM prior, share action semantics across embodiments, scaffold with pretraining heads discarded at fine-tuning time
- Partially unified cross-embodiment action layout: shared semantics without pretending robots are identical (embodiment-specific dims remain)
- Open recipe: fully open-source data, 16-GPU setup, public weights (`StarVLA/VLAct_Qwen3_Pretrain`), training pipelines and dataset-prep scripts

## Methodology

Continued pre-training sits between the base VLM and downstream task fine-tuning. The full model is unfrozen again during downstream fine-tuning; continued-pretraining action heads act as scaffolding and are replaced by freshly initialized task-specific heads.

1. **VLM-prior preservation** — keep what the VLM already knows. Caption supervision anchors broad visual and semantic knowledge during continued pre-training so robot-action learning does not wash out the general vision-language prior. Ablations on the vision-language data mixture show the prior-preservation term is load-bearing.
2. **Multi-head continuous action co-supervision** — joint supervision over continuous action heads across embodiments encourages shared, transferable action semantics instead of overfitting to one robot's action distribution.
3. **Partially unified cross-embodiment action layout** — compares three layouts: separate per-embodiment heads, naively unified (forces all robots into one space), and partially unified (shared semantic subspace + embodiment-specific dimensions). The partial layout wins: it shares what transfers while keeping what differs.

Training data is broad, heterogeneous, multi-embodiment open-source robot data; dataset-preparation scripts and run scripts are public in the VLAct repo.

## Results

- **Unseen embodiment generalization**: on RoboCasa-GR1 (unseen humanoid embodiment), a VLA using VLAct with only 20% of downstream trajectories outperforms the full-data GR00T-N1.6 baseline — the headline data-efficiency result.
- **Broad competitiveness**: strong results across simulations and seen embodiments despite the modest 16-GPU budget.
- **Ablations**: caption-mixture ablations confirm VLM-prior preservation matters; action-space comparisons favor the partially unified layout over separate or naively unified heads.
- **Efficiency claim**: competitive performance without proprietary data scale — representation work substitutes for raw trajectory volume.

## Limitations / Open Questions

- Continued pre-training still needs diverse multi-embodiment data curation; the recipe reduces but does not eliminate data dependence.
- Partially unified layout requires per-embodiment design decisions (which dims to share) — not fully automatic.
- Evaluation centers on manipulation/humanoid benchmarks (RoboCasa-style); very long-horizon and contact-rich tasks remain open.

## Relevance to Software Engineers

For SW engineers building robot stacks: start from the continued-pretraining backbone (`StarVLA/VLAct_Qwen3_Pretrain`) as the default adaptation base for a new robot, dataset, or action head instead of fine-tuning a raw VLM. Keep caption/prior-preservation data in your continued-pretraining mix, use a partially unified action layout when serving multiple embodiments, and treat pretraining action heads as throwaway scaffolding. The practical payoff is data efficiency — matching or beating full-data baselines with a fraction of downstream trajectories on a modest GPU budget.

## Related Concepts

- `concepts/ai-engineering/agent.md` (embodied agent architecture)
- `concepts/machine-learning/transformer.md` (VLM backbone representations)
- `concepts/ai-engineering/llm-training.md` (continued pre-training recipe)
- `guides/ai-engineering/build-agent.md` (robot agent deployment)

## References

- arXiv: https://arxiv.org/abs/2608.27550
- HuggingFace: https://huggingface.co/papers/2608.27550
- Project page: https://starvla.github.io/VLAct
- Weights: https://huggingface.co/StarVLA/VLAct_Qwen3_Pretrain
