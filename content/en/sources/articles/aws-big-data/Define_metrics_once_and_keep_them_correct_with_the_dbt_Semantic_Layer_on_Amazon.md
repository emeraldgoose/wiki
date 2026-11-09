---
title: "Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift"
description: "A pre-aggregated gold table silently reports average order value as $550 instead of $280; the open-source dbt Semantic Layer and MetricFlow define the metric once and recompute it correctly at any grain on Redshift."
tags: [source, aws-big-data, data-engineering, semantic-layer, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift"
blog: aws-big-data
published_date: 2026-11-10
---

# Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift

**Source**: [Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift](https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift) · **Published**: 2026-11-09

## Overview

A well-modeled gold layer is already a semantic layer for standardizing metrics, and reaching for a dedicated tool before you need one is over-engineering. The post is about the point where that stops being true: when users need to compute a metric across arbitrary combinations of dimensions chosen at query time, and some of those metrics are non-additive. The walkthrough builds a working answer on Amazon Redshift using the open-source dbt Semantic Layer powered by MetricFlow, defines average order value once, and proves it stays correct whether it is sliced by day, by week or by store.

Two limitations drive the argument. A gold table is pre-aggregated at one grain, so serving every dimension combination would need a table per combination — a count that grows as 2ⁿ, which nobody builds; teams build the dozen tables someone asked for and take a ticket for each new slice. The escape hatch, exposing one wide fact table and letting each BI tool run its own GROUP BY, restores flexibility and walks straight into the second problem: non-additive metrics that are quietly wrong. While the article notes that metric definition on AWS has largely lived downstream of the warehouse — Quick Sight Topics for dashboards and Amazon Q, and the newer AWS Context knowledge-graph layer over the Glue Data Catalog — its scope is the governed metric layer defined once in Git beside the Redshift models.

## Key points

- The worked example is deliberately tiny: five orders at one store, $1,000 on Monday 5 January 2026 and four $100 orders on Tuesday 6 January. A daily-grain gold table answers "average order value this week" by averaging the two daily figures and returns $550, while the truth from the orders is $1,400 / 5 = $280 — nearly double the real value, and plausible enough that nobody notices.
- Conversion rate, profit margin, cost per acquisition and distinct counts share the same trap, because the weekly figure must be recomputed as SUM(revenue) / COUNT(orders) at the week grain and a pre-aggregated table does not carry what that needs.
- The fix is declarative: in `sem_orders.yml` the semantic model declares one primary entity, categorical and time dimensions, and two measures (`order_total` as sum of amount, `order_count` as count of order_id), and the metric `average_order_value` is defined as a ratio of two simple metrics so MetricFlow always emits SUM(amount) / COUNT(orders) at whatever grain is requested.
- A time spine model built with `dbt_utils.date_spine` and registered in `_models.yml` gives MetricFlow the dates it reasons about; MetricFlow is driven by the `mf` CLI (`mf validate-configs`, `mf list metrics`, `mf query`).
- The payoff is visible in two commands: grouped by day the metric returns 1000.00 and 100.00, and grouped by week it returns 280.00 rather than 550.00, with the supporting `total_revenue` (1400.00) and `order_count` (5) available in the same query; slicing by the unrelated `order__store` dimension needs no new table.
- `mf query --explain` exposes the generated SQL — `date_trunc('week', ordered_at)`, `sum(amount)`, `count(order_id)`, `sum(amount) / nullif(count(order_id), 0)`, grouped by 1 — which confirms the recomputation and can be lifted into any tool.

## Details

The walkthrough targets Amazon Redshift Serverless and needs an account that can create a workgroup, a schema to write to and connection details (IAM authentication also works); an 8-RPU workgroup bills roughly $3 per hour of active query time, metered per second with a 60-second minimum, so the exercise typically costs under a dollar. Provisioning can be done from the console or with the companion repository's AWS CDK app, whose deploy script scopes inbound access to the caller's IP and rejects an overly broad CIDR such as 0.0.0.0/0 unless explicitly opted in. The environment pins `dbt-redshift==1.9.5` and `dbt-metricflow==0.11.0`, with dbt-core 1.9 or later required for the time-spine YAML; newer dbt-core releases print a deprecation notice but behave the same for this project.

Consumption is where open-source dbt differs from cloud. With dbt Core the options are the `mf query` CLI for validation, notebooks and scripts; `mf query --explain` to lift the generated SQL into any tool, scheduler or materialized model; a BI tool that reads MetricFlow's `semantic_manifest.json` from `dbt parse`, such as Lightdash's dbt MetricFlow integration; or, for a tool with no first-class connector such as Amazon Quick Sight, materializing the metric back into Redshift — wrapping the generated SQL in a dbt model, or on dbt Cloud using a saved query with an export on a schedule — after which Quick Sight simply reads an ordinary table. The fully hosted Semantic Layer API that Tableau and Power BI connect to over JDBC/GraphQL requires dbt Cloud, but the metric definitions are identical and only the serving layer differs, so the YAML does not change if you migrate later. Cleanup means dropping the schema and deleting the workgroup, or running the repo's destroy script.

## References

- Original article: [Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift](https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift)
