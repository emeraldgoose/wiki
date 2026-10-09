---
title: "CDC: Change Data Capture"
description: "Techniques for capturing row-level inserts, updates, and deletes from databases: log-based, trigger-based, and query-based approaches"
tags: [concept, data-engineering, cdc, debezium, kafka, real-time]
locale: en
published: 2026-09-07
---

# CDC: Change Data Capture

> Read this page in Korean: [/ko/concepts/data-engineering/cdc-change-data-capture](/ko/concepts/data-engineering/cdc-change-data-capture)

**Change Data Capture (CDC)** is a family of techniques for detecting row-level inserts, updates, and deletes in a source database and delivering them as an ordered event stream to downstream consumers such as data lakes, warehouses, caches, and microservices.

## Why CDC Exists

Batch ETL snapshots re-read whole tables on a schedule (see [[etl-vs-elt|ETL vs ELT]]). That is simple but wasteful and slow: a nightly dump of a large table to catch a few thousand changed rows burns I/O, misses intraday changes, and never tells you *what* changed, only the final state. CDC instead ships the change log itself, giving three properties batch snapshots cannot:

- **Freshness**: changes propagate in seconds, enabling real-time materialized views and [[stream-processing|stream processing]] pipelines.
- **Efficiency**: only deltas move across the network, not full tables.
- **History**: before/after row images preserve the full sequence of mutations, so consumers can reconstruct state at any point in time.

## Capture Methods

### Log-Based CDC (Preferred)

Most production CDC reads the database write-ahead log (WAL): PostgreSQL logical replication slots, MySQL binlog, SQL Server CDC tables fed by the transaction log, Oracle LogMiner/Redo. The log already serializes every committed transaction in order, so the approach adds near-zero load to the source and captures deletes and intermediate updates that a snapshot would miss.

- **Ordering guarantee**: log order equals commit order, so consumers see a causally consistent event sequence.
- **Low overhead**: asynchronous log shipping, no triggers firing per row, no polling queries.
- **Caveats**: requires elevated privileges to configure replication; schema changes (DDL) propagate awkwardly and need explicit handling; log retention must exceed consumer lag or events are lost, so monitor replication lag as a first-class metric.

### Trigger-Based CDC

AFTER INSERT/UPDATE/DELETE triggers write row copies into shadow or outbox tables that a poller drains. Works on any RDBMS without replication privileges, but every write pays trigger overhead, bulk loads become slow, and trigger logic must be maintained across schema migrations. Suitable for small tables or locked-down databases, not for high-throughput sources.

### Query-Based Polling

A scheduled query selects rows where `updated_at` advanced past the last poll watermark, or a monotonically increasing version column moved. Zero source-side setup, but deletes are invisible unless soft-deleted, rapid successive updates collapse into one, and polling frequency trades freshness against query load. This is the fallback when log access is unavailable.

| Method | Freshness | Overhead | Deletes | Privileges Needed |
|--------|-----------|----------|---------|-------------------|
| Log-based | Seconds | Minimal | Yes | Replication setup |
| Trigger-based | Seconds to minutes | Per-row write cost | Yes | DDL rights |
| Query-based | Poll interval | Periodic scans | No, needs soft delete | Read only |

## The Reference Stack: Debezium and Kafka

[Debezium](https://debezium.io/) is the de facto open-source log-based CDC platform. A Debezium connector (one per source table set) tails the database log and emits one event per row change to Apache Kafka topics, typically one topic per table, with keys set to the primary key so ordering per row is preserved.

A Debezium event envelope contains `before` and `after` row images, a `source` block with log position (LSN) and transaction ID used for exactly-once resumption after restarts, an `op` code (`c` create, `u` update, `d` delete, `r` snapshot read), and a timestamp. Downstream, Kafka Connect sink connectors land the stream into Iceberg or Delta tables (see [[apache-iceberg|Apache Iceberg]]), Elasticsearch, or a warehouse via streaming ingest, completing a sub-minute source-to-lake path.

## Key Design Patterns

### Transactional Outbox

Microservices with their own databases face the dual-write problem: updating the database and publishing an event atomically. The outbox pattern writes the event into an `outbox` table in the same local transaction, and CDC tails that table and publishes to the broker. Atomicity comes from the database transaction; delivery comes from CDC. Debezium ships a dedicated outbox event router for this.

### Snapshot Plus Streaming Seam

A new CDC pipeline must first carry existing data. The standard procedure is to take a consistent snapshot, record the log position, then stream only changes past that position. Consumers must handle snapshot-read events idempotently, since restarts can replay the seam.

### Schema Evolution

With a schema registry (Avro or Protobuf), connectors enforce compatible schema changes; otherwise an ALTER TABLE ADD COLUMN can break downstream parsers. Best practice is to gate DDL changes behind contract tests before applying them to sources feeding production CDC.

## Operational Concerns

- **Lag monitoring**: alert on replication-slot lag in both bytes and seconds; an idle consumer lets the WAL grow unboundedly and can fill the source disk.
- **Effectively-once delivery**: Kafka transactions plus idempotent sinks give effectively-once semantics; consumers should still be idempotent on the tuple of table, primary key, and log position.
- **Backfill**: adding tables requires a new snapshot for those tables only; schedule snapshots of large tables off-peak.
- **Security**: CDC streams carry PII verbatim; apply field-level masking or topic ACLs before fan-out.

## When Not to Use CDC

If freshness requirements are hourly or daily, plain batch extraction is simpler and cheaper. If the source offers no stable log access and no `updated_at` columns, the engineering cost of triggers may exceed the value. CDC pays off when sub-minute freshness, delete capture, or full change history is required.

## References

- Debezium documentation: https://debezium.io/documentation/
- Kleppmann, *Designing Data-Intensive Applications*, ch. 11 (Stream Processing)
- Related: [[etl-vs-elt|ETL vs ELT]], [[stream-processing|Stream Processing]], [[apache-flink|Apache Flink]]
