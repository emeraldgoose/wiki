---
title: "dbt and Amazon Redshift Data Sharing: Multi-cluster pipelines without moving a byte"
description: "Today’s global, data-driven organizations treat data as an asset and use it across different lines of businesses (LOBs) to drive timely insights and better business decisions."
tags: [source, aws-big-data, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte"
blog: aws-big-data
published_date: 2026-10-15
---

# dbt and Amazon Redshift Data Sharing: Multi-cluster pipelines without moving a byte

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte) · **Published**: 2026-10-15

## Overview

Today’s global, data-driven organizations treat data as an asset and use it across different lines of businesses (LOBs) to drive timely insights and better business decisions. This requires them to share and consume live, consistent data as a single source of truth without copying the data, regardless of where LOB users are located. With Amazon Redshift, a fast, scalable, secure, and fully managed data warehouse, you can analyze your data using standard SQL. As organizations scale, they often deploy multiple Amazon Redshift clusters to isolate workloads, manage costs independently across teams, or meet data residency requirements across Regions. However, this multi-cluster approach traditionally required complex extract, transform, and load (ETL) pipelines to copy data between clusters, in

## Key points

- Source objects are loaded from the Amazon Simple Storage Service (Amazon S3) data lake.
- AWS Glue or the Amazon Redshift COPY command ingests them into the producer cluster.
- The producer shares the schema through a datashare (zero-copy, live data).
- dbt Cloud connects over JDBC (5439) through an AWS PrivateLink endpoint.
- dbt reads source models from the datashare database and materializes transformed models in the consumer cluster.
- Amazon Quick Sight queries the transformed models.

## References

- Original article: [https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte](https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte)
