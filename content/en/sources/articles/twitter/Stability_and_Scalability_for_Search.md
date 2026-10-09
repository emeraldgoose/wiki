---
title: Stability and Scalability for Search
description: Proxy, Kafka-backed Ingestion Service, and Backfill Service that keep Twitter's Elasticsearch platform stable under traffic spikes
tags: [source, twitter, x, search, elasticsearch, kafka, scalability, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/stability-and-scalability-for-search"
blog: twitter
date: '2022-10-14'
---

# Stability and Scalability for Search

## Summary

Twitter's Search Infrastructure team runs search-as-a-service: real-time search over Tweets, Users, Direct Messages, and more, on **Open Distro for Elasticsearch**, exposing the full Elasticsearch API plus plugins for privacy, security, and Twitter-service integration. Operating at Twitter scale pushed Elasticsearch past its breaking point in three ways, each fixed with a dedicated guardrail: a **reverse proxy**, a Kafka-backed **Ingestion Service**, and a **Backfill Service**.

## Problem 1: Connectivity Bottleneck → Reverse Proxy

Customers talked directly to Elasticsearch for queries, indexing, monitoring, and metrics. Under normal load this was fine, but ingestion-heavy traffic could take down a whole cluster — there was no place to route, throttle, or observe centrally. The fix: a simple HTTP reverse proxy separating read and write traffic, handling all client authentication, fronting the Ingestion Service for writes, and creating one entry point with per-request-type metrics (success rate, read/write volume, cluster health) plus flexible routing and throttling — transparent to customers.

## Problem 2: Traffic Spikes → Ingestion Service

Public-conversation traffic spikes are sudden and enormous; stock Elasticsearch leaves queuing, retry, and backoff to the client, with no auto-throttling — so spikes drove indexing/query latency up and occasionally destroyed indexes entirely. The Ingestion Service smooths writes: client requests queue into **one Kafka topic per Elasticsearch cluster**, workers consume and forward them, applying **batching, backpressure response, auto-throttling, and retry with backoff**. Spikes are absorbed by Kafka instead of the cluster, at the cost of only modest ingestion latency.

## Problem 3: Preloading Data → Backfill Service

Backfills (bootstrapping an empty cluster, schema changes, post-outage gaps) move terabytes and billions of documents — far above normal ingestion throughput. The old path (a Scalding sink opening one HTTP client per Hadoop reducer, unthrottled) routinely degraded live query performance or killed clusters, with failures surfacing late and no safe resume. The Backfill Service splits the job: a **sink** (same entry point as the old Scalding code for easy migration) converts streams to index requests, partitions them into **temporary storage**, and calls the **orchestrator**, which launches a dynamic pool of **workers** that read staged requests and index with rate-limiting, backpressure response, and per-document retry inside bulk requests. Wins: resume without re-running data-prep jobs, no live-cluster collateral damage, and one backfill spanning all data centers at once.

## Results

Together the three guardrails ended the era of spike- and backfill-induced index loss: uptime is maintained, crashes prevented, and product teams scale search usage self-service.

## Relevance to SW Engineers

- Never let unbounded clients talk directly to a stateful store at scale: interpose a proxy for auth, throttling, and per-tenant metrics.
- Put a durable queue (Kafka) between bursty producers and a store with no native backpressure; batch + throttle + retry-with-backoff at the workers.
- Split bulk-load into *stage* (durable, partitionable, resumable) and *apply* (adaptive worker pool with backpressure) phases — backfills are a distinct workload from steady-state ingestion and deserve their own service.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/stability-and-scalability-for-search (Shelby Cohen, Jesse Akes, 14 Oct 2022)
- Related: `concepts/data-engineering/apache-kafka.md`, `concepts/data-engineering/stream-processing.md`
