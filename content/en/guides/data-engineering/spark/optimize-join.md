---
title: Optimize Spark Join — Guide (Seminar Level)
description: "Execution guide: how to optimize Spark joins (broadcast, sort-merge, skew, bucketing)"
tags: [guide, data-engineering, spark, join, performance]
locale: en
---

# Optimize Spark Join — Execution Guide

**Synthesizes**: `concepts/data-engineering/apache-spark.md`, `sources/articles/aws-bigdata.md`, `sources/articles/uber-engineering.md`

## Join Types & When to Use

| Join Type | Condition | Shuffle? | Best For |
|-----------|-----------|----------|----------|
| Broadcast Hash Join | One side < threshold | No (broadcast) | Small table (< 10MB default) |
| Sort-Merge Join | Both sides large, sortable | Yes (shuffle + sort) | Large tables, equi-join |
| Shuffle Hash Join | One side medium, no sort | Yes (shuffle) | Medium tables |
| Cartesian Join | No condition | Yes (massive) | Avoid unless tiny |

## Optimization Strategies

### 1. Broadcast Join (Default for Small Tables)
```python
from pyspark.sql.functions import broadcast

# Auto: spark.sql.autoBroadcastJoinThreshold (default 10MB)
df_large.join(broadcast(df_small), "key")

# Force broadcast
df_large.join(broadcast(df_small), "key").hint("broadcast")

# Verify in plan: "BroadcastHashJoin" + "BroadcastExchange"
```

**Threshold tuning**:
```python
# Increase for larger dimension tables
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "104857600")  # 100MB
```

### 2. Sort-Merge Join Optimization
```python
# Ensure both sides partitioned by join key
df1 = df1.repartition("join_key")
df2 = df2.repartition("join_key")

# Or use bucketing (pre-sorted)
df1.write.bucketBy(200, "join_key").sortBy("join_key").saveAsTable("t1_bucketed")
df2.write.bucketBy(200, "join_key").sortBy("join_key").saveAsTable("t2_bucketed")

# Join: no shuffle, direct merge
spark.table("t1_bucketed").join(spark.table("t2_bucketed"), "join_key")
```

### 3. Skew Join Handling (AQE)
```python
# Enable AQE skew join
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# AQE splits skewed partition automatically
# Check plan: "ShuffleQueryStage" with "skewed"
```

### 4. Manual Skew Mitigation (Salt/Partition)
```python
# For extreme skew: add salt to join key
import random

def add_salt(key, num_buckets=100):
    return f"{key}_{random.randint(0, num_buckets-1)}"

# Apply to skewed side
df_skewed = df_skewed.withColumn("salted_key", 
    concat(col("key"), lit("_"), (rand() * 100).cast("int")))

# Replicate other side
df_other = df_other.withColumn("salted_key",
    concat(col("key"), lit("_"), explode(sequence(lit(0), lit(99)))))

# Join on salted_key, then drop
result = df_skewed.join(df_other, "salted_key").drop("salted_key")
```

### 5. Join Order Optimization
```python
# Spark Catalyst reorders automatically, but hints help
df1.join(df2, "key").join(df3, "key")  # Catalyst decides

# Force order
df1.hint("broadcast").join(df2, "key").join(df3, "key")

# Statistics matter!
spark.sql("ANALYZE TABLE t1 COMPUTE STATISTICS FOR ALL COLUMNS")
```

### 6. Join with Null Handling
```python
# Null-safe join (==)
df1.join(df2, df1.key <=> df2.key)

# Filter nulls first if not needed
df1.filter(col("key").isNotNull()).join(df2, "key")
```

### 7. Memory for Join
```python
# Increase shuffle memory for large joins
spark.conf.set("spark.sql.shuffle.partitions", "800")
spark.conf.set("spark.memory.fraction", "0.7")
spark.conf.set("spark.memory.storageFraction", "0.3")

# Off-heap for Tungsten
spark.conf.set("spark.memory.offHeap.enabled", "true")
spark.conf.set("spark.memory.offHeap.size", "3g")
```

## From Sources

### AWS Lakehouse
- Iceberg metadata pruning → fewer files scanned for join
- Redshift Serverless for BI joins (star schema)

### Uber Hudi
- Column stats → file pruning before join
- Sorting on predicate → tighter min/max → less data for join

## Verification Checklist
- [ ] Broadcast join used for dimension tables (< 100MB)
- [ ] Skew join enabled (AQE) for fact-fact joins
- [ ] No Cartesian products
- [ ] Join order optimal (small → large)
- [ ] Statistics collected (`ANALYZE TABLE`)
- [ ] Partition count appropriate (128-256MB/shuffle partition)

## Related Concepts
- `concepts/data-engineering/apache-spark.md`
- `guides/data-engineering/spark/optimize-shuffle.md`
