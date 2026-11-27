---
title: "Long-term Amazon Redshift observability with Datadog and Amazon S3 Tables"
description: "Amazon Redshift retains query history for only 7 days, losing audit and compliance data beyond that window. The system table integration with Amazon S3 Tables automatically and continuously delivers system table data as Apache Iceberg tables to Amazon S3, where you set the retention policy. AWS and Datadog collaborated to make this data actionable: Datadog Data Observability reads from S3 Tables to provide column-level lineage, query analysis spanning weeks and months, and data quality monitoring — without adding load to your warehouses. You own the S3 data, pay only for S3 Tables storage and requests, and can query it with Amazon Redshift, Athena, or any Iceberg-compatible engine. Together, Redshift + S3 Tables + Datadog replace the 7-day limit with persistent observability across months and years."
tags: [source, article, aws-big-data, datadog, observability, s3-tables, iceberg, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables"
arxiv_id: ""
authors: []
blog: aws-big-data
published_date: 2026-11-27
---
# Long-term Amazon Redshift observability with Datadog and Amazon S3 Tables

**Source**: [AWS](https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables) · **Published**: 2026-11-18
**Authors**: AWS Staff

## Overview

Amazon Redshift captures operational history across more than 25 system views, ranging from query execution details in SYS_QUERY_HISTORY and full query text in SYS_QUERY_TEXT to connection activity, user changes, workload management events, and resource consumption metrics. This detailed record forms a complete operations log for Amazon Redshift clusters and serverless workgroups. However, Redshift retains this data for only 7 days — after that window closes, the history is gone, taking with it the ability to audit past activity, investigate slow-moving regressions, or satisfy compliance requirements spanning months or years.

The system table integration with Amazon S3 Tables changes this fundamental limitation. When enabled, Amazon Redshift automatically and continuously delivers system table data as Apache Iceberg tables to Amazon S3 in the user's account. The user owns the data, sets the retention policy, and S3 Tables handles compaction and snapshot maintenance at no delivery charge. The exported data can be queried directly with Amazon Redshift, Amazon Athena, or any Iceberg-compatible engine.

AWS and Datadog collaborated to make this exported data actionable for observability. Datadog Data Observability reads the Amazon Redshift query history from S3 Tables and transforms it into column-level lineage, query analysis, and data quality monitoring. Critically, this eliminates the need for Datadog to run read-only SQL against each warehouse hourly, as the same history is available directly from S3 Tables. For AWS-managed Redshift metrics and logs, Amazon CloudWatch remains an alternative monitoring channel.

## Key points

- Redshift query history limited to 7 days; beyond that, audit and compliance data is lost.
- Amazon S3 Tables integration delivers Redshift system tables as Apache Iceberg tables continuously, with zero delivery charge.
- Users own the data, set retention policies, and S3 Tables manages compaction and snapshots.
- Exported data is queryable via Amazon Redshift, Athena, or any Iceberg-compatible engine.
- Datadog Data Observability reads from S3 Tables to provide column-level lineage spanning entire fleet, query analysis over weeks/months, and data quality alerts.
- This solution removes the need for hourly read-only SQL queries against each warehouse.
- For AWS-managed Redshift metrics and logs, Amazon CloudWatch remains an alternative.

## Details

The integration configuration grants Datadog read access to S3 Tables. Datadog then parses the query history into column-level lineage graphs, showing how tables flow from raw through staging to marts. Query analysis surfaces patterns that slow down or scan more data over weeks and months, not just the last 7 days. Data quality monitors identify anomalous queries, connection changes, and workload events. The solution supports lineage from other integrations (Apache Airflow, dbt, Tableau, Looker, Power BI) alongside Redshift, creating a unified asset graph.

To configure: grant Datadog read access to S3 Tables, then enable Data Observability to begin reading the query history. The query history time window is configurable, allowing analysis of weekly or monthly patterns across the entire Redshift footprint.

## References

- Blog: [Long-term Amazon Redshift observability with Datadog and Amazon S3 Tables](https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables)
