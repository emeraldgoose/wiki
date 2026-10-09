---
title: Apache Kafka
description: "Seminar-level concept: Kafka architecture, partitioning, consumer groups, stream processing"
tags: [concept, data-engineering, kafka, stream-processing, messaging]
locale: en
---

# Apache Kafka

**Read from**: Source articles (Uber Kafka optimization, Netflix stream processing, Twitter Sparrow shift, LinkedIn FishDB)

## What It Is
Distributed event streaming platform: publish/subscribe, storage, processing. Log-structured, partitioned, replicated commit log.

## Architecture

### Core Primitives
- **Topic**: Category/feed name; partitioned, ordered
- **Partition**: Ordered, immutable sequence of records (offset)
- **Broker**: Server storing partitions; leader/follower replication
- **Consumer Group**: Parallel consumers; each partition → one consumer in group

### Replication
- **ISR (In-Sync Replicas)**: Followers caught up to leader
- **acks=all**: Wait for ISR ack (durability)
- **min.insync.replicas**: Minimum ISR for write acceptance

### Producer
- **Batching**: `linger.ms`, `batch.size`
- **Compression**: `snappy`, `lz4`, `zstd` (lz4 best throughput/compression)
- **Idempotence**: `enable.idempotence=true` + `acks=all` → exactly-once per partition
- **Transactions**: Atomic multi-partition writes

### Consumer
- **Poll loop**: `poll(Duration)` → records → process → commit offsets
- **Offset management**: Auto-commit (risk of loss/dup) vs manual (exactly-once with transactions)
- **Rebalancing**: Cooperative sticky assignor (minimizes disruption)

## Stream Processing (Kafka Streams / ksqlDB)
- **Topology**: Source → Transform → Sink
- **Stateful ops**: Aggregations, joins, windowing (tumbling, hopping, session)
- **State stores**: RocksDB-backed changelog topics (fault-tolerant)
- **Exactly-once**: `processing.guarantee=exactly_once_v2`

## Performance at Scale (from Sources)

### Uber (Cost-Efficient Export)
- Hudi column stats + sorting for predicate pruning
- Kafka as ingestion layer for Hudi tables

### Netflix (Real-time Distributed Graph)
- eBPF flow logs → Kafka → topology layers
- Millions records/sec; immutable data structures → GC pressure
- Hash-based partition redistribution on ASG changes

### Twitter (Sparrow: Batch → Streaming)
- Project Sparrow: batch event approach → streaming architecture
- Real-time pipelines for search, analytics

### LinkedIn (FishDB Retrieval)
- Feed retrieval engine backed by Kafka for real-time updates

## Key Optimizations (Seminar Checklist)

### Throughput
```properties
# Producer
linger.ms=5
batch.size=65536
compression.type=lz4
buffer.memory=67108864

# Broker
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
```

### Latency
```properties
# Consumer
fetch.min.bytes=1
fetch.max.wait.ms=500
max.poll.records=500
```

### Storage
```properties
# Log retention
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Compaction for keyed topics
cleanup.policy=compact
min.cleanable.dirty.ratio=0.5
```

## When to Use Kafka (vs Alternatives)
| Scenario | Kafka | Pulsar | RabbitMQ | Kinesis |
|----------|-------|--------|----------|---------|
| High-throughput event log | ✅ | ✅ | | |
| Multi-tenant, geo-replication | | ✅ | | |
| Complex routing, low latency | | | ✅ | |
| AWS-managed, serverless | | | | ✅ |
| Exactly-once, stateful processing | ✅ | ✅ | | |

## Related Sources
- `sources/articles/uber-engineering.md` (Kafka for Hudi ingestion)
- `sources/articles/netflix-techblog.md` (real-time graph, eBPF → Kafka)
- `sources/articles/twitter-engineering.md` (Sparrow batch→stream)
- `sources/articles/linkedin-engineering.md` (FishDB retrieval)

## Related Guides
- `guides/data-engineering/kafka/partitioning.md`
