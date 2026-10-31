---
title: "Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks"
description: "Real-Time Mode (RTM) on Spark Declarative Pipelines is now generally available, bringing millisecond end-to-end latency to SDP while keeping its built-in dependency handling, orchestration and data-quality features."
tags: [source, databricks, streaming, en]
locale: en
source_url: "https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks"
blog: databricks
published_date: 2026-10-29
---

# Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks

**Source**: [Databricks Blog](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks) · **Published**: 2026-10-29

## Overview
Databricks is making Real-Time Mode (RTM) generally available on Spark Declarative Pipelines (SDP), unifying operational low-latency streaming and batch/ETL workloads on a single framework. SDP already handles dependency resolution, incremental processing, orchestration, failure recovery and data quality, and RTM adds end-to-end processing latencies in the millisecond range on top of those benefits. RTM streams data continuously, runs all query stages simultaneously and passes data between stages as soon as it is produced, whereas traditional micro-batch architectures are multiple orders of magnitude slower. Customers no longer need a separate specialized engine such as Flink beside Spark, eliminating duplicate codebases, fragmented governance and operational overhead. RTM extends SDP into latency-sensitive workloads that demand instant response to streaming data, including fraud scoring, real-time alerting, live personalization, recommendations and ML feature computation.

## Key points
- Real-Time Mode on SDP is now generally available and delivers end-to-end latencies in the millisecond range for operational streaming workloads.
- RTM removes the need to operate a separate engine, so teams use one framework with one observability stack and one billing model across all pipelines.
- RTM pipelines retain SDP features such as versionless upgrades and low-downtime maintenance.
- SDP serverless provides sub-second latency without cluster sizing work, auto-tunes based on workload and bills only for the cores the query uses.
- Real-time flows can write computed features to any custom sink, such as Lakebase, Redis or other OLTP stores, through a ForEach sink with millisecond delivery to the online store.
- One highlighted use case is ML feature computation for fraud detection and personalization: the Databricks Feature Store reaches p99 latency of 200 ms from Kafka to the online feature store.

## Details
RTM suits any workload that needs to turn data into decisions in milliseconds. Benchmarks against Apache Flink on actual customer feature-computation workloads show RTM up to 92% faster than the specialized engine. To enable it, set the pipeline to continuous mode, set spark.databricks.streaming.realTimeMode.enabled to true, then define an update flow with pipelines.trigger set to RealTime and a target pointing to a sink; supported sources and sinks are described in the documentation.

For sinks, feature-computation or fraud use cases need features to land in a queryable low-latency store, not simply to compute. A ForEach sink lets developers define a writer implementing open, process and close so SDP writes row by row to an OLTP store, avoiding offline-to-online sync and allowing applications to query fresh features with ultra-low latency. Serverless RTM bin-packs multiple flows into a single pipeline instead of each query standing up its own resources, and the system auto-tunes source and shuffle partitions by workload. Planned additions include native Lakebase sink support with built-in batching, automatic retries and Unity-Catalog-managed authentication. In summary, RTM extends the SDP APIs teams already use, delivering single-figure millisecond latency while keeping one governed, server-managed, simply-tuned pipeline.

## References
- Original article: [Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks)
