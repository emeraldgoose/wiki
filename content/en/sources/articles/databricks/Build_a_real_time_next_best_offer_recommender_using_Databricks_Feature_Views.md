---
title: "Build a real-time next-best-offer recommender using Databricks Feature Views"
description: "Databricks Solution Accelerator walks through an end-to-end retail-banking next-best-offer recommender built on Feature Views: batch and streaming features declared once, point-in-time-correct training, and millisecond serving with ~34 ms p95 latency."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views"
blog: databricks
published_date: "2026-11-19"
---

# Build a real-time next-best-offer recommender using Databricks Feature Views

**Source**: [databricks](https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views) · **Published**: 2026-11-16

## Overview

Real-time personalization depends on understanding what a customer wants in the moment. When a retail banking customer checks their accounts, explores credit cards, or opens a loan calculator, each interaction signals current intent, and a relevant offer must reach them while they are still in the session. The hard part is making that intent available to the model: raw clickstream data must be aggregated into time-windowed features for two purposes — training on historical values as they existed at a given point in time, and serving predictions with millisecond latency. Building those pipelines separately creates duplicate feature definitions that can drift and degrade model accuracy.

Databricks Feature Views solve this by letting you define features once for both training and serving. The post walks through an open-source Solution Accelerator that builds a real-time next-best-offer (NBO) recommender for financial services on Databricks, end-to-end, with runnable notebooks.

## Key points

- **Build once, serve everywhere**: Feature Views unify batch and streaming features so training and serving share declarative definitions, eliminating train/serve skew.
- **Batch features** are materialized to offline Delta tables for point-in-time-correct training and to an online store for low-latency serving.
- **Streaming features** are continuously aggregated into the online store; historical values are computed point-in-time from source events for training and are not materialized to an offline store.
- **Point-in-time joins**: the `create_training_set` API retrieves feature values as they existed at each labeled event, preventing future data leakage.
- **Same definitions, two paths**: at inference time the Model Serving endpoint fetches batch features from the online store by `customer_id` using the same feature declarations as training.
- **In-session intent**: a SawtoothWindow keeps long-window streaming features (e.g. 30-day category counts) fresh as new events arrive without recomputing full history per event.
- **Benchmark**: in the smallest configuration (small endpoint, single-node online store, no tuning), streaming events became model-visible in roughly a tenth of a second, and training and serving paths produced identical values.
- **~34 ms p95 latency** for serving, per the accelerator's headline claim.

## Details

The accelerator implements a retail-banking NBO recommender. As a customer browses, the system ranks a catalog of offers (credit card upgrades, savings products, personal loans) by combining stable customer context (balances, spending, tenure, risk band) with recent clickstream activity capturing in-session intent. A single LightGBM ranker uses both, registered in Unity Catalog.

Three steps, delivered as runnable notebooks in two parts that share a catalog, schema, online store and feature definitions:

1. **Define batch and streaming features** — a `SlidingWindow` for 30-day average balance, `TumblingWindow` for 90-day spend, `ColumnSelection` for loyalty tier / risk band / income / tenure, a `RollingWindow` on a Kafka stream for category views in the last 10 minutes, a `SawtoothWindow` for 30-day category interest, and a `CustomUDF` for spend-to-income ratio. Feature Views point at a Kafka topic for streaming declarations and continuously aggregate events into the online store — no separate hand-written streaming job.
2. **Train with point-in-time-correct features** — a point-in-time join via the Feature Engineering SDK reconstructs each feature's value at the historical label time, feeding a LightGBM ranker in Unity Catalog.
3. **Serve in real time** — the ranker runs on a route-optimized Model Serving endpoint. Each request carries `{customer_id, candidate offers, session context}`; the endpoint retrieves features from the online store by key and scores all 40 offers directly, without a candidate-narrowing step. A second route-optimized Feature Serving endpoint exposes feature values so the application can explain why an offer was selected.

Benchmarking focuses on the two measurements that matter most: how quickly a click becomes a model-visible feature, and whether training and serving produce identical feature values. Both held up in the smallest, untuned configuration.

## References

- Original article: [Build a real-time next-best-offer recommender using Databricks Feature Views](https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views)
