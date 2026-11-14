---
title: "Migrating from Apache Hudi-based data lake to Apache Iceberg-based data lake"
description: "Convert Apache Hudi Copy-on-Write and Merge-on-Read tables to Apache Iceberg in place with the Spark add_files procedure or Apache XTable, or rewrite them fully with CTAS and CREATE + INSERT, from a Jupyter notebook on AWS Glue 5.1 interactive sessions."
tags: [source, aws-big-data, apache-iceberg, apache-hudi, data-lake, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/migrating-from-apache-hudi-based-data-lake-to-apache-iceberg-based-data-lake"
blog: aws-big-data
published_date: 2026-11-14
---

# Migrating from Apache Hudi-based data lake to Apache Iceberg-based data lake

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/migrating-from-apache-hudi-based-data-lake-to-apache-iceberg-based-data-lake) · **Published**: 2026-11-12

## Overview

Open table formats solved the classic data lake pain points on Amazon S3: Apache Hudi, Delta Lake, and Apache Iceberg add ACID transactions, row-level updates and deletes, snapshot history, and schema enforcement to files that analytics engines query directly. As architectures mature, organizations that built lakes on Apache Hudi increasingly evaluate Apache Iceberg, drawn by dynamic partition evolution without full data rewrites, hidden partitioning that decouples physical layout from query filters, an open REST Catalog protocol, and native integration with Amazon Athena, Amazon Redshift, Amazon EMR, AWS Glue, Amazon SageMaker, and Amazon Data Firehose.

This post walks through converting Apache Hudi tables to Apache Iceberg in a Jupyter notebook on AWS Glue 5.1 interactive sessions, covering both Hudi table types: Copy-on-Write (CoW), where an update or delete fully rewrites every base Parquet file containing an impacted row, and Merge-on-Read (MoR), where updates are appended to Avro log files and merged at read time. Two migration strategies are worked end to end: in-place migration, which generates fresh Iceberg metadata over the existing Parquet files without copying data, and full table (shadow) migration, which rewrites the data into a brand-new Iceberg table.

Every target table is registered in the AWS Glue Data Catalog, and Amazon Athena validates the migrated data. The post also details the operational guardrails that keep the source Hudi tables intact while both formats share the same data files.

## Key points

- Two approaches exist: in-place migration is fast and cheap because data is not rewritten, but the Iceberg table inherits the source schema, partitioning, and physical file shape; full table migration costs more compute and stores the dataset twice until cutover, but allows schema changes, Iceberg hidden partitioning, resorting for pruning, and larger target file sizes.
- In-place migration is demonstrated with two techniques: the Spark Iceberg add_files procedure and the Apache XTable (incubating) sync tool.
- add_files registers every Parquet file it finds under the source location with no awareness of Hudi file-group versioning, so the source must expose exactly one file version per record: CoW tables need Hudi CLEAN with the KEEP_LATEST_FILE_VERSIONS policy (file_versions_retained = 1), and MoR tables need COMPACTION plus CLEAN first because add_files cannot process delta log files.
- In the sample run, run_clean with KEEP_LATEST_FILE_VERSIONS deleted 3 stale files from the CoW events table in 382 milliseconds.
- XTable translates metadata between Hudi, Delta Lake, and Iceberg without copying data, supports one-time conversion and ongoing incremental sync, and runs anywhere a JVM is available, including Amazon ECS, Amazon EKS, or an AWS Lambda function triggered on a schedule through Amazon EventBridge. For MoR sources it reads only base Parquet files, so compact first; it needs no CLEAN because it builds Iceberg manifests from Hudi metadata and ignores superseded versions automatically.
- Full table migration uses a single CREATE TABLE AS SELECT statement or a CREATE + INSERT pattern that seeds the table with a small CTAS and then runs INSERT INTO ... SELECT partition by partition with checkpointing across batches. The process is identical for CoW and MoR because Spark reads the Hudi real-time view, which already merges pending delta logs.
- Known issue: in Iceberg 1.9.0 through 1.10.0, the add_files and snapshot procedures do not generate column statistics because of a NameMapping loss in ParquetUtil.footerMetrics, which degrades file-skipping at query planning time. The issue is fixed in Iceberg 1.10.1 (issue #14617); affected runtimes are AWS Glue 5.1 and Amazon EMR 7.11-7.13, and the authors recommend AWS Glue 6.0+ or Amazon EMR 7.14+ for production migrations.
- In-place migration leaves Iceberg pointing at the same Parquet files as Hudi: set the table property gc.enabled to false immediately after add_files and keep it off until full cutover; with XTable incremental sync GC must stay enabled, so operational discipline is required instead (no DROP TABLE ... PURGE, no expire_snapshots, no remove_orphan_files, no manual deletes on the shared prefix).
- Do not enable the AWS Glue Data Catalog table optimizer before cutover: Glue-managed compaction, snapshot retention, and orphan file cleanup would rewrite or delete Parquet files the Hudi table still depends on.
- The full-migration variant can target Amazon S3 Tables, which handle table maintenance such as compaction and snapshot management automatically; the notebook config uses glue_version 5.1, worker_type G.1X, 5 workers, and --datalake-formats hudi,iceberg.
- Cleanup drops the migrated Iceberg tables and namespaces, and S3 Tables resources are removed with DROP TABLE ... PURGE followed by DROP NAMESPACE.

## Details

### Preparing the Hudi sources

The notebook creates sample event tables in both flavors, performs inserts, updates, and deletes, and inspects the S3 layout with a list_table_files helper that renders an annotated directory tree. CoW keeps reads cheap while writes amplify with the fraction of files touched; MoR appends updates to Avro log files for cheaper writes but costlier reads until compaction. Before in-place registration, CLEAN keeps only the latest file slices so add_files cannot pick up superseded versions as duplicate rows.

### The add_files path

Create the target Iceberg table with the same schema and partitioning (the sample partitions by year, month, day), run the add_files procedure once per table, then validate by comparing row counts and sampled rows between the Hudi source and the Iceberg target in Athena. For the MoR table, run compaction first so delta logs merge into base Parquet, refresh the Hudi table to invalidate Spark cached metadata, and re-check the file listing after each step.

### The XTable path

XTable reads Hudi metadata and writes equivalent Iceberg metadata pointing at the same Parquet files. The initial run produces the full conversion; re-running the same command detects the previous execution and switches to incremental mode, keeping the Iceberg table in sync with ongoing Hudi writes while downstream consumers migrate. After all consumers are cut over, stop the sync and decommission Hudi.

### Full table migration and cutover

Shadow migration reads the Hudi real-time view and writes a brand-new Iceberg table with either CTAS or CREATE + INSERT, into a general purpose S3 bucket or Amazon S3 Tables. Because data is copied, storage doubles until the source is retired, but no compaction or cleanup of the Hudi source is required beforehand. After cutover completes, drop the migrated tables and namespaces to clean up and resume normal Iceberg maintenance.
