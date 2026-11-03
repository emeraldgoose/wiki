---
title: "Claude Platform now supports native OpenTelemetry observability in Databricks MLflow"
description: "Databricks MLflow is now a supported destination for native OpenTelemetry export from the Claude Platform, enabling agent tracing and evaluation."
tags: [source, databricks, observability, otel, en]
locale: en
source_url: "https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow"
blog: databricks
published_date: 2026-11-04
---

# Claude Platform now supports native OpenTelemetry observability in Databricks MLflow

**Source**: [databricks](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow) · **Published**: 2026-11-03

## Overview

An agent can return a plausible answer while missing an important finding or repeatedly reading the same source. The answer alone does not explain why. Traces reveal the model and tool calls behind it, allowing teams to investigate failures, find related cases, and test whether a change helps. Databricks MLflow is now a supported destination for native OpenTelemetry export from the Claude Platform. Developers using Anthropic SDKs, the Messages API, and Managed Agents can send native traces to Databricks and use MLflow to debug agents and evaluate changes.

## Key points

- Native OpenTelemetry export for the Claude Platform is in Public Beta.
- Traces can be stored in MLflow under Unity Catalog.
- Trace analysis and MLflow Issues can surface bad answers and repeated tool calls.
- Teams can review answers with domain experts and rerun evaluations with consistent test cases.
- Configuration guidance covers native export, Unity Catalog storage, and issue monitoring.

## Details

The integration brings Anthropic SDKs, the Messages API, and Claude Managed Agents into Databricks MLflow. It supports end-to-end agent observability by preserving trace data in Unity Catalog and by connecting debugging traces to evaluation workflows. Teams can investigate agent behavior, validate changes, and monitor recurring failure patterns over time.

## References

- Article: [Claude Platform native OpenTelemetry in Databricks MLflow](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow)
