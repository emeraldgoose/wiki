---
title: "Materialize once, query anywhere: Introducing Iceberg materialized views in Amazon Redshift"
description: "Redshift can now store materialized view results as open Iceberg tables, computed once and readable from Athena, Spark, and SageMaker with incremental refresh."
source_url: "https://aws.amazon.com/blogs/big-data/materialize-once-query-anywhere-introducing-iceberg-materialized-views-in-amazon-redshift"
blog: aws-big-data
locale: en
published_date: 2026-10-05
tags: [source, article, en, en]
---

# Materialize once, query anywhere: Introducing Iceberg materialized views in Amazon Redshift

## Overview

Amazon Redshift now supports creating materialized views stored as standard Apache Iceberg tables in S3, via `CREATE MATERIALIZED VIEW ... USING ICEBERG`. The expensive join or aggregation runs once on Redshift (Serverless or RG instances), and the result is an ordinary Iceberg table in the Glue Data Catalog that Athena, Spark on EMR, SageMaker, and Glue can read directly — no copies, no second transformation stack. Incremental refresh recomputes only changed partitions, and Lake Formation can govern sharing.

## When to use Iceberg MVs

Iceberg materialized views complement, not replace, native RMS materialized views. Use RMS views when only Redshift reads the result and you need the lowest latency for interactive dashboards. Use Iceberg MVs when the pre-computed result must be readable across engines, when standardizing on Iceberg for interoperability, or when running an end-to-end pipeline in one engine with shared open outputs. A common pattern layers both: Iceberg MVs for open-by-default sharing, RMS MVs on top for the hottest dashboards.

## How it works

Redshift tracks Iceberg snapshot IDs across refreshes and recomputes only deltas for eligible patterns (SUM/COUNT with GROUP BY, row-level deltas, inner joins between Iceberg tables); DISTINCT, outer joins, window functions, set operations, and MIN/MAX/AVG fall back to full refresh. The MV is not tied to its creating cluster — any authorized cluster or workgroup can refresh it, with concurrent refreshes coordinated through the Glue catalog. Supported on Serverless and RG (Graviton) instances; RA3 and DC2 are excluded.

## Setup sketch

Setup needs an IAM definer role trusted by both `redshift.amazonaws.com` and `glue.amazonaws.com`, scoped S3 and Glue inline policies plus PassRole, an S3 bucket, a Glue database with default permissive principals for cross-engine reads, and role association on the cluster. From there it is plain SQL: external schema, Iceberg base table, `CREATE MATERIALIZED VIEW ... USING ICEBERG`, then verification from Athena (`SELECT` on the catalog table) and PyIceberg/Spark readers. Optional Lake Formation layering adds table-level governance.

## References

- [Original post: Materialize once, query anywhere](https://aws.amazon.com/blogs/big-data/materialize-once-query-anywhere-introducing-iceberg-materialized-views-in-amazon-redshift)
- [Materialized views stored as Apache Iceberg tables (Redshift docs)](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-iceberg.html)
