---
title: "Cost-effective ETL with DuckDB and Amazon S3 Tables on AWS Glue"
description: "Run SQL-centric ETL with embedded DuckDB on Glue 6.0 writing Iceberg to S3 Tables at about half the time and cost of Spark."
tags: [source, aws-big-data, glue, duckdb, etl, iceberg, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/cost-effective-etl-with-duckdb-and-amazon-s3-tables-on-aws-glue"
blog: aws-big-data
published_date: 2026-10-06
---

# Cost-effective ETL with DuckDB and Amazon S3 Tables on AWS Glue

## Overview

Many integration jobs are SQL-centric — filter, join, aggregate on a schedule, running often enough that startup time matters. AWS Glue 6.0 can run DuckDB, an embedded in-process vectorized SQL engine, inside a standard `glueetl` job: DuckDB reads Parquet from S3 and writes Iceberg tables directly to S3 Tables via the REST catalog. This complements rather than replaces Spark on Glue — pick DuckDB per job for single-node SQL work, PySpark for distributed work, with identical infrastructure, IAM, and triggers.

## When to use it and how it runs

Reach for DuckDB when per-run data fits a single worker, parallelism needs are single-node, SQL is aggregations/joins/window functions, and minimizing per-run cost and duration matters; choose Spark for any-size horizontal scale, complex graphs, custom UDFs, or ML pipelines, and for native Spark Iceberg integration at scale.

Two things make it work. Glue 6.0 provides a modern runtime (Amazon Linux 2023, glibc 2.34, Python 3.13) where DuckDB 1.5.x and its native extensions install via `--additional-python-modules` or a virtual environment. DuckDB brings single-node vectorized execution with no shuffle or scheduler overhead, native S3/Parquet access through `httpfs` with the job role's credential chain, native Iceberg writes to S3 Tables, and larger-than-memory operators spilling to `/tmp`. Output is a standard Iceberg table queryable by Athena, Redshift, and EMR. Size the worker to the input: the walkthrough uses 2× G.1X (4 vCPU, 16 GB each), scaling to G.2X/G.4X/G.8X for bigger inputs.

## Walkthrough: daily order summary

Raw Parquet lands in S3 on a schedule; a Glue 6.0 job runs DuckDB SQL and commits an Iceberg snapshot to S3 Tables (queried by Athena/QuickSight, governed by Lake Formation), triggered by Glue triggers, EventBridge Scheduler, S3 events via Lambda, or Glue Workflows. The eCommerce example filters to completed/processing orders, derives revenue columns, aggregates daily revenue and order counts by day/region/category, and reloads per day idempotently (create-if-missing, delete the batch's date range, insert — noting delete+insert is not atomic, so keep `MaxRetries` at 1 or use a staging table).

- **Configure:** point DuckDB's home and extension directories at `/tmp` (the only writable path), load `httpfs`, `aws`, and `iceberg`, and create an S3 secret with the credential-chain provider — no keys in code. Requires DuckDB 1.4+ for Iceberg REST writes.
- **Transform:** `read_parquet()` over S3 glob patterns feeds a temp table with grouped aggregates (noting `GROUP BY ALL` is DuckDB-specific).
- **Write:** attach the table bucket as an Iceberg REST catalog, create schema/table if missing, delete-then-insert per day, and log the row count. The job needs scoped Lake Formation grants (`SELECT`/`INSERT`/`DELETE` on the table, `CREATE_TABLE` on the namespace) plus `lakeformation:GetDataAccess`.

## Measured results

On Glue 6.0 with 8.4M rows (~94 MB Parquet) at 2 DPU, DuckDB finished in ~56 seconds billed as 1 minute ($0.0103) versus Spark's ~117 seconds billed as 2 minutes ($0.0205) — about half the time and cost for identical 1,176-row output verified in Athena. At 20 runs/day that is roughly $75/year versus $150/year. Monitor with standard Glue CloudWatch metrics (driver heap pressure, bytes read) plus structured logging, since DuckDB internals are not exposed to CloudWatch.

## References

- Original post: [Cost-effective ETL with DuckDB and Amazon S3 Tables on AWS Glue](https://aws.amazon.com/blogs/big-data/cost-effective-etl-with-duckdb-and-amazon-s3-tables-on-aws-glue)
