---
title: "Read, don't copy: replacing file feeds with OpenSharing - Part 2 (How to Implement)"
description: "A hands-on Databricks-to-Databricks walkthrough of sharing a Delta table WITH HISTORY and consuming it as a checkpointed Structured Streaming source."
tags: [source, databricks, data-engineering, opensharing, streaming, en]
locale: en
source_url: "https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement"
blog: databricks
published_date: 2026-11-08
---

# Read, don't copy: replacing file feeds with OpenSharing - Part 2 (How to Implement)

**Source**: [Databricks Blog](https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement) · **Published**: 2026-11-06

## Overview

The classic sharing pattern is a provider exporting a file on a schedule, landing it in a bucket or over SFTP, and a recipient detecting the new file, loading it, deduplicating it and tracking what it already processed, with updates and deletes needing extra conventions or reconciliation jobs. The article replaces that chain with a shared Delta table: a Delta table keeps an ordered history of every change, and OpenSharing exposes it over an open protocol without copying it, so the data stays in the provider's storage and the recipient reads it live.

On the recipient side the change is mainly bookkeeping moving into the engine. A Structured Streaming reader is pointed at the shared table, and Spark records how far it has read in a checkpoint, so each run picks up only the changes committed since the previous one. The recipient still controls its own target tables and downstream logic, but tracking what is new, over governed data with lineage and access control intact, becomes the engine's job rather than a custom file or timestamp convention.

The walkthrough uses Databricks-to-Databricks sharing: the recipient has a Unity Catalog enabled workspace and reads the shared table through a shared catalog, and the provider shares the table with its history so it can serve as a streaming source. The article then extends the pattern to recipients that are not on Databricks, which connect through OpenSharing with a credentials file rather than a metastore sharing identifier.

## Key points

- OpenSharing exposes a Delta table over an open protocol, so recipients read it live instead of ingesting scheduled file or API exports.
- Per-recipient export jobs, file detection and reconciliation disappear from the provider's side of the contract.
- A provider publishes the share WITH HISTORY; without history the recipient only ever sees a static snapshot.
- The recipient mounts the share as a catalog and reads it like any other table, using Structured Streaming with a durable checkpoint such as a Unity Catalog volume.
- Trigger.AvailableNow processes the unprocessed data in one or more micro-batches and stops, which suits scheduled incremental jobs; a table update trigger can instead fire the job only when the provider commits.
- Change Data Feed is optional for the basic incremental read but required when the recipient must propagate updates and deletes.
- On Databricks Runtime 19 and above, automatic Change Data Feed computes row-level changes at query time for tables with row tracking enabled and works with Databricks-to-Databricks OpenSharing.
- Databricks-to-Open recipients that do not run Spark cannot hold a continuous stream and instead pull changes by version range through the delta-sharing connector.

## Details

Provider setup is short. Create the source table with Change Data Feed enabled if updates and deletes matter, publish it in a share WITH HISTORY, register the recipient by its sharing identifier, and grant the share; the article notes that creating shares and recipients needs a metastore-level privilege, not just workspace admin. On the recipient side the share appears as a provider in the metastore, mounts as a catalog, and behaves like any other table.

The proof that the read is actually incremental comes from the target table's commit history. A first run over an initial set of rows writes them, and a second run after new rows land on the provider writes only the new ones, because the checkpoint recorded the last version read; the article shows a second streaming write of 200 rows where a naive reload would have written 1,200. It also flags a real limitation of the landing pattern: reading a shared table through Delta Sharing with ignoreChanges may re-emit rows and does not propagate deletes, so if downstream consumers need inserts, updates and deletes the recipient should read the shared table's Change Data Feed instead. The post adds that newer Databricks runtimes use skipChangeCommits when streaming directly from a regular Delta table.

Operationally the differences are what the article calls significant. Onboarding a customer no longer means standing up an SFTP endpoint or a new export job, only granting access to the share, and the provider maintains a single governed source table while recipients keep their own targets and business logic. Access is managed through the share, permissions on the shared Unity Catalog for Databricks-to-Databricks and the OpenSharing credential flow otherwise, backfills can read historical table versions instead of asking the provider to recreate old files, and responsibilities are split cleanly between the provider's data product and the recipient's downstream processing.

Non-Databricks recipients such as pandas, BI tools or Snowflake connect with a credentials file, and if they run open source Spark the same streaming read works through the delta-sharing connector. The article closes with a starting checklist, whether the recipient is Databricks-to-Databricks or Databricks-to-Open, whether it needs a snapshot, incremental reads or row-level change data, whether the share includes history, whether Change Data Feed is on, which runtime or connector version the recipient uses, how retries, duplicates, deletes and schema changes are handled, and who owns monitoring in production, plus the advice to validate the smallest end-to-end flow first: create the share, read a snapshot, then insert, update and delete a row and confirm the recipient sees the expected result.

## References

- Original article: [https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement](https://www.databricks.com/blog/read-dont-copy-replacing-file-feeds-opensharing-part-2-how-implement)
