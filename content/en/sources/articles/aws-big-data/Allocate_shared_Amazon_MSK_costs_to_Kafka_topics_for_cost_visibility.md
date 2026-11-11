---
title: "Allocate shared Amazon MSK costs to Kafka topics for cost visibility"
description: "A serverless pipeline that takes cluster-level Amazon MSK charges from the Cost and Usage Report and distributes them across Kafka topics by throughput, giving each team a usage-based share of the spend."
tags: [source, aws-big-data, kafka, msk, cost-allocation, cost-visibility, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility"
blog: aws-big-data
published_date: 2026-11-12
---

# Allocate shared Amazon MSK costs to Kafka topics for cost visibility

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility) · **Published**: 2026-11-11

## Overview

Amazon Managed Streaming for Apache Kafka (Amazon MSK) charges at the cluster level, with one cost line item per cluster. When one cluster serves several teams and each team owns its own Kafka topics, that line item says nothing about who uses what. This post shows how to combine cluster-level billing data from the AWS Cost and Usage Report (CUR) with per-topic throughput metrics to produce a usage-based picture of each team's share of the spend.

The core idea is proportional allocation. For each cluster and day, the pipeline computes each topic's share of ingress bytes and applies that share to the day's cluster cost, separately for broker compute and storage:

```
topic_run_cost = day_broker_cost × (topic_bytes / total_cluster_bytes)
topic_storage_cost = day_storage_cost × (topic_bytes / total_cluster_bytes)
```

The function assigns 30 percent of the cost to a topic that carries 30 percent of ingress, and allocations always sum to the day's total. During a partial outage, costs are distributed only among topics for which metrics are configured, and the `allocation_method` column records that behavior.

## Key points

- The pipeline is a five-step daily Lambda function: read cluster cost from CUR by cluster ARN and day, bridge cluster names to ARNs via ListClustersV2, read each topic's daily throughput, allocate proportionally, and publish the results as Parquet to S3 with a refreshed Athena table for visualization in Quick Sight.
- Bytes-in is the allocation weight and correlates well with broker compute and network cost, but it is a proxy with known limits: it cannot see retention, replication factor, compression, or consumer fan-out, so teams can swap in a different weight or a blended model.
- Idle topics get no row — if only 3 of 20 topics report traffic, those 3 absorb the full cost — and if no topic reports traffic for a cluster-day, the function falls back to an even split across all configured topics.
- Per-topic usage can be collected two ways, selected with one environment variable: Enhanced Monitoring (PER_TOPIC_PER_BROKER publishes metrics to CloudWatch) or Open Monitoring with Amazon Managed Service for Prometheus, which scrapes JMX metrics at no additional charge and keeps metric cost growth low as topic count grows.
- Topic discovery is tiered — a static topic map in an environment variable, the MSK ListTopics API, CloudWatch ListMetrics, or yesterday's allocation output — so the function works whether or not Enhanced Monitoring is enabled.
- Cost guidance: if monitoring costs stay below 5 percent of MSK spend, use Option A; above 10 percent, Option B repays its setup quickly, and Enhanced Monitoring can be enabled only on clusters where chargeback accuracy matters.
- The pipeline extends to multi-account setups: the central account reads the consolidated CUR, the Lambda assumes a read-only role in each member account to list clusters and read usage, and a single central Prometheus workspace receives remote-writes from every member account's scraper.
- Two triggers provide resilience: an S3 event notification fires when a new CUR Parquet file arrives, and an Amazon EventBridge rule runs daily at 06:00 UTC as a fallback if CUR delivery lags.

## Details

The solution requires an active Amazon MSK Provisioned cluster with topics carrying traffic — Amazon MSK Serverless is out of scope because it bills differently and does not expose per-topic BytesInPerSec — plus a CUR (or AWS Data Exports for CUR 2.0) delivering Parquet to S3 with resource IDs enabled, a Glue catalog table over the CUR data with correct partitioning, permissions to create Lambda functions, IAM roles, Athena tables, and Quick Sight resources, and Quick Sight Enterprise edition for SPICE datasets and row-level security.

The Lambda function is Python 3.11, 1 GB, with a 10-minute timeout and uses the AWS SDK for pandas layer for Parquet processing. It reads CUR through Athena with a query filtered on partition columns so Athena prunes whole partitions, filtering on `line_item_product_code = 'AmazonMSK'` and `line_item_resource_id LIKE 'arn:aws:kafka:%'`, reading two months because AWS can update CUR line items after the first delivery. Results are written as Snappy-compressed Parquet partitioned by billing period, with each run overwriting its billing-period file to prevent double-counting on CUR redeliveries. A reconciliation query compares allocated totals against billed cluster costs; an empty result means allocations reconcile.

For the reporting layer, an Athena data source is imported into a Quick Sight SPICE dataset with a detail table of cost by team, topic, and month, filter controls for cluster, topic, and time period, and row-level security against client_id so teams see only their own numbers. Owners are derived from topic naming conventions, with an explicit topic-to-team map available where conventions fail.

The pipeline itself is inexpensive — Lambda, Athena, S3, and EventBridge are negligible — but two items dominate: the metric source costs about $90 per month for Option A versus about $11 for Option B on the example cluster, and Quick Sight user licenses are frequently the largest cost, scaling with how many people get access. Financial data should be encrypted at rest with SSE-KMS and in transit with TLS, including the scraper's remote write and Athena connections, and for Option B, port 11001 should be restricted to the scraper's security group. Unallocated charges such as data transfer, tiered storage, and MSK Connect should be reported explicitly so finance has a complete picture.

## References

- Original article: [Allocate shared Amazon MSK costs to Kafka topics for cost visibility](https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility)