---
title: "Branch, sync, serve: What our Lakebase Hackathon taught us about building on Lakebase"
description: "Databricks' Lakebase Hackathon split into branching (Track 1) and syncing/serving (Track 2): Lyft's Jevons Search resolved 10 of 11 support backlogs with copy-on-write branches, CIBC's Branchflight shipped PR preview environments in under five seconds, and Data Axle's PriceWise served pricing responses in as little as 4 ms."
tags: [source, article, databricks, lakebase, postgres, hackathon, en]
locale: en
source_url: "https://www.databricks.com/blog/branch-sync-serve-what-our-lakebase-hackathon-taught-us-about-building-lakebase"
blog: databricks
published_date: 2026-11-19
---

# Branch, sync, serve: What our Lakebase Hackathon taught us about building on Lakebase

**Source**: [Databricks Blog](https://www.databricks.com/blog/branch-sync-serve-what-our-lakebase-hackathon-taught-us-about-building-lakebase)
**Published**: 2026-11-18

## Overview

Databricks ran a Lakebase Hackathon open to a wider customer group than ever. Lakebase is fully managed Postgres with storage separated from compute, living next to lakehouse data under Unity Catalog governance. It enables three things ordinary Postgres cannot easily do: branch (copy-on-write database branches like Git branches, instant, no production impact), sync (synced tables continuously copy Unity Catalog tables into Postgres as read-only tables — reverse ETL — and Lakehouse Sync replicates Postgres back to Delta via CDC), and serve (hold application state, pgvector/PostGIS/pg_trgm search, online store for Online Feature Stores). Track 1 covered branching and app building; Track 2 covered syncing and serving. Unity Catalog governs access underneath both tracks.

## Key points

- Lyft's Jevons Search: agents that issue refunds/cancel bookings without knowing DB business rules (triggers). Each batch of support tickets forks a copy-on-write branch of production in ~6 seconds; a lightweight gte-large embedding classifier (tracked in MLflow, served on Model Serving) sorts tickets into eight policy categories with no LLM tokens at runtime. Planning up front fully resolved 2 of 11 backlogs within policy; testing on branches resolved 10 of 11. Forking fast enough to score 4x more branches did not produce more passes — precise decisions plus real database feedback beat brute force.
- CIBC's Branchflight: every pull request gets a preview environment — a zero-copy Lakebase branch from a PII-masked template branch in under five seconds, deploying a preview Databricks App; environments scale to zero, expire automatically, pass a schema-diff check before merge; platform state, audit logs, and cost metrics also live in Lakebase.
- Arbital Health's 7NF benchmark: keeps data fixed and varies schema, each layout its own Lakebase branch; models graded only on returning correct rows — a way to pick the best schema for a customer database or improve text-to-SQL.
- Other branching projects: OneTrust used Lakebase branches to test firewall-rule changes (Go app, copy-on-write branch with dedicated compute, recursive reachability queries; trial runs expanding attack surface were discarded instantly); a second CIBC team built BranchCut, a 3D cinematic workspace with Git-style branching/merging for creative work; Reach Mobile built StreetCart (price/distance/stock comparison; branching to test new category attributes before production schema changes); Markel serves claims/underwriting/call-center reads from governed gold tables through Lakebase instead of a separate Elasticsearch copy.
- Data Axle's PriceWise (Track 2): 18,000+ listings; estimated hosts leave ~64% of potential nightly revenue on the table. Hybrid search (pgvector embeddings + BM25 fused with Reciprocal Rank Fusion), pricing suggestions driven by four demand drivers including PostGIS comparisons of listings within 20 miles, and an embedded Genie agent; Genie conversations saved in Lakebase as agent memory; pricing responses in as little as 4 ms.
- A transportation company synced flight/airport/weather-alert tables from Unity Catalog into Lakebase to power a live map in a Databricks App; an insurance company applied risk scoring after policy issuance (inspector findings prediction).
- Synced tables move curated Unity Catalog data into Lakebase Postgres via managed Spark Declarative Pipelines; Lakebase Change Data Feed streams Postgres changes back to Delta; Online Feature Stores run on Lakebase so lakehouse features serve models in real time.

## Details

- Hackathons start with an enablement session, then about a week of building; strongest solutions win prizes.
- Lakebase branches are instant via copy-on-write; you pay only for changed data and creating a branch has no performance impact on production.
- Every Lakebase project starts with a production branch; child branches serve development, testing, or experiments, and teams built with Genie Code treating branches as cheap disposable copies of production.
