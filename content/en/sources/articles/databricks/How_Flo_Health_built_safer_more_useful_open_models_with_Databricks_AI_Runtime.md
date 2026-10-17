---
title: "How Flo Health built safer, more useful open models with Databricks AI Runtime"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime"
blog: databricks
published: 2026-10-17
---

# How Flo Health built safer, more useful open models with Databricks AI Runtime

**Source**: Databricks Blog, 2026-10-12

**Lead**: Flo Health serves 81 million monthly active users with women's health products, where AI responses must be both medically safe and genuinely useful. Instead of relying on a single general-purpose model, Flo built a judge-driven post-training pipeline on Databricks AI Runtime that converts clinician expertise into training signal for fine-tuned open models. The result: medical safety rose from 34% to about 61%, usefulness from 42% to 76%, and the combined score from 16% to 47%.

## Background

As Flo moved from traditional ML toward generative-AI-powered personalized insights, a single frontier model imposed three constraints: inference cost at 81M-user scale, dependence on a provider's model lifecycle, and limited ability to encode Flo's own domain expertise. Flo's longer-term vision is a compound AI system that routes each task to the right model while holding a consistent safety standard. That required fine-tuned open models plus a reusable way to define and measure "good" — so Flo started with evaluation, not training.

## Turning expert judgment into a scalable training signal

Flo's medical, product, and engineering teams decomposed medical risk into testable rubrics — e.g. a "balanced causes" rule requiring coverage of both benign and serious causes in symptom answers — and encoded each rubric as an AI judge with a definition, grading instructions, and training cases. Judges were validated against synthetic and anonymized real-user cases, with blinded clinicians adjudicating disagreements to set ground truth.

The final framework uses 26 judges in three groups:

- **12 medical-safety judges** as hard constraints.
- **6 "micro" judges** for nuanced behaviors such as voice, grounding, framing, and fine-grained safety.
- **8 usefulness criteria** covering completeness, relevance, coherence, and tone.

Clinicians concentrated their time on designing and calibrating this system, which then scores training candidates at scale — no per-example human labeling required.

## Fine-tuning with AI judges and preference optimization

Flo generated 15,000+ synthetic questions under privacy-first principles (model-generated or anonymously aggregated signals, never user free text) and adopted a Reinforcement Fine-Tuning loop:

1. Synthesize privacy-preserving questions.
2. Generate multiple candidate answers.
3. Score them across safety, usefulness, and behavioral criteria.
4. Build preference pairs from the strongest responses.
5. Train with supervised fine-tuning plus Direct Preference Optimization (DPO), then re-verify with the judges.

An early iteration improved usefulness while safety stayed flat, because pairs did not separate degrees of medical quality. Flo fixed this with a graded safety score: responses passing the binary safety gate were re-ranked by how thoroughly they met the medical criteria, producing preference pairs with a clearer safety contrast.

## Scaling post-training with Databricks AI Runtime

The generate-score-select-train loop ran on Databricks AI Runtime with LLM Foundry for distributed training, Compose-RL for preference optimization, and MLflow for tracking and checkpoints. The fine-tuning run used 32 NVIDIA H100 GPUs with PyTorch and Fully Sharded Data Parallel (FSDP), SFT followed by DPO — on serverless GPU compute, without per-experiment cluster setup. Flo estimates tailored fine-tuned models cut inference cost by an order of magnitude versus frontier APIs, while giving control over behavior and lifecycle.

## Results

| Metric | Before | After |
|--------|--------|-------|
| Medical safety | 34% | ~61% |
| Usefulness | 42% | 76% |
| Combined (both criteria met) | 16% | 47% |

The combined score nearly tripled. More durable than the numbers, Flo notes, is the reusable evaluation-and-training system itself: it carries forward to newer open-weight models (Gemma, Qwen, Kimi) without rebuilding the training environment.

## Relevance to Software Engineers

- **Evaluation-first post-training**: invest expert time in calibrated judges once, then reuse them as both reward signal and regression suite — a pattern applicable to any domain with correctness constraints (health, finance, legal).
- **Graded over binary preferences**: when DPO improves style but not correctness, re-rank passing outputs by quality depth to restore the contrast the optimizer needs.
- **Privacy-preserving synthetic data**: derive training inputs from model-generated or aggregated signals so clinicians (or domain experts) validate standards, not individual pairs.
- **Cost engineering**: at high QPS, a fine-tuned smaller model can be ~10x cheaper to serve than frontier APIs while being more controllable.

## References

- Original article: [https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime](https://www.databricks.com/blog/how-flo-health-built-safer-more-useful-open-models-databricks-ai-runtime)
