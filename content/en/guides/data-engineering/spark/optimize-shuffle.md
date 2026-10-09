---
title: Optimize Spark Shuffle — Guide (Seminar Level)
description: "Execution guide: how to optimize Spark shuffle (technical seminar level)"
tags: [guide, data-engineering, spark, performance, shuffle]
locale: en
---

# Optimize Spark Shuffle — Execution Guide

**Synthesizes**: `concepts/data-engineering/apache-spark.md`, `sources/articles/aws-bigdata.md`, `sources/articles/netflix-techblog.md`, `sources/articles/uber-engineering.md`

## Problem
Shuffle = data redistribution across partitions (groupBy, join, repartition). Dominates runtime for large-scale ETL. Network I/O + disk spill + serialization.

## Diagnosis (Check First)

```python
# Spark UI → SQL / Stages tab
# Look for:
# - Shuffle Read / Write (GB)
# - Shuffle Spill (Memory + Disk)
# - Skew: some tasks >> median duration
# - Partition count vs data size
```

## Optimization Checklist

### 1. Minimize Shuffle Volume
```python
# Filter BEFORE shuffle
df.filter(col("date") > "2026-01-01").groupBy("user_id").count()

# Project only needed columns
df.select("user_id", "event_type").groupBy("user_id").count()

# Use approximate algorithms when exact not required
df.approx_count_distinct("user_id")  # vs countDistinct
```

### 2. Adaptive Query Execution (AQE) — Enable Always
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")
```
- **Coalesce partitions**: Merge small partitions post-shuffle
- **Skew join**: Split skewed partition into sub-partitions
- **Local shuffle reader**: Read shuffle locally when possible

### 3. Shuffle Partitions Tuning
```python
# Target: 128-256 MB per partition
# For 100GB shuffle data: 400-800 partitions
spark.conf.set("spark.sql.shuffle.partitions", "800")

# Or auto-size (Spark 3.3+)
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "134217728")  # 128MB
```

### 4. Broadcast Joins (Small Table)
```python
from pyspark.sql.functions import broadcast

# Threshold: spark.sql.autoBroadcastJoinThreshold (default 10MB)
large_df.join(broadcast(small_df), "key")

# Verify in plan: "BroadcastHashJoin"
```

### 5. Sort + Bucket for Repeated Joins
```python
# Pre-sort and bucket
df.write.bucketBy(200, "user_id").sortBy("user_id").saveAsTable("events_bucketed")

# Subsequent joins: no shuffle (sort-merge join without shuffle)
spark.read.table("events_bucketed").join(other_bucketed, "user_id")
```

### 6. Serialization & Memory
```python
# Kryo (faster, smaller than Java serialization)
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
spark.conf.set("spark.kryo.registrator", "com.my.CustomKryoRegistrator")

# Off-heap (Tungsten)
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "2g")

# Shuffle compression
spark.conf.set("spark.shuffle.compress", "true")
spark.conf.set("spark.shuffle.spill.compress", "true")
spark.conf.set("spark.io.compression.codec", "lz4")  # or zstd
```

### 7. Shuffle Service (for Dynamic Allocation)
```python
# External shuffle service (keeps shuffle data when executors removed)
spark.conf.set("spark.shuffle.service.enabled", "true")
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
```

## From Sources

### AWS Lakehouse (Razor Group)
- Spark on EC2 (Graviton + Spot)
- Iceberg metadata pruning reduces shuffle need
- Column pruning at file level

### Netflix Kueue
- Batch jobs with Spark; Kueue manages queueing
- Preemption for priority workloads

### Uber Hudi
- Column stats in metadata table → file pruning
- Sorting on predicate column → tighter min/max → less shuffle

## Verification Checklist
- [ ] Shuffle Read/Write reduced >50%
- [ ] Shuffle Spill (Disk) = 0
- [ ] No task skew (max/median < 3x)
- [ ] Broadcast joins used where applicable
- [ ] AQE enabled (check plan: "AdaptiveSparkPlan")
- [ ] Partition count appropriate (128-256MB/partition)

## Related Concepts
- `concepts/data-engineering/apache-spark.md`
- `concepts/data-engineering/stream-processing.md`

## Related Guides
- `guides/data-engineering/spark/optimize-join.md`
