---
title: "How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway"
description: "Concurrence's governed healthcare AI stack — immutable event-sourced patient state, pre-production simulation, compliance-gated routing, and Unity Gateway for all AI access."
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway"
blog: databricks
published_date: 2026-09-23
---

# How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway

**Source**: [Databricks Blog](https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway) · **Published**: 2026-09-23

## Overview

Clinical AI company Concurrence now processes about 100B input tokens and 11M LLM calls per 30 days (roughly a 1.2T annualized run rate, up 5x in under a year) across patient- and provider-facing agents. Its Databricks foundation — Zerobus ingestion into Delta, Declarative Pipelines deriving a world-model patient state, Lakebase for operational state, Unity Catalog for governance, Unity Gateway for AI access — keeps reliability and compliance intact at that scale.

## Trusted data and pre-production testing

Instead of overwriting records, Concurrence logs immutable events and computes current patient state with full provenance, so agents see consistent context and learnings feed back into future workflows. Because state derives from replayable history, every agent is tested against simulated patients first — simulation traffic runs about 7x production — with traces, clinical data, and ai_query-scored evaluations sharing one governed foundation so regressions trace to model, data, or workflow.

## Compliance-gated governance and unified AI access

Each customer gets its own schema and service principal under Unity Catalog; batch workloads run on BAA-covered Databricks-hosted models with an endpoint resolver that blocks PHI from reaching uncovered models, and routing is compliance-gated before it is cost-gated. Coding-agent traffic already flows through Unity Gateway's `ug` CLI (61B cumulative tokens, 360K requests, identity-level attribution and centrally managed MCP access), with real-time inference feature-flagged behind a synthetic canary until coverage allows cutover. The compounding payoff: each interaction enriches shared patient state, lowering the marginal cost of the next workflow.

## References

- [How Concurrence governs clinical AI at a trillion-token scale with Unity Gateway](https://www.databricks.com/blog/how-concurrence-governs-clinical-ai-trillion-token-scale-unity-gateway)
