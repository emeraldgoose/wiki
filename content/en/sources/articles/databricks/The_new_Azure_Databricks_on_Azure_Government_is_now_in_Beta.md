---
title: "The new Azure Databricks on Azure Government is now in Beta"
description: "Azure Databricks on Azure Government enters Beta with Unity Catalog, Databricks SQL, classic and serverless compute, Compliance Security Profile by default, Private Link, and US Gov Virginia/Arizona data residency — working toward FedRAMP Class D and DoW IL5 authorization (expected early 2027)."
tags: [source, article, databricks, azure-government, fedramp, il5, en]
locale: en
source_url: "https://www.databricks.com/blog/new-azure-databricks-azure-government-now-beta"
blog: databricks
published_date: 2026-11-19
---

# The new Azure Databricks on Azure Government is now in Beta

**Source**: [Databricks Blog](https://www.databricks.com/blog/new-azure-databricks-azure-government-now-beta)
**Published**: 2026-11-18

## Overview

Azure Databricks on Azure Government is entering Beta — a milestone in delivering the full Databricks Data + AI Platform to the U.S. public sector. Government agencies and their partners now get the modern data foundation already standard in commercial (Unity Catalog, Databricks SQL, serverless compute), with the full AI suite to follow, in an environment working toward FedRAMP Class D (formerly High) and DoW IL5 authorization. As a first-party Azure service, it is managed through the Azure portal, integrates with Microsoft Entra ID, and counts toward existing Azure commitments.

## Key points

- Two paths: for federal civilian agencies, state and local governments, and partners whose workloads fit FedRAMP Class D, Azure Commercial is available today (FedRAMP Class D offering launched recently). For organizations needing a dedicated government cloud with a path to FedRAMP Class D and DoW IL5, the new Azure Government environment is in Beta now.
- Unlike the legacy environment, the new environment runs the same architecture as commercial Azure Databricks and is designed to receive every commercial feature through the same ongoing releases; Beta is the first release on that path.
- What's available in Beta: Unity Catalog (manage access, lineage, auditing across all data and AI assets — define a policy once, apply it everywhere); Databricks SQL for fast, high-concurrency analytics with classic clusters or serverless compute; Secure-by-default Compliance Security Profile on every workspace (enhanced monitoring, automatic cluster updates, hardened compute image, encrypted inter-node traffic); Azure Private Link required on front and back end (all traffic stays on the Azure backbone); System tables for administrators (one queryable view of audit logs, billing, compute, pipelines, ML experiments, query history, storage); data stored and processed only in US Gov Virginia and US Gov Arizona.
- AI roadmap (governed by Unity Catalog): conversational analytics with Genie; AI-assisted development (write, explain, debug code); production-grade agents with Agent Bricks (build, evaluate, deploy agents over your documents/data, built-in quality evaluation); Model Serving and Foundation Model APIs; Vector Search and AI Functions for RAG apps and SQL-native classification/extraction/summarization; Databricks Apps and Lakebase for secure applications and operational workloads.
- Authorization: actively pursuing FedRAMP Class D and DoW IL5, expected early 2027; once authorized, agencies and defense partners can run CUI and IL5 mission-critical workloads (not supported on Azure Commercial). Track progress on the FedRAMP Marketplace.
- Getting started: opt in with a dedicated Azure Government subscription never used for Azure Databricks; register the preview feature in the Azure portal — every new workspace in that subscription is created in the new environment. Beta is intended for non-production workloads; workspaces carry forward to production at GA (expected early 2027).
- Migrating from legacy: existing workspaces/notebooks/data unaffected; explore side by side. Recommended starting points: Unity Catalog (legacy Azure Government workspaces never had it), serverless compute (new to government environments — begin security/compliance review now), network encryption (Compliance Security Profile requires instance types supporting Azure Virtual Network encryption — update cluster configs and Terraform/ARM templates), and your ATO (work with security and authorizing officials now; updating SSPs and data flows during Beta positions you to run CUI production workloads at GA).

## Details

- The new environment is a first-party Azure service: Azure portal management, native Entra ID integration, counts toward Azure commitments.
- Roadmap capabilities and timelines are forward-looking and subject to change.
- Databricks' Federal team can help assess workloads and plan the move; contact your Databricks representative or see the Azure Databricks documentation.
