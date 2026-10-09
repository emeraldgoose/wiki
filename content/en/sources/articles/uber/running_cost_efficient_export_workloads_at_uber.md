---
title: Running Cost-Efficient Export Workloads at Uber
description: Apache Hudi column stats plus table sorting turn full-table export scans into selective low-touch lookups on Uber's GCS lakehouse
tags: [source, uber, data-engineering, hudi, lakehouse, gcs, cost-optimization]
locale: en
source_url: "https://www.uber.com/us/en/blog/running-cost-efficient-export/"
blog: uber
published_date: 2026-08-12
---

# Running Cost-Efficient Export Workloads at Uber

**Authors**: Pankaj Mohapatra, Arun Mahadeva Iyer, Balajee Nagasubramaniam
**Source**: [Uber Blog](https://www.uber.com/us/en/blog/running-cost-efficient-export/)
**Date**: Aug 12, 2026

## Problem

Export workloads (DSAR, compliance, privacy) retrieve small result sets from large historical datasets. Characteristics: point or narrow-predicate queries over Hudi tables partitioned by date, run repeatedly (multiple times/week) with different parameters, touching history-wide search space despite tiny outputs. On Uber's GCS-backed lakehouse, repeated full-table scans keep data hot, preventing GCS auto-class tiering (desired ~60% Standard / 15% Nearline / 10% Coldline / 15% Archive collapses to 100% Standard) and inflating storage, retrieval, Class B metadata operations, GCS egress, and latency.

## Solution: Hudi Column Stats + Table Sorting

- **Column stats**: Hudi's metadata table stores min/max/null/count per column per file. The engine prunes files via a metadata-table query *before* scanning data — no need to open Parquet footers (footer reads themselves keep files hot).
- **Table sorting**: clustering on the predicate column (e.g. user ID) tightens per-file min/max ranges, making pruning far more selective. Column stats provide the mechanism; sorting improves its effectiveness.

## Results

Benchmark on a real partition:

- Disk footprint reduction: 24.8% (sorting clusters identical values → better compression)
- Effective file pruning across low/mid/high predicate counts
- Reduced GCS egress, Class B operations, and query latency
- Older data stays cold → auto-class tiering works again

## Why Not Sorting + Secondary Index?

Column stats scale with file count × tracked columns; a secondary index must maintain per-value lookup mappings (heavier metadata, more compute). If the table is unsorted, a secondary index alone doesn't prune enough to change scan cost; if sorted, column stats are the simpler, more storage-efficient choice. Uber chose sorted tables + column stats.

## Applicability Beyond Uber

The export access pattern (small selective retrieval from vast history under compliance/operational pressure) recurs in finance (audit trails), healthcare (patient record requests), and legal discovery. The Hudi Table Service is the enabler — central engine for backfill sorting, index construction, and incremental sorting.

## Seminar Takeaways

- Cloud storage cost is driven by *access pattern × file layout*, not just bytes stored.
- Move pruning metadata to the table level so cold files are never touched — footer reads are themselves a "touch".
- Physical clustering (sorting) multiplies the value of any min/max-based pruning.
- Prefer the lightest index that prunes enough; measure scan surface, not just output size.

## Related Concepts

- `concepts/data-engineering/apache-hudi.md` (column stats, table services)
- `concepts/data-engineering/lakehouse.md` (storage tiering, file layout)
