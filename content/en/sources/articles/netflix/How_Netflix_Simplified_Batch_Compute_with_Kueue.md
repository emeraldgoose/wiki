---
title: "How Netflix Simplified Batch Compute with Kueue"
description: Migrating millions of batch jobs from custom CMB scheduler to Kueue on Titus with zero-lift transparent migration and preemption-based fair sharing
tags: [source, article, netflix, kubernetes, kueue, batch, platform-engineering]
locale: en
source_url: "https://netflixtechblog.com/how-netflix-simplified-batch-compute-with-kueue-87860682629c"
blog: netflix
published: 2026-06-22
---

# How Netflix Simplified Batch Compute with Kueue

Authors: Alvin Bao, Alex Petrov, Jennifer Lai, Aidan Sherr, Samartha Chandrashekar. As Netflix's compute goes Kubernetes-native, the Compute team replaced custom queuing/scheduling in the homegrown Compute Managed Batch (CMB, est. 2018) with Kueue, the cloud-native Kubernetes job-queueing system, running on the Titus container platform — covering what motivated it, how millions of jobs migrated, and what the platform now offers.

## Background: CMB and Titus

CMB is a managed run-to-completion batch solution: tenant hierarchies (internal tenants organizing subtrees; leaf tenants with queues), per-tenant capacity configs (weights for fair sharing, resource dimensions), reserved capacity (partitioned, isolated) plus a global shared pool for bursting — but admission-time-only fair sharing with no preemption (admitted jobs ran to completion). Titus provides workload federation across cells and federated capacity reservations behind one endpoint.

## Methodology

**Why Kueue.** CMB predates mature open-source batch options; the ecosystem caught up (fair sharing, hierarchical tenants, capacity management, priority queuing) while CMB's distance from the cluster made features like preemption painful. Kueue won because it doesn't replace kube-scheduler (preserving Titus scheduling profiles and placement efficiency — unlike YuniKorn/Volcano), has adoption momentum, supports multi-tenant quotas over heterogeneous hardware, operates on Pod/Job plus RayJob/RayCluster for extensibility, and ships preemption, all-or-nothing, and topology-aware scheduling natively.

**Migration ("Netflix Batch") tenets.** Zero lift for end users (fully transparent); no regressions in launch rate/throughput; replace CMB queuing/scheduling with Kueue. Queuing deferred to per-cell Kueue via a custom router over Titus federation; enrollment is a UI button-click converting internal tenants → Cohorts and leaf tenants → ClusterQueue + LocalQueue, capacity configs → flavors/nominal quotas, with easy rollback. Lessons: keep API parity and migrate internals first (unstack bets, no customer disruption); migrate the largest/most complex customer first (production migration took 4 weeks); run Kueue far above default QPS/Burst/groupKindConcurrency after Titus-mirroring load tests.

**Fair sharing and preemption.** Preemption-based fair sharing preserves reservation semantics while lending idle reserved capacity to others (`reclaimWithinCohort: Any`, `withinClusterQueue: LowerPriority`): tenants burst into idle reservations, submit without starvation risk, and get faster turnaround for business-critical workloads.

## Results

Kueue fully rolled out in production managing millions of workloads, higher utilization of reserved capacity, learnings reused by internal Kubernetes-native training-infra teams; more Titus batch enrollment planned.

## Limitations / open questions

- Non-Kueue Titus batch workloads remain outside the managed experience.
- Preemption churn vs utilization trade-offs need ongoing tuning per tenant class.
- Above-default API-server load from high QPS/Burst is accepted operational cost.

## Relevance to SW engineers

- Prefer adopting ecosystem projects over extending homegrown systems once the ecosystem catches up — but only if the choice preserves your scheduler/placement investments.
- Migrate internals behind a stable API first; move the hardest customer early to derisk the tail.
- Load-test control-plane knobs (QPS, burst, concurrency) against production-mirror environments before rollout.
- Preemption converts static reservations into elastic sharing without abandoning isolation guarantees.

## Related concepts

- `concepts/system-design/kubernetes.md` (scheduling, quotas, preemption)
- `concepts/data-engineering/apache-spark.md` (batch orchestration)
