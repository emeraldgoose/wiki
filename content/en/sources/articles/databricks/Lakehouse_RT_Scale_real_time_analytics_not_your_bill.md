---
title: "Lakehouse//RT: Scale real-time analytics, not your bill"
description: "Why real-time bills explode when AI agents drive query volume, and how Lakehouse//RT holds latency with high concurrency, fast execution, fine-grained autoscaling, and no separate serving layer."
tags: [source, databricks, data-engineering, real-time-analytics, en]
locale: en
source_url: "https://www.databricks.com/blog/lakehousert-scale-real-time-analytics-not-your-bill"
blog: databricks
published_date: 2026-11-13
---

# Lakehouse//RT: Scale real-time analytics, not your bill

**Source**: [Databricks Blog](https://www.databricks.com/blog/lakehousert-scale-real-time-analytics-not-your-bill) · **Published**: 2026-11-12

## Overview

AI agents are breaking the assumptions data warehouses were built on. A human analyst runs a few dozen queries in an afternoon; an agent can run hundreds per second, around the clock. Add use cases that are becoming standard — customer-facing dashboards that refresh in milliseconds, applications with embedded analytics — and real-time query volume grows far faster than headcount ever did. Most warehouses were designed for human-scale traffic, and even where they can deliver low latency, the bill grows as fast as demand: ten times the queries can easily mean ten times the cost.

Lakehouse//RT is Databricks' answer: serve real-time workloads directly on the governed lakehouse while scaling efficiency instead of cost. Instead of adding capacity in step with demand and overprovisioning for spiky traffic, its engine is architected to serve dramatically more queries on the same resources. The article breaks the approach into four areas: high concurrency so more queries share the same resources, faster execution so each query holds compute for less time, autoscaling in small increments so capacity follows demand instead of jumping in whole-cluster steps, and one system instead of several so duplicate infrastructure disappears.

The customer numbers are the concrete payoff. Aurasell replaced several clusters serving 200 queries per second with one small Lakehouse//RT warehouse sustaining more than 250 QPS, running queries 4–5x faster at 10x lower cost. VisionHeight moved its pre-attack intelligence platform off Apache Pinot and always-on EC2 clusters onto Lakehouse//RT's serverless model, cutting costs by more than 90% with sub-second responses on its heaviest query and a three-day migration. nOps, which manages over $5 billion in annual cloud spend, replaced Apache Druid plus a separate cluster and 40TB of duplicated data, reducing infrastructure costs by more than 6x while eliminating the duplicate copy entirely. Lakehouse//RT is in beta, with a 30% discount through January 2027.

## Key points

- Concurrency is where real-time costs usually grow fastest: traditional warehouses queue excess queries or spin up more clusters, even when most queries are small lookups. Lakehouse//RT ran sub-100 millisecond latency at 12,000 queries per second in its launch benchmarks.
- Your bill is rate times runtime. Each query — including planning, routing, and returning results — holds compute for less time, and across millions of agent queries a day the difference compounds.
- Autoscaling comes in small increments, even one node at a time, so a 10% traffic burst no longer forces paying for a 100% cluster doubling the way traditional whole-cluster scaling does.
- One system replaces the bolt-on serving layer (Apache Druid, Apache Pinot, or a cache) with its always-on infrastructure, second copy of data, and sync pipelines; Lakehouse//RT queries governed lakehouse data directly.
- Aurasell: from several clusters at 200 QPS to one small warehouse above 250 QPS, queries 4–5x faster, costs down 10x.
- VisionHeight: more than 90% cost reduction after leaving Pinot, nearly 3x faster than Pinot on its heaviest query, migration completed in three days.
- nOps: more than 6x lower infrastructure costs with zero data copying, no new ingestion pipelines, and 40TB of duplicated storage removed.
- Customers report 6x to 10x lower total infrastructure costs versus running a separate real-time serving layer.
