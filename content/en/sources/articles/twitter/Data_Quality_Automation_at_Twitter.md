---
title: Data Quality Automation at Twitter
description: The Data Quality Platform — config-driven Great Expectations + Airflow checks over exabyte-scale BigQuery data
tags: [source, twitter, x, data-quality, bigquery, airflow, great-expectations, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter"
blog: twitter
date: '2022-09-15'
---

# Data Quality Automation at Twitter

## Summary

Twitter's ingestion framework (GCP Dataflow + Airflow, moving on-premise Hadoop data to BigQuery) lets employees run 10M+ queries a month over nearly an exabyte. Availability solved, the next gap was *quality*: datasets powering Core Ads analytics, ML feature generation, and personalization had only manual spot-checks (hand-written SQL in the BigQuery UI or notebooks), with no统一 automated framework. The team built the **Data Quality Platform (DQP)**: a managed, config-driven, workflow-based solution that builds standard and custom quality metrics, alerts on validation failures, and monitors metric trends — all inside GCP.

## Why Data Quality

Freshness, completeness, accuracy, and consistency determine data quality. Automated checks deliver: **confidence** (lower-risk decisions, higher efficiency), **productivity** (customers build instead of hand-validating), and **revenue protection** (bad data loses money).

## Architecture

- **Check logic**: open-source [Great Expectations](https://greatexpectations.io/) plus an in-house Stats Collector Library, wrapped as operators.
- **Orchestration/state**: Airflow workflows at resource-and-cadence granularity.
- **Delivery**: YAML configs shipped via CI/CD to GCS → Airflow workers run tests → results published to a **PubSub** queue → a **Dataflow** job lands them in BigQuery tables surfaced in **Looker** for debugging and trend analysis.

## Impact (Reported Numbers)

- **Revenue Analytics Platform** (ingests/aggregates/serves revenue analytics to AdsManager): ~**20% reduction** in new-feature rollout time via automated output validation, plus continuous measurement raising advertiser confidence.
- **Core Served Impressions** (core direct-revenue dataset consumed by 400+ internal downstream customers): first automated visibility into upstream/downstream deviance, with alignment metrics across all downstream datasets — previously zero.

## Relevance to SW Engineers

- After solving data *availability*, schedule the quality milestone explicitly; usage (10M queries/month) magnifies the blast radius of silent corruption.
- Config-driven checks (YAML in CI/CD) scale across thousands of datasets where hand-written SQL cannot; Great Expectations supplies the expectation vocabulary so teams write *what* to check, not *how*.
- Land check results as queryable data (BigQuery + Looker), not just alerts: trend visibility turns point-in-time validation into anomaly detection.
- Report adoption metrics that matter to producers (rollout time −20%) and consumers (400+ customers with alignment metrics), not just check counts.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter (Eduardo Luiz Ohe, Bi Ling Wu, 15 Sep 2022)
- Related: `concepts/data-engineering/delta-lake.md`, `concepts/data-engineering/stream-processing.md`
