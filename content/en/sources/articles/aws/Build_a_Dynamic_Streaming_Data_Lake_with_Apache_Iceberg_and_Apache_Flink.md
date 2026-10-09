---
title: Build a Dynamic Streaming Data Lake with Apache Iceberg and Apache Flink
description: Per-record table routing and automatic schema evolution with Iceberg Dynamic Sink on Managed Service for Flink — new event types and columns without pipeline restarts.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, apache-flink, streaming, schema-evolution]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-a-dynamic-streaming-data-lake-with-apache-iceberg-and-apache-flink/"
blog: aws
---

# Build a Dynamic Streaming Data Lake with Apache Iceberg and Apache Flink

**Published**: Sep 2, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-dynamic-streaming-data-lake-with-apache-iceberg-and-apache-flink/)

## Problem

Upstream schema changes force streaming lake pipelines into a bad choice: restart the job (pausing ingestion, risking in-flight data) or run a manual migration (engineering time, schema-inconsistency risk) while the lake falls behind the source. Example: a Flink job writing `order_events` to Iceberg learns on Wednesday that the producer added a `loyalty_tier` field and a whole new `interaction_events` event type.

## Solution: Iceberg Dynamic Sink on Managed Service for Flink

With Flink 2.3 + Iceberg 1.11.0, the **Dynamic Iceberg Sink** resolves the target table **per record** and evolves schemas mid-stream — no restart:

- **Routing**: a `DynamicRecordGenerator` maps each input to a `DynamicRecord` carrying its own table ID, branch, Iceberg schema, partition spec, distribution mode, and row payload. One Flink job routes `order_events`, `interaction_events`, `user_events`, and future types to separate Iceberg tables. The sink creates missing tables on first sight.
- **Schema evolution**: before each write the sink compares record schema to table schema; new fields become optional columns committed with the next data file. Old files stay valid (new column reads null). Supports adding columns, type widening (int→long, float→double), relaxing required→optional, and dropping columns — but **not column renames**.
- **`immediateTableUpdate`**: `true` applies create/alter inline in the writer subtask (lowest latency, more catalog calls); `false` routes changed-schema records, keyed by table, to an update operator so same-table updates serialize. Steady state adds no extra shuffle either way.
- **Exactly-once**: Flink checkpointing + Iceberg two-phase commit gives end-to-end consistency without duplication or loss.

## Two schema-source options (same downstream)

1. **JSON inference** (`SchemaAgnosticRoutingGenerator`): infers Iceberg schema per record with deliberately conservative rules (all integers→long, floats→double, ISO-8601 strings→timestamp, nested objects→structs). Convenient but lossy and contract-free — nothing stops a producer silently changing a field's meaning.
2. **AWS Glue Schema Registry (Avro)**: producers register Avro schemas; Kinesis records carry a schema-version ID; the consumer decodes against the exact registered schema. Precise types (long stays long, timestamp-micros preserved), GSR compatibility policy enforced at registration, one shared source of truth. New registered versions evolve the Iceberg table with no restart.

## Partitioning

The generator — not the sink — decides partitioning: it reads a global `partition.candidates` list (e.g. `event_time,region,product`) and derives a per-table spec from fields actually present. Tables missing all candidates stay unpartitioned (monitor via `$partitions`/catalog spec — a producer emitting `create_timestamp` instead of `event_time` silently creates unpartitioned tables). Specs evolve metadata-only; old files keep their original spec until compaction rewrites them.

## Topology and isolation trade-off

One Kinesis stream with many event types keeps the walkthrough simple, but separate streams work identically: union sources into one DataStream and let the generator route per record. Unioning adds no shuffle (the sink always re-distributes by an internal per-table writer key). The real trade-off is **isolation**: all tables share one writer pool, commit aggregator, and committer, so a hot stream's backpressure couples to every table and writer parallelism is job-wide. Pool many small-to-medium event types in one job; give high-volume streams their own application.

## Deploy (CDK) and verify

`cdk-infrastructure`: `npm install`, `cdk bootstrap`, then `cdk deploy -c appType=dynamic|dynamic-avro -c tableFormatVersion=2` (add `-c catalogType=s3tables` for S3 Tables instead of Glue catalog; format v2 for broad engine compatibility, v3 for v3-aware engines like Spark on EMR 7.12+/Glue ETL). Start the app, send v1 payloads with the data generator, then v2 payloads adding `userAgent`/`scrollDepth` — new tables appear within a checkpoint interval, new fields as optional columns, queryable in Athena. Full code: [aws-samples GitHub repo](https://github.com/aws-samples/sample-streaming-data-lake-with-apache-iceberg-and-apache-flink).

## Takeaways for the seminar

- Per-record destination + carried schema turns the sink from a static endpoint into a **router with a schema contract** — the architectural reason restarts disappear.
- The JSON-vs-registry choice is a governance decision, not a performance one: inference is for exploration, registry-backed Avro for production where silent type drift is unacceptable.
- Union-into-one-sink is free on shuffle but taxed in isolation — size the blast radius deliberately.

## Related concepts

- `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/apache-flink.md`
