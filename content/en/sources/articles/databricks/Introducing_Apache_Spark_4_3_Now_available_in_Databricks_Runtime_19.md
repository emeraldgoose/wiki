---
title: "Introducing Apache Spark® 4.3 - Now available in Databricks Runtime 19"
description: "Spark 4.3 brings stateful processing to Real-Time Mode with sub-150 ms P99 latency, plus Auto CDC, faster small-data iteration, and richer SQL support."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19"
blog: databricks
published_date: 2026-11-06
---

# Introducing Apache Spark® 4.3 - Now available in Databricks Runtime 19

**Source**: [databricks](https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19) · **Published**: 2026-11-05

## Overview

Apache Spark 4.3 extends Structured Streaming with stateful processing in Real-Time Mode, enabling streaming aggregation, deduplication, and custom stateful processing for applications that must remember context across events. Representative stateful workloads achieved P99 end-to-end latency below 150 milliseconds in reported benchmarks, extending Real-Time Mode toward a complete streaming engine and reducing the need for a separate engine to reach millisecond-scale latency. The release also strengthens Spark across batch analytics, change data capture, small-dataset iteration, remote execution, and SQL.

Several capabilities define the release. SCD Type 2 Auto CDC tracks how records change over time through Python, SQL, and Spark Connect with less custom change-processing logic. Project Feather targets fixed execution overhead on small or single-partition query fragments, while Arrow-native caching supports more efficient data reuse. Spark Connect gains observability and JDBC and Python improvements that make remote execution easier to develop and operate. SQL support grows through VARIANT transformations, JSON_TABLE, temporal joins, and a preview of nanosecond timestamps for nested and time-oriented data. Spark 4.3 also starts a quarterly feature-release cadence, moving from a release every six months to one every three months.

Real-Time Mode builds on Structured Streaming's existing APIs and state store and checkpointing mechanisms for durability and recovery. Supporting stateful processing required fundamental changes to scheduling and shuffle behavior: native concurrent stage scheduling and pipelined shuffles let producer and consumer stages run concurrently instead of requiring a blocking materialization step between them. Pipelined shuffle dependencies define this execution contract while shuffle managers provide the underlying data transfer.

## Key points

- Stateful real-time applications can now use streaming aggregation, deduplication, and transformWithState with low-latency execution.
- Three benchmarked stateful workloads reported P99 latency below 150 ms, though this is not a universal latency guarantee.
- SCD Type 2 Auto CDC records record history with less custom logic across Python, SQL, and Spark Connect.
- Project Feather reduces scheduling and shuffle overhead for eligible small, single-partition fragments.
- Spark Connect observability and JDBC and Python usability improvements ease remote development and operation.
- VARIANT processing, JSON_TABLE, temporal joins, and nanosecond timestamps expand native SQL analytics.
- The project moves from a six-month to a quarterly feature-release cadence.

## Details

Reported P99 end-to-end latency figures were 136 ms for dropDuplicates, 139 ms for window aggregation, and 141 ms for transformWithState. Spark routes regular dependencies through a blocking shuffle manager and pipelined dependencies through a streaming shuffle manager, and stages in a pipelined group run and fail together only when sufficient task slots are available. The Real-Time Mode benchmarks and execution details are drawn from the linked source; exact benchmark configurations, APIs, previews, and platform availability should be checked there.

## References

- Source: [databricks](https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19)
