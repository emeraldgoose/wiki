---
title: "DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation"
description: HuggingFace Daily Papers — 2026-09-01 — Tencent Hunyuan
tags: [source, paper, huggingface, tencent-hunyuan, ai-engineering]
locale: en
arxiv_id: 2609.00646
---

# DramaChain Bench: An End-to-End Benchmark for Short-Drama Generation

**arXiv**: 2609.00646 | **Published**: 2026-09-01 | **Organization**: Tencent Hunyuan | **Submitted by**: Haoyuan Shi | **Upvotes**: 2

**Authors**: Paper authors (arXiv: 2609.00646),

 Haoyuan Shi, Mingtao Chen, Shuo Jiang, Ziyan Chen, Xuyi Sheng, Yiming Liu, Ying Zhang, Miao Wang, Jianxiang Lu, Fanyang Lu, Songyuanyi Lu, Xiele Wu, Zhichao Hu, Yuhong Liu, Richeng Xuan

## Abstract

Commercial short-drama production follows a multi-stage chain: script, storyboard, keyframe imagery, shot-level video, and the finished short drama. Most existing benchmarks evaluate solely the video-generation stage using pre-authored inputs instead of real upstream pipeline outputs. This leaves two critical questions unanswerable: whether each stage adheres to the original script intent (rather than only its immediate input prompt), and whether disparate shots remain coherent after assembly into multi-episode releases. We present DramaChain Bench, the first short-drama benchmark that evaluates every stage of the complete production chain. It is built upon three in-house systems sharing one dimension system, DramaChain Dimensions: five evaluation axes instantiated at every stage, resolving into 63 leaf dimensions. DramaChain Agent is calibrated against commercial short-drama platforms in both workflow and finished short-drama quality, enabling stage-wise fair comparison across models. DramaChain Labeling System has each of the 5,785 items scored independently by three professional annotators, with all defects spatio-temporally localised and selected from a predefined defect list. This process produces 17,488 valid scores and 255,925 traceable attribution records. The human annotations confirm that upstream defects cascade across the pipeline, demonstrating that final episode quality is not governed by video generation alone. DramaChain Agentic Judge then scores every leaf dimension automatically, gathering evidence over multiple agentic rounds before judging against a per-item checklist; it reproduces the model ranking at a mean PLCC of 0.918, enough to admit new models at no annotation cost.

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

- arXiv: https://arxiv.org/abs/2609.00646
- HuggingFace: https://huggingface.co/papers/2609.00646
