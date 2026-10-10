---
title: "DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation"
description: HuggingFace Daily Papers — 2026-09-01 — Tencent Hunyuan
tags: [source, paper, huggingface, tencent-hunyuan, ai-engineering]
locale: en
source_url: "https://arxiv.org/abs/2609.00646"
arxiv_id: 2609.00646
---

# DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation

**arXiv**: 2609.00646 | **Published**: 2026-09-01 | **Organization**: Tencent Hunyuan | **Submitted by**: Haoyuan Shi | **Upvotes**: 2

**Authors**: Paper authors (arXiv: 2609.00646),

 Haoyuan Shi, Mingtao Chen, Shuo Jiang, Ziyan Chen, Xuyi Sheng, Yiming Liu, Ying Zhang, Miao Wang, Jianxiang Lu, Fanyang Lu, Songyuanyi Lu, Xiele Wu, Zhichao Hu, Yuhong Liu, Richeng Xuan

## Abstract

Commercial short-drama production follows a multi-stage chain: script, storyboard, keyframe imagery, shot-level video, and the finished short drama. Most existing benchmarks evaluate solely the video-generation stage using pre-authored inputs instead of real upstream pipeline outputs. This leaves two critical questions unanswerable: whether each stage adheres to the original script intent (rather than only its immediate input prompt), and whether disparate shots remain coherent after assembly into multi-episode releases. We present DramaChain Bench, the first short-drama benchmark that evaluates every stage of the complete production chain. It is built upon three in-house systems sharing one dimension system, DramaChain Dimensions: five evaluation axes instantiated at every stage, resolving into 63 leaf dimensions. DramaChain Agent is calibrated against commercial short-drama platforms in both workflow and finished short-drama quality, enabling stage-wise fair comparison across models. DramaChain Labeling System has each of the 5,785 items scored independently by three professional annotators, with all defects spatio-temporally localised and selected from a predefined defect list. This process produces 17,488 valid scores and 255,925 traceable attribution records. The human annotations confirm that upstream defects cascade across the pipeline, demonstrating that final episode quality is not governed by video generation alone. DramaChain Agentic Judge then scores every leaf dimension automatically, gathering evidence over multiple agentic rounds before judging against a per-item checklist; it reproduces the model ranking at a mean PLCC of 0.918, enough to admit new models at no annotation cost.

## Key Contributions

- **First end-to-end short-drama benchmark**: evaluates all five production stages (script → storyboard → keyframes → shot video → finished drama) instead of video-only generation from pre-authored inputs
- **DramaChain Dimensions**: five evaluation axes instantiated at every stage, resolving into 63 leaf dimensions; DramaChain Agent calibrated against commercial platforms for fair stage-wise comparison
- **DramaChain Labeling System**: 5,785 items × 3 professional annotators → 17,488 valid scores + 255,925 traceable attribution records, defects spatio-temporally localized from a predefined list
- **DramaChain Agentic Judge**: multi-round evidence gathering against per-item checklists; reproduces model ranking at mean PLCC 0.918, admitting new models at zero annotation cost

## Methodology

Real upstream pipeline outputs feed each stage (not pre-authored inputs), so two questions become answerable: stage adherence to original script intent, and cross-shot coherence after multi-episode assembly. Human annotations establish the reference; the agentic judge is validated by rank correlation.

## Results

| Finding | Number |
|---|---|
| Annotation scale | 5,785 items, 17,488 scores, 255,925 attributions |
| Key empirical result | upstream defects cascade — final quality not governed by video generation alone |
| Agentic judge fidelity | mean PLCC **0.918** vs human ranking |

## Relevance to Software Engineers

Evaluate generative pipelines stage-by-stage against the original intent, not each stage's immediate prompt — upstream drift dominates final quality. The checklist + multi-round-evidence judge pattern (PLCC 0.918) is a reusable recipe for cheap, trustworthy eval of new models.

## Related Concepts

- [Agent Evaluation](../../concepts/ai-engineering/agent-evaluation.md)
- [Agent](../../concepts/ai-engineering/agent.md)

## References

- arXiv: https://arxiv.org/abs/2609.00646
- HuggingFace: https://huggingface.co/papers/2609.00646
- Scope: abstract-based; dimension definitions are in the full text
