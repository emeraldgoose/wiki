---
title: Apache Iceberg
description: Open table format for large-scale analytics datasets with ACID transactions, time travel, and schema evolution
tags: [concept, data-engineering, lakehouse, iceberg, table-format]
locale: en
---

# Apache Iceberg

**Apache Iceberg** is an open table format designed for large-scale analytic datasets. It brings database-like reliability and simplicity to data lakes while supporting multiple compute engines (Spark, Trino, Flink, Athena, etc.).

## Core Features

### ACID Transactions
- Full ACID compliance for table operations
- Snapshot isolation for readers; serializable isolation for writers
- No partial writes or corrupted states

### Time Travel & Rollback
- Query any historical snapshot by timestamp or snapshot ID
- Instant rollback to previous state (metadata operation only)
- Enables reproducible experiments and compliance auditing

### Schema Evolution
- **Add/Remove/Rename columns** without rewriting data
- **Type promotion** (e.g., int → long, float → double) safely
- **Column reordering** without data movement
- **Partition evolution** — change partition spec without rewriting data

### Partition Layout Evolution
- Change partitioning strategy (e.g., day → hour) without full table rewrite
- Hidden partitioning — partition values derived from data columns automatically
- Partition pruning at query time via manifest files

### Hidden Partitioning
- Partition transforms: `year(ts)`, `month(ts)`, `day(ts)`, `hour(ts)`, `bucket(N, col)`, `truncate(L, col)`
- No need for explicit partition columns in data
- Engine computes partition values at write time

## Architecture

### Metadata Layers
```
Catalog (REST/Hive/Glue/Nessie)
    ↓
Metadata File (table metadata, schema, partition spec, snapshots)
    ↓
Manifest List (snapshot → list of manifest files + partition stats)
    ↓
Manifest Files (data file list + partition tuples + stats: min/max/count/nulls)
    ↓
Data Files (Parquet/Avro/ORC)
```

### Key Components
- **Catalog**: Tracks current metadata pointer (REST catalog, Hive Metastore, AWS Glue, Project Nessie)
- **Metadata File**: Immutable; new version created on each commit
- **Manifest List**: Per-snapshot index of manifest files with partition bounds
- **Manifest Files**: Track data files with partition values and column-level stats
- **Data Files**: Actual data in Parquet (default), Avro, or ORC

## Compute Engine Support

| Engine | Read | Write | Notes |
|--------|------|-------|-------|
| Apache Spark | ✅ | ✅ | Native support via `spark.sql.catalog` |
| Apache Flink | ✅ | ✅ | Streaming reads/writes; dynamic sink |
| Trino/Presto | ✅ | ✅ | Iceberg connector; predicate pushdown |
| Amazon Athena | ✅ | ✅ | Serverless SQL; CTAS/INSERT |
| AWS Glue | ✅ | ✅ | ETL jobs; materialized views (5.1+) |
| Dremio | ✅ | ✅ | Reflections acceleration |
| Snowflake | ✅ | ✅ | Iceberg tables (external) |

## Iceberg REST Catalog

Standardized HTTP API for catalog operations (v1 spec):
- **Tables**: CRUD, metadata, snapshots
- **Namespaces**: Hierarchical organization
- **Views**: Logical views support
- **Authentication**: OAuth2, AWS SigV4, custom

Enables engine-agnostic table management; adopted by S3 Tables, Polaris, Unity Catalog, Gravitino.

## Streaming with Iceberg

### Flink Dynamic Sink (Iceberg 1.5+)
- **Schema evolution**: Automatic handling of new columns (null for old files)
- **New event types**: Automatic table creation per event type
- **Exactly-once**: Checkpointed writes with transaction coordination
- **Format versions**: v2 (broad compatibility) or v3 (row-level deletes, better compression)

### CDC Integration
- Debezium → Kafka → Flink → Iceberg (upsert via equality delete + insert)
- Native merge-on-read (MoR) for high-throughput CDC

## Performance Optimizations

### Compaction
- **Automatic** (S3 Tables, Athena) or **manual** (Spark `rewriteDataFiles`)
- Merges small files; rewrites for partition alignment
- Snapshot expiration + orphan file cleanup

### Manifest Merging
- Combine small manifest files for faster planning
- Triggered automatically or via `rewriteManifests`

### Scan Planning
- Partition pruning via manifest list partition bounds
- Column stats (min/max/nulls) for predicate pushdown
- File-level pruning without opening data files

## Operational Patterns

### Branching & Tagging (Nessie/Catalog)
- **Branches**: Isolated development; merge back via catalog
- **Tags**: Immutable snapshots for releases/audits
- **Multi-table transactions**: Cross-table ACID via Nessie

### Multi-Engine Access
- Single copy of data; Spark for ETL, Trino for interactive, Flink for streaming
- No data duplication; compute scales independently

### Governance
- **Row/Column-level security**: Via catalog (Lake Formation, Polaris, Unity)
- **Audit logging**: Catalog tracks all metadata changes
- **Data contracts**: Schema validation on write

## Key References
- [Iceberg Spec](https://iceberg.apache.org/spec/)
- [Iceberg REST Catalog Spec](https://github.com/apache/iceberg/tree/master/rest-catalog)
- [Flink Iceberg Integration](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/iceberg/)
- [AWS S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html)
- [Project Nessie](https://projectnessie.org/) — Git-like versioning for Iceberg

## Related Concepts
- `concepts/data-engineering/stream-processing.md`
- `concepts/data-engineering/delta-lake.md`
- `concepts/data-engineering/apache-spark.md`
- `concepts/infrastructure/kubernetes.md` (Flink on K8s)