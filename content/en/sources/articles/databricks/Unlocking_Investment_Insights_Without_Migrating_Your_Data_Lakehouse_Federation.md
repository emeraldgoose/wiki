---
title: "Unlocking Investment Insights Without Migrating Your Data: Lakehouse Federation"
description: "Lakehouse Federation queries on-premises portfolio data in place and joins it with FactSet marketplace data, enabling dashboards and Genie without moving or copying anything."
tags: [source, databricks, data-engineering, federation, lakehouse, finance, en]
locale: en
source_url: "https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation"
blog: databricks
published_date: "2026-10-27"
---

# Unlocking Investment Insights Without Migrating Your Data: Lakehouse Federation

**Source**: [databricks](https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation) · **Published**: 2026-10-27

## Overview

In today's enterprise landscape, data rarely sits in one place. Financial institutions, asset managers and individual investors face a common challenge: sensitive data such as portfolio holdings, trading positions and client information often resides on-premises behind corporate firewalls, in the cloud, or both, while third-party market data, analyst estimates and financial fundamentals increasingly live in the cloud. Traditional approaches force an uncomfortable choice: copy sensitive data to the cloud, stand up brittle ETL pipelines, or give up on integration altogether.

Databricks Lakehouse Federation changes this by federating on-premises sources and subscribing to third-party cloud data so a single SQL query can join both catalogs without copying or persisting intermediate objects.

## Key points

- Lakehouse Federation creates federated connections to external databases such as SQL Server, PostgreSQL, MySQL and Snowflake, and queries them directly from Databricks with standard SQL. The data never moves.
- A marketplace data share such as FactSet sits alongside the federated catalog in Unity Catalog, and a single SQL query joins them like ordinary tables.
- A concrete wealth-management example federates on-premises holdings from SQL Server with FactSet estimates, fundamentals and symbology data from the Marketplace.
- The dashboard inlines the combined query in each widget, with no persisted views or tables; each refresh re-federates the source.
- Genie translates natural language into the same queries, democratizing access for portfolio managers, financial advisors and individual investors.
- The pattern applies broadly: healthcare can join HIPAA-protected patient records with drug interaction databases, manufacturing can federate IoT telemetry with cloud supply chain data, and retailers can combine in-store POS with third-party demographics.

## Details

The walkthrough creates a foreign catalog that maps to an on-premises database so external tables appear as native Unity Catalog objects. The data never leaves SQL Server, and every query runs against the source in real time. FactSet data is subscribed from the Marketplace and appears as a shared catalog with schemas such as estimates, fundamentals and symbology.

After both sources are accessible, an asset manager runs one query spanning the federated holdings and the FactSet tables, producing portfolio health, risk distribution, investment recommendations, top performers, a full holdings table and Genie natural-language answers. There is no pipeline to author, no materialized view to schedule and no gold layer to maintain.

By bringing compute to the data, Lakehouse Federation keeps sensitive first-party data protected while enabling rich analytics with third-party data, changing the economics of hybrid data analytics.

## References

- Original article: [https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation](https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation)
