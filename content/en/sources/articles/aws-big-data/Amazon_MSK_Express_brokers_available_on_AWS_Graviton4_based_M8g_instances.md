---
title: "Amazon MSK Express brokers available on AWS Graviton4-based M8g instances"
description: "Amazon MSK Express brokers on Graviton4 M8g instances cut broker-hour pricing 15%, drop broker-side cross-AZ client charges (50% lower cross-AZ transfer), add a 24xlarge size, and show 21–54% lower P99 produce latency and 9–11pp lower broker CPU in testing."
tags: [source, article, aws-big-data, kafka, msk, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/amazon-msk-express-brokers-available-on-aws-graviton4-based-m8g-instances"
blog: aws-big-data
published_date: 2026-11-19
---

# Amazon MSK Express brokers available on AWS Graviton4-based M8g instances

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/amazon-msk-express-brokers-available-on-aws-graviton4-based-m8g-instances)
**Published**: 2026-11-17

## Overview

Apache Kafka teams often trade performance against cost. Amazon MSK Express brokers are now available on AWS Graviton4-based M8g instances, promising both: 15% lower broker-hour pricing than Express brokers on M7g, no broker-side charge for cross-AZ client traffic (cutting total cross-AZ data transfer cost by 50%), and a new 24xlarge size for more headroom. In same-size, same-load testing, P99 produce latency was 21–54% lower on M8g, broker CPU was 9–11 percentage points lower, and consumers that fell behind cleared up to 3x more backlog in 30 minutes.

## Key points

- Express brokers on M8g keep everything M7g Express brokers support: same Kafka versions, authentication methods, custom configurations, CloudWatch metrics, and Open Monitoring with Prometheus.
- Throughput per broker, connection limits, and data-in/storage pricing are unchanged versus M7g at the same size, so you can move to M8g at your current size and keep per-broker throughput.
- Broker-hour pricing is 15% lower at each size (US East (N. Virginia): express.m8g.large $0.347/hr vs express.m7g.large $0.408/hr). Data-in and storage pricing do not change.
- Cross-AZ client traffic: AWS no longer charges the broker side, so cross-AZ traffic between clients and brokers costs $0.01/GB total instead of $0.02/GB — 50% lower. With rack awareness (replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector and client.rack set to the AZ ID), consumers read from local replicas and only produce-side cross-AZ traffic remains at $0.01/GB.
- Sizes range from express.m8g.large (2 vCPUs, 8 GiB, ~15.6/31.2 MBps in/out, 1,000 recommended / 1,500 max partitions) up to 24xlarge; M7g topped out at 16xlarge. Recommended partition and throughput limits apply per size.
- Example month: a three-large-broker cluster in us-east-1 with 30 MBps ingress and two consumer groups (~155,520 GB cross-AZ) costs $749.52 broker hours on M8g vs $881.28 on M7g, plus cross-AZ produce traffic $518.40 vs $1,036.80.
- For sizes available on both generations, storage and network throughput per broker are the same as M7g.

## Details

- Express brokers already offer up to 3x more throughput per broker, up to 20x faster scaling, and up to 90% faster recovery than Standard brokers, with storage and broker tuning managed for you.
- Benchmarks were run at the large size only; AWS recommends creating a test Express cluster on M8g and running your own workload, then deleting it to avoid ongoing charges.
- Express on M8g is offered in the following sizes with recommended ingress/egress throughput and partition counts per size (large through 24xlarge); check the AWS docs for the full table before sizing.
- Migration is moving the cluster to M8g at the same size; no application changes are required because Kafka versions, auth, and configs carry over.
