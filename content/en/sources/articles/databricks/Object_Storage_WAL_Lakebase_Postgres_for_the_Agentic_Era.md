---
title: Object Storage Plus WAL Lakebase Postgres for the Agentic Era
description: Lakebase Postgres decouples compute from storage with WAL-on-object-storage as the source of truth — branching, instant restore, time travel, and LTAP analytics from one copy.
date: 2026-08-27
tags: [databricks, lakebase, postgres, oltp, ltap, object-storage, wal, ai-agents, database]
locale: en
source_url: "https://www.databricks.com/blog/object-storage-wal-lakebase-postgres-agentic-era"
blog: databricks
---

# Object Storage + WAL: Lakebase Postgres for the Agentic Era

**Authors**: Cassie Murray, Carlota Soto · **Published**: Aug 27, 2026 · **Source**: [Databricks Engineering Blog](https://www.databricks.com/blog/object-storage-wal-lakebase-postgres-agentic-era)

## The question: can object storage sit under a transactional database?

Agents hammer OLTP storage layers in an unusual way: every new deployment, copy, restore, or replica means moving large data volumes — slow and expensive. Object storage (S3-style) is the polar opposite: cheap, performant, nearly invisible to operate, a natural substrate for agent memory. Lakebase Postgres asks whether object storage can sit underneath Postgres and make agents' lives easier. The answer turns on *where the source of truth sits*, not just how fast the object store is.

## Two OLTP mental models

The familiar **data-centric** model: the database stores current state in tables; storage holds the present. The alternative **transaction-centric** model: the database is a journal of transactions — a timeline of operations from which the present is derived. Agent workloads almost exclusively want timeline operations (branch, copy, restore to a point, diff across time, read replicas) — queries a present-only store answers with slow, expensive copies. Postgres already contains the timeline: the **write-ahead log (WAL)**. Every modification is appended to the WAL before reaching data files; each record carries a monotonically increasing **log sequence number (LSN)** naming the exact 8 KB page changed at an exact timeline point (`pg_waldump` renders this). Read as a journal rather than a recovery aid, the WAL is a complete, ordered, byte-level account of every page ever changed — and the LSN makes "the database as of time T" well-defined with zero Postgres changes. It only needs a storage layer that keeps the log and answers questions against it.

## Architecture: compute executes, storage owns truth

Conventional Postgres treats data files as the database and trims the WAL once applied. Lakebase inverts this: **the log is the database; data files are a derived, cached representation**. Full history is kept; copies become pointers, not file sets.

- **Compute layer**: stock Postgres — parses SQL, plans, MVCC, locks, indexes. RAM for shared buffers, local NVMe as page cache. Exists to execute work, not preserve data: nodes can start, stop, scale, or die with no durability risk. Nothing in the query engine is rewritten.
- **Storage layer** (outlives any compute node): **safekeepers** replicate WAL via a Paxos-based protocol — quorum ack *is* the commit (replaces rather than adds to the synchronous-replication network hop); **pageserver** materializes page versions into object storage asynchronously, off the commit critical path; **object storage** holds immutable history in open columnar formats, append-only, never updated in place.
- **Read path (`GetPage@LSN`)**: every read names page + LSN; served RAM → NVMe → pageserver (reconstructs from layers) → cached locally. A primary asking for latest behaves like warm-cache Postgres — but any historical LSN works identically, so live data vs. backup collapses into one addressable system.

### Non-overwriting layers and the lookup trick

The pageserver organizes data into **delta layers** (WAL records per page range) and **image layers** (page snapshots that shorten replay chains and let old deltas be collected); background compaction reshuffles, and out-of-retention layers are garbage-collected — a perfect fit for object storage's no-random-update constraint. The hard problem is finding, across tens of millions of layers, the nearest layer covering key K at-or-before LSN L (R-trees answer the wrong query; segment trees scale with coordinate space). The solution: for one fixed LSN, coverage changes at only a handful of key-space points — record them in a binary search tree for single-lookup reads. Then make the tree **persistent** (functional-persistent): insert layers in LSN order bottom-up, copying only nodes along the touched root path and sharing unchanged subtrees — accumulating every historical root for near the price of one tree. Historical reads then cost the same as current ones: pick the root for the wanted LSN, one lookup.

## Agent features and LTAP

Because history is addressable and copies are references, Postgres gains the lightweight workflows agents require:

- **Branching**: a branch is a pointer to an LSN with copy-on-write divergence — a 2 TB branch in seconds, zero cost until written, no parent load. Twenty agents can each branch production per task, test migrations against real data volume, and discard. Branching extends beyond tables to buckets, functions, auth state, AI Gateway config — an isolated backend copy.
- **Instant restore / PITR**: restore is pointing at an earlier LSN — cost independent of database size, bounded by a retention setting. An agent's bad statement is undone by rewinding the branch, not by a restore window and recovery plan.
- **Time-travel queries**: query past state directly (diff pre/post-migration) before committing to a restore.
- **Read replicas without replicas**: a read-only compute node reads from the same storage layer — adding one is a metadata operation, no dataset provisioning or catch-up.
- **Scale to zero**: idle computes suspend after 5 minutes of inactivity, resume in hundreds of ms; compute billing stops (storage continues). A database per agent/session/branch becomes the affordable default.

**LTAP (Lake Transactional/Analytical Processing)**: with the durable record in open columnar object storage, the pageserver transcodes materialized pages from Postgres row format to columnar, preserving exact Postgres value semantics. An analytical query fetches the current LSN (cheap metadata), reads the bulk from object storage at that LSN, and pulls only unmaterialized recent changes from the pageserver — Postgres serves ~zero analytical read traffic. Unlike CDC/mirroring there is nothing to opt into, no replicated-table list, and the two views cannot drift: the table already exists in the lake.

## Takeaways for the seminar

- **Source-of-truth placement is the whole trick**: object storage under OLTP works only if the WAL — not the data files — is durable truth; queries still serve from RAM/NVMe, never from S3 on the hot path.
- **Addressability (LSN) converts operations into pointers**: branch, restore, replica, and time-travel are all the same primitive — name an LSN.
- **The persistent-coverage-tree** is the load-bearing data structure: without O(1)-ish historical page lookup, cheap history is unusable — persistence-by-path-copying makes every LSN's index nearly free.
- **One copy kills the pipeline class**: LTAP removes CDC/replication/drift as a category by transcoding the same durable bytes both engines read.

## Related concepts

- `concepts/data-engineering/lakehouse.md`, `concepts/ai-engineering/agent.md`, `concepts/data-engineering/stream-processing.md`
