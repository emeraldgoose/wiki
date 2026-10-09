---
title: Data Platform Cluster Operator Service for Hadoop Cluster Management
description: Twitter's DCO service — a Flask-based Python operator automating Hadoop host lifecycle, quotas, and keytabs
tags: [source, twitter, x, hadoop, sre, automation, operators, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/the-data-platform-cluster-operator-service-for-hadoop-cluster-management"
blog: twitter
date: '2023-02-08'
---

# Data Platform Cluster Operator Service for Hadoop Cluster Management

## Summary

Twitter runs Apache Hadoop with no enterprise Hadoop distribution, so no standard cluster-management tooling existed for its scale. Data Platform SREs spent most of their time on routine cluster operations: adding/removing hosts, draining hosts, handling capacity requests, host lifecycle, and cluster health. The team built the **Data Platform Cluster Operator (DCO)** — a Python/Flask service that turns these into API-driven, orchestrated, single-step operations across all data centers and cloud.

## Architecture

- **Flask** web tier behind a load balancer + WSGI gateway exposes API endpoints.
- Requests from Hadoop administration are parsed, stored in a **sharded MySQL** database (sharding allows horizontal scaling of request volume), and forwarded to an **internally managed reliable workflow engine** that executes plans as sets of per-host tasks, each retriable a configured number of times with failure-dependent task selection.
- A callback updates job state in DCO's database; if DCO is down at callback time, a periodic poller reconciles plan status — so orchestration survives DCO outages.
- A **request management controller** receives API calls and dispatches tasks.
- Tech stack: Flask, MySQL backend, deployment infrastructure, workflow engine.

## Features

- **hadoop-admin library** — Python library with Hadoop administration logic: cluster/service status lookup and per-node operations via on-node binaries.
- **Adding hosts** — SREs submit a hostname file plus cluster variables; DCO installs packages, rewrites configs, restarts services, and returns a job ID for progress tracking. A multi-step error-prone procedure becomes one call.
- **Removing hosts** — one step: hosts leave the cluster, go through reinstallation, and are ready for another cluster.
- **HDFS/YARN quota management** — storage and compute allocation/deallocation with change history usable for customer chargeback.
- **Keytab management** — DCO provisions and manages the lifecycle of every node's Kerberos keytabs (the companion piece to the Hadoop kerberization effort).
- **Feature flags** — per-cluster YAML declares which features a cluster needs, gating rollout.
- **High availability posture** — DCO runs per datacenter serving local operations; since it never sits on the HDFS data path or YARN capacity path, it carries a modest uptime SLO by design.

## Results

DCO was tested comprehensively and deployed to production clusters, making Hadoop operations faster, less error-prone, and scalable without growing SRE headcount linearly with fleet size.

## Relevance to SW Engineers

- This is the Kubernetes-operator pattern applied to a system with no operator framework: desired state in MySQL, reconciliation in a workflow engine, per-host retriable tasks.
- Design the callback path for receiver outages (poll-based reconciliation as backup), not just worker outages.
- Keep the control plane off the data path so its SLO can stay modest while the data plane stays strict.
- Per-cluster feature-flag YAML files let one operator binary serve heterogeneous fleets safely.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/the-data-platform-cluster-operator-service-for-hadoop-cluster-management (Ashwin Poojary, Lakshman Ganesh Rajamani, Sampath Kumar, 8 Feb 2023)
- Related: `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/apache-kafka.md`
