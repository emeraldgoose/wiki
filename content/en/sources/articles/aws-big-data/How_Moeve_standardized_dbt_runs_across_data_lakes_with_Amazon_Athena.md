---
title: "How Moeve standardized dbt runs across data lakes with Amazon Athena"
description: Promoted on 2026-10-17
published: 2026-10-17
source_url: "https://aws.amazon.com/blogs/big-data/how-moeve-standardized-dbt-runs-across-data-lakes-with-amazon-athena"
blog: aws-big-data
locale: en
tags: [source, article, en, en]
---

# How Moeve standardized dbt runs across data lakes with Amazon Athena

## Overview

Moeve's analytics teams each ran dbt their own way, with run logic embedded in project-specific pipelines, different compute engines per team, and no consistent cost visibility. The company built a centralized, serverless dbt launcher on Amazon Athena that gives every project the same run lifecycle: parameters in from DynamoDB, a completion event out to EventBridge. Onboarding a new dbt project dropped from days to about 15 minutes.

## Why Athena became the default engine

Athena fit because the workload is bursty rather than continuous: each dbt project runs for a few minutes on schedule or on data arrival, then idles. Serverless processing removes cluster management for a small central team, per-query scan pricing maps naturally to that shape, and each data-lake account pays for its own scans since compute runs in the account that owns the data. The dbt Athena adapter's maturity and Athena's Iceberg support for idempotent incremental merges reinforced the choice.

A key cost optimization is data-derived merge predicates: instead of a fixed lookback window, the platform builds the target partition filter from the distinct partition values in the incoming dataset, so merges scan only affected partitions. Source input is likewise bounded by explicit ranges or a configured default window.

## The centralized launcher architecture

A Step Functions state machine receives a run request, reads project parameters (environment, IAM role, engine, timeout, retries, default window) from DynamoDB, launches an ephemeral Fargate container from a shared dbt image, and the container assumes a `dbt-child` role in the target data-lake account so compute stays close to the data. Model-level results and data-quality outcomes are recorded with the Elementary dbt package, and a structured completion event goes to a central EventBridge bus.

Storing parameters in DynamoDB rather than pipeline code was deliberate: timeouts and retries can change without a deployment, and new projects register with one config entry plus a model merge — no Terraform or infrastructure review. Local CI validation with DuckDB returns feedback in under two minutes; Athena behavior in the target account remains the final proof.

## Decoupled orchestration via events

The launcher never decides what runs next. Downstream consumers subscribe to completion events; Moeve's orchestration layer models dataset dependencies as a graph and starts projects whose inputs are ready. Running and orchestrating evolve independently — the orchestration layer was rebuilt without touching the launcher. Observability comes free from standardization: Step Functions state, Fargate logs, dbt/Elementary model results, and the bus event as audit record.

## References

- [Original post: How Moeve standardized dbt runs across data lakes with Amazon Athena](https://aws.amazon.com/blogs/big-data/how-moeve-standardized-dbt-runs-across-data-lakes-with-amazon-athena)
- [Top 10 performance tuning tips for Amazon Athena](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/)
