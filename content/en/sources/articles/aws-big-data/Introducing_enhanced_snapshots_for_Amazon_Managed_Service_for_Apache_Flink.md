---
title: "Introducing enhanced snapshots for Amazon Managed Service for Apache Flink"
description: "Enhanced snapshots make an Apache Flink application's state a first-class AWS resource: restore one application from another's snapshot, export/import via S3, and enable blue/green deploys, cross-Region disaster recovery, and stateful migration."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink"
blog: aws-big-data
published_date: "2026-11-19"
---

# Introducing enhanced snapshots for Amazon Managed Service for Apache Flink

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink) · **Published**: 2026-11-16

## Overview

An Apache Flink application that runs aggregations, joins, or windows builds up state as it processes events, and Amazon Managed Service for Apache Flink saves that state in snapshots. Until now a snapshot belonged to the application that created it — restorable only into the same application, in the same Region. Enhanced snapshots, now generally available, are AWS resources with their own ARNs, decoupled from the creating application: you can start a *different* application from one in the same account and Region, export it to an S3 bucket you own, and import a Flink savepoint from S3 as a new enhanced snapshot to start an application from.

With enhanced snapshots you can deploy updates to a stateful application without a long processing pause, recover in a second Region, and move a self-managed Flink job to the managed service together with its state. Enhanced snapshots work with applications on Apache Flink 1.20 and later.

## Key points

- **Blue/green deployments for stateful apps**: take an enhanced snapshot of the running "blue" app, start "green" (new code) from that snapshot — it begins with blue's state and processes only events written since the snapshot. When green catches up, cut downstream consumers over and stop blue; if green fails, blue is still running. Caveats: while both run you pay for both compute; green reprocesses events since the snapshot so its output overlaps blue's; downstream must tolerate or deduplicate duplicates (no exactly-once across the switch). Also usable for A/B testing against production state or cloning state to reproduce a bug.
- **Disaster recovery in a second Region**: export snapshots on a schedule to a bucket in the primary Region, replicate it to the standby Region with S3 Cross-Region Replication, and on failover import the latest replicated snapshot in the standby Region and start the standby app from it. Export frequency trades cost (operations + S3 storage/replication) against recovery point objective; pick the interval from your RTO.
- **Migrate a self-managed Flink job with its state**: take a savepoint on your self-managed cluster, copy it to S3 in the target account/Region, import it as an enhanced snapshot, start the managed application from it — the app resumes from the savepoint's offsets and processes only newer data instead of replaying history. Import validates the savepoint first (source objects must meet documented requirements, including a full-object CRC-64/NVME checksum). Operator IDs (UIDs) and state types must match; the snapshot must come from a supported Flink version. An imported snapshot has no source application, so it does not appear in per-application snapshot listings — track them via ListSnapshots with SnapshotInitiatorOperation=ImportSnapshot.
- **Turning it on**: for new apps set `SnapshotMode: ENHANCED_SNAPSHOTS` in `ApplicationSnapshotConfiguration`; an existing running app can be switched in place while keeping its state (`update-application` with `SnapshotModeUpdate`). `RollbackApplication` undoes the switch only before the next update; once switched, `CreateApplicationSnapshot` errors — move snapshot scripts to `CreateSnapshot`. Take an enhanced snapshot right after switching.
- **Restoring**: `create-snapshot` is asynchronous (poll `describe-snapshot` until READY; response returns SnapshotArn). Start the target app with `ApplicationRestoreConfiguration` using `RESTORE_FROM_CUSTOM_SNAPSHOT` and pass `SnapshotArn` (vs. `SnapshotName` for classic application snapshots). The restoring app's operator UIDs, state types, and maxParallelism must be compatible, and it must run a compatible Flink version. Enhanced snapshots persist until deleted with `DeleteSnapshot`, even after the creating app is deleted.
- **Export/import permissions**: export and import use an IAM role passed in the request; the service assumes it, so S3 permissions belong on the role, not the caller. The role's trust policy allows `kinesisanalytics.amazonaws.com` scoped with `aws:SourceAccount`/`aws:SourceArn`. The bucket must be in the same account and Region as the snapshot. End `KeyPrefix` with a slash; each export writes a new folder reported as `ExportedPrefix` — point import at that exact folder, not the parent prefix. Customer-managed KMS keys are supported for destination encryption.

## Details

The three use cases reduce to one concept: application state as a reusable AWS resource. Blue/green eliminates the long outage and full-history reprocessing of classic stop/restart deploys of stateful Flink jobs. Cross-Region DR removes the need to start empty and rebuild state from the source during a regional failure. Migration with state removes the painful "start empty and replay everything" cutover when adopting the managed service.

Mechanically it is a handful of API calls plus one app setting: enable the snapshot mode, `create-snapshot` (or export/import for cross-Region/migration flows), then start the new app with `RESTORE_FROM_CUSTOM_SNAPSHOT` + `SnapshotArn`. AWS CLI examples in the post cover `update-application`, `create-snapshot`, `describe-snapshot`, `start-application`, `export-snapshot`, and `import-snapshot`. An Agent Skill at the end of the post gives coding agents the same guidance. See Enhanced snapshots in the Managed Service for Apache Flink Developer Guide for the full reference, including import prerequisites and the complete trust/permissions policies for the export and import roles.

## References

- Original article: [Introducing enhanced snapshots for Amazon Managed Service for Apache Flink](https://aws.amazon.com/blogs/big-data/introducing-enhanced-snapshots-for-amazon-managed-service-for-apache-flink)
