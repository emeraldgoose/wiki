---
title: "Built on object storage, served from cache"
description: "Lakebase Postgres reads almost never touch object storage: ~1.1B page accesses/sec (~99.46%) are served from compute-local cache, ~6M/sec (~0.54%) from pageserver NVMe, and only ~39/sec from object storage — about 1 in 28M page accesses."
tags: [source, article, databricks, lakebase, postgres, object-storage, en]
locale: en
source_url: "https://www.databricks.com/blog/built-object-storage-served-cache"
blog: databricks
published_date: 2026-11-19
---

# Built on object storage, served from cache

**Source**: [Databricks Blog](https://www.databricks.com/blog/built-object-storage-served-cache)
**Published**: 2026-11-19

## Overview

The common argument against Postgres on object storage: Postgres does many small latency-sensitive reads; object storage is built for large requests at higher latency (a single read can take hundreds of ms); therefore object-storage-backed Postgres must be slow. The premise is right but the conclusion is wrong — a database on object storage does not have to read from object storage to answer queries, and Lakebase Postgres almost never does.

## Key points

- Production fleet page-read stats: compute local cache served ~1.1 billion page accesses/sec (~99.46% of total); pageserver local NVMe served ~6 million/sec (~0.54%); object storage served only ~39 requests/sec.
- Put differently: 99.46% of page accesses are answered from the compute node's local cache at memory/microsecond latency (like a warm traditional Postgres). Only about 1 in 28 million page accesses needs a fetch from object storage, so more than 99.99999% are served without it.
- Object-storage reads are typically wakeups of long-dormant projects, restores, or old branches.
- Building on object storage buys: durability (S3 targets 99.999999999% durability), cheap storage with no provisioning or disk sizing, immutable addressable history (branching/instant restores as metadata operations, no data copies), stateless compute (scale to zero without moving data), and one copy for transactions and analytics (analytical engines read the same copy via LTAP).
- Architecture: compute runs standard Postgres with a local page cache and holds no durable state. The storage layer owns correctness, durability and history: Safekeepers replicate the WAL (commit once a quorum acknowledges; Paxos-based leader election/failover); Pageservers turn WAL into pages (LSM tree on local NVMe, persist materialized history to object storage asynchronously); object storage holds immutable long-term history and Postgres never reads from it directly.
- Read path: compute checks its local cache; on a miss it sends GetPage@LSN to a pageserver (returns the page as of that LSN); only if the pageserver lacks the needed layers does it fetch from object storage. Every tier caches what it fetches from the tier below.
- Pageserver internals: image layers (full snapshot of a key range at an LSN) and delta layers (WAL records for a key range across an LSN range). GetPage@LSN walks layers collecting deltas until it hits the first image, then replays deltas. Across us-east-1 (Oct 13–19, 2026): p90 stayed under 1 delta per GetPage (served straight from an image); p99 was around 6 after a change that creates base-page images more eagerly.
- Object-storage misses in practice are almost always one of two cases: branches/restores at old points in time (history not on pageserver NVMe), or inactive databases waking after weeks at zero (first reads go to object storage). In both cases only the first reads pay the cost; afterwards data is cached in the fast tiers.

## Details

- Lakebase Postgres belongs to a new category Databricks calls the "lakebase": compute and storage decoupled for Postgres, with object storage as the durable backing store but never in the query critical path.
- The eager-image-creation rollout reduced p99 deltas applied per GetPage to ~6.
- In active query execution, object storage is simply not in the critical path.
