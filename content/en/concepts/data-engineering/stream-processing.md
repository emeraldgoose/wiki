---
title: Stream Processing
description: "Seminar-level concept: stream processing fundamentals, event-time, watermarks, stateful ops, frameworks"
tags: [concept, data-engineering, stream-processing, flink, spark-streaming, kafka-streams]
locale: en
---

# Stream Processing

**Read from**: Netflix real-time graph, Twitter Sparrow, Uber export workloads, Databricks monitoring, LinkedIn FishDB

## What It Is
Continuous computation on unbounded data streams. Event-driven, low-latency, stateful processing.

## Core Concepts

### Event-Time vs Processing-Time
| Aspect | Event-Time | Processing-Time |
|--------|------------|-----------------|
| Definition | When event occurred | When event processed |
| Correctness | Handles late/out-of-order | Simple, non-deterministic |
| Watermarks | Required | Not needed |

**Watermarks**: Monotonic timestamp threshold; "all events before T have arrived". Late events → side output or drop.

### Windowing
| Type | Definition | Use Case |
|------|------------|----------|
| Tumbling | Fixed-size, non-overlapping | Hourly counts |
| Hopping | Fixed-size, overlapping | 5-min every 1 min |
| Session | Activity-gap based | User sessions |
| Global | All elements | Single aggregation |

### Stateful Processing
- **Keyed state**: Per-key (map, list, aggregating)
- **Operator state**: Per-operator (Kafka consumer offsets)
- **Checkpointing**: Periodic snapshots to durable storage (exactly-once)

### Event-Time Join
- **Interval join**: `left.ts BETWEEN right.ts - X AND right.ts + Y`
- **Temporal table join**: Join with versioned table (lookup at event-time)

## Frameworks Comparison

| Feature | Flink | Spark Structured Streaming | Kafka Streams |
|---------|-------|---------------------------|---------------|
| Event-time | ✅ Native | ✅ Native | ✅ Native |
| Exactly-once | ✅ | ✅ | ✅ (v2) |
| Latency | ~ms | ~100ms | ~ms |
| State backend | RocksDB/memory | RocksDB/memory | RocksDB |
| SQL support | Flink SQL | Spark SQL | ksqlDB |
| Deployment | K8s/YARN | K8s/YARN | Embedded |

## Patterns from Sources

### Netflix (Real-Time Distributed Graph)
- eBPF → Kafka → multi-layer topology (network, IPC, tracing)
- Immutable data structures → GC pressure at millions records/sec
- Hash-based partition redistribution on ASG scale
- Real-time updates: tens of minutes vs hour-old batch

### Twitter (Sparrow: Batch → Streaming)
- Shift from batch event approach to streaming pipelines
- Real-time search, analytics, data quality

### Uber (Export Workloads)
- Hudi column stats for file pruning (avoids footer reads)
- Sorting on predicate column for tighter min/max
- Streaming-friendly: incremental updates

### Databricks (Hydra)
- High-cardinality metrics → Delta Lake
- PromQL-to-SQL conversion for Grafana
- Direct SQL access for deep analysis

## Seminar-Level Design Checklist

1. **Define event-time semantics** (source timestamp, watermark strategy)
2. **Choose windowing** (tumbling/hopping/session based on business logic)
3. **Design state** (keyed vs operator, TTL for cleanup)
4. **Checkpointing interval** (trade-off: recovery time vs overhead)
5. **Handle late events** (side output, allowed lateness)
5. **Exactly-once sinks** (idempotent writes, transactional sinks)
6. **Monitor**: lag, latency, throughput, backpressure

## Related Sources
- `sources/articles/netflix-techblog.md` (real-time graph)
- `sources/articles/twitter-engineering.md` (Sparrow batch→stream)
- `sources/articles/uber-engineering.md` (Hudi streaming-friendly)
- `sources/articles/databricks-engineering.md` (Hydra high-cardinality)
- `sources/articles/linkedin-engineering.md` (FishDB retrieval)

## Related Guides
- `guides/data-engineering/spark/optimize-shuffle.md`
- `guides/data-engineering/kafka/partitioning.md`
