---
title: "From Delta Sharing to OpenSharing: what changed, what’s next"
description: "How Delta Sharing became OpenSharing, an open vendor-neutral protocol that extends zero-copy sharing beyond tables to agent skills, AI models, and unstructured data."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next"
blog: databricks
published_date: 2026-11-06
---

# From Delta Sharing to OpenSharing: what changed, what’s next

**Source**: [databricks](https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next) · **Published**: 2026-11-05

## Overview

Delta Sharing let thousands of organizations exchange live data across clouds without copying it. In June 2026, Databricks and the Linux Foundation announced its evolution into OpenSharing, an open, vendor-neutral protocol for sharing not only tables but the broader AI assets teams now depend on, including agent skills, AI models, and unstructured data. Delta Sharing had been contributed to the Linux Foundation as an open protocol built on Delta Lake and Parquet and reached more than 28,000 recipients, with many shares flowing through open connectors. Its scope remained centered on tables, while internal Databricks-to-Databricks sharing had already moved beyond tables, and agents increased the demand for sharing more asset types across platforms.

OpenSharing addresses both interoperability and scope questions. It adds Apache Iceberg REST Catalog support so providers can share to Iceberg-compatible engines, and storage ecosystem integrations let on-premises or private-cloud providers run an OpenSharing server that connects to Unity Catalog without migrating data first. Data also does not move: the server issues temporary, scoped credentials and stays outside the data path, consistent with Delta Sharing. Existing Delta Sharing clients and integrations remain compatible; this is an evolution rather than a break, and the delta-io/delta-sharing repository continues alongside the OpenSharing-IO/OpenSharing organization.

At two distinct layers, OpenSharing exists as an Apache 2.0 open source protocol and specification under the Linux Foundation AI & Data Foundation, and as Databricks OpenSharing, the enterprise implementation integrated with Unity Catalog, Databricks Marketplace, and Clean Rooms. Open source Unity Catalog can provide vendor-neutral cataloging and governance outside Databricks when paired with an open server. The protocol introduces a Share, Schema, Asset hierarchy extending sharing beyond tables to Volumes, Agent Skills, and AI models.

## Key points

- OpenSharing extends cross-platform, zero-copy sharing from tables to volumes, agent skills, AI models, and other assets.
- The protocol is Apache 2.0 and developed under the Linux Foundation AI & Data Foundation, separate from the Databricks enterprise implementation.
- Existing Delta Sharing clients and connectors remain compatible, so the rollout is an evolution rather than a breaking change.
- Iceberg REST Catalog support lets providers reach recipients standardized on Iceberg tooling.
- On-premises and private-cloud providers can run OpenSharing servers through the Databricks Storage Ecosystem without migrating data first.
- Zero-copy credential vending remains the model: data stays in place and access is granted via temporary credentials.

## Details

Announcement date was June 10, 2026. The asset hierarchy currently specifies Table, Volume, Agent Skill, and Model types, while Agent and Page or Glossary types remain community proposals. Companion additions include SecureConnect for managed recipient connectivity, Global Distribution for regional replication in private preview, Genie Agent Sharing for conversational access in beta, and Lakebase table and change data feed sharing in public preview. Relay and query scenarios such as advertising measurement, healthcare collaboration, or retail and CPG planning illustrate where clean rooms and marketplace distribution also fit. Full protocol details, partner lists, governance specifics, and exact versioning terms are in the linked source.

## References

- Source: [databricks](https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next)
