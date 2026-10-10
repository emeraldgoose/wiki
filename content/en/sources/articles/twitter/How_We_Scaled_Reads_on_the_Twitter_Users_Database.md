---
title: How We Scaled Reads on the Twitter Users Database
description: Scaling the Twitter User Reservation System to millions of read QPS with Vitess Vtgate on Aurora Mesos
tags: [source, twitter, x, mysql, vitess, databases, scalability, tier-2, data-engineering]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database"
blog: twitter
date: '2023-02-23'
---

# How We Scaled Reads on the Twitter Users Database

## Summary

Twitter's User Reservation System (URS) — one of the world's largest username reservation stores — was originally built on Gizzard, an old MySQL framework with bespoke features like quorum reads. Growth made it impossible to meet strict SLOs on QPS, latency, success rate, and cross-datacenter consistency while keeping maintenance costs down. The team moved URS to plain MySQL scaled with [Vitess](https://vitess.io/), using its stateless proxy component **Vtgate** to scale *reads* to millions of queries per second — an unusual use of Vitess, which is usually adopted for sharding writes.

## Why Not Just Add Replicas?

The MySQL servers are on-premise commodity hardware tuned for Twitter's workloads. Adding enough replicas to serve millions of read QPS was rejected as infeasible: it would burn resources better used by MySQL itself and still leave connection fan-out and topology management unsolved.

## Architecture

Each MySQL instance is paired with a **Vttablet** process providing connection pooling, query rewriting, and query deduplication. **Vtgate** is Vitess's stateless routing proxy: it routes each query to the correct Vttablet and consolidates results back to the application.

The critical decision was to move Vtgates *off* the MySQL hosts:

1. Co-located Vtgates would steal CPU/memory from MySQL.
2. Reads needed to scale to *hundreds* of Vtgate instances.

Because Vtgates are stateless, they were deployed as containerized applications on **Aurora Mesos**. The team tuned instance counts, CPU, OS thread counts, and Go GC settings (GOGC) until the tier sustained millions of QPS, with each Vtgate tested to a couple of thousand connections.

## Why Vitess

- Open source with good MySQL integration.
- Built-in topology service (backed by Twitter's highly available ZooKeeper clusters) storing all configuration.
- Integrates with Orchestrator (VTORC) for MySQL replication topology management, removing cluster-maintenance overhead and giving a highly available MySQL cluster — with sharding available later if writes ever need it.

## Security

Encryption-in-transit is mandatory at Twitter, and Vitess supports TLS between every hop (application ↔ Vtgate ↔ components). To enable TLS with zero downtime the team upstreamed an **optional-TLS** feature to open-source Vitess. They also found Vitess verified clients against a single certificate rather than the full chain, and patched upstream Vitess to use the full chain.

## Results

URS now runs in production as a tier-1 application with extremely high availability for both reads and writes, serving millions of read QPS. The team recommends Vitess to the industry for read scaling, not just write sharding.

## Relevance to SW Engineers

- Separate stateless query-routing proxies from stateful storage hosts so each scales independently; stateless proxies are ideal container/Mesos/Kubernetes citizens.
- Connection pooling + query deduplication at the tablet layer multiplies effective read capacity without touching application code.
- When adopting open source for a critical path, budget for upstreaming: optional-TLS and full-chain verification were prerequisites, and contributing them back reduced long-term fork maintenance.
- Tune the Go runtime (threads, GOGC) explicitly when a proxy must hold thousands of connections per instance.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database (Doyel Mitra Sinha, Ashwin Poojary, 23 Feb 2023)
- Related: `concepts/data-engineering/delta-lake.md`
