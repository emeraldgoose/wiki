---
title: "Optimizing Apache HBase availability on Amazon EMR, Part 2: Diagnose and tune compaction"
description: "Diagnose HBase compaction pressure on Amazon EMR with a decision flow, web UI checks, logs, and the canary tool, then tune throughput bounds, off-peak windows, the S3A read policy, and major compaction scheduling before escalating to AWS Support."
tags: [source, aws-big-data, apache-hbase, amazon-emr, compaction, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/optimizing-apache-hbase-availability-on-amazon-emr-part-2-diagnose-and-tune-compaction"
blog: aws-big-data
published_date: 2026-11-14
---

# Optimizing Apache HBase availability on Amazon EMR, Part 2: Diagnose and tune compaction

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/optimizing-apache-hbase-availability-on-amazon-emr-part-2-diagnose-and-tune-compaction) · **Published**: 2026-11-11

## Overview

Compaction is the Apache HBase background process that merges store files, and when it competes with your workload during peak hours you see higher read and write latency, write stalls, and RegionTooBusyException errors. On Amazon EMR with Amazon S3 storage, compaction also raises the cluster's S3 request rate, which shows up as more 503 Slow Down responses. This second post in a two-part series shifts from availability to performance: Part 1 covered the three-level troubleshooting model plus coordinator startup, RegionServer stops, and regions in transition, while this part covers how to confirm compaction is the cause, which parameters to tune first, and when to contact AWS Support.

Before touching any parameter, the post prescribes a decision flow. If latency is high, check whether compaction is even running on the affected RegionServer; if not, investigate garbage collection, disk, and network instead. If compaction is running and the queue is growing, work through the S3A read policy, throughput bounds, compaction frequency parameters, off-peak hours, and finally manual major compaction scheduling.

Terminology matters for the commands: Amazon EMR runs the HMaster on the primary node, and the post calls it the HBase coordinator, reserving names containing master for commands and log files. The HBase web UI listens on port 16010 for the coordinator and 16030 for the RegionServer, and SSH access to primary and core nodes is a prerequisite along with knowing whether the cluster uses HDFS or Amazon S3 storage.

## Key points

- By default, HBase runs a major compaction roughly every seven days (604800000 ms) and uses a jitter factor of 0.5 to spread start times so regions do not all compact at once; major compaction reads and rewrites all store files in a region, improving reads and removing deleted and expired cells but competing with client requests.
- Write stalls follow a chain: when a store reaches hbase.hstore.blockingStoreFiles files, HBase delays MemStore flushes for up to hbase.hstore.blockingWaitTime (90 seconds by default); if the MemStore exceeds hbase.hregion.memstore.flush.size multiplied by hbase.hregion.memstore.block.multiplier, HBase blocks updates to the region.
- On HBase on Amazon S3, compaction reads and rewrites store files in S3, so a high request rate triggers more 503 Slow Down responses asking the cluster to slow down.
- Level 1 diagnosis in the web UI: sort RegionServers by request count and store file count, check the compaction queue length and store file count per region, and watch the BlockCache hit rate, because a cache miss on HBase on S3 reads from Amazon S3 with higher latency than a local read.
- Level 2 diagnosis: grep RegionServer logs for Starting compaction, Completed compaction, and too many store files; rule out GC with JvmPauseMonitor entries; check memory, CPU, and disk with free, top, and df; and run the canary tool (sudo -u hbase hbase canary my_table) to establish a per-region read latency baseline in /var/log/hbase/hbase.log.
- On Amazon EMR 7.10 to 7.13 with HBase on Amazon S3, set fs.s3a.experimental.input.fadvise to sequential in the hbase-site classification before tuning any compaction parameter: starting with EMR 7.10 the S3A client defaults to normal, which can switch to a random read policy and slow compactions, scans, and bulk loads. The change requires an HBase restart, making it a Level 3 action, and setting it on individual commands does not help.
- Key defaults: hbase.hstore.compaction.throughput.higher.bound 104857600 (100 MB/s), lower.bound 52428800 (50 MB/s), compaction.min 3, compaction.max 10, compaction.min.size 134217728 (128 MB), ratio 1.2; hbase.hstore.blockingStoreFiles is 16 in Apache HBase 2.x but Amazon EMR sets it to 10 for HBase on Amazon S3; memstore flush size 128 MB, block multiplier 4, max filesize 10737418240 (10 GB), offpeak compaction ratio 5.0, and hbase.bucketcache.size 8,192 MB on EMR.
- Turning off automatic major compaction (hbase.hregion.majorcompaction=0) shifts responsibility to you: schedule major_compact per table in a maintenance window on the primary cluster only, because read-replica clusters must not run manual compactions; on EMR releases earlier than 7.4.0 also set hbase.regionserver.compaction.enabled=false on replicas. Alarm when a store's file count approaches 80 percent of blockingStoreFiles.
- Practices that reduce compaction work: limit region size (HBase splits at hbase.hregion.max.filesize, 10 GB by default on HBase on S3), pre-split with the SPLITS option or the RegionSplitter tool, fix row-key hotspotting by salting, hashing, or reversing keys, reduce small MemStore flushes, size the BucketCache to hold more of the dataset on local instance store and EBS, and use multiple primary nodes so the coordinator survives a primary node stopping.
- Escalate to AWS Support when HBCK2 bypass or setRegionState is the next step, when znodes would need to be deleted, when a procedure stays stuck after three thread dumps, when several RegionServers stop at once, when two rounds of tuning have not improved latency, or when stack traces are unrecognized.
- Bring a support case the coordinator log extract around the first ERROR, the RegionServer log extract from the affected core node, three thread dumps taken 30 seconds apart with jstack, stuck procedure identifiers from list_procedures or the Procedures and Locks page, and the encoded region names involved.

## Details

### Diagnose before you tune

The decision flow maps symptoms to actions before any configuration change. Config changes applied through the hbase-site classification are Level 3 actions and require an EMR HBase restart, so the post insists on changing one parameter at a time and comparing against the canary baseline, because several parameters interact.

### The S3A read policy fix

On EMR 7.10 through 7.13, compactions, scans, and bulk loads that run slower than expected while HFiles keep growing may be the S3A client rather than compaction pressure. Check the release label and the current fadvise setting, then set the property to sequential and restart the HBase coordinator and RegionServer processes. From EMR 7.4 and later, HBase on S3 tracks store files in a meta file per store directory instead of relying on directory listings, so the RegionServer web UI count is the number of active files.

### Tuning parameters and scheduling

The parameter table spans throughput bounds, minor compaction selection (min, max, min.size, ratio), blocking thresholds, MemStore sizing, region size, off-peak windows, major compaction interval and jitter, and BucketCache size, with defaults checked against /etc/hbase/conf/hbase-site.xml where the documentation does not list one. Off-peak hours apply the larger offpeak ratio of 5.0 and lift the throughput limit unless a separate offpeak throughput bound is set.

### Reducing compaction work and knowing when to stop

Pre-splitting predictable key distributions, spreading hotspotting, and sizing flushes and caches reduce how much compaction the cluster must do in the first place. Some repair actions are hard to reverse: HBCK2 bypass can leave procedures or regions inconsistent, and deleting ZooKeeper znodes discards meta location, RegionServer registrations, and store file tracking state, so those paths belong with AWS Support rather than as first steps.
