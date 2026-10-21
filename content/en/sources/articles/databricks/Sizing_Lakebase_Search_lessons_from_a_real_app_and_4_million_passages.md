---
title: "Sizing Lakebase Search: Lessons from a Real App and 4 Million Passages"
description: "Lakebase Search runs vector and BM25 keyword search as Postgres extensions inside the application database. Benchmarks on the Slide Hub app (700 presentations) show sizing Local File Cache to match vector index keeps 95-98% pages in memory, dropping warm vector latency to single-digit ms; reducing candidate pool 1000→200 preserves 90.5% top-10 results at 1/3 page reads."
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages"
blog: databricks
published_date: 2026-10-15
---

# Sizing Lakebase Search: Lessons from a Real App and 4 Million Passages

**Source**: Tiefenbacher, Databricks Blog, 2026-10-15

**Lead**: Lakebase Search runs vector and BM25 keyword search as Postgres extensions inside the application database—no separate search system, no second transaction path. Benchmarks on the Slide Hub app (internal tool for 700 presentations) reveal practical sizing rules: cache the vector index, trim the candidate pool, and run a minimal always-on floor to avoid cold starts.

## One Database for App and Search

Lakebase Search (GA since Sept 2026) is a set of Postgres extensions:
- `lakebase_vector` + `lakebase_ann` (IVF + RaBitQ quantization) for ANN vector search
- `lakebase_text` + `lakebase_bm25` for BM25 keyword search
- `lakebase_tokenizer` (optional) for custom tokenization

The app does not copy data to a separate search system. No second transaction path to maintain.

## Slide Hub: Real App Baseline

Slide Hub is an internal Databricks app. Field engineers search ~700 presentations (event talks, product decks, architecture decks) by meaning and keyword. An MCP server gives AI agents the same search. All data—slides, votes, search telemetry, change history—lives in Lakebase Postgres.

This is a real app with real users, so its numbers reflect actual workload behavior.

## Key Sizing Findings

### 1. Local File Cache ≈ Vector Index Size
- Sizing the Local File Cache to roughly match the vector index keeps **95–98% of pages in memory**
- Warm vector latency drops to **single-digit milliseconds**
- Cache smaller than index → page reads from object storage → latency spikes

### 2. Candidate Pool: 1000 → 200
- Reducing the ANN candidate pool from 1,000 to 200 preserves **90.5% of top-10 results**
- Page reads drop to **one-third**
- Trade-off: slight recall loss for massive latency/IO gain

### 3. Scale Testing: 1M → 4M Passages
- Benchmarked on a public corpus scaled from 1M to 4M rows
- Latency scales sub-linearly with proper cache sizing
- BM25 scales well; vector search is the bottleneck without adequate cache

### 4. Cost: $0.02 for 109k Requests
- 14-minute load test serving 109k requests used **$0.02** of Lakebase Postgres compute
- **Recommended production baseline**: $31–40/month always-on 0.5 CU floor to avoid cold starts
- Lakebase Postgres bills compute only while running

## Practical Recommendations

| Parameter | Recommendation |
|-----------|----------------|
| Local File Cache | Match vector index size (95-98% hit rate) |
| ANN candidate pool | 200 (from default 1000) for 90.5% recall at 1/3 IO |
| Always-on floor | 0.5 CU ($31-40/mo) to eliminate cold starts |
| Hybrid search | Use BM25 + vector together; BM25 handles exact matches, vector handles semantic |

## Relevance to Software Engineers

For teams building **search into applications on Databricks**: Lakebase Search eliminates the separate search cluster (Elasticsearch, OpenSearch, Pinecone, etc.). You get:
- **Single database** for app data + search indexes
- **Transactional consistency** between app writes and search updates
- **SQL-native** search—no new query language
- **Predictable sizing** from real-app benchmarks

## References

- Original article: [https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages](https://www.databricks.com/blog/sizing-lakebase-search-lessons-real-app-and-4-million-passages)
- Lakebase Search GA announcement: [Databricks Blog](https://www.databricks.com/blog/lakebase-search-general-availability)