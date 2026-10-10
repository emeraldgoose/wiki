---
title: "Announcing Workday Data Connect federation in Unity Catalog"
description: "Zero-copy Workday HR and finance data in Unity Catalog via a native Data Connect federation connector (Beta)"
tags: [source, databricks, data-engineering, federation, iceberg, unity-catalog, en]
locale: en
source_url: "https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog"
blog: databricks
published: "2026-10-08"
---

# Announcing Workday Data Connect federation in Unity Catalog

**Source**: [Databricks Blog](https://www.databricks.com/blog/announcing-workday-data-connect-federation-unity-catalog)
**Date**: Oct 8, 2026

## What Shipped

A public Beta connector that federates Workday Data Connect into Unity Catalog. HR and finance tables shared through Workday Data Cloud become queryable in Databricks with no ingestion pipeline and no duplicate copies. Databricks, a Workday Data Cloud launch partner since Workday Rising 2025, is among the first platform partners with a native connector. Note the scope split: this connector does not ingest or copy — durable history (e.g. SCD2) stays with the Lakeflow Connect ingestion connectors.

## How It Works

Setup is a short handshake between two admins:

- Workday side: enable Data Connect, share tables through its Iceberg REST catalog, register an API client (JWT Bearer Grant), and grant an Integration System User read access.
- Databricks side: create one OAuth connection plus a foreign catalog; Databricks handles the token exchange with Workday's Iceberg REST catalog, so no token endpoint to manage. Requires a Unity Catalog workspace, Runtime 19+, and a workspace admin enabling the Beta from Previews.

Queries run on Databricks compute reading straight from Workday's managed object storage, governed end to end by Unity Catalog: catalog/schema/table permissions, lineage, and auditing identical to native assets. Access is read-only, so Workday remains the system of record.

## Catalog vs Query Federation

Query federation pushes SQL into the external system and runs it there. Catalog federation — what this connector uses — pulls table metadata from Workday's Iceberg REST catalog while Databricks compute reads the data and executes the query itself. Either way Unity Catalog governs access.

## Three Paths for Workday Data

- **Lakeflow Connect**: managed incremental ingestion into Delta — durable copies, scheduled pipelines.
- **Data Connect federation (Beta)**: zero-copy live analytics on shared Iceberg tables, joinable with the rest of the estate.
- **Live Data Query over JDBC**: on-demand real-time lookups that store nothing.

Pick per use case instead of forcing everything through one pipeline.

## What It Unlocks

Federated people-and-money data joins enterprise data in place: Genie natural-language exploration over workforce and financial trends, real-time planning unified with market or sales data, workforce analytics blended with operational metrics, and AI agents fed governed current data instead of stale exports. Example questions: fastest-growing cost centers by headcount, attrition by region and job family, workforce change vs bookings or opex.

## Seminar Takeaways

- Federation shape follows the access pattern: durable copy vs live view vs lookup are different tools, not tiers of the same tool.
- Zero-copy only works with governance at the read path — permissions, lineage, and audit must behave identically to native tables.
- Keeping the source system of record (read-only) removes an entire class of staleness bugs.
- OAuth token exchange done by the platform (not hand-rolled per team) is what makes the two-admin setup actually short.

## Related Concepts

- [Apache Iceberg](concepts/data-engineering/apache-iceberg.md) (shared Iceberg tables as the interop surface)
