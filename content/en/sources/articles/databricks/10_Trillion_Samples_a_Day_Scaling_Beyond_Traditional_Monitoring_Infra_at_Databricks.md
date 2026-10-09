---
title: 10 Trillion Samples a Day Scaling Beyond Traditional Monitoring Infra at Databricks
description: How Databricks scaled monitoring to 5B active timeseries and 10T samples/day — Pantheon (Thanos fork), cardinality-shielding aggregation, and the Hydra lakehouse troubleshooting platform.
date: 2026-05-05
tags: [databricks, monitoring, observability, thanos, prometheus, timeseries, data-engineering, lakehouse, delta-lake, cardinality]
locale: en
source_url: "https://www.databricks.com/blog/10-trillion-samples-day-scaling-beyond-traditional-monitoring-infra-databricks"
blog: databricks
---

# 10 Trillion Samples a Day: Scaling Beyond Traditional Monitoring Infra at Databricks

**Authors**: David Yuan, Yi Jin, Karan Bavishi, HC Zhu, Joey Beyda · **Published**: May 5, 2026 · **Source**: [Databricks Engineering Blog](https://www.databricks.com/blog/10-trillion-samples-day-scaling-beyond-traditional-monitoring-infra-databricks)

## The scale problem

Databricks' monitoring infrastructure more than tripled in a year, reaching **5 billion active timeseries in real time** and **over 10 trillion samples ingested per day**, spread across roughly **70 cloud regions on AWS, Azure, and GCP**. Three constraints made off-the-shelf solutions unworkable:

- **Global heterogeneity**: equivalent performance required across three clouds and dozens of regions that differ from each other.
- **Hands-off operations**: with that breadth, oncalls cannot manage each regional stack by hand — the system must be self-healing and self-scaling while exposing simple interfaces.
- **Cardinality explosion from serverless/AI churn**: serverless compute launches tens of millions of VMs daily; short-lived pods/nodes mean identifier labels (pod ID, node ID) churn constantly, and TSDB cost scales with label cardinality.

The old stack — TSDBs built for an order of magnitude less scale — became the #1 reliability problem in all of monitoring infrastructure. Scaling a TSDB, an infrequent event at most companies, was needed almost daily. The team attacked three problems: (1) a reliable, efficient TSDB, (2) metric aggregation to shield TSDBs from cardinality, (3) highly dimensional troubleshooting on the lakehouse.

## Pantheon: a Thanos fork for the TSDB layer

TSDBs ingest huge volumes of timeseries and serve high-QPS, low-latency real-time reads — ideal for alerts and dashboard refreshes that re-issue the same queries against the newest data. The team built **Pantheon**, a fork of the CNCF open-source [Thanos](https://thanos.io/) project: **160+ Thanos instances across all regions and three clouds**, ~5B in-memory active timeseries total. The largest single instance holds ~300M in-memory timeseries and serves nearly 1,000 PromQL queries/sec; deployments range down to small 3-node setups. Edge cases and optimizations found at this scale are contributed back upstream.

**Headline results**: millions of dollars in annual cloud cost saved, ~5x reduction in monitoring-infrastructure downtime, elimination of large sources of manual toil.

### Tiered storage and cost optimizations

Thanos' tiered storage keeps the freshest series in memory, the last 24h on disk, and everything older on object storage — so real-time queries hit RAM while compute stays decoupled from historical data (scale-up without rebalancing history). On top of that, four optimizations:

- **Split memory retention by workload lifespan**: two Receive groups — long-lived series from persistent services keep 2h in memory; short-lived serverless series keep only 30min. Matches observed serverless lifespan; cuts memory footprint while preserving correctness.
- **Three isolated StatefulSets per Receive group**: instead of one large hash ring, three replicas as three isolated StatefulSets. Preserves 3-way replication with quorum writes, but an entire StatefulSet can be rolled/restarted in parallel during releases or node rotations without breaking quorum or write availability.
- **Rule-based multitenancy**: the router infers the tenant per sample from metric name and selected labels, so one write batch can fan out to different tenants/Receive groups with no upstream client changes.
- **At-least-once uploads**: only 2 of 3 StatefulSets upload blocks to object storage — less redundant upload traffic and storage cost, with durability preserved via replication + quorum.

### Purpose-built control plane

Vanilla Thanos/Kubernetes automation was insufficient — every release, scale event, or host failure must preserve quorum automatically. Three controllers:

- **Rollout Operator**: coordinates releases/scaling across the three Receive StatefulSets, parallel StatefulSet updates, at most one replica unavailable at a time.
- **Hashring Controller**: only healthy, fully-ready pods enter the hashring; removals staged during scale-down/maintenance — traffic management decoupled from pod lifecycle, no accidental quorum violations.
- **Autoscaling/Self-Healing Controller**: scales on Pantheon-specific ingestion/resource pressure (not generic K8s signals); a healer remediates bad hosts, overloaded pods, corrupted WALs without operators — firing dozens of times per week.

## Aggregation: bending the cardinality curve

Cardinality — the number of unique label combinations per metric — is the primary TSDB scaling factor. A 10x pod-count increase means 10x cardinality for any metric carrying a pod-ID label. The fix: **drop expensive labels during ingestion while keeping an aggregated fleetwide view** ("bend the curve" so monitoring infra need not outgrow the rest of Databricks).

Stateful aggregation at scale is genuinely hard: aggregators holding millions of input counters must handle counter resets (a vanished input series must not make the aggregated output dip) plus pod restarts and load imbalance across partitioned aggregators. Kafka-based partitioning state is costly at this scale and adds ingestion delay; naive in-memory state with rerouting loses data on redeploy (their first version produced "almost unintelligible" aggregates). The working design uses **Telegraf plus Databricks' "auto-sharder" Dicer with intelligent sticky routing** instead of rerouting — scaled past **1 GB/s in the largest region with thousands of aggregation rules**. It proved itself during a real infra incident causing 2–5x metric surges: Telegraf absorbed the surge while Pantheon saw only +20%, with alerting/debugging unaffected.

## Hydra: high-cardinality troubleshooting on the lakehouse

Aggregation has a price: it deletes exactly the dimensions engineers need in incidents (aggregates say "region CPU elevated"; they can't say which tenant causes swap pressure, which node crashed, which shard is isolated). Pantheon fundamentally can't store that raw needle-in-haystack data — so the team built **Hydra** on the lakehouse, which decouples cheap object storage + Delta Lake from streaming/query compute: **20 billion unaggregated active timeseries from millions of nodes, 5-minute end-to-end freshness, 50x cheaper storage than Thanos**. Ingestion is Spark Structured Streaming (exactly-once) + Auto Loader for millions of arriving files, partitioned per region for independent autoscaling and blast-radius isolation.

The harder half was interface design, built around Critical User Journeys rather than storage internals:

- **Grafana/PromQL preserved**: a PromQL-to-SQL conversion layer runs existing dashboards unmodified against Delta tables.
- **Direct SQL access**: engineers query the same Delta tables from Databricks SQL/notebooks — joining metrics with deployment metadata and logs, wide time-range scans, anomaly detection. Observability data becomes a governed, first-class analytical asset instead of a silo.
- **Unified metric semantics**: teams emit once through one interface; the platform handles aggregation, raw preservation, routing. Engineers never learn which backend serves their query. The stated direction is converging Hydra's freshness with Pantheon's until the two experiences merge.

## Takeaways for the seminar

- **Split retention by series lifespan**: uniform retention overpays for the shortest-lived data — the 2h/30min Receive-group split is the single cheapest Pantheon win.
- **Isolate failure domains inside the replication scheme**: 3 StatefulSets × quorum gives rolling freedom a single hash ring cannot.
- **Shield before you scale**: aggregation absorbed a 5x surge into +20% TSDB load — cardinality control is a reliability mechanism, not just a cost one.
- **Keep the raw data somewhere cheap and meet users where they are**: Hydra's insight is that the drill-down path needs a different storage engine but the *same* query interface (PromQL-to-SQL), or engineers won't adopt it.

## Related concepts

- `concepts/data-engineering/lakehouse.md`, `concepts/data-engineering/stream-processing.md`, `concepts/infrastructure/kubernetes.md`
