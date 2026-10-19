---
title: "Optimize consumer rebalancing on Amazon MSK with next generation protocol"
description: Promoted on 2026-10-17
published: 2026-10-17
source_url: "https://aws.amazon.com/blogs/big-data/optimize-consumer-rebalancing-on-amazon-msk-with-next-generation-protocol"
blog: aws-big-data
locale: en
tags: [source, article, en, en]
---

# Optimize consumer rebalancing on Amazon MSK with next generation protocol

## Overview

The classic Kafka rebalance protocol pauses every consumer behind a global synchronization barrier whenever one member joins or leaves, producing rebalance storms in large groups. The KIP-848 consumer protocol in Kafka 4.0 moves coordination to the broker-side group coordinator with continuous heartbeats and incremental server-driven reconciliation, so only affected partitions move. It is available on MSK Standard and Express brokers running Kafka 4.x, and helps most for large groups, high-availability workloads, frequently rescaling environments, and dynamic partition scaling.

## Enabling it on MSK

Verify the cluster runs Kafka 4.0+, set `group.protocol=consumer` on clients (it defaults to classic), and drop now-server-controlled client settings (`heartbeat.interval.ms`, `session.timeout.ms`, `partition.assignment.strategy`) — heartbeat and session timeout are configured server-side instead. Confirm client support first: Java 4.0+, confluent-kafka-python 2.12.0+, librdkafka-based clients 2.12.0+. Upgrades can roll in place; the coordinator serves classic and consumer-protocol members side by side.

## Diagnosing slow rebalances

First confirm which protocol is actually active via broker logs in CloudWatch: consumer-protocol lines mention epochs, target assignments, and fencing, while classic lines show `PreparingRebalance` and leader assignments. If KIP-848 is active but rebalances still lag, the usual culprits are session timeouts expiring (45s default, server-side) — especially static members killed without `consumer.close()` in containers — missing SIGTERM graceful-shutdown handling, and churn from unstable consumers. Fixes include graceful shutdown with adequate Kubernetes termination grace periods, static membership via `group.instance.id` so quick restarts skip reassignment, and investigating frozen consumers when timeouts fire during normal operation. Validate with broker logs, CloudWatch lag metrics, and consumer-group descriptions.

## References

- [Original post: Optimize consumer rebalancing on Amazon MSK with next generation protocol](https://aws.amazon.com/blogs/big-data/optimize-consumer-rebalancing-on-amazon-msk-with-next-generation-protocol)
- [KIP-848: The Next Generation of the Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/217387038/KIP-848+The+Next+Generation+of+the+Consumer+Rebalance+Protocol)
