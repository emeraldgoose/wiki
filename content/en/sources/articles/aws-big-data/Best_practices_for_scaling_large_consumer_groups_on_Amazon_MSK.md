---
title: "Best practices for scaling large consumer groups on Amazon MSK"
description: "Avoid RecordTooLargeException rebalances on MSK by sizing consumer-group metadata, raising internal-topic limits, and planning capacity."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/best-practices-for-scaling-large-consumer-groups-on-amazon-msk"
blog: aws-big-data
published_date: 2026-09-22
---

# Best practices for scaling large consumer groups on Amazon MSK

## Overview

Large Kafka consumer groups on Amazon MSK can fail when the `GroupMetadata` record persisted to the internal `__consumer_offsets` topic during a rebalance exceeds the default 1 MB limit, causing `RecordTooLargeException` and a rebalance retry loop. This guide explains why metadata grows, how to estimate its size, and four remediation strategies — raising the size limit, splitting groups, right-sizing partitions and autoscaling, and tightening naming — plus capacity planning, monitoring, and the long-term KIP-848 fix.

## Why metadata grows

During a rebalance, the Group Coordinator serializes one record per group containing every member's subscription topics, owned partitions, new assignment, and client ID, stored uncompressed in `__consumer_offsets`. Kafka's serialization repeats topic names three times per member, and client IDs add further per-member overhead. Rough estimate:

**record size ≈ members × (3 × topic-name bytes + 2 × client-id bytes + ~200 bytes)**

With 1,000 members, a 50-byte topic name, and a 40-byte client ID, that is already ~430 KB; longer names or multi-topic subscriptions cross 1 MB well before 2,000 members.

## Primary fix: raise the size limit

The most direct remediation for groups already past the limit:

1. Raise `max.message.bytes` on `__consumer_offsets` (for example to 2 MB) via `kafka-configs.sh`.
2. Raise broker-level `replica.fetch.max.bytes` to at least the same value through the MSK cluster configuration, so followers can replicate the large records — otherwise expect `UnderReplicatedPartitions`.
3. Test in non-production first: trigger a rebalance, confirm no `RecordTooLargeException`, and check heap usage and replication lag stay healthy.

## Complementary strategies

- **Split large groups:** deploy multiple consumers with distinct `group.id` values over partition subsets. This cuts per-group metadata proportionally at the cost of operating more groups.
- **Right-size partitions and autoscaling bounds:** over-partitioned topics force more consumers; cap autoscaling replicas (for example HPA on EKS) and align partition count with intended maximum consumers. Best applied proactively at topic design time.
- **Optimize naming:** shorter, standardized group and client-ID names reduce per-member overhead, but renaming an active group loses committed offsets — practical mainly for new deployments.

## Capacity planning, monitoring, and KIP-848

Plan by computing current record size, projecting peak membership from autoscaling bounds, applying a 2× safety margin, then choosing the limit and broker size (for example, `kafka.m5.xlarge`+ around 500–1,000 members, `m5.2xlarge`+ beyond that, plus group splitting past 2,000). Watch `HeapMemoryAfterGC` (alarm at 60% warning, 80% critical), `UnderReplicatedPartitions` (alarm above 0 for 5+ minutes), GC pauses, rebalance rate, and consumer lag.

Long term, Kafka 4.0's KIP-848 makes server-side assignment the default consumer protocol, shrinking per-member metadata and enabling incremental rebalances. Prepare by tracking MSK version support, verifying client compatibility, testing in non-production, and rolling out starting with non-critical groups.

## References

- Original post: [Best practices for scaling large consumer groups on Amazon MSK](https://aws.amazon.com/blogs/big-data/best-practices-for-scaling-large-consumer-groups-on-amazon-msk)
