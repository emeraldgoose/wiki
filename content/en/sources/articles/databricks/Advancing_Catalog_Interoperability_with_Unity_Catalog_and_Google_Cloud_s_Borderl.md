---
title: "Advancing Catalog Interoperability with Unity Catalog and Google Cloud’s Borderless Lakehouse"
description: "Databricks and Google Cloud opened bi-directional catalog federation between Unity Catalog and Google Cloud's borderless Lakehouse (Iceberg tables, GA), and co-drove the Iceberg catalog-labels proposal so governance metadata (domain, status, PII tags) travels with tables across catalogs."
tags: [source, article, databricks, unity-catalog, iceberg, google-cloud, en]
locale: en
source_url: "https://www.databricks.com/blog/advancing-catalog-interoperability-unity-catalog-and-google-clouds-borderless-lakehouse"
blog: databricks
published_date: 2026-11-19
---

# Advancing Catalog Interoperability with Unity Catalog and Google Cloud’s Borderless Lakehouse

**Source**: [Databricks Blog](https://www.databricks.com/blog/advancing-catalog-interoperability-unity-catalog-and-google-clouds-borderless-lakehouse)
**Published**: 2026-11-18

## Overview

Databricks and Google Cloud announced a catalog-interoperability milestone: customers can now access a single copy of data from both Unity Catalog and Google Cloud's borderless Lakehouse. This extends the partnership's open-lakehouse work — open table formats (Delta Lake, Iceberg) and catalog federation for zero-copy access — into bi-directional interoperability and open catalog metadata.

## Key points

- Inbound (Google Cloud → Databricks): Lakehouse Federation to Google Cloud is now generally available. Customers can mount Iceberg tables managed by Google Cloud's Lakehouse runtime catalog in Unity Catalog, then query them with Databricks (including serverless Databricks SQL / Lakehouse) or analyze them with Genie, which answers natural-language data questions without code or SQL.
- Outbound (Databricks → Google Cloud): data from Databricks can be brought into Google Cloud's Lakehouse, so engines like BigQuery can read Unity Catalog managed tables without data copies.
- Next frontier — catalog metadata: Databricks and Google Cloud helped drive and land catalog labels in the Iceberg community, a proposal letting catalogs share metadata as key-value pairs (labels). A table tagged `domain=finance` and `status=certified`, or a column tagged `pii=ssn`, keeps those tags when federated between catalogs.
- Shared labels matter for governance in the agent era: catalog metadata can flag sensitive data for masking and give agents context when searching assets. Both companies commit to advancing open governance so business and access semantics travel with data instead of being redefined per system.
- Getting started: read the documentation for Catalog Federation between Unity Catalog and Google Cloud's borderless Lakehouse, or Google's docs on catalog federation to Unity Catalog; interested customers can reach out to their Databricks account team.

## Details

- The Lakehouse architecture has moved from open table formats to catalog federation for zero-copy cross-platform access; this announcement is the latest milestone in that progression.
- Interoperability is bi-directional: Google Cloud → Databricks via Lakehouse Federation (GA), and Databricks → Google Cloud for BigQuery reads of Unity Catalog tables.
- Catalog labels are the mechanism for metadata portability: governance and business semantics (PII tags, certification status, domains) remain attached to tables and columns as they move between catalogs.
