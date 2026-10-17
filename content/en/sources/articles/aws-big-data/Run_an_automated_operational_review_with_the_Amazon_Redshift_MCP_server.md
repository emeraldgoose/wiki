---
title: "Run an automated operational review with the Amazon Redshift MCP server"
description: Promoted on 2026-10-17
published: 2026-10-17
source_url: "https://aws.amazon.com/blogs/big-data/run-an-automated-operational-review-with-the-amazon-redshift-mcp-server"
blog: aws-big-data
locale: en
tags: [source, article, en]
---

# Run an automated operational review with the Amazon Redshift MCP server

## Overview

Periodic operational reviews keep a growing Redshift deployment tuned, but manually assembling diagnostics, interpreting results, and writing prioritized reports costs 4–8 hours of specialist effort per cluster — so teams skip them. The `review_cluster` tool in the Amazon Redshift MCP server compresses that into a single natural-language request: it runs curated checks against system views across 12 diagnostic areas, evaluates results against best-practice thresholds, and returns findings with effort-ordered recommendations linked to documentation. The tool is read-only; remediation stays with you.

## What it inspects

The twelve areas span automatic table optimization, unapplied advisor recommendations, COPY/Spectrum ingestion efficiency, materialized view health, node and storage utilization, statistics/vacuum/skew/encoding, slow queries and nested loops, workload usage patterns, WLM configuration, deployment-model fit, and serverless AI-scaling range. Four checks are provisioned-only and one is serverless-only, so a provisioned cluster evaluates 11 areas and a serverless workgroup 8. A sample review surfaced missing statistics, distribution alerts, nested loops, sort-key and distribution misconfigurations, and scaling tuning, ordered from a low-effort ANALYZE up to QMR rules.

## Running reviews and acting on findings

Prerequisites are an MCP client configured with the Redshift MCP server and the `sys:monitor` role granted to the connecting user; then one prompt starts the review. Findings become an interactive session: ask which tables a finding affects, have the agent draft the ALTER TABLE statements, or discuss trade-offs of architectural moves like serverless migration. Recommendations split into quick config changes, batch table operations, upstream ingestion fixes, and architectural decisions. Best practice is weekly or event-triggered cadence (schema changes, big loads, pre-peak), starting with low-effort wins and using before/after reviews as a baseline.

## References

- [Original post: Run an automated operational review with the Redshift MCP server](https://aws.amazon.com/blogs/big-data/run-an-automated-operational-review-with-the-amazon-redshift-mcp-server)
- [Amazon Redshift MCP server](https://github.com/awslabs/mcp/tree/main/src/redshift-mcp-server)
