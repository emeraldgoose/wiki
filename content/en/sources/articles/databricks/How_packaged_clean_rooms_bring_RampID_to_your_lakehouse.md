---
title: "How packaged clean rooms bring RampID to your lakehouse"
description: "LiveRamp Embedded Identity on Databricks delivers RampID resolution via a packaged clean room: identity service runs next to your data with no PII round-trip, OpenSharing read-only access, serverless compute in a central clean room, and Unity Catalog governance — no code review or approval step."
tags: [source, article, databricks, clean-room, liveramp, rampid, privacy, en]
locale: en
source_url: "https://www.databricks.com/blog/liveramp-rampid-identity-resolution-packaged-clean-rooms"
blog: databricks
published_date: 2026-11-19
---

# How packaged clean rooms bring RampID to your lakehouse

**Source**: [Databricks Blog](https://www.databricks.com/blog/liveramp-rampid-identity-resolution-packaged-clean-rooms)
**Published**: 2026-11-18

## Overview

Historically, resolving customer records to a person-based ID like RampID meant exporting PII to an outside service, waiting for a match file, and loading it back — adding pipelines, sensitive-data copies, and delay. Packaged clean rooms remove that round-trip: LiveRamp Embedded Identity on Databricks brings the identity service to the data, so customers receive a resolved list of RampIDs in their own environment, governed by Unity Catalog.

## Key points

- Use cases: a publisher builds a sports-fan segment from authenticated viewing data and sizes it against an advertiser's CRM prospect pool (excluding existing customers); an agency combines publishers' streaming/digital exposure logs with a retailer's loyalty-linked purchases to deduplicate reach, measure exposed-shopper purchases, and estimate incremental sales with a holdout.
- What a packaged clean room is: a Databricks clean room is a secure environment where two or more parties run approved code across combined data without revealing raw data or IP. In a standard approval-based room all parties are peers and must approve code. A packaged clean room extends privacy to the entire analysis: one party (LiveRamp, the identity provider) ships the analysis as a product; the customer runs it against its own data — no approval step, and neither party sees the other's data assets at all (not even table names or schemas).
- Architecture: three components — LiveRamp (identity resolution data + code: notebooks, JARs), the customer (creates the room, adds input/config tables, triggers runs, receives results), Databricks (hosts and isolates the clean room; its creator is billed for compute).
- Central clean room: Databricks-managed, separate from both parties' workspaces, no admin access for either side; created in the customer's chosen cloud/region (egress mitigation); serverless compute per run, released when done, scales vertically and horizontally; each party's assets are shared read-only via OpenSharing; SecureConnect proxies access for storage-firewalled/private-endpoint tables.
- OpenSharing (formerly Delta Sharing) grants read-only access without copying; shares live tables (runs read the current version, not last week's extract); keeps Unity Catalog governance on both sides with audited sharing; Databricks-to-Databricks sharing; can share models, unstructured data, JARs, private libraries, wheels.
- Run, step by step: customer creates the LiveRamp packaged clean room in a few clicks; LiveRamp adds its assets after approval (customer sees analysis names, not contents); customer adds an input table of touchpoints (names, emails, phone numbers, addresses or device identifiers) plus attributes and a metadata table in LiveRamp's documented format; selects an output catalog and triggers a run; LiveRamp's code runs serverless in the central room; resolved RampIDs land in the customer's output schema (customer-only read; PII stripped).
- Two output schemas: the output schema (customer-only; shared only on successful completion; LiveRamp cannot read it) and a shared output schema (both parties; run metrics and diagnostic logs; shared during the run regardless of final status). Both are delivered via OpenSharing to customer- and provider-owned environments (Catalog Explorer → Shares received).
- Identity resolution fits packaged clean rooms because the split protects both sides: LiveRamp's identity graph and matching logic stay its IP, invisible to the customer; the customer's PII and resolved results stay private to the customer.

## Details

- Packaged clean rooms scale: one package offered to many customers, each in a separate room, each getting a turnkey run with nothing to review — simpler than approval-based rooms for repeatable identity workloads.
- Results feed downstream Unity Catalog work: customer 360 tables, audience building, activation, partner collaboration, and measurement.
