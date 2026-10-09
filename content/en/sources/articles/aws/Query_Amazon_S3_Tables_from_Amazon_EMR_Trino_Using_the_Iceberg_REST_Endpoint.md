---
title: Query Amazon S3 Tables from Amazon EMR Trino Using the Iceberg REST Endpoint
description: Trino on EMR 7.11+ querying managed S3 Tables Iceberg storage via the Iceberg REST catalog — CloudFormation deploy, catalog config, and ACID interactive analytics.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, trino, emr, s3-tables]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/query-amazon-s3-tables-from-amazon-emr-trino-using-the-iceberg-rest-endpoint/"
blog: aws
---

# Query Amazon S3 Tables from Amazon EMR Trino Using the Iceberg REST Endpoint

**Authors**: Shubham Purwar, Anirudh Chawla, Nitin Kumar, Prashanthi Chinthala · **Published**: Sep 2, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/query-amazon-s3-tables-from-amazon-emr-trino-using-the-iceberg-rest-endpoint/)

## Problem

Data lakes on Amazon S3 backed by Apache Iceberg deliver open-format analytics, but teams operating them directly carry the undifferentiated work: file compaction, snapshot expiration, orphan-file cleanup, and metadata tracking — while still needing fast interactive SQL over large volumes.

## Solution: managed Iceberg storage + distributed SQL

- **Amazon S3 Tables** — purpose-built S3 capability with native Iceberg support; automates compaction, snapshot expiration, and metadata management. Exposes an Iceberg REST catalog endpoint (SigV4-authenticated).
- **Trino on Amazon EMR** (v475+, EMR 7.11+) — distributed ANSI-SQL engine for low-latency interactive queries across massive datasets.
- **Iceberg REST catalog spec** — standardized interface between engine and storage, so tables created here remain readable from Spark, Flink, or Dremio (no vendor lock-in).

Data flow: Trino CLI/JDBC → Iceberg connector fetches metadata via the S3 Tables REST endpoint → engine reads Parquet/ORC directly from S3 with partition pruning and predicate pushdown. Writes commit atomically through the REST endpoint.

## Implementation

1. **Deploy with CloudFormation** (`emr-trino-s3tables.yaml`, ~15 min): VPC + private subnet, S3 Tables interface VPC endpoint, EMR cluster with Trino, S3 Tables bucket, general-purpose S3 bucket, IAM roles, security groups. The template auto-generates the Trino catalog file and bootstrap script.
2. **Trino catalog** (`/etc/trino/conf/catalog/s3tables_irc.properties`):
   ```
   connector.name=iceberg
   iceberg.catalog.type=rest
   iceberg.rest-catalog.uri=https://s3tables.<REGION>.amazonaws.com/iceberg
   iceberg.rest-catalog.warehouse=arn:aws:s3tables:<REGION>:<ACCOUNT-ID>:bucket/<BUCKET-NAME>
   iceberg.rest-catalog.sigv4-enabled=true
   iceberg.rest-catalog.signing-name=s3tables
   iceberg.rest-catalog.view-endpoints-enabled=false
   fs.hadoop.enabled=false
   fs.native-s3.enabled=true
   s3.region=us-east-1
   s3.iam-role=arn:aws:iam::<ACCOUNT-ID>:role/service-role/<ROLE-NAME>
   ```
   One catalog per S3 table bucket (keyed by `iceberg.rest-catalog.warehouse`).
3. **EMR service-role trust**: allow `elasticmapreduce.amazonaws.com` and the EC2 instance profile to assume the role, so cluster nodes can reach S3 Tables with elevated permissions.
4. **Use it**: SSH to the primary node via Session Manager, `trino-cli --catalog s3tables_irc`, then `CREATE SCHEMA`, `CREATE TABLE ... WITH (format='PARQUET', sorted_by=ARRAY[...])`, `INSERT INTO ... SELECT`, and analytical `SELECT`s. Advanced Iceberg features work directly: time travel (`SELECT ... FOR VERSION AS OF <snapshot_id>`, snapshot listing via `"table$snapshots"`), schema evolution (`ADD COLUMN`, `RENAME COLUMN`).

## Why it matters

- **Operational simplicity**: no compaction schedules or snapshot lifecycle policies to manage.
- **Independent scaling**: compute (EMR, elastic) separated from storage (S3).
- **ACID + governance**: Iceberg transactions give atomic concurrent reads/writes; IAM plus Lake Formation covers table-/column-/row-level access.
- **Portability**: open table format + REST catalog keeps every engine choice open.

## Takeaways for the seminar

- Managed catalog + open format is the pairing that removes the classic "flexibility vs. toil" trade-off: Trino keeps query control, S3 Tables absorbs maintenance.
- The catalog properties that must be exact (`sigv4-enabled=true`, `signing-name=s3tables`, `view-endpoints-enabled=false`, native-S3 fs on / Hadoop fs off) are the integration's sharp edges — worth memorizing.

## Related concepts

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/data-engineering/stream-processing.md`
