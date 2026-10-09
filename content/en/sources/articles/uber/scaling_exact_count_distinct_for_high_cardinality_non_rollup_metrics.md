---
title: Scaling Exact COUNT(DISTINCT) for High-Cardinality Non-Rollup Metrics in Distributed Data Pipelines
description: Chunked aggregation buffer strategy partitions Roaring bitmaps by hash prefix to beat the JVM 2GB limit for exact distinct counts at billions scale
tags: [source, uber, data-engineering, count-distinct, spark, hive, bitmap]
locale: en
source_url: "https://www.uber.com/us/en/blog/scaling-exact-count/"
blog: uber
published_date: 2026-07-30
---

# Scaling Exact COUNT(DISTINCT) for High-Cardinality Non-Rollup Metrics in Distributed Data Pipelines

**Authors**: Prakhar Agarwal, Avinash Varma Sagi, Abhay Singh Chauhan
**Source**: [Uber Blog](https://www.uber.com/us/en/blog/scaling-exact-count/)
**Date**: Jul 30, 2026

## Problem

Non-rollup metrics (MAU, quarterly retention, cross-window engagement) cannot be derived from coarser pre-aggregates — no composition of daily/monthly counts yields a correct quarterly result. At quarterly scale: exact distinct count over 3.6B UUIDs. RoaringBitmap hits the JVM 2GB single-array limit at ~179M unique identifiers.

## Failed Approaches

- **Bitmap-32 + Global Dictionary**: single point of failure, sequential backfills.
- **Bitmap-64 monolithic**: 2GB JVM array limit breached at ~179M uniques — structural, not tunable.
- **HyperLogLog**: 1–5% error unacceptable for financial reporting.

## Solution: Chunked Aggregation Buffer Strategy

Partition the bitmap aggregation buffer as `Map<Integer, Roaring64Bitmap>` keyed by the top 16 bits of xxHash64:

```
chunkId = (int)(hash >>> 48)   // 65,536 chunks
```

- Average ~55K values/chunk at 3.6B scale; Chernoff bound confirms near-zero OOM probability.
- 16-bit is the sweet spot: 8 bits gives insufficient headroom; 24 bits adds map overhead/GC pressure.
- Each chunk serializes independently → peak memory bounded by the largest chunk; the 2GB constraint is eliminated entirely.
- Self-describing partial results (0xDEADBEEF magic number), streaming serialization (no monolithic `byte[]`).
- UDAF returns a constant 8-byte long per group key instead of multi-KB bitmaps → less shuffle, less HDFS/network I/O.

## Deployed Results

- 75 metric families across Mobility, Delivery, Platform; zero OOM failures post-deployment.
- Two-year backfill time −65% on average (up to −94% for highest-cardinality workloads).
- Daily pipeline runtime −23%; monthly data-prep time −43%.

## Next Steps (from the article)

- Richer analytics on non-rollup metrics: dimensional slicing, cohort comparisons, trend analysis.
- Self-serve metric primitive: chunked exact COUNT(DISTINCT) as a first-class type in uMetric.
- Generalization beyond UUID workloads to any 64-bit hashed domain (device IDs, session tokens, geohashes).

## Seminar Takeaways

- Distinguish rollup vs non-rollup metrics early: the distinction dictates the entire aggregation architecture.
- When a limit is structural (JVM array size), only a structural fix (value-space partitioning) works — no tuning escapes it.
- Partition by hash prefix to keep chunks disjoint, balanced, and independently serializable.
- Exactness at scale is achievable: hash-partitioned bitmaps give exact counts with bounded memory.

## Related Concepts

- `concepts/data-engineering/apache-spark.md` (Spark UDAF, aggregation state)
- `concepts/data-engineering/stream-processing.md` (real-time metrics)
