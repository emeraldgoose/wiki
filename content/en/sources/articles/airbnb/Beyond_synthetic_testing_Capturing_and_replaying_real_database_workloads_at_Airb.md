---
title: "Beyond synthetic testing: Capturing and replaying real database workloads at Airbnb"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb"
blog: airbnb
published: 2026-10-17
---

# Beyond synthetic testing: Capturing and replaying real database workloads at Airbnb

## Overview

Airbnb operates hundreds of MySQL-compatible clusters serving millions of queries per second. Synthetic benchmarks like sysbench never reflected real production behavior, so the team built a capture-and-replay pipeline on top of ProxySQL: capture live query traffic at the proxy layer, process it offline into per-cluster replayable datasets, and replay it against target databases to test load, verify upgrade compatibility, and debug performance problems.

## Why capture at the proxy layer

An earlier approach logged queries inside each application's language binding (Java, Python, Ruby) and funneled traces through Kafka to a custom replayer. It worked as a first step but had heavy per-language maintenance cost, scaled poorly across services, and lost transaction context — concurrent statements were interleaved without ordering, so transactions could not be reproduced faithfully.

Since all database traffic already flows through ProxySQL, the team moved capture there: a single client-agnostic point needing no application changes. ProxySQL's built-in query logging can be enabled per cluster with little performance impact, and a Log Mover sidecar ships log files to object storage to keep local disk usage bounded.

## Capture, process, replay

The pipeline has three stages. The Log Mover collects raw binary query logs from ProxySQL pods. The Log Processor, an offline job, decodes the logs, splits mixed-backend traffic into per-cluster files, reassembles each transaction's statements in original order, buckets queries into five-minute time windows for fine-grained pacing control, and rewrites `INSERT` statements to pin the captured `last_insert_id` explicitly — keeping auto-increment behavior consistent across engines at the cost of no longer exercising the target's native ID generation. The Log Replayer then runs the processed logs via an API server, a task scheduler, and horizontally scalable workers that preserve original timing (or accelerate by a speed factor) using a shared expected-start-time per batch.

Two replay modes exist: replay-only for load testing (ignoring results, tracking errors, latency histograms, and resource use) and replay-and-compare, which runs identical traffic against two targets and diffs results for migration validation.

## Impact on upgrades and capacity planning

Replay testing carried Airbnb's MySQL 5.7 to 8.0 upgrade: bisection replays isolated a query-cache effect and surfaced a severe latency regression (one pattern went from 0.03s to 2.6s per join), while compare-mode runs caught non-deterministic queries lacking a full `ORDER BY` before they broke production. For capacity planning, replaying traffic at 2x speed ahead of peak season exposed ceilings early — one large cluster's commit latency rose from ~6ms to ~34ms under 80% more writes. Teams now request replays through a self-serve tool.

## References

- Original article: https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb
