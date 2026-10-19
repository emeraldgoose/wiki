---
title: "From post-training to production: How TinyFish runs its web-native model on Databricks AI Runtime"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime"
blog: databricks
published: 2026-10-17
---

# From post-training to production: How TinyFish runs its web-native model on Databricks AI Runtime

**Source**: Databricks Blog, 2026-10-09

**Lead**: TinyFish builds Search, Fetch, Browser, and Agent APIs for enterprises whose agents must work across the live web — dynamic sites, authenticated workflows, multi-step tasks. It trains its own specialized web-native model for that job and runs the full lifecycle on Databricks: post-training on managed GPUs via AI Runtime, evaluation with MLflow, and production inference with Model Serving. Its internal go/no-go benchmark reports a 77.6% task-success rate over 2,178 web-agent tasks.

## Background

General-purpose foundation models remain part of TinyFish's agent architecture, but a model optimized specifically for web-agent tasks gives the team something it can control and improve. The hard part was the surrounding infrastructure: GPU compute for post-training, evaluation that measures whole-agent behavior rather than single responses, production serving, and operational data (usage, cost) to guide the next iteration. TinyFish consolidated all of this on Databricks instead of operating separate systems per stage.

## Turning agent behavior into better models

TinyFish started post-training with supervised fine-tuning and is extending into Direct Preference Optimization (DPO), running on Databricks-managed GPUs through AI Runtime. Because the model acts inside a larger agent, evaluation judges whether the full agent completed the requested task: an LLM judge reviews the original request, the action history, and the final result, and a task passes only on full completion — partial or incorrect results count as failures.

| Metric | Value |
|--------|-------|
| Tasks completed | 1,691 / 2,178 |
| Task-success rate | 77.6% |
| Judge | LLM review of request + action history + result |

This gives a direct signal for model development: each post-training change is measurable in end-task performance, and successful iterations move into production through Databricks Model Serving — which already serves TinyFish's search reranker and query rewriter.

## Production serving and cost tracking

Over a recent 15-day window, TinyFish logged 294,781 agent runs involving the web-native model across 6.4 million tool steps. Serving economics (model only, not the full agent stack):

| Metric | Value |
|--------|-------|
| Cost per agent run | $0.088 |
| Cost per tool step | $0.0040 |

Evaluation results, usage data, and cost reporting live in Databricks alongside the serving workload, so quality, usage, and economics are tracked on one foundation.

## Building models for the work agents actually perform

The article's broader point is organizational: keeping training, evaluation, serving, and operational data in one environment lets engineers spend time on model and product behavior rather than GPU operations and data plumbing between disconnected systems. Alongside its own models, TinyFish routes external foundation-model traffic through Unity Gateway for centralized cost tracking, key management, and governance.

## Relevance to Software Engineers

- **Evaluate the agent, not the response**: for tool-using models, task-completion benchmarks with action-history review are a truer training signal than per-response scoring.
- **Close the loop in one platform**: co-locating post-training, eval data, serving, and cost metrics shortens the production-behavior → retraining cycle.
- **Track unit economics early**: per-run and per-tool-step serving costs turn model quality work into budgetable engineering decisions.
- **Gateway external models**: a single gateway (Unity Gateway here) centralizes keys, spend, and governance as the agent stack grows.

## References

- Original article: [https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime](https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime)
