---
title: "Trino"
description: "Distributed MPP SQL query engine: coordinator-worker architecture, connectors, cost-based optimizer, and lakehouse querying"
tags: [concept, data-engineering, trino, sql, query-engine, lakehouse]
locale: en
published: 2026-09-07
---

# Trino

> Read this page in Korean: [/ko/concepts/data-engineering/trino](/ko/concepts/data-engineering/trino)

**Trino** (formerly PrestoSQL, forked from Facebook's Presto in 2020) is a distributed SQL query engine for interactive analytics over heterogeneous sources: data lakes, warehouses, NoSQL, and event streams. It executes federated ANSI SQL at memory speed without owning storage.

## Positioning

Trino separates compute from storage. Unlike [[apache-spark|Spark]], which ships a full processing framework with its own APIs, Trino does one thing: answer SQL fast by pushing execution to wherever the data lives. A single query can join an [[apache-iceberg|Iceberg]] table on S3 with a Postgres dimension and an Elasticsearch index, with Trino handling type coercion, distributed joins, and partial pushdown into each source.

## Architecture

### Coordinator and Workers

- **Coordinator**: parses SQL, plans and optimizes the query, and schedules stages onto workers. It also serves the UI and REST API. Deploy active-standby or with failover coordinators; a dead coordinator kills in-flight queries.
- **Workers**: execute pipeline stages, exchange intermediate pages over the network, and stream results back. Workers are stateless and horizontally scalable: add nodes, get roughly linear speedup on scan-heavy queries until the object store or shuffle bandwidth saturates.
- **Discovery**: workers register with the coordinator via service discovery, so clusters autoscale on Kubernetes without config rewrites.

### Execution Model

Trino compiles each query stage into pipelined, vectorized operators running in a volcano-style pull loop across worker threads. Data moves in compressed columnar pages (sized to CPU caches), spilling to disk only when memory limits demand it. Fault tolerance is at query-retry granularity rather than Spark-style stage recomputation, which is why Trino targets minutes-long interactive queries, not multi-hour ETL.

## Connectors

Connectors are Trino's superpower: each exposes an external system as SQL tables with metadata mapping and predicate/projection pushdown.

| Connector | Source | Notes |
|-----------|--------|-------|
| Hive / Iceberg / Delta / Hudi | Data lakes (S3, GCS, ADLS) | Columnar scan, partition pruning, dynamic filtering |
| Postgres / MySQL | RDBMS | Join pushdown where safe; watch source load |
| Kafka | Event streams | Table-per-topic with offsets as pseudo-columns |
| Elasticsearch / OpenSearch | Search indexes | Full-text predicates pushed down |
| BigQuery / Snowflake / Redshift | Warehouses | Federation over existing marts |

Pushdown quality decides performance: a connector that pushes `WHERE date = ...` into partition pruning scans megabytes; one that does not scans terabytes. Always verify with `EXPLAIN` that filters reach the source.

## Cost-Based Optimizer

Trino's cost-based optimizer (CBO) uses table and column statistics to order joins, choose broadcast versus partitioned exchange, and place aggregations. Concretely:

- **Statistics**: run `ANALYZE` on large lake tables so the planner knows row counts and NDVs; stale stats are the leading cause of sudden plan regressions.
- **Join strategies**: small dimensions broadcast to all workers (no shuffle), large-to-large joins repartition on keys. Automatic, but skewed keys still need salted pre-aggregation or filtered semi-joins.
- **Dynamic filtering**: at runtime, the build side of a join ships a Bloom filter to the probe-side scan, skipping entire splits before they are read. This single feature often cuts lake-query I/O by an order of magnitude.

## Memory and Concurrency Management

Production clusters live or die by resource groups: JSON-configured queues assigning query classes (interactive BI, batch reports, ETL service accounts) separate memory caps, concurrency limits, and priorities. Set per-query memory limits plus cluster-wide spill policies; a single runaway Cartesian join must queue or fail, never wedge the cluster. Enable high-concurrency mode (many small queries sharing workers) distinctly from batch mode (few large scans).

## Security and Governance

Kerberos or OIDC authentication at the coordinator, TLS everywhere, and fine-grained access control via Apache Ranger or Open Policy Agent plugins down to column and row-filter granularity. Impersonation chains (Trino service user mapped to end-user identity) keep audit trails accurate when BI tools share one connection pool.

## Trino Versus Neighbors

- **Versus Spark SQL**: Trino wins interactive latency and federation; Spark wins multi-hour batch, ML pipelines, and fine-grained recovery. Many lakehouses run both on the same Iceberg tables.
- **Versus Flink**: Trino queries bounded snapshots; [[apache-flink|Flink]] processes unbounded streams. Trino-plus-Iceberg covers near-real-time (minute-fresh) analytics; Flink covers sub-second.
- **Versus warehouse compute** (Snowflake/BigQuery): warehouses bundle storage and compute with elastic scale; Trino queries data where it already sits, avoiding copies and egress.

## Production Practices

- Keep coordinator heap generous and GC-logged; coordinator OOM is a cluster-wide outage.
- Pin connector and catalog versions; a lake connector upgrade can change pushdown behavior silently.
- Cache hot Parquet/ORC splits with Alluxio or RubiX-style local SSD caching when object-store latency dominates.
- Monitor queued-vs-running queries per resource group; sustained queuing means add workers or split workloads.

## References

- Trino documentation: https://trino.io/docs/current/
- Related: [[apache-iceberg|Apache Iceberg]], [[apache-spark|Apache Spark]], [[apache-flink|Apache Flink]]
