---
title: Constraint Management for Cluster Operation Safety and Reliability at Twitter
description: A centralized cluster-aware arbiter preventing colliding maintenance operations on stateful fleets like Kafka
tags: [source, twitter, x, kafka, sre, reliability, safety, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/constraint-management-for-cluster-operation-safety-and-reliability-at-twitter"
blog: twitter
date: '2023-01-19'
---

# Constraint Management for Cluster Operation Safety and Reliability at Twitter

## Summary

Twitter's Platforms Messaging team runs dozens of Kafka broker clusters (tens to hundreds of stateful brokers on hybrid-Mesos) where data on SSDs cannot be lost and `n` replicas tolerate at most `n-1` simultaneous machine losses. Repeated incidents showed the dominant risk was not hardware but *coordination*: operator-to-operator collisions (two operators removing machines concurrently), operator-to-automation collisions (manual work during a kernel-upgrade rolling reboot), and plain human error (wrong batch size rebooting too many machines at once; decommissioning production instead of staging, leaving clusters under-replicated). The answer was an in-house **constraint management service**: a centralized, cluster-aware final arbiter that decides whether a requested operation is safe to execute right now.

## How It Works

### Resources

A cluster is defined by resources — compute, storage, memory, network (on bare metal: machine counts and SKUs). Each cluster is provisioned with a buffer (e.g. 20% extra storage, 30% extra network) so that host removal/reboot for maintenance stays invisible to customers.

### Constraints

A constraint is the minimum resources required to keep serving plus the maximum removable at once. Defined per cluster, examples include: max simultaneous hosts in maintenance (absolute, percentage, or per-rack), max non-drained downtime hosts, minimum healthy/active hosts, minimum network bandwidth and compute capacity. Custom success-rate queries with thresholds are supported — e.g. the Messaging team gates maintenance on a Kafka under-replication check. Determinations draw on live cluster state: host counts, healthy hosts, success rates, machine types.

### Example constraint rules (stored in ConfigBus, injected at runtime)

1. At most X operations on Y machines at once per cluster (reboot, drain, Aurora restart/kill) — for Kafka, operate on one shard at a time to avoid under-replicated partitions.
2. Rate limits: operation Y at most Z times per window — essential for auto-remediation loops answering pages.
3. One operation per machine at a time (never drain and reboot simultaneously).
4. Multi-party operations on the same cluster must not jointly violate constraints (allows several humans to collaborate during site incidents).
5. During site-impacting incidents, automatic operations are refused unless forced; humans may override with an explicit `--force` plus `--reason`.

### Moratoriums

Clusters/roles can enter moratorium (e.g. production change freeze); only emergency-flagged maintenance is admitted.

### ConfigBus

Constraints live in Twitter's dynamic configuration system (ConfigBus), so rules update at runtime without redeploying the service.

## Results

The service converts a class of coordination incidents into clean rejections: unsafe operations are refused before execution instead of being cleaned up afterward, and automation (fleet management, paging auto-remediation) becomes safe to run at scale.

## Relevance to SW Engineers

- Any fleet running stateful services needs a *safety arbiter* separate from the executors: executors propose, the arbiter disposes, based on live cluster state.
- Encode blast-radius limits as data (per-cluster/per-rack caps, rate limits), not as operator runbook discipline — humans under incident pressure will exceed runbook limits.
- Always provide a `--force` + `--reason` escape hatch for emergencies, and log it; a safety system without an override gets bypassed permanently after the first real incident.
- Freeze support (moratoriums) is a first-class feature, not an afterthought, for change freezes and holidays.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/constraint-management-for-cluster-operation-safety-and-reliability-at-twitter (Ashwin Poojary, 19 Jan 2023)
- Related: `concepts/data-engineering/apache-kafka.md`, `concepts/infrastructure/kubernetes.md`
