---
title: "Running open-Jev in SQL on Databricks"
description: "Serve open-weight Jev decision models on serverless GPUs and invoke them directly from SQL via ai_query over governed data."
tags: [source, databricks, model-serving, sql, llm, en]
locale: en
source_url: "https://www.databricks.com/blog/running-open-jev-sql-databricks"
blog: databricks
published_date: 2026-09-24
---

# Running open-Jev in SQL on Databricks

## Overview

Jev-style "System One" decision models return fast, well-calibrated choices from a discrete option set, making them cheap to apply at scale — but only if they can reach large governed datasets. This post shows serving an open-weight decision model (SemIf-OpenJev) on Databricks and calling it straight from SQL or Lakeflow jobs, demonstrated by classifying hotel reviews.

## From notebook to endpoint

An importable notebook automates the whole setup: pick the model, select serverless GPU compute, and run all. It downloads the weights, registers the model through Express Deployments, and creates a GPU Model Serving endpoint — no GPU infrastructure to manage — leaving a managed classifier endpoint ready for applications or SQL.

## Calling the model from SQL with ai_query

Because `ai_query` supports arbitrary custom model APIs (not just chat-completions shapes), the endpoint's structured request format can be sent directly from SQL, returning the chosen classification plus per-option probabilities as structured columns. That makes it practical to score tables already in Databricks at production scale, and the same models can be customized or post-trained via AI Runtime for enterprise-specific decision criteria.

## References

- Original article: [Running open-Jev in SQL on Databricks](https://www.databricks.com/blog/running-open-jev-sql-databricks)
