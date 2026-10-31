---
title: "Lakebase branching for CI/CD: lessons from 100 PR databases"
description: "How Snorkel AI uses copy-on-write Lakebase Postgres branches to give each pull request an isolated database for CI/CD, cutting environment provisioning from minutes to seconds."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases"
blog: databricks
published_date: 2026-10-31
---

# Lakebase branching for CI/CD: lessons from 100 PR databases

**Source**: [Databricks Blog](https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases) · **Published**: 2026-10-31

## Overview

Snorkel AI builds data development tools for AI teams, used by expert data annotators and frontier model providers. Its engineers ship code through a CI pipeline running on Kubernetes, where every open pull request and ad-hoc commit gets its own ephemeral namespace used to deploy the branch and run the full test suite before merging. Those tests are most valuable when they run against real data, and Snorkel's production database was an Amazon Aurora PostgreSQL cluster, so each PR namespace needed its own copy of production data. Restoring a copy took about 20 minutes per environment, which is too slow when developers open PRs throughout the day and the merge queue needs a fresh environment for each run.

After moving production to Databricks Lakebase Postgres, Snorkel replaced the restore step with copy-on-write branches. A new PR branch is ready in under 60 seconds at p95, presents itself as a standard Postgres database, and supports the existing application and CI suite with performance comparable to Aurora, including large JSONB and LOB columns. Because branching is copy-on-write, roughly 100 concurrent PR branches on a production dataset of about 2.5 TB only add storage for the data each branch actually changes, while branch TTLs automatically clean up environments once the PR is closed or merged.

## Key points

- Lakebase gives every pull request its own isolated, read/write Postgres copy of production data that is ready in under a minute instead of roughly 20 minutes.
- Copy-on-write branching keeps concurrent PR databases economical: about 100 branches on a ~2.5 TB dataset only consume storage for changed data.
- Automatic branch expiration (TTL) cleans up each PR database when its pull request is closed or merged.
- Existing CI and application code run unchanged because Lakebase exposes a standard Postgres interface with performance comparable to Aurora.
- The write path supports large objects, including JSONB and LOB columns, so realistic data shapes survive the migration from Aurora.
- Private connectivity and Okta SSO support a governed, secure environment for the PR databases.

## Details

The article is a case study of Snorkel AI's CI/CD migration. Before Lakebase, provisioning a realistic test database was the bottleneck: each environment required restoring a snapshot of the production Aurora cluster, consuming roughly 20 minutes. Lakebase's branch creation reduces that to less than 60 seconds, which lets the team treat realistic end-to-end tests as a normal part of the pull request lifecycle rather than a scarce resource. Storage efficiency comes from copy-on-write semantics, so concurrent branches only diverge from the parent where they are written to. Operational guardrails include TTL-based expiry for ephemeral branches and private networking with Okta SSO for access control. The migration keeps the application on Postgres over standard drivers, so query behavior, including large JSONB and LOB payloads, carries over without rewriting test code.

## References

- Original article: [Lakebase branching for CI/CD: lessons from 100 PR databases](https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases)
