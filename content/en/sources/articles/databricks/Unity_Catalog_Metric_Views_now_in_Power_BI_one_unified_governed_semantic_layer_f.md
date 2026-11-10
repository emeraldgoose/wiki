---
title: "Unity Catalog Metric Views, now in Power BI: one unified, governed semantic layer for all your reporting and AI"
description: "Databricks adds Publish to Power BI, letting Unity Catalog metric views drive Power BI semantic models so definitions are modelled once in Databricks and stay governed, in sync and identical across Power BI, AI/BI dashboards and Genie."
tags: [source, databricks, unity-catalog, semantic-layer, power-bi, en]
locale: en
source_url: "https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting"
blog: databricks
published_date: 2026-11-11
---

# Unity Catalog Metric Views, now in Power BI: one unified, governed semantic layer for all your reporting and AI

**Source**: [Databricks Blog](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting) · **Published**: 2026-11-10

## Overview

Databricks is connecting Unity Catalog metric views to Power BI so that a single governed definition of business semantics drives both the lakehouse and the reporting tool business users already open every day. The problem it addresses is definitional drift: revenue, margin, and active customers should mean the same thing in every report, notebook, and AI application, and when they do not, business users and AI agents read the same data differently, finance and sales produce different revenue numbers, and decisions get made on the wrong ones. Unity Catalog metric views — part of Unity Catalog semantics — exist to define those KPIs once, in an open governed semantic layer on top of the lakehouse.

The other half of the problem lives in Power BI, where organizations often run thousands of workspaces, each with its own semantic models. When every team rebuilds metrics and relationships inside Power BI, the same logic is copied into many places, reports drift apart, and each definition change means editing every copy. Publish to Power BI is the answer the customers asked for: Databricks stays the unified open semantic layer and Power BI stays the front end. Business users build self-serve reports and explore metrics across any dimension without waiting for a data team to model the data or write DAX, while data teams maintain one definition instead of many.

Mechanically, each metric view becomes a table in the Power BI semantic model, its dimensions become columns, and its measures become DAX measures. Power BI queries the metric view itself, so the metric view remains the source of truth and joins declared inside it run in Databricks; joined dimensions such as campaign channel or region arrive as ordinary columns, which means table relationships do not have to be rebuilt in Power BI.

## Key points

- Publishing can be on demand from Catalog Explorer or automated by adding a Power BI task to a Lakeflow Job, so metric views and semantic models stay in sync in production — on a schedule or right after upstream tables refresh — and updated measures, new measures, and new dimensions flow into Power BI without manual rework.
- In the article's marketing example, a `campaign_performance` metric view defines dimensions such as channel and region and measures such as total spend, total revenue, and return on ad spend; in Power BI those become `SUM('campaign_performance'[spend])`, `SUM('campaign_performance'[revenue])` and a `DIVIDE([total_revenue], [total_spend])` ratio measure.
- Governance survives the trip: with DirectQuery every Power BI query honors Unity Catalog access controls and security policies, and lineage stays connected to the metrics teams already use in AI/BI dashboards, Genie, and the Databricks Lakehouse.
- Real-time reporting is covered by Lakehouse//RT plus DirectQuery, which runs on managed Delta tables so there is no separate serving system to copy data into, while still enforcing the same Unity Catalog row filters, column masks, and ABAC policies.
- Metric view materialization will soon benefit Power BI too: it pre-computes results without changing how metrics are calculated, Databricks serves a query from a matching materialization when one exists, and otherwise runs it against the metric view as usual, with identical definitions, DAX measures, and results either way.
- The preview covers the metric definitions most teams use daily: joins and relationships, dimensions, measures, and other semantic metadata; standard aggregations including distinct counts, ratios, filtered measures, and measures composed from other measures; current, offset, and trailing window measures; and metadata such as descriptions and currency, decimal, or percentage display formats that carry over to Power BI field properties.
- Storage can be DirectQuery, the default for live queries against Lakehouse//RT or Databricks SQL, or Import mode for loading data into Power BI.

## Details

Publishing is a three-step flow. First prepare the metric views, adding any measure inputs as dimensions and making sure every field is named. Then publish from Catalog Explorer via Publish > Publish to Power BI, signing in with Power BI credentials and choosing a target workspace — or, for production, add a Power BI task to a Lakeflow Job so publishing happens as part of the data pipeline. Finally validate in Power BI by opening the semantic model and confirming that the metric view appears as a table, dimensions as columns, and measures as DAX measures. The capability is available in Private Preview, and Databricks directs teams to their account team to test it.

The strategic framing is that Databricks becomes the home of the semantics: metric views, relationships, Pages, and other modeling metadata stay in one governed place instead of being scattered across tools, and the same definitions serve Power BI reports, AI/BI dashboards, and Genie. The article's closing multi-step workflow recaps the same three ideas — keep semantics in Unity Catalog, model once and consume across AI and BI, and stay governed and in sync through DirectQuery access controls plus task orchestration.

## References

- Original article: [Databricks Blog](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting)
