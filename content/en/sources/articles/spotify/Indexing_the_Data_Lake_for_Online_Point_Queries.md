---
title: Indexing the Data Lake for Online Point Queries
description: Spotify's Random Access Parquet (RAP) — an external index over lake Parquet files enabling low-latency point queries via targeted ranged reads, without KV-store replication
tags: [source, rss, spotify, data-lake, parquet, indexing, online-serving, ai-agents]
locale: en
source_url: "https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries"
blog: spotify
published_date: 2026-07-27
---

# Indexing the Data Lake for Online Point Queries

Author: Will Edwards, Staff Data Engineer. Source: Spotify Engineering, Jul 27, 2026.

**Lead**: Spotify's exabyte-scale data lake is too large to replicate into key-value stores, and distributed SQL engines add seconds of overhead per lookup. Random Access Parquet (RAP) bridges the gap: an external index maps keys directly to file and row locations, and precise ranged reads fetch exactly the bytes needed — store once, serve both analytics and interactive point queries from the same Parquet files.

## Background: the serving gap

Two workloads need the same primitive — fast point queries by key over datasets far too large to keep resident in Bigtable or DynamoDB:

- **Online services**: portals and personalization features that look up and paginate per-user data (e.g. listening history) at interactive speeds.
- **AI agents**: answering "what was I listening to last summer?" requires retrieving a user's data quickly so the agent can filter, aggregate, or run SQL locally to build LLM prompt context.

Scale at Spotify: petabytes in Bigtable for online use-cases, but **exabytes** in the GCS data lake. Object storage itself is fast and getting faster — GCS delivers 30–100 ms per request, and S3 Express One Zone / GCS Rapid Storage offer single-digit millisecond latency. The bottleneck is the query engine: Trino and BigQuery add seconds of job scheduling and planning overhead even for a single-row lookup, because they are built for analytical throughput, not interactive point queries.

## Why naive lake lookups fail: the needle in the haystack

A "last summer" listening-history query spans billions of users across thousands of large daily files — roughly 90 days × 1,000 files/day = **90,000 Parquet files**. Standard pruning helps but not enough:

1. **Partitioning by key**: files further partitioned by key (as for joins) let the engine skip files by filename alone — 90,000 candidates drop to ~90.
2. **Bloom filters** on the user-ID column, cached in a metadata store, discard files without opening them — ~90 narrows to perhaps the 12 days the user was actually active.
3. **But 12 large files must still be read**, and finding one user's rows inside each requires opening row groups and scanning — a chain of dependent reads, each adding latency.

## The RAP approach: look up instead of scanning

An external index maps each key directly to every file and row number where its data resides. Given a key, the reader looks up the index, resolves the row number to page locations using cached file metadata, and issues ranged reads fetching exactly the pages needed:

- Index lookup is **O(1)**; page mapping is a low-latency cached operation; data retrieval is a small number of precise ranged reads, issuable **in parallel**.
- RAP operates on the **same Parquet files** already shared by ML pipelines, notebooks, experimentation platforms, and batch analytics — store once, pay once, instead of maintaining copies in specialized serving systems.
- **No special preparation required**: RAP works on any existing Parquet files. The index builder reads footers and page locations for the columns to be retrieved and scans key columns to build the key-to-location mapping.
- **Incremental**: as new data lands in Apache Iceberg tables, the builder emits append-only index fragments without rewriting immutable Parquet files.

## Write-time optimizations for prepared files

For datasets written with serving in mind, Parquet layout optimizations compound the gains: sorting by key, co-grouping related rows, one-page-per-key layouts, and ZSTD compression — all reducing the bytes per point lookup. Secondary indexes extend the pattern beyond the primary key.

## Limitations / open questions

- Point-lookup latency still depends on object-store tail latency and index freshness; rapidly mutating datasets need tight index-build pipelines.
- Index storage and build compute are new costs to weigh against KV-store replication they replace.
- Multi-key range scans and paginated traversals stress different paths than single-key fetches.

## Relevance to SW engineers

- Before replicating lake datasets into DynamoDB/Bigtable for serving, consider an external-index + ranged-read design — it eliminates dual-write consistency and duplicate storage.
- Parquet file layout (sort keys, page sizing, compression) is a serving concern, not just a scan concern, once point queries hit the lake.
- Related: `concepts/data-engineering/delta-lake.md`, `concepts/data-engineering/apache-spark.md`.

## References

- Source article: https://engineering.atspotify.com/2026/7/indexing-the-data-lake-for-online-point-queries
- Secondary coverage: InfoQ, "Spotify Builds External Index to Enable Low Latency Point Queries on its Data Lake" (Aug 2026)
