---
title: "Eval-Driven Development: Lessons from Evaluating GenAI at Scale"
description: Airbnb's eval-driven development — three-layer evaluation, calibrated LLM judges, agentic trajectory evals
tags: [source, airbnb, genai, llm, evaluation, llm-as-judge, agents]
locale: en
source_url: "https://medium.com/airbnb-engineering/eval-driven-development-lessons-from-evaluating-genai-at-scale-e817e5ae5788"
blog: airbnb
date: 2026-07-28
---

# Eval-Driven Development: Lessons from Evaluating GenAI at Scale

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-07-28 · **Authors**: Rohit Girme, Dan Miller, Mia Zhao, Lifan Yang, Clint Kelly

## Why GenAI Breaks Software Testing Assumptions

LLM outputs are non-deterministic, "correct" is subjective, judging often needs AI-evaluating-AI (its own failure modes), and one interaction chains retrieval → reasoning → tool calls → generation, each failing independently. Airbnb runs LLM features across product (review highlights, AI support, guest/host messaging) on shared infra-team foundations. Key budgeting fact: **expect a meaningful share of total project effort to go to evaluation** — it is how products ship that work.

## The One Rule + Eval-Driven Development

**When in doubt, look at your data.** Prototype → run 100 examples → *read the outputs and traces* → categorize mistakes → build an eval. Formalized, this is **eval-driven development (EDD)**, the GenAI analogue of TDD: discover, encode, and continuously test failure modes as they appear.

Five principles: (1) define goals and ship-gates upfront; (2) let real observed errors guide metrics (never invent in a vacuum, co-develop with cross-functional partners); (3) keep the evaluator set **small and sharp — 3–5 calibrated judges beat 20–30 noisy ones**, one per correctness dimension, no "God evaluators"; (4) appoint a human decision-maker for good-vs-bad disputes; (5) collaborate continuously ("is X better than Y? what's actually wrong here?").

## The Three Evaluation Layers

1. **Programmatic/heuristic checks** (fast, deterministic first filter): structured JSON-schema outputs, never prompt-only formatting; catch obvious failures before spending judge/human budget.
2. **LLM-as-judge** (nuanced quality: tone, coherence, faithfulness): rubric design is everything — "readable and up to standards" is useless; specify tone/format/grammar/complexity rules with scored examples returning `{reason, score}`. **Calibration is mandatory**: 50–100 golden examples *including bad ones*, target high-80s–90s% agreement (Cohen's κ / Krippendorff's α), disagreement analysis → refine prompt/few-shots → re-run; recalibrate as failures evolve. An uncalibrated judge is worse than none (false confidence).
3. **Human evaluation** (gold standard for ground truth, high-stakes, tie-breaking): start with 20–100 SME-labeled rows; scale to annotation workforce only when the rubric is rock-solid. **If experts disagree, stop** — resolve human disagreement before automating.

## Evaluating Agentic Systems

Final-output-only eval is insufficient: a right answer can hide a broken path (wrong tool params, inefficient trajectory). Instrument **traces/spans** (agent type, sub-agents, I/O, tool invocations) into observability/persistent storage and evaluate three layers: trajectory quality, tool-use correctness, and end result.

## Suggested Iteration Loop

Fix one variable at a time (model → prompt → serving config); judges narrow candidates, top-candidate samples improve judges (co-sharpening). Then scale to ~5k examples and **mirror evals in production**: sample ~5% of de-identified live traffic daily through programmatic + judge layers, human-review flags, weekly PM review feeding new evals (with privacy-preserving de-identification and purpose limitation).

## Ten Takeaways (from the post)

Look at data · real-failure-mode evaluators, not generic helpfulness · start 50–100 rows · one evaluator per dimension · calibrate to high-80s–90s% · layer all three methods · include bad examples · evaluate the system (retrieval/tools/pipeline), trajectories for agents · mirror in prod · evaluation is a team sport (best communication wins, not best model).

## Related Concepts

- LLM-as-judge calibration; golden datasets; agentic observability/tracing

## References

- Cohen's kappa / Krippendorff's alpha (agreement metrics)
