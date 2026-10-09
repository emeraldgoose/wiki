---
title: Apache Spark
description: "Seminar-level concept: Spark architecture, RDD/DAG, Structured Streaming, use cases, optimization"
tags: [concept, data-engineering, spark, distributed-computing, performance]
locale: en
---

# Apache Spark

**Read from**: Full documentation + source articles (AWS lakehouse, Netflix Kueue comparison, Databricks engineering, Uber Hudi)

## What It Is
Unified batch + stream processing engine for large-scale data. Memory-based cluster computing with fault-tolerant RDD/DataFrame/Dataset APIs.

## Architecture (Full Detail)

### Core Components
- **Driver**: Converts user code → logical plan → physical plan (DAG) → tasks
- **Cluster Manager**: YARN, Kubernetes, Standalone, Mesos — allocates resources
- **Workers (Executors)**: Run tasks, cache data in memory/disk, report heartbeats
- **Block Manager**: Manages cached blocks (memory + disk), handles shuffle

### Execution Model
```
User Code → Logical Plan (Catalyst) → Physical Plan (DAG) → Stages (shuffle boundaries) → Tasks
```

**Lazy Evaluation**: Transformations build lineage graph; actions trigger execution.

### RDD Lineage & Fault Tolerance
- Each RDD tracks parent RDDs + transformation function
- Lost partition → recompute from lineage (deterministic)
- Checkpointing for long lineages (truncate lineage graph)

### DAG Scheduler
- **Narrow transformations** (map, filter): pipelined within stage
- **Wide transformations** (shuffle: groupBy, join, repartition): stage boundaries
- **Task scheduling**: locality-aware (PROCESS_LOCAL → NODE_LOCAL → RACK_LOCAL → ANY)

## APIs

| API | Type Safety | Optimization | Use Case |
|-----|-------------|--------------|----------|
| RDD | Low (Java/Scala) | Manual | Low-level control, custom logic |
| DataFrame | None (untyped) | Catalyst optimizer | SQL-like, structured data |
| Dataset | High (typed) | Catalyst + encoder | Type-safe, complex logic |

**Structured APIs** (DataFrame/Dataset): Catalyst optimizer (logical → physical), Tungsten (off-heap memory, codegen).

## Streaming: Structured Streaming
- Stream as **unbounded table** (event-time + watermarks)
- **Exactly-once** via checkpointing + idempotent sinks
- **Event-time processing**: windowed aggregations, late data handling
- **Stateful operations**: `mapGroupsWithState`, `flatMapGroupsWithState`

## Performance at Scale (from Sources)

### AWS Lakehouse (Razor Group)
- Spark on EC2 (Graviton + Spot) for heavy ETL
- Bronze/Silver/Gold Iceberg tables
- Column pruning + partition pruning via Iceberg metadata

### Netflix Kueue Comparison
- Netflix moved batch to Kueue (K8s job queueing)
- Spark jobs as Kueue workloads
- Preemption/fair sharing for multi-tenant

### Databricks Monitoring
- 5B timeseries, 10T samples/day
- Pantheon (Thanos fork) for metrics
- Hydra: Lakehouse (Delta) for high-cardinality troubleshooting

### Uber Hudi + Spark
- Hudi column stats in metadata table → file pruning without footer reads
- Sorting on predicate column → tighter min/max → better pruning
- 24.8% disk reduction on export workloads

## Key Optimizations (Seminar Checklist)

### Shuffle Optimization
```python
# 1. Reduce shuffle volume
df.filter(...).groupBy(...)  # filter BEFORE groupBy
spark.sql.adaptive.enabled = True  # AQE: coalesce partitions, skew join

# 2. Broadcast joins for small tables
df.join(broadcast(small_df), ...)

# 3. Shuffle partitions
spark.sql.shuffle.partitions = 200  # tune to data size (128-256MB/partition)

# 4. Shuffle service (external shuffle service for dynamic allocation)
```

### Memory Management
```python
# Off-heap (Tungsten)
spark.memory.offHeap.enabled = true
spark.memory.offHeap.size = 2g

# Storage vs Execution fraction
spark.memory.fraction = 0.6  # default
spark.storage.memoryFraction = 0.5  # within fraction
```

### Serialization
```python
spark.serializer = org.apache.spark.serializer.KryoSerializer
spark.kryo.registrator = com.my.CustomKryoRegistrator
```

### File Formats
- **Parquet**: Columnar, predicate pushdown, dictionary encoding
- **ORC**: Similar, better predicate pushdown for Hive
- **Delta/Iceberg**: ACID, time travel, schema evolution

## When to Use Spark (vs Alternatives)
| Scenario | Spark | Flink | Trino/Presto |
|----------|-------|-------|--------------|
| Large-scale ETL | ✅ | | |
| Stream processing (exactly-once) | ✅ | ✅ | |
| Ad-hoc SQL | | | ✅ |
| ML pipelines | ✅ (MLlib) | | |
| Low-latency serving | | ✅ | |

## Related Sources
- `sources/articles/aws-bigdata.md` (lakehouse with Spark on EC2)
- `sources/articles/netflix-techblog.md` (Kueue batch orchestration)
- `sources/articles/databricks-engineering.md` (monitoring, Delta Lake)
- `sources/articles/uber-engineering.md` (Hudi column stats + Spark)

## Related Guides
- `guides/data-engineering/spark/optimize-shuffle.md`
- `guides/data-engineering/spark/optimize-join.md`
