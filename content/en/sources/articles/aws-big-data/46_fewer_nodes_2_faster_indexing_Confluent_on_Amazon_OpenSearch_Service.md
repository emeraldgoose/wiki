---
title: "46% fewer nodes, 2× faster indexing: Confluent on Amazon OpenSearch Service"
description: "Confluent migrated its OpenSearch hot tier from r6gd to the OpenSearch Optimized oi2 instances, consolidating 168 nodes to 90 with roughly halved indexing latency and lower hot-tier cost."
tags: [source, aws-big-data, opensearch, search, cost-optimization, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/46-fewer-nodes-2x-faster-indexing-confluent-on-amazon-opensearch-service"
blog: aws-big-data
published_date: 2026-11-12
---

# 46% fewer nodes, 2× faster indexing: Confluent on Amazon OpenSearch Service

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/46-fewer-nodes-2x-faster-indexing-confluent-on-amazon-opensearch-service) · **Published**: 2026-11-10

## Overview

Confluent, the company founded by the original creators of Apache Kafka and now part of IBM, runs its internal logging system on Amazon OpenSearch Service and ingests hundreds of terabytes of logs per day to support its Kafka, Connect, and Flink fleets. Because indexing work dominates the hot tier at that volume, the engineering team did not ask whether the workload could run on cheaper hardware; it asked how much more ingest a single node could absorb. The post describes a measure-first migration of the hot tier from r6gd — a previous-generation general-purpose Graviton2 instance where local NVMe was a bolt-on — to oi2, the current-generation instance family purpose-built for OpenSearch.

The instance change is the lever. On oi2, local NVMe is the primary storage tier with no separate Amazon EBS volume: data is written locally and copied synchronously to Amazon S3 for durability (11 nines), and the storage and network path is integrated for indexing and merge I/O. OpenSearch Optimized Instances also replace logical (document) replication with physical (segment) replication, indexing data only on the primary copy and building the other copies by copying segments that are already persisted to S3. That removes redundant indexing work on replicas and network overhead on the primary. One operational consequence is that reported indexing rates can understate reality when replicas are configured — a domain showing 1,000 documents per second may actually be indexing 2,000, because only primary shards do the work.

Each domain was modernized in two logical phases so that efficiency could be measured in production before capacity was removed. Phase 1 was a type swap at constant node count through an in-place blue/green re-provision: at equal nodes, oi2 ran at roughly one-third the CPU of r6gd for the same ingest, about 2.7x the headroom per node. Phase 2 spent that headroom in iterative rightsizing steps, holding at each step to confirm cluster health until a guardrail became binding — and that guardrail turned out to be JVM heap, not CPU, because heap pressure follows query patterns and removing nodes concentrates the same shards onto fewer of them. The fleet consolidated to roughly half the nodes, with each oi2 node carrying about 1.9x the load of an r6gd node (168 ÷ 90) while indexing sped up.

## Key points

- Fleet size fell from 168 r6gd nodes to 90 oi2 nodes, a 46% reduction; per-domain cuts ranged from 31 to 60 percent.
- Indexing latency roughly halved across all four domains, from approximately 0.18–0.19 ms on r6gd to approximately 0.08–0.10 ms on oi2.
- Write backpressure cleared: every r6gd domain carried a double-digit write queue of 8–38 queued operations, while all four oi2 domains dropped below approximately 1.
- CPU fell even on far fewer nodes in three of four domains — for example Domain B went from 60% to 40% on half the nodes.
- Heap, not CPU, set the floor on rightsizing: oi2 has the same heap per node as r6gd, so concentrating shards onto fewer nodes raised average heap on every domain.
- Domain D is the honest outlier: it was cut the hardest relative to its load, its CPU rose from 43% to 56%, and its write queue is the only one not near zero — the team flags it as the domain to watch through peak traffic.
- Stability held: zero write and primary-write rejections in the final state, with all clusters healthy throughout.
- Cost dropped despite a higher per-node price. The roughly 46% consolidation more than offset the oi2 premium for an estimated 18% lower hot-tier cost at on-demand pricing; committing the final footprint to 1-year reserved instances is estimated to land 47–51% below the original r6gd on-demand baseline.

## Details

The production figures compare like-for-like work: a 7-day r6gd baseline against a 24-hour oi2 window at the final node counts, at identical ingest. R8gd was not benchmarked; the evaluation deliberately focused on the optimized oi2 family, and reference points come from AWS internal benchmarks, where oi2 delivers up to 9 percent higher indexing throughput than OR2 instances and up to 33 percent more than I8g. The oi2 family scales from large to 24xlarge with up to 22.5 TB of storage, and each instance bundles compute with third-generation AWS Nitro SSDs for caching plus remote managed storage on Amazon S3.

For teams maximizing indexing throughput on Optimized Instances, the authors recommend using large bulk sizes (10 MB) to improve buffer utilization, using multiple clients for parallel processing, considering more primary shards for throughput while avoiding over-sharding that raises per-node shard density, and keeping the refresh interval at 10 seconds or more — which is already the default for Optimized Instances. Cost numbers are approximate list-derived percentages at on-demand pricing, with reserved-instance values estimated pending a quoted rate; storage tiers (UltraWarm and snapshots) and dedicated-master tiers were unchanged and excluded from the comparison. The takeaway the authors draw is to optimize efficiency per unit of work rather than instance unit price, and to let the real sizing signal — heap in this case — guide the work before any capacity is removed.

## References

- Original article: [46% fewer nodes, 2× faster indexing: Confluent on Amazon OpenSearch Service](https://aws.amazon.com/blogs/big-data/46-fewer-nodes-2x-faster-indexing-confluent-on-amazon-opensearch-service)
