---
title: "Multi-statement transactions for Apache Iceberg tables in Amazon Redshift"
description: "Amazon Redshift now runs several DML statements against one Apache Iceberg table inside a single BEGIN … COMMIT and publishes the batch as one atomic Iceberg snapshot (Patch 206 and later), with rebase-based conflict resolution, stricter transaction rules, and measured latency and throughput gains."
tags: [source, aws-big-data, redshift, iceberg, transactions, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/multi-statement-transactions-for-apache-iceberg-tables-in-amazon-redshift"
blog: aws-big-data
published_date: 2026-11-14
---

# Multi-statement transactions for Apache Iceberg tables in Amazon Redshift

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/multi-statement-transactions-for-apache-iceberg-tables-in-amazon-redshift) · **Published**: 2026-11-13

## Overview

Data pipelines often change a table in several steps — upserting the day's sales, then removing canceled orders. Until now, each write to an Apache Iceberg table in Amazon Redshift committed on its own, one statement at a time: the state between statements was public, a failed step left the table half-updated with nothing to undo cleanly, and a job of N statements paid the catalog update N times. Redshift already supported creating Iceberg tables, writing with INSERT, modifying rows with DELETE, UPDATE, and MERGE, storing materialized views as Iceberg tables, and committing non-overlapping concurrent writes — but always per statement.

Multi-statement transactions change this. Several data manipulation language statements against one Iceberg table run inside a single BEGIN … COMMIT, and Amazon Redshift publishes the batch as one Iceberg snapshot with one catalog update. Readers in other sessions and engines see the table before the batch or after it, never in between; a failed or rolled-back transaction leaves nothing to undo. The feature is available in Amazon Redshift with Patch 206 and later and requires no new syntax.

The post walks through a retailer example in which a nightly job merges POS sales and deletes voided sales, wraps both steps plus data-quality audit queries in one transaction, and commits only when the checks pass — a session-scoped write-audit-publish pattern in plain SQL. It then documents what statements a transaction accepts, the guarantees for concurrent readers and writers, orphan file cleanup, and measured performance.

## Key points

- Several DML statements (INSERT, UPDATE, DELETE, MERGE) against one Iceberg table inside BEGIN … COMMIT publish as one snapshot at COMMIT; Iceberg DML is also accepted in multi-statement command strings and prepared statements, including through the Amazon Redshift JDBC driver.
- All writes in a transaction must go to the same Iceberg table; a write to a second Iceberg table, RMS or temporary table DML, COPY, UNLOAD, GRANT, REVOKE, ANALYZE, and other DDL are rejected, and an Iceberg write inside a stored procedure is rejected.
- A single Iceberg DDL statement inside BEGIN … COMMIT used to succeed and is now rejected — run Iceberg DDL as a standalone statement. This changes behavior for existing workloads.
- If you reference one physical table through two external schemas, or through an external schema and awsdatacatalog, it counts as two tables and a write through the second name is rejected; Redshift identifies a table by how you reference it.
- Reads of the table you are writing see your uncommitted changes when you use the same name; the first read of each Iceberg table fixes its version for the rest of the transaction (repeatable reads), while a table first read later can include other sessions' commits made after the transaction started.
- Conflict resolution applies to every multi-statement transaction: if another writer's changes don't overlap, Redshift rebases your transaction onto the latest table version and commits it as one snapshot without re-running statements; only a genuine conflict fails the COMMIT, and the application retries.
- Batching 25 small statements per commit reduced total run time by 14.77% for INSERT and 11.29% for DELETE versus per-statement commits; more than half the gain (9.20% and 6.21%) already arrives at 4 statements per commit.
- With one writer, transactions commit 1.18× as many statements as auto-commit; at 32 concurrent writers, auto-commit reaches 2.89× the single-writer rate while transactions reach 10.37× — 3.59 times as many committed statements.
- Batching doesn't help when each statement already does heavy data work; the saved commit time is too small to notice.
- Orphan files from uncommitted transactions: unreferenced file removal is enabled by default for Amazon S3 Tables buckets; for AWS Glue Data Catalog tables, enable the orphan file deletion table optimizer before you start using multi-statement transactions, because it only removes files created after enabling.

## Details

### What a transaction may contain

The allowed set is deliberately narrow. Reads of Iceberg, Redshift managed storage, and external tables across databases are allowed; INSERT, UPDATE, DELETE, and MERGE against one Iceberg table are allowed and publish as one snapshot at COMMIT; REFRESH MATERIALIZED VIEW on one Iceberg materialized view is allowed, with the view as the transaction's write target. Everything else is rejected: writes to a second Iceberg table, any RMS or temporary table DML, COPY, UNLOAD, GRANT, REVOKE, ANALYZE, other DDL, and DDL on Iceberg tables (CREATE TABLE, CREATE TABLE AS, ALTER TABLE, CREATE MATERIALIZED VIEW, DROP TABLE, DROP MATERIALIZED VIEW). A rejected statement fails and aborts the transaction, so nothing that ran before it is published. The nightly retailer job fits these rules: it reads the Iceberg tables pos_sales and pos_voids and writes only sales, and any staging-table cleanup happens after COMMIT.

### Three guarantees for readers and writers

Atomic publishing: other sessions and engines see none of the changes until COMMIT, then all of them in one snapshot. Read your own writes: reads of the table being written include uncommitted changes, as long as the same name is used. Repeatable reads of each table: the first read fixes that table's version for the rest of the transaction, and later reads return the same data even if other sessions commit meanwhile. Each table's version is fixed at its first read, not at transaction start — a store-details lookup issued after the sales merge can include another session's insert into the stores table. RMS tables follow their own snapshot, taken at the transaction's first statement and not coordinated with the Iceberg catalog.

### Performance measurements

Setup: an Iceberg table registered in the AWS Glue Data Catalog in the US East (N. Virginia) Region (us-east-1), written from a single Amazon Redshift provisioned cluster, one session per writer, failed commits rolled back and not counted. For latency, 500 small statements against one table: 25 statements per commit cut total run time by 14.77% for INSERT and 11.29% for DELETE, with more than half the gain at 4 statements per commit. The gain comes from paying one catalog commit per transaction instead of one per statement, plus less per-statement transaction overhead. For throughput, concurrent writers compared auto-commit single-statement INSERTs with transactions of four INSERTs, measured in committed statements per second normalized to a single auto-commit writer. The advantage grows with concurrency: catalog commits per second level off for both configurations, but each transaction commit carries four statements instead of one.

### Getting started and cleanup

Intermediate files from a transaction that doesn't commit become orphan files. S3 Tables handles unreferenced file removal by default for table buckets; Glue Data Catalog tables need the orphan file deletion table optimizer enabled, which only removes files created after you enable it. To adopt the feature, upgrade to Patch 206 or later; related resources cover Iceberg write support, concurrent write conflict resolution, Iceberg materialized views, and referencing Iceberg tables in Amazon Redshift.
