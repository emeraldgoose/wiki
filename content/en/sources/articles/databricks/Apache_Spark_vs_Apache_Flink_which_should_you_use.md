---
title: "Apache Spark vs Apache Flink: which should you use?"
description: "Databricks argues that Spark Real-Time Mode removes the latency gap that once justified adding Apache Flink: in its public benchmark, Spark matched or beat Flink on p99 latency for stateless, aggregation and join workloads, framed as up to 92% faster than Flink. The post compares the engines feature by feature and narrows Flink's remaining fit to very large keyed state, complex event processing, event-time timers and existing Flink platforms."
tags: [source, databricks, apache-spark, apache-flink, streaming, en]
locale: en
source_url: "https://www.databricks.com/blog/spark-vs-flink"
blog: databricks
published_date: 2026-11-14
---

# Apache Spark vs Apache Flink: which should you use?

**Source**: [Databricks Blog](https://www.databricks.com/blog/spark-vs-flink)

## Overview

For years the main reason to put Apache Flink next to Apache Spark was latency: Flink was stream-native, while Spark streamed in micro-batches measured in seconds. Databricks' answer is Real-Time Mode, a trigger that takes an existing Structured Streaming query down to millisecond, end-to-end latency. With that gap closed, the post argues, the question stops being which engine is faster at the edge and becomes how many engines a team wants to build, operate and govern.

Spark is the unified option: batch ETL, SQL analytics, machine learning and streaming on one engine, with the same DataFrame and SQL code moving between a scheduled batch job, a micro-batch stream and a Real-Time Mode stream. Flink is the specialist: designed streaming-first, treating batch as a bounded stream, strong at keyed state and complex event processing. Databricks positions Flink for a narrow set of cases and backs its consolidation argument with a public benchmark and named production users.

The article is candid about the evidence: Databricks ran the benchmark, Spark ran on Databricks while Flink ran on AWS Managed Service for Apache Flink 1.18, and the comparison pits Spark's worst run against Flink's best run. Results depend on the workload, so teams should benchmark their own pipelines before deciding.

## Key points

- In Databricks' published benchmark, Spark Real-Time Mode matched Flink on stateless work and had lower p99 latency on stateful aggregation and stream-static joins.
- The benchmark code is public, uses customer-derived feature-computation workloads, and ran at 10,000 records per second for 30 minutes, measuring Kafka input-to-output latency.
- Reported p99 end-to-end latency: stateless transformation 3 ms for both engines; stateful aggregation 14 ms (Spark) versus 45 ms (Flink); stream-static join 9 ms versus 95 ms.
- Databricks summarized the results as up to 92% faster than Flink, while noting Spark ran on Databricks and Flink on AWS Managed Service for Apache Flink 1.18, comparing Spark's worst run with Flink's best run.
- MakeMyTrip considered Flink, chose Spark Real-Time Mode to avoid a second engine, and cut P50 latency to 44 ms and P99 from more than a minute to about 500 ms; Coinbase and DraftKings also run Real-Time Mode in production.
- Real-Time Mode is a trigger on an existing Structured Streaming query, so the same code moves between latency tiers without a rewrite; it needs update output mode and Kafka or a row-level foreach sink.
- Stateful operators arrive in open source with Apache Spark 4.3 and are generally available on Databricks, on classic compute or in Lakeflow Spark Declarative Pipelines.
- Flink's remaining fits: very large keyed state via Flink 2.x disaggregated state (ForSt), complex event processing with the built-in CEP library or SQL MATCH_RECOGNIZE, and an existing Flink platform for standalone streams.
- Event-time timers on the low-latency path remain the one listed technical gap: Spark Real-Time Mode does not yet support them in transformWithState.
- One engine means one codebase, one team and one governance model: streaming tables and batch tables share lineage and access control in Unity Catalog, and the same pipelines build ML features for training and online inference, as DraftKings does with transformWithState.
- Migration is a mapping exercise: most Flink SQL and DataStream logic maps to Spark SQL and DataFrames in Structured Streaming; start with stateless and aggregation jobs, then move stateful logic to transformWithState.

## Details

### Scope: unified engine versus stream-first specialist

Spark started as a batch engine and added Structured Streaming, which treats a stream as a table that keeps growing. Flink was designed for streaming first and treats batch as a bounded stream. Both are Apache Software Foundation projects with exactly-once processing, stateful operators and SQL APIs — the difference is scope. Languages differ too: Spark covers Python, SQL, Scala and Java, plus Go, Rust and Swift clients through Spark Connect, while Flink offers Java, SQL and Python (PyFlink). On machine learning, Spark has MLlib, feature pipelines, vector search in SQL and LLM data prep; Flink has limited native ML and is usually paired with another system. Lakehouse access is native Delta Lake and Apache Iceberg read and write on Spark, versus connectors for Flink.

### Inside the latency benchmark

The benchmark measured Kafka input-to-output latency at 10,000 records per second for 30 minutes on customer-derived feature-computation workloads. Spark Real-Time Mode tied Flink at 3 ms p99 on stateless transformation, then pulled ahead where state mattered: 14 ms versus 45 ms on stateful aggregation, and 9 ms versus 95 ms on stream-static joins. Databricks framed the aggregate as up to 92% faster than Flink. The caveats are stated plainly: Spark ran on Databricks, Flink on AWS Managed Service for Apache Flink 1.18, and Spark's worst run was compared with Flink's best run, so treat the numbers as evidence for these workload patterns rather than a universal verdict. Production results point the same way — MakeMyTrip cut P50 to 44 ms and P99 from over a minute to about 500 ms after choosing Spark to avoid a second engine.

### Choosing Flink, and why one engine matters

Flink makes sense when most of four conditions hold: state far larger than local disk (Flink 2.x disaggregated state), pattern matching across event sequences with Flink CEP or SQL MATCH_RECOGNIZE, heavy reliance on event-time timers on the low-latency path, or an existing Flink platform whose streams do not feed batch, SQL or ML. If the stream also feeds analytics, ML features or lakehouse tables, Spark avoids duplicating logic, operations and governance. Every second engine adds a second codebase, a second skill set and a second set of governance rules; teams that pair Spark for batch with Flink for streaming often rewrite the same business logic twice and debug drift between them. Pipelines can also be declared instead of hand-wired: Spark Declarative Pipelines manage dependencies and incremental refresh for streaming tables. Databricks, founded by the original creators of Apache Spark, runs Real-Time Mode as generally available, and code written for open source Spark runs on Databricks unchanged.
