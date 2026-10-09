---
title: "FishDB: A Generic Retrieval Engine for Scaling LinkedIn's Feed"
description: LinkedIn's Rust-based generic retrieval engine replacing FollowFeed — scatter-gather serving, lambda ingestion, 2x efficiency
date: 2025-11-17
tags: [source, linkedin, feed, retrieval, rust, infrastructure]
locale: en
source_url: "https://www.linkedin.com/blog/engineering/infrastructure/fishdb-a-generic-retrieval-engine-for-scaling-linkedins-feed"
blog: linkedin
author: Kenneth Li
---

# FishDB: A Generic Retrieval Engine for Scaling LinkedIn's Feed

FishDB is LinkedIn's generic retrieval engine for Feed, built in Rust to replace the legacy Java-based FollowFeed system. It delivers **2× processing efficiency** and **50% less hardware** while holding a strict **40 ms p99** latency SLO.

## Why: limits of FollowFeed

- **Memory inefficiency.** JVM-based storage carried ~5× memory overhead vs. native representation; GC pauses threatened tail latency.
- **Content duplication** across indexes and rigid data models.
- **Tightly coupled business logic**, slowing feature rollouts and holistic optimization.

## Architecture

### Scatter-gather serving

Requests fan out across partitioned shards; each shard scores its local candidates and the results are merged to return top results. Partitioning plus in-memory indexes keeps p99 at 40 ms under growing QPS.

### Lambda ingestion

- **Speed path:** Kafka streams feed real-time updates.
- **Batch path:** bulk rebuilds correct and compact state.
- The combination keeps the index fresh without sacrificing consistency of large backfills.

### Storage and indexing

- **Inverted index** as an in-memory hashmap from terms to document-ID lists for efficient term lookup.
- **RocksDB key-value attribute stores** for larger-volume per-document attributes that don't fit the in-memory budget.
- **Graph-based document references** for query execution over relationships (e.g. actor → activity edges).

### Expressive query language

A purpose-built query language decouples business logic from the engine: product teams express retrieval predicates without engine changes — the "generic" in FishDB.

## Why Rust

Ownership-based memory management eliminates GC pauses and slashes per-object overhead — the direct source of the 2× efficiency and 50% hardware savings. The trade-off is real Rust engineering cost (lifetimes, FFI with the JVM/Kafka ecosystem), paid once for permanent fleet-wide savings.

## Takeaways for SW engineers

1. For latency-critical retrieval with huge live sets, GC-free runtimes beat even tuned JVMs.
2. Scatter-gather + partitioned in-memory indexes is the standard recipe for p99-bounded retrieval.
3. Separate the query language from the engine to keep business logic evolvable.
4. Lambda ingestion (Kafka speed layer + batch correction) handles freshness + correctness.

## Related concepts

- `concepts/data-engineering/stream-processing.md` (Kafka ingestion path)
- `concepts/infrastructure/kubernetes.md` (fleet deployment)
- `concepts/ai-engineering/rag.md` (retrieval engine architecture)

## References

- Source: https://www.linkedin.com/blog/engineering/infrastructure/fishdb-a-generic-retrieval-engine-for-scaling-linkedins-feed
