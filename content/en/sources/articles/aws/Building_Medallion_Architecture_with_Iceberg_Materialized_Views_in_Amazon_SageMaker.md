---
title: Building Medallion Architecture with Iceberg Materialized Views in Amazon SageMaker
description: Bronze to Silver to Gold medallion pipeline expressed as three Iceberg materialized view SQL statements — no DAGs, no CDC plumbing — with incremental refresh and nested views.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, medallion, materialized-views, sagemaker, s3-tables]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/building-medallion-architecture-with-iceberg-materialized-views-in-amazon-sagemaker/"
blog: aws
---

# Building Medallion Architecture with Iceberg Materialized Views in Amazon SageMaker

**Published**: Sep 2, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/building-medallion-architecture-with-iceberg-materialized-views-in-amazon-sagemaker/)

## Problem

A classic medallion (Bronze → Silver → Gold) pipeline is three systems, not one: ETL jobs per layer transition, an orchestrator (Airflow, Step Functions) sequencing them, and hand-rolled CDC (watermarks, snapshot diffs, change streams) so each job processes only new rows. Every piece is authored, tested, deployed, and maintained separately — and one failure stalls the chain.

## Declarative alternative

With Apache Iceberg materialized views in Amazon SageMaker, transformation + orchestration + incremental processing collapse into **one SQL definition per layer**. You declare what each layer contains (`CREATE MATERIALIZED VIEW ... SCHEDULE REFRESH EVERY 1 DAY AS SELECT ...`); managed Spark compute (AWS Glue) executes the refresh, and Iceberg's row-level change tracking (position/equality deletes) restricts each refresh to changed rows. The full Bronze → Silver → Gold pipeline in the post is three SQL statements, built in under 2 minutes. Supported engines: Athena Spark, Glue 5.1+, EMR 7.12+.

## How it works

- **Bronze** (`trips_bronze` on S3 Tables): raw ride-sharing trips ingested as-is (INSERT/append), preserving original format for audit and replay.
- **Silver** (`mv_trips_silver`): null filtering, string→timestamp casts, derived columns (`revenue_per_mile`, `rating_category`). Definition only — data flows at refresh time.
- **Gold** (nested MVs on Silver): `mv_city_daily_metrics` (city × date: trips, drivers, revenue, tips) and `mv_vehicle_performance` (vehicle type × city), each on a daily schedule. A materialized view built on another materialized view; Gold reads incrementally from Silver.
- **Propagation demo**: INSERT new Bronze rows → `REFRESH MATERIALIZED VIEW` Silver (only 3 new records processed) → refresh Gold (cascading, incremental). MERGE-based UPDATEs propagate the same way.
- **Storage**: S3 Tables (managed Iceberg) + Glue Data Catalog; authored in SageMaker Unified Studio notebooks (Athena Spark or Glue Spark runtime), optionally with the SageMaker Data Agent generating SQL from natural language.

## Limitations (stated explicitly)

1. Minimum schedule granularity is **1 hour** — no sub-hour freshness.
2. **Cascading refresh is not automatic** — refreshing Silver does not trigger Gold; refresh sequentially or on separate schedules.
3. **Deletes need `REFRESH ... FULL`** — incremental refresh detects inserts/updates via Iceberg metadata, not row removals.
4. SQL subset only (some window functions, UDFs, complex expressions unsupported).
5. Source schema changes affecting the view definition require drop + recreate.
6. **AWS-specific extension** — not part of open-source Iceberg; not portable off AWS.

## Pricing

Scheduled auto-refresh bills at ~$0.44 per DPU-hour (4 vCPU/16 GB, per-second, 1-min minimum) on managed Spark; manual refreshes bill under the invoking service (Athena/EMR/Glue). MV data lives as Iceberg files in S3 Tables/S3 at standard storage rates. The tutorial's 300-record run costs <0.5 DPU-hour (~$0.22).

## Takeaways for the seminar

- The conceptual move is from **imperative pipelines to declarative data**: maintain the SQL, let the platform own scheduling, CDC, and incremental compute.
- The honest boundary (hourly floor, manual cascade, FULL refresh for deletes, AWS-only) defines exactly where this pattern fits — curated batch marts — and where it does not: sub-hour SLAs or portable open-source stacks.

## Related concepts

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/ai-engineering/feature-store.md`
