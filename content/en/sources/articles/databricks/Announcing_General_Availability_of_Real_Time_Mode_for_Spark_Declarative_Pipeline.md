---
title: "Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks"
description: "We introduced Real-Time Mode (RTM) last year which enabled customers to build low-latency, operational use cases. This was a game changer"
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks"
blog: databricks
published: "2026-10-29"
---

# Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks

**Source**: [databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks)
**Date**: 2026-10-29


## Overview

We introduced Real-Time Mode (RTM) last year which enabled customers to build low-latency, operational use cases. This was a game changer because it allowed customers to process streaming data in milliseconds, up to 100x faster than traditional micro-batch architecture. Furthermore, they no longer needed to maintain separate, specialized engines like Flink alongside Spark, eliminating duplicate codebases, fragmented governance models, and operational overhead. Today, we are announcing RTM in Spark Declarative Pipelines (SDP) is now Genearally Available. SDP has become the standard way to build streaming and ETL pipelines on Databricks, automatically handling dependency resolution, incremental processing, orchestration, failure recovery, and data quality enforcement. With RTM, customers can

## Key points

- Announcing General Availability of Real-Time Mode (RTM) on Spark Declarative Pipelines (SDP), delivering end-to-end processing latencies in the millisecond range for operational streaming workloads.
- Real-Time Mode eliminates the need for separate specialized engines such as Apache Flink, unifying batch, ETL, and low-latency streaming under a single framework.
- Real-Time Mode enables real-time computation and instant writes to operational stores via ForEach sinks, powering time-critical use cases like fraud detection and live personalization.
- Running RTM pipelines at lower cost: Bin-pack multiple RTM flows into a single pipeline instead of each query standing up its own resources. The system also auto-tunes source and shuffle partitions based on workload, so 
- Expanded sink support: Native Lakebase sink for SDP, with built-in batching, automatic retries, and UC-managed authentication.
- Documentation: Use Real-Time Mode on Lakeflow pipelines

## Source outline

- See the original article for section details.

## References

- Original article: [https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks)
