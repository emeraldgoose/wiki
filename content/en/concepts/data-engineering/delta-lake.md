---
title: Delta Lake
description: "Seminar-level concept: Delta Lake architecture, ACID, time travel, schema evolution, optimization"
tags: [concept, data-engineering, delta-lake, lakehouse, iceberg]
locale: en
---

# Delta Lake

**Read from**: AWS lakehouse (Iceberg comparison), Databricks monitoring (Hydra), Databricks Lakebase Postgres

## What It Is
Open-source storage layer bringing ACID transactions to data lakes. Built on Parquet + transaction log.

## Architecture

### Transaction Log (DeltaLog)
- Ordered, atomic commits (JSON + checkpoint Parquet)
- **Optimistic concurrency control**: validate no conflicts at commit
- **Checkpointing**: every 10 commits (configurable) → Parquet for fast replay

### ACID Guarantees
- **Atomicity**: All-or-nothing commits (single file rename)
- **Consistency**: Schema enforcement, constraint validation
- **Isolation**: Serializable (default) via conflict detection
- **Durability**: Commits persisted to object storage

### Time Travel
```sql
SELECT * FROM table VERSION AS OF 123
SELECT * FROM table TIMESTAMP AS OF '2026-08-01'
```
- Query any historical version (audit, reproducibility, rollback)

### Schema Evolution
- `mergeSchema` / `overwriteSchema` options
- Add columns, change types (widening), reorder
- **Schema enforcement** on write (reject bad data)

### DML Operations
| Operation | Mechanism |
|-----------|-----------|
| MERGE | Upsert (CDC, slowly changing dimensions) |
| UPDATE/DELETE | Rewrite affected files (predicate pushdown) |
| INSERT | Append new files |

## Optimizations

### Partitioning + Z-Ordering
```sql
-- Partition by date, Z-order by user_id
OPTIMIZE table ZORDER BY (user_id)
```
- Co-locate related data → better predicate pushdown

### File Compaction
```sql
OPTIMIZE table
-- or with conditions
OPTIMIZE table WHERE date > '2026-01-01'
```
- Combine small files (default 128MB target)

### Vacuum (Retention)
```sql
VACUUM table RETAIN 168 HOURS  -- default 7 days
```
- Remove files not in transaction log
- **Caution**: Breaks time travel for removed versions

## Delta vs Iceberg (from AWS Source)

| Feature | Delta Lake | Apache Iceberg |
|---------|------------|----------------|
| Transaction log | JSON + checkpoint | Manifest list + manifest files |
| Partition evolution | Limited | Full (split/merge partitions) |
| Hidden partitioning | No | Yes (partition by transform) |
| Ecosystem | Databricks, Spark, Presto | Spark, Flink, Trino, Presto, Hive |
| Time travel | Version + timestamp | Snapshot ID + timestamp |

**Key Insight**: Both provide ACID on object storage. Iceberg has more flexible partitioning; Delta has tighter Databricks/Spark integration.

## Performance at Scale (from Sources)

### AWS Lakehouse (Razor Group)
- **Chose Iceberg** over Delta for: partition evolution, hidden partitioning, engine-agnostic
- But Delta would work similarly for Bronze/Silver/Gold pattern

### Databricks Hydra
- High-cardinality metrics → Delta tables in Lakehouse
- PromQL-to-SQL conversion for Grafana
- Direct SQL access for joins with deployment metadata

### Lakebase Postgres (LTAP)
- One durable copy in open columnar for OLTP + OLAP
- Delta/Iceberg as unified storage format

## Related Sources
- `sources/articles/aws-bigdata.md` (Iceberg vs Delta choice)
- `sources/articles/databricks-engineering.md` (Hydra on Delta, Lakebase LTAP)

## Related Guides
- `guides/data-engineering/spark/optimize-shuffle.md` (Delta write optimization)
