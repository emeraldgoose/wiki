---
title: Razor Group's Journey to a Modern Data Lakehouse on AWS
description: How Razor Group migrated from always-on Redshift clusters to an open Iceberg lakehouse on S3 Tables in five phases — 65% faster P95, 63% lower infra cost.
date: 2026-08-28
tags: [aws, data-engineering, lakehouse, apache-iceberg, redshift, spark, s3-tables]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/razor-groups-journey-to-a-modern-data-lakehouse-on-aws/"
blog: aws
---

# Razor Group's Journey to a Modern Data Lakehouse on AWS

**Authors**: Yaswanth Kothainti, et al. · **Published**: Aug 28, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/razor-groups-journey-to-a-modern-data-lakehouse-on-aws/)

## The business challenge

Razor Group (an e-commerce aggregator) runs its "Razor Operating System" on signal sources such as the Amazon Selling Partner API, Shopify, NetSuite, Walmart, and Target, ingested through AWS Lambda and Amazon MSK, staged in Amazon S3 and DynamoDB, and modeled in Amazon Redshift. Hypergrowth exposed three structural problems:

- **Workload contention**: 1,000+ SQL models for ETL, transformation, and analytics competed for the same Redshift cluster compute, causing resource contention during peak windows.
- **Always-on cost**: provisioned clusters billed 24/7 regardless of utilization.
- **Single-engine lock-in**: every workload — heavy ETL, ad-hoc exploration, BI dashboards — had to fit one engine.

## Why a lakehouse

The answer was an open lakehouse: store data once in Apache Iceberg format on Amazon S3 Tables and let each workload pick its engine.

- **Open table format**: Iceberg provides ACID transactions, time travel, schema and partition evolution. One copy of data is accessible from any compatible engine without duplication.
- **Elastic per-workload scaling**: with data persisted on S3, each engine spins up for peak processing and scales to zero when idle — no over-provisioned shared infrastructure.
- **Managed storage**: S3 Tables handles compaction, snapshot expiration, and orphan-file cleanup automatically.

## Solution architecture

| Layer | Choice |
|---|---|
| Ingestion | AWS Lambda (event-driven) + Amazon MSK |
| Storage | Bronze / Silver / Gold Iceberg tables on S3 Tables |
| Governance | AWS Glue Data Catalog (unified metadata) + AWS Lake Formation (column/row-level security) |
| Compute (ETL) | Apache Spark Connect on EC2 (Graviton leader on-demand, Spot workers ≈ 70% cheaper) behind an internal NLB |
| Compute (ad-hoc) | Amazon Athena (serverless SQL) |
| Compute (BI) | Amazon Redshift Serverless (auto-scale/pause) |
| Orchestration | Apache Airflow — 9,300+ pipelines with dependency tracking and SLA monitoring |
| Observability | Cost attribution per workload, pipeline health, data quality checks |

Note: when the architecture was designed, Redshift lacked Iceberg write support, so self-managed Spark was the only viable ingestion path. That constraint has since been removed (Redshift now supports Iceberg UPDATE/DELETE/MERGE and CREATE/INSERT).

## Five-phase migration (no big-bang)

1. **Lakehouse foundation** — S3 Tables buckets, Glue Data Catalog, Lake Formation policies; deploy the Spark Connect cluster.
2. **Bronze ingestion** — migrate pipelines to Lambda functions orchestrated by Airflow, writing raw data directly to Iceberg; shift from schedule-driven to event-driven for better freshness.
3. **Silver/gold transformation** — the hardest phase: migrate 1,000+ SQL models from Redshift to Spark incrementally up the dependency chain across 40+ schemas.
4. **Unify serving** — end users query Gold Iceberg tables via Redshift Serverless; exploration and ML read the same tables via Spark Connect.
5. **Cutover and validation** — parallel run of old and new stacks with output comparison before decommissioning.

## Results

| Metric | Before | After |
|---|---|---|
| P95 query runtime | 180 s | 63 s (**65% faster**) |
| Infrastructure cost | always-on cluster + managed storage | EC2 (Spot/on-demand) + Lambda + Glue + Athena + Redshift Serverless + S3 Tables (**63% reduction**) |
| Concurrent capacity | limited by cluster size | elastic, independent per-engine scaling |
| Engine flexibility | single engine | Spark / Athena / Redshift on one open copy |

Cost comparison covers Redshift cluster compute + managed storage before, versus EC2 workers, Lambda, Glue, Athena, Redshift Serverless, and S3 Tables storage after.

## Takeaways for the seminar

- **Store once, compute many**: an open format decouples storage from engines, so each workload gets the cheapest engine that fits.
- **Observability must include cost attribution** — without per-workload cost visibility, optimization is guesswork. Razor Group found Iceberg snapshot maintenance alone consumed 35+ hours of compute weekly until observability surfaced it and automation fixed it.
- **Incremental migration beats big-bang**: each phase delivered standalone value (freshness first, then models, then serving) while de-risking cutover.

## Related concepts

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/data-engineering/stream-processing.md`
