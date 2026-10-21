---
title: "Top 5 System Table Queries for Understanding Your Databricks Costs"
description: "Five system-table SQL queries break down Databricks spend by product, warehouse, and team, then flag anomalies and forecast next month."
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/top-5-system-table-queries-understanding-your-databricks-costs"
blog: databricks
published_date: 2026-09-22
---

# Top 5 System Table Queries for Understanding Your Databricks Costs

## Overview

The `system.billing.usage` table joined with `system.billing.list_prices` gives a near-real-time, account-wide view of Databricks spend. Five starter queries progress from describing today's costs to predicting next month's, and work best pinned as datasets in an AI/BI dashboard for visualization and Genie interrogation.

## Where the money goes: product, warehouse, team

Query 1 breaks daily spend down by product (joining usage facts to the list-price dimension, substitutable with a discount-adjusted table). Query 2 tracks per-warehouse daily cost trends — consumption proxies for usage — to spot candidates for rescaling or auto-stop tuning, cross-checkable against warehouse events and monitoring pages. Query 3 groups spend by enforced custom tags (team, project), surfacing untagged records that reveal where tag enforcement is slipping.

## Catching spikes and projecting forward

Query 4 flags anomalous days against a rolling 14-day mean (elevated beyond one standard deviation, anomaly beyond two), suitable as a dashboard panel or an automated alert for runaway jobs and warehouses. Query 5 uses the `ai_forecast` SQL AI function to extrapolate recent usage into a 30-day projection with no manual time-series modeling — remembering that genuinely new planned workloads won't be captured by history.

## References

- Original article: [Top 5 System Table Queries for Understanding Your Databricks Costs](https://www.databricks.com/blog/top-5-system-table-queries-understanding-your-databricks-costs)
