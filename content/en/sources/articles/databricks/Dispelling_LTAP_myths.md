---
title: "Dispelling LTAP myths"
description: "Databricks' Sergey Melnik rebuts four misreadings of Lakebase's LTAP design: it is not CDC replication, one copy can serve both point lookups (heap pages) and scans (Parquet), analytical queries see a consistent snapshot by merging pageserver pages up to a shared LSN, and logical replication is a costly way to build the lake copy. The lake is the database's storage, not a replica of it."
tags: [source, databricks, lakebase, ltap, postgres, en]
locale: en
source_url: "https://www.databricks.com/blog/dispelling-ltap-myths"
blog: databricks
published_date: 2026-11-14
---

# Dispelling LTAP myths

**Source**: [Databricks Blog](https://www.databricks.com/blog/dispelling-ltap-myths) · **Published**: November 12, 2026

## Overview

A Reynold Xin post, "From monolith to Lakebase to LTAP", described Lakebase's ambition: one governed copy of operational data serving both Postgres and analytics, with no CDC pipeline and no second database. Commentary then produced four recurring myths by reading it through familiar systems: LTAP is CDC under another name; a single copy can have only one physical layout; Iceberg or Delta on object storage are inherently stale; and Postgres logical replication already provides the extraction path.

Sergey Melnik answers each with storage mechanics, not slogans. The recurring confusion, he argues, is treating every materialization of the data as a second database. The test is simple: a layer is a replica if it can be queried or failed over to as its own database; otherwise it is a tier, like an index or a cache.

The argument runs through Lakebase's write and read paths — safekeepers, pageservers, Parquet and the LSN watermark — and closes noting logical replication stays right for migrations and cutovers, not for building the lake copy.

## Key points

- Lakebase's LTAP design makes the lake the database's storage, not a replica: one Delta or Iceberg table, one catalog, with Postgres caches and pageservers in front for speed.
- The replica test: can the layer be queried, or failed over to, as its own database? If yes, it is a replica; if no, it is a tier.
- Postgres has always been tiered — the WAL, the buffer cache and the indexes all overlap with the heap, and nobody calls an index a replica because it has no catalog or timeline of its own.
- A write is durable when its WAL reaches a quorum of safekeepers; the pageserver then applies the log, keeps hot pages in memory and on local disk, and materializes data into object storage — mirroring how an S3 PUT is already stored more than once, often across availability zones with erasure coding, with no sync job between the copies.
- One copy does not imply one encoding: heap pages serve point lookups, Parquet behind Delta or Iceberg serves scans; the columnar files carry heap block, offset and MVCC metadata so the original pages can be rebuilt.
- Values that Parquet cannot represent losslessly are not coerced or dropped — they travel in an overflow field in the same table; indexes stay in the hot tier and are not transcoded into Parquet.
- An analytical query asks Postgres for the current LSN (a metadata lookup), reads nearly all data from object storage, and merges pages committed since the last materialization from the pageserver, so nothing committed before the query is missed.
- Every table is read at a single LSN — a shared watermark like the cutoff Postgres uses for REPEATABLE READ — which also keeps joins consistent, where CDC's per-table pipelines can mix two points in time; small tables stay in the page cache and skip the Iceberg commit.
- On a hot page, Postgres may log the same 8 KB a hundred times between checkpoints; logical decoding emits a hundred events that a downstream job upserts by primary key, while a page-tiering path reads the page once.
- In measured write-intensive workloads, CDC reads at least the WAL volume, while dirty-page compaction may read a fraction of it.
- Logical decoding does not emit DDL, so ALTER TABLE, type changes and renames can invalidate the slot; tables without a primary key need REPLICA IDENTITY FULL.
- WAL records are ordered because later ones assume earlier ones, so independent workers cannot decode disjoint byte ranges into correct current rows; what LTAP parallelizes is pages, using WAL summaries on Postgres 17+ or the pageserver's log-structured merge trees.

## Details

### Replica versus tier

Replication keeps two databases aligned by shipping changes; each side has its own catalog and timeline, and if shipping stalls the copies drift apart with nothing forcing them back. Tiering keeps one database and puts caches in front: a missed read costs a layer of latency, but a lost cache never takes the table with it. By that test CDC does create a second database — a decoded stream upserted into a foreign schema the source never reads back, where types drift and DDL goes missing. LTAP keeps one logical table instead; there is no opt-in list — a table that exists in Postgres exists in the lake.

### Two lossless encodings, one copy

The myth assumes one copy implies one encoding. Lakebase's answer is two lossless formats over the same rows: Postgres heap pages for point lookups and updates, Parquet behind Delta or Iceberg for analytics. Because values are preserved and the physical metadata suffices to rebuild pages, the columnar copy can be the durable store and the heap pages a cache of it. Lookups hit 8 KB pages on the compute node, local disk and pageserver; scans hit Parquet through an OLAP engine. One narrower point survives: the columnar files are heap-ordered — rows sit in page-number order — a poor clustering key for range predicates like order-date filters; a warehouse wanting different clustering can derive it as silver tables are derived; the CDC pipeline that existed to create the lake copy is no longer required.

### Consistent snapshots at a single LSN

Iceberg and Delta give snapshot isolation on high-latency object storage, so analytics can look forever behind. The hidden assumption: a query sees only what has already landed in object storage. In LTAP a query also sees pages that have not: it takes the current LSN from Postgres, reads almost everything from object storage up to that LSN, and merges the rest from the pageserver. The materialized snapshot can lag by a compaction interval, but the query itself does not. A long query not seeing new commits is snapshot isolation; missing data already durable at the starting LSN would be an incorrect result — merging recent pages as of that LSN is how LTAP avoids it.

### Why logical replication is the expensive path

The WAL is a physical log of page edits; logical decoding turns it into commit-ordered row events and cannot collapse many updates to one page into its current image, so every change has to pass through. Replication slots are cursors that must keep advancing, or WAL accumulates until the slot is dropped or the disk fills. Parallel decoding does not rescue it: visibility lives in pg_xact, the proc array and the catalog, not the tuple, so workers cannot decode disjoint ranges into correct rows. LTAP parallelizes pages, not log records — it commits one Iceberg snapshot of the pages changed since the last snapshot. Replication stays right for migrations, upgrades and cutovers — but as storage it produces a second source of truth.
