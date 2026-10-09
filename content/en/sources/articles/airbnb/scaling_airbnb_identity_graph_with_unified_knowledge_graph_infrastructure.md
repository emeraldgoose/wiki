---
title: "Scaling Airbnb's Identity Graph with a Unified Knowledge Graph Infrastructure"
description: JanusGraph + DynamoDB paved-path graph platform — identity graph migration off SaaS, P99 wins, 10x write scale
tags: [source, airbnb, knowledge-graph, janusgraph, infrastructure, trust-and-safety]
locale: en
source_url: "https://medium.com/airbnb-engineering/scaling-airbnbs-identity-graph-with-a-unified-knowledge-graph-infrastructure-ebac467b7836"
blog: airbnb
date: 2026-05-19
---

# Scaling Airbnb's Identity Graph with a Unified Knowledge Graph Infrastructure

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-05-19

## The Identity Graph

Airbnb's identity graph (users/relationships as vertices/edges) underpins Trust & Safety: identity resolution, linked accounts, suspicious-activity detection. Two components: **graph data storage** (graph DB + KV cache; near-real-time async ingestion, low-latency serving) and **graph service** (unified access + aggregation/model layer for downstream consumers).

**Evolution**: relational DB + JSON edge-lists in KV (joins too costly as density grew) → third-party SaaS graph DB in 2021 (scalable but long-tail latency, instability, no tuning/fine-grained ACLs) → internal graph infrastructure. Persistent challenges: **7B nodes / 11B edges, +5M edges/day** (write scale); **4–8 hop reads** (latency); **fanout skew** (P95/P99 explode vs P50 on hot nodes); slow-query resource hogs (stability).

## The Platform: Paved-Path Knowledge Graph Infrastructure

Before it, teams fell into four anti-patterns: relational "graphs" (expensive traversal joins), offline warehouse graphs (day-old), DIY open-source (ops toil), managed PaaS (lock-in, bottlenecks). The 2024 platform unifies tenants (identity graph first adopter) in isolated namespaces under one supported stack.

**Tech choice — JanusGraph + DynamoDB (+ OpenSearch indexing)**, picked for: online-query scalability, expressive schema/queries, infra/ops fit, extensible codebase. JanusGraph (Apache TinkerPop, labeled property graph, **Gremlin**) over DynamoDB gives **storage separation**: managed distributed persistence underneath, full control of graph logic on top, swappable storage later. A management service adds schema enforcement, index management, schematized Thrift APIs.

**Engine optimizations**: custom transaction strategy on DynamoDB conditional writes/transactions (lighter than JanusGraph default locking); parallelized `getMultiSlices` for high-fanout fetches; Airbnb distributed-tracing integration into the internal fork.

## The Migration (Gremlin on Both Sides)

Four identity-graph apps (event ingestion, bulk load, serving, precompute); read/write traffic isolated at the compute layer. Gremlin compatibility enabled **shadow-traffic side-by-side benchmarking** before production cutover and vendor deprecation. But identical Gremlin ≠ identical performance (different planner optimizations), so **client-side query rewriting**: drop `Path`/`SimplePath` steps (fall back to slow non-batched backend queries hogging storage threads → acyclic conditional-query chains) and minimize computation inside side-effect aggregation steps.

**Gains**: end-to-end read API latency down across all patterns with sharp **P99 reduction**; stability (no more periodic manual instance reboots; faster transparent incidents); **write QPS auto-scaled to 10x** the vendor solution in load tests. Same infra now serves fraud detection, inventory graphs, data lineage.

## Takeaways for SW Engineers

- **Storage separation** (pluggable graph logic over managed KV) buys iteration speed without rebuilding distributed storage.
- Same query language ≠ same plan: budget for **client-side query rewriting** in engine migrations; shadow traffic first.
- Attack tail latency at the fanout: parallel slice fetches + path-step elimination.
- Paved-path multi-tenancy kills the four anti-patterns at the root.

## Related Concepts

- Labeled property graphs, Gremlin/TinkerPop; KV-backed graph storage tradeoffs
