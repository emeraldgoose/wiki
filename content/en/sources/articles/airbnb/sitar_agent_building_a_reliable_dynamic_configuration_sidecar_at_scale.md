---
title: "Sitar-Agent: Building a Reliable Dynamic Configuration Sidecar at Scale"
description: Kubernetes sidecar for dynamic config delivery — S3 snapshots, pull-with-cache, SQLite migration, main-vs-sidecar tradeoffs
tags: [source, airbnb, infrastructure, kubernetes, configuration, distributed-systems]
locale: en
source_url: "https://medium.com/airbnb-engineering/sitar-agent-building-a-reliable-dynamic-configuration-sidecar-at-scale-b7e00c152068"
blog: airbnb
date: 2026-06-04
---

# Sitar-Agent: Building a Reliable Dynamic Configuration Sidecar at Scale

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-06-04 · **Authors**: Bo Teng, Cosmo Qiu, Siyuan Zhou, Ankur Soni, Xin Huang, Willis Harvey. Companion to the earlier Sitar service-architecture/safety post.

## Problem

Config changes commit several times per minute — how do they reach thousands of service instances **reliably, in seconds, without redeploys**? Constraints: configs must always be readable (stale beats unreadable, even if Sitar Service is down); propagation in tens of seconds across tens of thousands of pods; polyglot fleet (Java, Python, Go, TypeScript, Ruby) with minimal per-language maintenance.

## Delivery Lifecycle

1. **Create/update** via Git flow or web UI → Sitar Service (versioned, changelogged, ACL-enforced).
2. **Hourly snapshot** — Snapshot Service packages full config-group state → compressed snapshots on S3.
3. **Pod startup**: (3.1) sidecar preloads latest S3 snapshot to shared disk (fast restart, survives Sitar outages, no thundering herd on deploy); (3.2) initial sync with Sitar Service catches post-snapshot changes → signals readiness, unblocking the main container.
4. **Steady state**: polling loop (order of seconds + jitter) for subscribed-group changes.
5. **Read path**: main container reads mounted disk via client library with transparent in-memory cache refresh.

## Key Decisions (2024 Ruby → Java rewrite)

**Sidecar vs in-process library**: library saves per-pod JVM overhead and operational surface — but requires reimplementation in 5 languages, removes fault isolation (Sitar bug can crash/starve the app and vice versa), mixes logs/metrics, and blocks container-level optimization. **Kept the sidecar**: savings didn't justify reliability/maintenance costs.

**Pull vs push**: pull-every-10s is simple but load-heavy when idle; push is efficient but complex. Kept pull + two server-side optimizations: (1) **short-TTL (10s) server cache** — manual changes tolerate slight delay; most polls hit cache, skipping compute/DB; (2) **change token** (last scanned DB row) on cache miss — server skips already-seen rows. Simple, stateless, scales.

**Local store: Sparkey → SQLite**: both beat Sparkey on size/memory/QPS, but SQLite won over RocksDB — workload fits comfortably in its envelope, first-class multi-language libraries, WAL-based concurrent access, simpler ops (no compaction/column-family tuning, no deep RocksDB expertise needed). **Safe migration**: shadow read-and-compare per service (serve Sparkey, validate SQLite in parallel) + feature-flagged gradual rollout, Tier-0 last.

## Takeaways for SW Engineers

- **Stale-beats-unavailable** as an explicit design goal drives snapshot preload + disk reads.
- Keep the simple architecture (pull) and **optimize the server side** (TTL cache + incremental tokens) before reaching for push.
- Polyglot fleets favor sidecars over libraries; isolation is worth the per-pod cost.
- Storage migrations: shadow reads + flag-gated rollout, critical tiers last.

## References

- Prior post: Safeguarding dynamic configuration changes at scale
