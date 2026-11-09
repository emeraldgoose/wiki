---
title: "Amazon Athena introduces system tables for query execution observability"
description: "Athena's new query_executions system table keeps per-query usage data in an Iceberg table on S3 Tables, so cost attribution, performance analysis and audit questions become ordinary SQL."
tags: [source, aws-big-data, data-engineering, observability, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability"
blog: aws-big-data
published_date: 2026-11-10
---

# Amazon Athena introduces system tables for query execution observability

**Source**: [Amazon Athena introduces system tables for query execution observability](https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability) · **Published**: 2026-11-09

## Overview

Teams running SQL on Amazon Athena have always been able to see individual queries, but not their workload as a whole. Questions such as which workgroup scans the most data, whether a query got slower than last week, or who touched a particular table last quarter had to be answered by joining the Athena API, CloudWatch metrics and CloudTrail logs by hand — building analytics pipelines in order to analyze analytics pipelines. Athena now ships system tables, and the first of them, `query_executions`, records one row for every query that completes across the account.

Enabling the feature takes a few console steps, after which usage data shows up within minutes of query completion for all current and future workgroups. Athena stores the records as Apache Iceberg tables on Amazon S3 Tables and manages the plumbing for you: schema definition, partitioning, compaction and snapshot maintenance. Because the format is open, the same data can be read from DuckDB, Amazon Redshift or any other Iceberg-compatible engine in addition to Athena itself.

Each row of `query_executions` carries query identification (execution ID, query string, submission time), context (workgroup, catalog, database, tables accessed), performance counters (total execution, planning and queue time), resource consumption (bytes scanned, DPU count for capacity-reservation queries) and the outcome (state and detailed error information). That per-query detail is what CloudWatch's aggregate metrics cannot express: it separates a harmless spike of user syntax errors from an actionable spike of system errors.

## Key points

- `query_executions` captures identification, workgroup and catalog context, timing, bytes scanned, DPU count and final state plus error details for every completed query.
- Setup is a one-time console flow under Administration → System tables → Configure; an optional AWS KMS key controls encryption (SSE-S3 otherwise) and Athena provisions a service-managed S3 table bucket for the records.
- Because the table is registered in the AWS Glue Data Catalog, an MCP-compatible agent such as Kiro or Claude Code can be pointed at it through the AWS MCP Server; AWS's open-source Agent Skill for Athena system tables supplies schemas, example queries and partition-pruning conventions, and can be scoped to read-only IAM permissions.
- The post's query library covers usage patterns (daily and weekly volume, distinct users, scan-size histograms), cost attribution per workgroup or user, performance regressions (week-over-week average and p95 execution time, queue-time outliers) and the top data-scanning queries.
- Audit and operational use cases are covered too: replaying one principal's query history, finding every query that touched a given database and table, splitting failed queries into system versus user errors, and trending DPU-hours consumed by Capacity Reservations.
- Records are immutable — only the Athena service can write to the table, so no IAM principal can alter or delete individual rows — while retention, access policies and encryption keys stay under customer control.

## Details

Retention has no default: Athena keeps records until record expiration is configured on the S3 Tables side, with a minimum of one day and no upper bound. Data arrives in batches, typically within a few minutes, and the service partitions the table for efficient scanning; `DESCRIBE` lists the partition columns. Turning the feature on is: choose System tables under Administration in the left navigation, choose Configure, enable system tables for current and future resources, optionally pick a KMS key, then save. From then on the table is queryable like any other from the query editor, the API and SDKs, and the JDBC/ODBC drivers.

The example queries in the post are grouped by intent. Workgroup spend is derived by summing `data_scanned_size` per `work_group_name` and dividing by the per-TB price (obtainable programmatically from the AWS Price List API), and swapping the group-by column to `principal_arn` breaks the same report down per user. Performance analysis compares this week's and last week's query counts, average duration and p95 latency per workgroup, and flags workgroups whose average queue time exceeds a threshold. The largest cost drivers are found by ordering queries by bytes scanned, which points at candidates for partitioning, predicate pushdown or format changes. For attribution of a specific table, the query unnests the `tables_accessed` array and filters on database and table name.

Operational monitoring uses the `error_category_enum` column to separate engine-side failures from user syntax errors, and follows up by grouping failures by error message — for instance queries that exhausted resources, which are candidates for partitioning improvements, rewrites or more capacity. The `dpu_count` column is populated only for queries that ran on a capacity reservation, so a weekly sum of `dpu_count × execution duration` yields the reservation's DPU-hours and shows whether it is sized correctly. Finally, because the table is plain Iceberg in the customer's own account, Amazon Quick Sight or another BI tool can be pointed straight at it, removing the custom pipelines previously needed for these reports.

## References

- Original article: [Amazon Athena introduces system tables for query execution observability](https://aws.amazon.com/blogs/big-data/amazon-athena-introduces-system-tables-for-query-execution-observability)
