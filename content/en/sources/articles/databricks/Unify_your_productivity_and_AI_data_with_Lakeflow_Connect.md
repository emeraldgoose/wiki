---
title: "Unify your productivity and AI data with Lakeflow Connect"
description: "Lakeflow Connect ingests productivity and collaboration data into governed Unity Catalog tables so downstream AI agents gain complete enterprise context."
tags: [source, databricks, data-engineering, ingestion, lakeflow, en]
locale: en
source_url: "https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect"
blog: databricks
published_date: "2026-10-26"
---

# Unify your productivity and AI data with Lakeflow Connect

**Source**: [databricks](https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect) · **Published**: 2026-10-26

## Overview

This is the second post in a series on how Lakeflow Connect brings fully managed data ingestion to every line of business. Following a deep dive into unifying marketing data, this post focuses on unlocking enterprise knowledge trapped in the productivity stack, such as wikis, project management tools and AI foundation model data, so downstream AI agents get complete business context.

Lakeflow Connect provides a comprehensive suite of fully managed native connectors across SaaS applications, databases and file sources that ingest data directly into the Databricks platform. Connectors are configured through a point-and-click UI or a simple API, and data arrives incrementally as governed, managed tables in Unity Catalog without infrastructure to provision or scale.

## Key points

- Productivity and collaboration tools hold valuable enterprise knowledge but have historically been siloed behind custom API integration for every source.
- Native connectors cover collaboration tools (Jira, Monday.com, Smartsheet, Aha!, GitHub), enterprise knowledge stores (Confluence, Notion, Glean, SharePoint, Google Drive), communication (Outlook, Gmail) and AI providers (OpenAI, Anthropic).
- Toyota Finance Australia, Seguros SURA and VaxCare report zero-maintenance pipelines and governed, analytics-ready Delta tables.
- Unstructured content such as documents, pages and messages lands as governed tables in Unity Catalog and is ready to be parsed with `ai_parse_document` and indexed for retrieval.
- OpenAI and Anthropic connectors expose usage, costs, API keys, projects, users and audit logs to govern AI spend.
- M3 Accounting unified GitHub and SharePoint documentation into Databricks within days using Lakeflow Connect.

## Details

The average productivity stack spans project trackers, wikis, document stores, inboxes and AI tools, each holding only a slice of how work gets done. Custom pipelines are slow to build and painful to maintain, so impactful use cases such as AI agents grounded in internal knowledge remain out of reach.

Lakeflow Connect resolves this with built-in connectors that bring scattered productivity data into one governed foundation without integration bottlenecks. Data is incrementally ingested as managed Delta tables in Unity Catalog with governance and access control handled centrally.

For AI use cases, unstructured content lands as one row per file or message in governed tables. Structured files can be landed directly as Delta tables, while document bytes are converted to text with Databricks' built-in document intelligence before chunking and embedding for retrieval.

Beyond productivity data, foundation model connectors give organisations visibility into AI usage, cost and compliance. Leaders can attribute spend by team, model and application while integrating productivity, engineering and business data on the same platform.

## References

- Original article: [https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect](https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect)
