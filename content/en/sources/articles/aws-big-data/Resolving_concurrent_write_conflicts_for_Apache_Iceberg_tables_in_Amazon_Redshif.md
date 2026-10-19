---
title: "Resolving Concurrent Write Conflicts for Apache Iceberg Tables in Amazon Redshift"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/resolving-concurrent-write-conflicts-for-apache-iceberg-tables-in-amazon-redshift"
blog: aws-big-data
published: 2026-10-17
---

# Resolving Concurrent Write Conflicts for Apache Iceberg Tables in Amazon Redshift

**Source**: AWS Big Data Blog, 2026-10-13

**Lead**: Apache Iceberg uses optimistic concurrency control (OCC) at the table version level—any concurrent commit fails the version check and the entire write is discarded, even when writes touch completely disjoint data. Amazon Redshift now rebases non-conflicting writes automatically at three granularity levels (operation → partition → file), preserving work that previously had to retry.

## The Problem: Blunt OCC at Table Version Level

Iceberg's OCC ensures snapshot isolation by requiring each writer to commit against the current table version. If another writer commits first, the condition fails and the **entire write is discarded**—regardless of whether the two writes actually touched the same data.

Example: A retail `customer_orders` Iceberg table. A streaming pipeline inserts new orders continuously (hundreds/minute). A nightly compliance job deletes records older than 7 years (takes ~1 hour). The writes **never touch the same data**—stream adds recent orders, compliance removes old ones. But under basic OCC, if a single streaming insert commits during the compliance job's window, the compliance job loses the race, its hour of work is discarded, and it must re-scan terabytes.

Traditional workarounds are all manual and costly:
- Serialize writers (give up concurrency)
- Split into multiple physical tables (fragmented data model)
- Application-side retry loops (absorb cost of re-running non-conflicting work)

## Redshift's Solution: Automatic Conflict Resolution via Rebase

When a commit loses the race, Redshift now asks: **Did the writers that committed ahead actually change the same partitions/files/rows?** If no, rebase the change onto the latest table version and commit—no re-scan, no re-execution, no application retry.

In the retail example: Compliance delete previously failed when a streaming insert committed inside its window. Now Redshift sees inserts only *added* data files while delete only *removed* others—provably independent. It rebases the delete onto the updated version; both succeed.

Two governing principles:
1. **Conflict is a matter of granularity** — A failed race isn't automatically a conflict. Check at operation level first (cheapest), then partition, then file. Finer checks cost more but resolve more cases.
2. **Correctness over concurrency** — Resolution uses only table metadata, never re-scans data. When independence can't be proven, it declines to resolve and the write retries (safe outcome).

## Three-Level Escalation

| Level | Check | Resolves |
|-------|-------|----------|
| **Operation** | At least one write only appended (`INSERT`) | Any write vs. insert; insert vs. any write including compaction |
| **Partition** | Both removed data, but disjoint partitions | Batch jobs on different dates; per-region pipelines |
| **File** | Same partition, different files | Two jobs deleting different rows in same date partition |

If both modified the **same file**, conflict surfaces and statement re-runs (correct behavior).

## Results

**Microbenchmark** (1 unpartitioned table, insert-only, 1–16 concurrent writers, 60s):
- Basic OCC: Throughput at 16 writers = **0.17×** single writer (94% failure rate)
- Auto resolution: **2×** single writer throughput, **0 conflicts** at all levels

**Fleet data**: Before resolution, concurrent-write conflicts were the #1 cause of failed Iceberg writes (~1 in 5 failed writes/week). After operation-level check rollout (early Sept 2026), conflict errors dropped to **near zero** even as Iceberg write volume **more than doubled**.

## Observability

Every commit attempt recorded in `stl_iceberg_commit` system table: outcome, attempts, concurrent operations rebased over, rebase time.

## Relevance to Software Engineers

For teams running **concurrent pipelines on Iceberg tables** (streaming + batch, multiple ETL jobs, CDC + compaction): Redshift's automatic resolution eliminates the need to manually coordinate writers or build retry logic. The engine handles the common case (appends vs. anything, disjoint partitions/files) transparently.

Available on Redshift patch 203+. Tables with `write.*.isolation-level = serializable` retain strict OCC (no resolution).

## References

- Original article: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/resolving-concurrent-write-conflicts-for-apache-iceberg-tables-in-amazon-redshift)
- Iceberg OCC docs: [iceberg.apache.org/docs/1.6.0/reliability/#concurrent-write-operations](https://iceberg.apache.org/docs/1.6.0/reliability/#concurrent-write-operations)