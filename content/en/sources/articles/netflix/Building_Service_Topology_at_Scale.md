---
title: "Building Service Topology at Scale"
description: Streaming-first real-time service dependency map — three-stage aggregation, intermediary resolution, time travel, and production lessons
tags: [source, article, netflix, distributed-systems, observability, data-engineering, backend]
locale: en
source_url: "https://netflixtechblog.com/building-service-topology-at-scale-architecture-challenges-and-lessons-learned-f4b792f3f0d8"
blog: netflix
published: 2026-07-13
---

# Building Service Topology at Scale

Authors: Parth Jain, Rakesh Sukumar, Yingwu Zhao, Renzo Sanchez-Silva, Nathan Fisher. Companion to the earlier "why" post: engineers needed a unified real-time service-dependency view for faster troubleshooting, blast-radius analysis, and architecture navigation. This post is the *how* — the learning journey from a version that worked locally to one surviving production (lagging Kafka consumers, OOMs, 100x traffic skew, GC pauses dwarfing business logic).

## Background: streaming-first and multi-layer

Batch-built topology (hourly/daily snapshots) is archaeology during a 3am incident. Netflix built streaming-first: continuous ingestion of multi-region Kafka flow records plus IPC metrics as SSE, reactive pipelines with backpressure, near-real-time updates (tens of minutes). Three physically separate layers, each with optimized storage, queried in parallel and merged (sub-second latency): Network (eBPF flows, graph store — full coverage, no app context), IPC (app metrics, separate graph store — rich endpoints, instrumented services only), Tracing (Parquet columnar — real paths, sampled).

## Methodology

**Backpressure over drop/buffer/batch.** Unbounded queues OOM; drop-based control loses edges; batch is stale. Reactive streams propagate backpressure upstream (Stage 3 → Stage 2 → Stage 1 → Kafka pause): slow down sustainably, lose nothing, degrade gracefully — at the cost of harder-to-reason-about code.

**Three-stage aggregation with intermediary resolution.** Raw flow logs show hops (App A → LB → App B), not logical dependencies. Stage 1 (FlowLog Ingestion): filter, 5-minute window batching, initial aggregators, consistent-hash distribution, SSE to Stage 2. Stage 2: resolves LBs/NAT/API-gateway/proxy intermediaries into App A → App B. Stage 3: enrichment, graph writes.

**Production challenges and fixes.** Hash-based partition redistribution on ASG scale changes; immutable data structures causing GC pressure at millions of records/sec; skewed partitions; consumer lag — each attacked via measurement-driven optimization (methodology: reproduce, profile, fix, verify at scale).

**Time-travel queries.** Versioned topology snapshots reconstruct the dependency graph at any point in time — critical for "what changed before the incident" analysis.

## Results

Millions of flow records/sec processed, topology reconstructible at any timestamp, sub-second merged queries, freshness in tens of minutes vs hours/days for batch — the system that enables live-event response, incident triage on current data, and immediate change-impact validation.

## Limitations / open questions

- Freshness is tens of minutes, not seconds — accepted for topology, insufficient for per-request tracing.
- Reactive-stream complexity is permanent operational cost.
- Tracing-layer integration deferred to a follow-up post.

## Relevance to SW engineers

- For observability during incidents, freshness beats completeness: slightly-delayed real-time beats hour-old batch or lossy drops.
- Physically separate per-source stores with query-time merging beat one-size-fits-all storage when sources differ in throughput, query patterns, and evolution speed.
- Resolve infrastructure intermediaries into logical dependencies or topology drowns in load balancers.
- Optimize with production-shaped load: local-success ≠ production-success; profile GC, skew, and rebalance behavior explicitly.

## Related concepts

- `concepts/system-design/distributed-systems.md` (backpressure, partitioning)
- `concepts/data-engineering/stream-processing.md` (Kafka, SSE pipelines)
- `concepts/system-design/observability.md` (tracing, dependency maps)
