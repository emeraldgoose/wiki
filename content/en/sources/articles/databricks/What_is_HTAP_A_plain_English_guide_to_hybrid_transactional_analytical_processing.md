---
title: "What is HTAP? A plain-English guide to hybrid transactional/analytical processing"
description: "Consider a payment system processing a purchase."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/what-htap-plain-english-guide-hybrid-transactionalanalytical-processing"
blog: databricks
published_date: 2026-10-13
---

# What is HTAP? A plain-English guide to hybrid transactional/analytical processing

**Source**: [databricks](https://www.databricks.com/blog/what-htap-plain-english-guide-hybrid-transactionalanalytical-processing) · **Published**: 2026-10-13

## Overview

Consider a payment system processing a purchase. Before approving the transaction, a fraud model may need to evaluate it against the account's recent activity. But if that transactional data must first move from the transactional database to a data warehouse for analysis, even a short delay can make the result less useful. Hybrid Transactional/Analytical Processing (HTAP) brings transaction processing and analytics closer together to address this problem. An HTAP database lets you run analytical queries on operational data while it is still current, without waiting for a batch data pipeline to move it into a separate analytical system.

## Key points

- HTAP brings transactional and analytical processing closer together so applications can run analytics on fresh transactional data.
- Different HTAP architectures involve different trade-offs in performance, isolation, data consistency, and freshness.
- Choose the architecture based on your workload. LTAP provides greater separation between transactional and analytical compute while both operate on the same data.
- Converged HTAP: Runs transactional and analytical workloads through a single database engine. The workloads may use different indexes, storage formats, or execution paths, but they share much of the same database.
- Composed HTAP: Uses separate transactional and analytical engines within an integrated architecture. The engines may share a storage layer or propagate changes through replication while remaining optimized for their resp
- Map your workloads and dependencies: Identify the applications, queries, pipelines, and downstream consumers involved. Separate transactional and analytical workloads from those that genuinely need both.

## References

- Original article: [https://www.databricks.com/blog/what-htap-plain-english-guide-hybrid-transactionalanalytical-processing](https://www.databricks.com/blog/what-htap-plain-english-guide-hybrid-transactionalanalytical-processing)
