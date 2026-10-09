---
title: "Batch vs Stream Processing"
description: "Batch and stream processing compared: execution models, latency and cost tradeoffs, Spark versus Flink, and how to choose"
tags: [concept, data-engineering, batch, streaming, spark, flink]
locale: en
published: 2026-09-07
---

# Batch vs Stream Processing

**Batch processing** computes over bounded, finite datasets on a schedule (hourly, daily), while **stream processing** computes over unbounded, continuous event flows with per-record or small-window latency. The choice shapes latency, cost, correctness guarantees, and operational burden more than any single tool choice.

## Why the Distinction Matters

Every data pipeline answers three questions: how fresh must results be, how complete must each result be, and what happens when data arrives late or out of order. Batch gives complete, deterministic answers slowly. Streaming gives fast, incremental answers that must explicitly handle lateness, retractions, and state. Picking wrong costs real money: a daily batch job forced into sub-second freshness becomes a fragile hourly cron, while a streaming cluster built for a report nobody reads before 9am burns compute around the clock.

## How Batch Works

A batch job reads a fixed input (a partition, a snapshot, yesterday's events), runs a DAG of stages to completion, and writes an output. Concrete example: an Apache [[apache-spark|Spark]] job that reads the day's order events from S3, joins them against a product dimension, aggregates revenue per category, and overwrites a reporting table. Scheduling comes from an orchestrator (Airflow, Dagster), retries re-run whole tasks or stages, and correctness is straightforward: re-run the job over corrected inputs and the output converges.

Batch strengths are simplicity and efficiency. Full-dataset scans amortize startup cost, columnar formats (Parquet, [[apache-iceberg|Iceberg]]) give high throughput per dollar, and exactly-once output is achievable with idempotent writers (overwrite partition, transactional commit). Weakness is freshness: results are only as new as the last successful run, and shrinking the interval toward minutes turns batch into "micro-batch with extra operational pain."

## How Stream Processing Works

A streaming job runs continuously: it ingests events (typically from Kafka, Pulsar, or Kinesis), maintains keyed state, and emits results per event or window. Concrete example: an Apache [[apache-flink|Flink]] job keyed by user session that counts clicks in 5-minute tumbling windows, updates a fraud score per transaction, and sinks alerts to a queue within seconds. Time semantics matter here: **event time** (when it happened) versus **processing time** (when the system saw it). Watermarks track event-time progress so windows can close; late events go to side outputs or trigger recomputation.

Streaming strengths are freshness and per-event reactions: recommendations, fraud blocks, live dashboards. Cost is complexity: state backends (RocksDB, heap), checkpointing to durable storage, savepoint-compatible upgrades, and exactly-once semantics that require transactional sinks (Kafka transactions, two-phase Iceberg commits). A streaming job is a stateful service, not a script: it needs alerting, backpressure monitoring, and capacity for peak throughput plus replay.

## Tradeoff Comparison

| Dimension | Batch | Stream |
|-----------|-------|--------|
| Latency | Minutes to hours | Milliseconds to seconds |
| Throughput per dollar | High (sequential scans) | Lower (always-on state + coordination) |
| Correctness model | Re-run converges | Watermarks, allowed lateness, retractions |
| Late data | Free (next run includes it) | Explicit policy (drop, side output, update) |
| Operational shape | Scheduled jobs + retries | Long-lived service + checkpoints |
| Debugging | Re-run with logs | Replay from Kafka offsets, savepoints |

The middle ground is real: Spark Structured Streaming and Flink in micro-batch mode trade single-digit-second latency for simpler exactly-once and higher throughput. Many teams land here before committing to pure per-event streaming.

## Choosing in Practice

- Default to batch when freshness tolerance exceeds ~15 minutes: reports, billing, training-data generation, backfills.
- Choose streaming when a decision or alert loses value within seconds: fraud, abuse, live personalization, operational monitoring.
- Common hybrid: Flink or Kafka Streams for per-event enrichment and windowing into an [[apache-iceberg|Iceberg]] table, then [[trino|Trino]] or Spark SQL for minute-fresh interactive analytics on top.
- Cost check: estimate the always-on streaming cluster (plus state storage and cross-AZ traffic) against the batch alternative before committing; streaming justifies itself on value-per-second, rarely on compute-per-byte.

## Pitfalls

- **Treating streams as fast batch**: fixed-interval cron over growing inputs drifts late under load; if you need sub-interval freshness constantly, that is a streaming problem.
- **Ignoring event time**: windowing on processing time silently misattributes late mobile or IoT events; use event time plus watermarks from the start.
- **Unbounded state**: keyed joins or sessions without TTLs grow RocksDB until checkpoints time out; set state TTL and monitor state size per operator.
- **No replay plan**: without retained Kafka topics (or an Iceberg changelog) you cannot rebuild state after a bug; size retention for at least one full reprocessing window.
- **Dual pipelines drifting**: maintaining separate batch and streaming logic for the same metric invites silent divergence; share definitions (SQL, dbt models, or a single Flink SQL query) where possible.

## References

- Flink documentation on timely stream processing: https://flink.apache.org/
- Spark Structured Streaming guide: https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
- Related: [[apache-spark|Apache Spark]], [[apache-flink|Apache Flink]], [[apache-iceberg|Apache Iceberg]], [[trino|Trino]]
