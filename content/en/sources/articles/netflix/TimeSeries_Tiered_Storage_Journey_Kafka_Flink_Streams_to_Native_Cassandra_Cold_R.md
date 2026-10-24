---
title: "TimeSeries Tiered Storage Journey: Kafka/Flink Streams to Native Cassandra Cold Reads"
description: "By Oleksii Tkachuk, Rajiv Shringi, Chris Lohfink, Abe Ratnofsky, Kartik Sathyanarayanan In an earlier post, we introduced the TimeSeries Abstraction, our high-throughput, low-latency platform designed to store and query..."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60"
blog: netflix
published_date: 2026-10-14
---

# TimeSeries Tiered Storage Journey: Kafka/Flink Streams to Native Cassandra Cold Reads

**Source**: [netflix](https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60) · **Published**: 2026-10-14

## Overview

By Oleksii Tkachuk, Rajiv Shringi, Chris Lohfink, Abe Ratnofsky, Kartik Sathyanarayanan In an earlier post, we introduced the TimeSeries Abstraction, our high-throughput, low-latency platform designed to store and query temporal event data at scale. It has since become the operational backbone for Netflix’s largest datasets, which now span multiple petabytes.

## Key points

- Solution 1: Uses Apache Kafka and Flink to stream data directly to S3
- Solution 2: Leverages Cassandra backups in S3 and pluggable Memtables to read data directly from S3
- Growing retention demands: Users often push for increasing data retention to serve a broader range of use cases, which in turn increases the storage costs.
- Escalating costs: Maintaining massive, dense clusters for infrequently accessed historical data is prohibitively expensive.
- Sparse historical access: Most queries target recent events, but older data must remain readily available for occasional audits and investigations.
- Operational strain: High storage density on hot nodes complicates scaling, deployment, and cluster stability.

## References

- Original article: [https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60](https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60)
