---
title: 'Java Heap Memory and Garbage Collection: Tuning for High-Performance Services'
description: LinkedIn FollowFeed's JVM journey — CMS to G1GC to generational ZGC on JDK 21, 55% lower P999, 28% more capacity
date: 2024-09-13
tags: [source, linkedin, jvm, gc, performance, followfeed]
locale: en
source_url: "https://www.linkedin.com/blog/engineering/infrastructure/java-heap-memory-and-garbage-collection-tuning-for-high-performance-services"
blog: linkedin
author: Nisheedh Raveendran
---

# Java Heap Memory and Garbage Collection: Tuning for High-Performance Services

FollowFeed — the indexing and recommendation system behind LinkedIn's feed, SLA < 50 ms — models member actions as "Activity" triples (actor–verb–object, e.g. "Jeff shared article XYZ"). Explosive growth pushed per-shard heaps to **183 GB**, breaking the original GC setup. This post chronicles the path from CMS to generational ZGC on JDK 21.

## The problem

- **183 GB heap per shard.** More shards would shrink heaps but worsen fan-out tail latency — so heaps had to stay huge.
- **Hostile allocation profile:** up to 12 GB/s allocation, large live set (up to ~110 GB), continuous promotion to old-gen from Kafka-driven cache eviction; values cached as POJOs (not serialized) to skip deserialization on reads.
- **CMS removed.** The app ran JDK 11 + Concurrent Mark Sweep; CMS was deprecated in 11 and removed in 17, forcing a move. G1GC was fine at median but mixed collections over the giant live set / complex object graph wrecked tail latency despite meticulous tuning. Non-generational Shenandoah/ZGC on JDK 17 constantly rescanned the huge live set, stalling mutators and maxing CPU.

## Step 1: cut allocation at the source (JFR-guided)

- **Event logging** deserialized full Avro objects just for logs; only the event ID was used → log the ID only, **−50% byte-array allocation**.
- **Optional on hot paths** (request serving, event consumption) allocates per call → refactored away.
- Result: allocation rate **12 GB/s → 1–2 GB/s**, the precondition for everything after.

## Step 2: shrink the live set (JXRay-guided)

- Eliminated duplicate strings and flattened in-memory object representations (less per-object header overhead).
- Result: **−34% heap usage** — headroom for growth and less heap for the GC to scan.

## Step 3: generational ZGC on JDK 21

With allocation and live set tamed, the team moved to JDK 21's generational ZGC (in collaboration with ZGC developer Erik Österlund):

- `-XX:SoftMaxHeapSize` as a buffer against allocation spikes.
- Raised fragmentation limit, lowered tenuring threshold, disabled proactive collections to calm load-barrier storms.
- **OS tuning:** enabled transparent huge pages for ZGC's shared-memory mappings (up to +15% performance) and raised `vm.max_map_count` for large-heap mapping needs.

## Results (at 450 qps)

- **P999: 100 ms → 45 ms (−55%)**; P99: 40 ms → 30 ms; zero thread-stall time.
- **+28% serving capacity** from latency reduction alone.

## Takeaways for SW engineers

1. **Know your data first** — heap-dump analysis (JXRay) before collector shopping.
2. **Allocation rate dominates** — JFR allocation profiling; kill Optional/logging waste on hot paths.
3. Huge heaps + fan-out constraints rule out "just add shards"; generational concurrent collectors (ZGC) are built for exactly this shape.
4. Budget OS-level work (huge pages, map counts) — managed runtimes still sit on kernels.

## Related concepts

- FishDB (`sources/articles/linkedin/FishDB_A_Generic_Retrieval_Engine_for_Scaling_LinkedIn_Feed.md`) — the Rust successor that sidesteps GC entirely.

## References

- Source: https://www.linkedin.com/blog/engineering/infrastructure/java-heap-memory-and-garbage-collection-tuning-for-high-performance-services
