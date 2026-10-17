---
title: "How Moovit achieved 33% cost optimization through architectural modernization"
description: Promoted on 2026-10-17
published: 2026-10-17
source_url: "https://aws.amazon.com/blogs/big-data/how-moovit-achieved-33-cost-optimization-through-architectural-modernization"
blog: aws-big-data
locale: en
tags: [source, article, en]
---

# How Moovit achieved 33% cost optimization through architectural modernization

## Overview

Moovit's single Amazon Redshift cluster had grown over a decade into the backbone of the whole data platform, serving heavy ETL, near-real-time monitoring, Tableau BI, data science, and ad-hoc queries from one engine. Queue times grew and adding nodes barely helped. By measuring workloads, cleaning up waste, and assigning each workload to the engine that fit it best — EMR for heavy aggregation, provisioned Redshift for BI serving, Redshift Serverless for ad-hoc and data science — Moovit halved its Redshift cluster and cut overall pipeline cost by 33%.

## Measure first, then clean up

Before moving anything, Moovit built automated query attribution classifying every query by owner and execution context (user/service account, query signatures, orchestrator metadata), surfaced in a Tableau dashboard with CPU time as the primary impact metric. That baseline separated compute-heavy-but-healthy workloads from queue-constrained, high-frequency, or misclassified ones, and ranked offload candidates by evidence.

Cleanup came before migration: unused processes (about 7% of CPU), over-frequent schedules, and misaligned WLM priorities were fixed first, so only genuinely heavy workloads were selected for offloading. The prime candidate was raw-data aggregation pipelines — heavy sessionization over S3 data whose consumers only needed aggregated outputs.

## POC and production migration to EMR

A proof of concept ported the aggregation pipelines to EMR Serverless with Spark SQL, requiring only minor syntax changes. Early runs were slow (4 hours on 100 executors vs a 30–40 minute Redshift baseline) until the team rewrote shuffle-heavy patterns and expensive DISTINCTs for Spark's distributed model — landing at about 10 minutes on fewer than 50 executors. Rigorous parity validation (row counts, distinct users, metrics, trends, spot checks over consecutive runs) gated each cutover. For steady-state production, Moovit moved from EMR Serverless to EMR on EC2 to use existing compute reservations, with zero application changes.

## Rightsizing and workload isolation

With heavy work offloaded, the provisioned cluster was shrunk incrementally — two nodes at a time via elastic resize, validating SLAs at each step — to 50% of original capacity. Ad-hoc analyst and data-science queries moved to Redshift Serverless through data sharing, isolating unpredictable load, and WLM priorities were rebalanced toward Tableau serving. Aggregation p90 wall-clock time fell from 5.48 to 2.77 hours.

## References

- [Original post: How Moovit achieved 33% cost optimization through architectural modernization](https://aws.amazon.com/blogs/big-data/how-moovit-achieved-33-cost-optimization-through-architectural-modernization)
