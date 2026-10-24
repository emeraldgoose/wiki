---
title: "How our AI Research team uses AI Runtime"
description: "At Databricks, we continuously develop and evaluate new AI research techniques to make our products more intelligent, efficient, and useful for customers."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime"
blog: databricks
published_date: 2026-10-15
---

# How our AI Research team uses AI Runtime

**Source**: [databricks](https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime) · **Published**: 2026-10-15

## Overview

At Databricks, we continuously develop and evaluate new AI research techniques to make our products more intelligent, efficient, and useful for customers. Our research spans products like Genie, Smart Routing, and AI Functions. Recently, we've published how we made search 3x faster, developed new techniques for offline reinforcement learning, and pushed the frontier of complex document extraction.

## Key points

- Databricks AI Research uses AI Runtime to train and fine-tune models at scale, from small experiments to workloads spanning hundreds of GPUs.
- Built-in GPU reliability, fast job launches, and integrations with MLflow and Unity Catalog help researchers experiment faster.
- Agent-driven research has increased training jobs 8x, with AI Runtime supporting faster, automated experimentation.
- Resiliency for long-running training jobs. Training can require thousands of GPU hours. A single node or RDMA network failure can leave hundreds of GPUs idle and force us to restart from an earlier checkpoint, losing hou
- Fast experimentation and prototyping. Improving AI Functions means testing thousands of approaches, from different models and training techniques to data recipes. We need to launch experiments quickly without repeatedly
- GPU fleet management. We balance multiple research projects with different compute requirements, priorities, and deadlines, while remaining flexible enough to respond to new research techniques or open-source models.

## References

- Original article: [https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime](https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime)
