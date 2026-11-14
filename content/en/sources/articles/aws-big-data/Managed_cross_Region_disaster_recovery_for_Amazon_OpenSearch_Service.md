---
title: "Managed cross-Region disaster recovery for Amazon OpenSearch Service"
description: "Amazon OpenSearch Service now offers managed disaster recovery for domains on OpenSearch 3.7 or later: a read-only secondary domain in another Region stays continuously in sync with the primary, with a planned zero-data-loss switchover, a failover bounded by an RPO under 1 minute, and an RTO under 20 minutes. Pairing is a two-step setup on the console or via the AddReplicationPeer API, with no charge beyond the secondary domain's instances and cross-Region data transfer."
tags: [source, aws-big-data, disaster-recovery, opensearch, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/managed-cross-region-disaster-recovery-for-amazon-opensearch-service"
blog: aws-big-data
published_date: 2026-11-14
---

# Managed cross-Region disaster recovery for Amazon OpenSearch Service

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/managed-cross-region-disaster-recovery-for-amazon-opensearch-service) · **Published**: 2026-11-11

## Overview

Amazon OpenSearch Service already provides high availability within a single Region through Multi-AZ deployments, but some organizations need a multi-Region architecture to meet strict recovery point and recovery time objectives, data residency mandates, or business continuity plans for mission-critical search and AI workloads. Until now, meeting that bar meant building and operating your own replication with cross-cluster replication or dual writes to multiple Regions — months of engineering and ongoing maintenance, no coordinated way to switch roles between Regions, and no guaranteed recovery point objective.

The service now offers managed disaster recovery for domains running OpenSearch 3.7 or later. A primary domain in one Region accepts reads and writes while a secondary domain in another Region continuously receives changes and serves reads only. When you pair the domains, the service first copies the existing Lucene segments, after which every new document and update is indexed on both domains. Replication traffic stays within the OpenSearch Service network, so no VPC peering or extra networking is needed, and data is encrypted in transit. Because both domains index the data, the secondary is ready to take over as primary at any time.

Two API-driven operations move the primary role. Switchover is a planned, coordinated role swap with zero data loss, because pending writes replicate before roles swap. Failover is an unplanned, unilateral promotion of the secondary, where writes not yet replicated are lost, bounded by the replication lag; it is the recovery path when the primary domain is unavailable. The blog targets customer-facing search, financial services and risk workloads, and mission-critical operational data, and sets up in two steps with an RPO under 1 minute and an RTO under 20 minutes.

## Key points

- Requires OpenSearch 3.7 or later on both domains, in the same AWS account but different Regions, with matching sizes: the same number of primary shards and replicas and similar CPU, memory and storage.
- Setup flow: create the primary, create a same-version secondary in another Region, pair primary with secondary, then check replication status; pairing takes a few minutes.
- Pair with the console or the CLI: aws opensearch add-replication-peer with --domain-name PRIMARY_DOMAIN, --peer-domain-arn SECONDARY_DOMAIN_ARN and --region PRIMARY_REGION; CompareDomainConfiguration can surface configuration drift before pairing.
- Replication status is visible on a built-in console dashboard or via DescribeDomainReplication; RemoveReplicationPeer stops replication while each domain keeps its data.
- Five CloudWatch metrics publish on the secondary: DisasterRecoveryReplicationLagTime, DisasterRecoveryReplicationLagOps, DisasterRecoveryBootstrappingIndices, DisasterRecoveryDegradedIndices and DisasterRecoveryFailedIndices, each with a suggested alarm; healthy lag is up to 10 seconds even when caught up.
- SwitchoverReplication runs on the secondary for a coordinated swap with zero data loss; FailoverReplication promotes the secondary unilaterally and requires the --allow-data-loss flag.
- The service does not redirect application writes: after either operation, your runbook must repoint the write path, for example by updating a DNS record, configuration parameter or service discovery entry.
- After a switchover, the former primary becomes the secondary and replication continues in reverse with no further action; after a failover, the original domain must be re-seeded before it can replicate again.
- Measured on r7g domains (6 data nodes plus 3 m7g.large cluster managers, 12 TiB gp3 per node, 12 primary shards plus 1 replica, rollover at 50 GB per primary shard) under a sustained 240 MBps synthetic Apache log write load.
- Pairing completed in 1 to 3 minutes from 1 TiB to 10 TiB; initial sync took 20 minutes for 1 TiB on r7g.4xlarge and 2 hr 31 min for 10 TiB on r7g.4xlarge (2 hr 18 min on r7g.8xlarge).
- Steady-state replication lag was about 10 seconds at the 95th percentile across 1 TiB and 10 TiB at 240 MBps; planned switchover lost zero writes with writes-down times of 36.8 s, 38 s and 57 s.
- Unplanned failover confirmed the role flip in 5.8 to 8.1 s, resumed writes in 60 to 69 s, and lost about 8 s (2.0M docs) to 10 s (2.46M docs) — well within the under-1-minute RPO and under-20-minute RTO targets.

## Details

### Prerequisites and limitations

UltraWarm, Writable Warm storage and the OpenSearch Optimized engine for log analytics are not supported in this release. Managed disaster recovery replicates data only: Index State Management policies, index templates, settings and roles are not replicated, so manage them on both domains with infrastructure as code. Configuration changes need attention on both sides, and client write redirection after a role change is always your application's job.

### Upgrading to OpenSearch 3.7

Domains on earlier versions can use a clone-based upgrade: the service creates a clone of the domain on the target version, keeps it in sync, and the original keeps serving traffic. You can validate the clone with your own read requests, cut over when ready (writes are blocked during cutover, which can last up to several minutes), and cancel any time before cutover or roll back during a retention period you set. Clone-based upgrades are available for domains running Elasticsearch 7.10 or OpenSearch 1.1 or later; you are charged for both clusters while validating and during retention, and a manual snapshot plus the pre-upgrade check should precede the upgrade.

### Operating practices and pricing

Best practices from the post: keep configuration in a Git repository applied to both domains, for example with the OpenSearch Terraform provider; upgrade the secondary first and the active primary last, never running mixed versions permanently; keep instance types, counts, storage and shard configuration aligned and use CompareDomainConfiguration to detect drift; decide your failover automation deliberately, since failover is manual by design but can be driven by CloudWatch alarms and the failover and switchover APIs; and rehearse the runbook regularly with switchover, including the client write redirection step. There is no additional charge for managed disaster recovery itself — you pay for the secondary domain's instances and for cross-Region data transfer. The post is by Cédric Pelvet and Michael Torio.
