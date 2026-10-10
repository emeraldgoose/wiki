---
title: "ZGCM-1: A Fully Open and Extremely Efficient Foundation Model for Math and Agentic Search"
published: 2026-09-11
arxiv_id: "2609.13356"
url: "https://arxiv.org/abs/2609.13356"
authors: ["Jiyan He", "Guang Liang", "Hao Liu", "Haoxiang Guan", "Jinbo Sun", "Junyi Guo", "Wenjun Feng", "Yantai Xie", "Yifei Shen", "Bin Shao", "Chuyang Wei", "Kai Chen", "Kexin Zhou", "Minghang Zhu", "Shuxin Zheng", "Tie-Yan Liu", "Taine Zhao", "Wenhui Zhu", "Xueyin Xu", "Xiaoqing Zhang", "Yatao Li", "Yuxuan Ren"]
tags: [source, paper, machine-learning]
---

# ZGCM-1: A Fully Open and Extremely Efficient Foundation Model for Math and Agentic Search

[KO version](../ko/sources/papers/ZGCM-1_A_Fully_Open_and_Extremely_Efficient_Foundation_Model_for_Math_and_Agentic_Search.md)

## Abstract
In this work, we present ZGCM-1, a fully open 7B dense foundation model trained from scratch with extreme data, system, and algorithmic efficiency. ZGCM-1 is founded on a core premise: compact models cannot passively memorize the open web, but can overcome parametric capacity limits by coupling deliberate internal thinking with active external tool use. To support this paradigm across a 256K context, we develop an end-to-end, high-efficiency open training recipe: Architecture & System Co-design: interleaved gated sliding-window and full attention, and a stable FP8 Muon optimizer; Progressive Curriculum & MDP Mid-Training: context scaling across 16K, 64K, and 256K, and the reformulation of interaction traces into Markov Decision Processes. Furthermore, we establish an AI-native R&D workflow where agent swarms autonomously manage cluster operations, data curation, and rapid diagnostic evaluation. Extensive evaluations show that ZGCM-1-7B is competitive across 7B model family on general benchmarks. On several challenging mathematical reasoning and agentic search suites, it remains competitive with frontier models orders of magnitude larger, such as Qwen3-235B-A22B and GLM-5.1. We also show that our pre-training design offers a ~4.2x efficiency improvement in 16K pre-training time-to-loss. Across the full development lifecycle, we distill eight actionable empirical findings-spanning architectural scaling, SFT quality pruning, long-context generalization, and agentic co-training dynamics. To facilitate community research, we open-source model weights from the pre-training, mid-training, and post-training stages, intermediate checkpoints, training code, per-stage data and data recipes, and W&B logs.

## Background & Problem Setup
The "parametric capacity limit" refers to the fact that small models (e.g., 7B) cannot memorize all the facts of the internet. Traditional scaling laws suggest that for more knowledge or complex reasoning, you need more parameters. ZGCM-1 challenges this by proposing that a small model can act as a high-efficiency "reasoning engine" that uses external tools to compensate for its lack of internal memory. The challenge is to maintain high efficiency and long-context (256K) capabilities without the massive compute typical of frontier models.

## Methodology
ZGCM-1's efficiency comes from three primary design pillars:

1. **Architecture & System Co-design**:
    - **Attention Mechanism**: Uses interleaved gated sliding-window and full attention. This reduces the quadratic cost of full attention while maintaining global context where necessary.
    - **Optimizer**: Employs a stable FP8 Muon optimizer, which allows for faster convergence and reduced memory overhead during training.

2. **Progressive Curriculum & MDP Mid-Training**:
    - **Context Scaling**: Training doesn't start at 256K. It follows a curriculum: 16K $\rightarrow$ 64K $\rightarrow$ 256K. This stabilizes training and improves generalization.
    - **MDP Reformulation**: Interaction traces (how an agent uses a tool) are reformulated as Markov Decision Processes (MDPs). This frames agentic search as a sequential decision problem, optimizing the model's policy for tool use.

3. **AI-Native R&D Workflow**:
    - The model was developed using "agent swarms" that managed the cluster, curated data, and performed diagnostics, drastically reducing human operational overhead.

## Results
- **General Benchmarks**: Competitive with other 7B class models.
- **Math & Agentic Search**: Remarkably, the 7B model competes with models like Qwen3-235B-A22B and GLM-5.1 on specialized reasoning tasks.
- **Training Efficiency**: Achieved a $\sim 4.2\times$ improvement in time-to-loss during the 16K pre-training phase.
- **Open Source**: The team released all weights, checkpoints, code, and data recipes.

## Limitations & Open Questions
- **Dense vs. MoE**: As a dense model, it may still hit hard limits compared to Mixture-of-Experts (MoE) models of similar "active" parameter counts.
- **Dependency on Tools**: The model's strength is coupled with the quality and availability of external tools; without them, its raw knowledge is limited by its 7B size.

## Relevance to SW Engineers
For engineers, ZGCM-1 demonstrates that **algorithmic efficiency can substitute for raw scale**. The use of FP8 Muon and curated context scaling are practical lessons for those training domain-specific models. More importantly, it reinforces the "LLM as a Controller" pattern: rather than trying to build a model that "knows everything," build a compact, efficient model that "knows how to use everything" via tools.
