---
title: "Load terabytes of data in minutes into Lakebase Postgres"
description: "LTAP architecture offloads bulk loads from the Lakebase primary to Spark, building valid Postgres pages in parallel for up to 147x faster ingestion."
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres"
blog: databricks
published_date: 2026-10-08
---

# Load terabytes of data in minutes into Lakebase Postgres

## Overview

Bulk ingestion is the classic threat to an operational Postgres database: terabytes funneled through a single primary writer steal CPU, I/O, and WAL bandwidth from live application traffic. Lakebase's LTAP (Lake Transactional/Analytical Processing) design sidesteps this by letting Spark build valid Postgres state directly in storage while the primary merely publishes the result — cutting a reported 8-hour billion-row daily sync down sharply (internal benchmarks put 1 TB under 5 minutes) with the primary untouched.

## Why bulk loads hurt Postgres

Even when Spark reads source partitions in parallel, every row still passes through one writer: the primary converts rows to heap and index pages, records WAL, and flushes before commit. Throughput is capped by that single gatekeeper, and the same instance serves OLTP traffic, so teams end up scheduling loads for off-hours, overprovisioning the primary, and hand-managing backfills and checkpoints.

## What LTAP changes

In Lakebase, durable state lives in a distributed storage layer rather than on the primary's disk, so the primary is no longer the only path to durable Postgres state. Spark constructs heap and index slices and writes them to object storage; the primary then records the import as one compact WAL record instead of the full data volume. Consequences: loads stop competing with OLTP, concurrent imports no longer queue behind each other's `COPY` streams, and a small primary can keep serving traffic while Spark scales throughput near-linearly and terminates when done.

## Building valid pages and indexes in parallel

Each Spark executor runs a sandboxed Postgres in binary-upgrade mode (preserving catalog OIDs so generated pages match the destination), uses binary `COPY ... FREEZE` for its heap slice, gets a non-overlapping OID range, and checksums every page for pageserver validation — all via extensions and a table access method, without touching Postgres core. Indexes avoid downloading the distributed heap: workers export compact key-plus-tuple-ID streams, a helper table plus a custom access method feeds the standard B-tree builder while remapping slice-local tuple IDs to final positions. The driver then writes a manifest, invokes one SQL function, pageservers claim and prewarm the pages, and the staged data swaps atomically into the visible table.

## References

- Original article: [Load terabytes of data in minutes into Lakebase Postgres](https://www.databricks.com/blog/load-terabytes-data-minutes-lakebase-postgres)
