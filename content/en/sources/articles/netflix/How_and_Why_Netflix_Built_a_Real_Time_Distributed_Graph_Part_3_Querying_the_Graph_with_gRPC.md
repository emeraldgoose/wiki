---
title: "How and Why Netflix Built a Real-Time Distributed Graph Part 3: Querying the Graph with gRPC"
description: gRPC serving layer for an 8B-node 150B-edge real-time graph — breadth-first async traversal, early filtering, selective caching
tags: [source, article, netflix, distributed-systems, graph, grpc, serving]
locale: en
source_url: "https://netflixtechblog.com/how-and-why-netflix-built-a-real-time-distributed-graph-part-3-querying-the-graph-with-grpc-0f3468349607"
blog: netflix
published: 2026-08-07
---

# How and Why Netflix Built a Real-Time Distributed Graph Part 3: Querying the Graph with gRPC

Authors: Nilesh Mishra, Ajit Koti. Part 3 of the Real-Time Distributed Graph (RDG) series (Part 1: Flink ingestion pipeline; Part 2: billion-scale storage layer). All ingestion/storage work matters only if complex questions return in sub-100ms while the graph keeps growing — this post covers the serving layer: 8B nodes, 150B edges, tens of thousands of QPS.

## Background: two query shapes pulling opposite ways

- **Shallow-wide** ("which devices did this account stream from in 30 days?"): single hop, massive fan-out — stresses I/O throughput.
- **Deep-narrow** ("Account X's Stranger Things viewing across profiles"): 2–4 chained hops with sequential dependency (Hop 2 can't start until Hop 1 resolves) — stresses execution efficiency; naive per-hop network round trips blow the 100ms budget.

## Methodology

**Breadth-first, not depth-first.** Expand one level at a time across all nodes (fetch all profiles, then all their watch edges, then content details) — a few parallel rounds instead of sequential chains. Cost scales with level width, bounded by per-edge-type limits.

**Async-first, not thread-per-request.** Latency is I/O-dominated, so the whole pipeline is async-composed: 16–24 threads serve thousands of concurrent requests since no thread blocks on I/O.

**Three-layer architecture.** Graph Query Service (gRPC entry, traversal-plan validation) → execution engine (breadth-first orchestration) → Storage Abstraction Layer over KVDAL (node lookups, streamed edge retrieval, EVCache node caching) → opt-in Enrichment Layer (batched external metadata, fail-open).

**Per-query journey (2-hop example).** (1) Parse the gRPC request into a plan via a filter/limit hierarchy (app defaults → global overrides → per-depth → per-edge-type), preventing over-fetch upfront. (2) Adjacency-list lookups turn "neighbors of X" into direct indexed reads; large adjacencies stream in batches of 100 with source-side filtering (time windows, title match) and early termination at max_edge_cnt. (3) Breadth-first level expansion with bounded parallelism (explicit concurrency limits + limiter that grows capacity when healthy, backs off under stress). (4) Selective caching: stable, hot nodes (accounts, profiles, content) in EVCache with volatility-matched TTLs (70–80% hit rates, ~3–4x fewer storage calls); nodes near graph-retention expiry are skipped via "smart TTL".

**Design trade-offs made explicit.** Eventual consistency (nearest-replica reads) since queries ask "recently", not "last millisecond"; enrichments opt-in per request since callers know what they need.

## Results

- Single-hop: P50 15–30ms, P99 < 100ms. 3-hop traversals: P99 100–150ms, stable under growing fan-out.
- Thousands of concurrent requests on 16–24 threads; cache gives 70–80% hit rates on popular entities.

## Limitations / open questions

- Async composition slashed infra cost but hurt debuggability (unreadable stack traces, lost exceptions) — compensated with per-stage metrics.
- Caching took iteration: aggressive caching wasted memory on soon-expiring nodes before selective/smart-TTL policy.
- Memory cost scales with frontier width; adversarial wide queries depend on per-edge limits holding.

## Relevance to SW engineers

- Think in frontiers, not features: APIs describe what frontier to explore; the system decides how to walk it.
- Filter early, not late: push filters/limits to storage; never fetch-then-trim.
- Parallelize deliberately: concurrency is a dial with explicit limits and dynamic adjustment, not a switch.
- Caching is first-class design: decide what is worth remembering, for how long, matched to data volatility.

## Related concepts

- `concepts/data-engineering/stream-processing.md` (Flink ingestion, Part 1)
- `concepts/system-design/distributed-systems.md` (consistency, fan-out patterns)
