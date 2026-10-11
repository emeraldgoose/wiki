---
title: "RADAR: Catch gray failures with anomaly detection"
description: "RADAR catches partial silent outages via a four-stage anomaly-detection pipeline, cutting discovery time 95% at over 90% precision."
tags: [source, databricks, observability, anomaly-detection, en]
locale: en
source_url: "https://www.databricks.com/blog/radar-catch-gray-failures-anomaly-detection"
blog: databricks
published_date: 2026-09-19
---

# RADAR: Catch gray failures with anomaly detection

## Overview

Gray failures — partial outages where dashboards stay green while one slice of users quietly fails — leak customers and revenue for hours because teams discover them through support tickets. RADAR (Reliability Anomaly Detection, Alerting, and Root-cause analysis) is Databricks' internal four-stage, metric-agnostic pipeline that surfaces such failures in minutes, reportedly cutting discovery time by 95% at over 90% precision.

## What makes gray failures sneaky

They are partial (one card type, one region — no crashing server to page on) and they grow (a handful of affected users spreads while the issue looks like isolated user error). Waiting on customer reports fails three ways: triage is manual, detection lags by hours or days, and most affected users never report at all. The fix is automatic detection that fires when far more users than usual hit the same issue at once — e.g., a sudden spike in one "user-fault" error code across a region is really the provider's fault.

## The four RADAR stages

First, record reliability metrics over time: error counts plus distinct affected users, broken down by error code and region. Second, run unsupervised streaming anomaly detection (the SPOT model, trained on 14 days of history with a single risk parameter) instead of hand-tuned thresholds. Third, enrich, filter, and dedupe alerts, then file tickets routed to the owning team. Fourth, attach anomaly deep-dives and a Genie-backed dashboard link so on-call starts at diagnosis instead of data gathering.

## Build it yourself on Databricks

The pattern is metric-agnostic — billing anomalies, checkout conversion, claims throughput, model drift — and every stage maps to native components: Zerobus plus Unity Catalog/Metric View and Delta Lake for metrics; MLflow, Model Serving, and Workflows for detection; SQL Alerts for alerting; Genie and AI/BI Dashboards for root cause; all deployed as one asset bundle. The team published a scaffold recipe plus a demo prompt so an AI agent can generate the whole system from your chosen metric.

## References

- Original article: [RADAR: Catch gray failures with anomaly detection](https://www.databricks.com/blog/radar-catch-gray-failures-anomaly-detection)
