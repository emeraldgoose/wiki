---
title: "Dagster"
description: "Asset-centric data orchestrator: software-defined assets, ops and jobs, sensors, I/O managers, and dbt integration"
tags: [concept, data-engineering, dagster, orchestration, data-assets]
locale: en
published: 2026-09-07
---

# Dagster

> Read this page in Korean: [/ko/concepts/data-engineering/dagster](/ko/concepts/data-engineering/dagster)

**Dagster** is an open-source data orchestrator built around *software-defined assets*: instead of declaring tasks and their order, you declare the data artifacts you want (tables, files, models) and the code that produces them, and Dagster derives the dependency graph, schedules computation, and tracks lineage.

## The Asset-First Inversion

Task-centric orchestrators such as [Apache Airflow](/en/concepts/data-engineering/apache-airflow) ask "what steps run, in what order?" Dagster asks "what data should exist, and how is each piece computed?" An `@asset` function returns a dataframe or writes a table; its upstream dependencies are inferred from function arguments naming other assets. Benefits:

- **Lineage for free**: the asset graph is the lineage graph, visible in the UI without extra instrumentation.
- **Partial execution**: request one asset and Dagster computes exactly its ancestors; re-materialize one stale asset without rerunning the world.
- **Data-aware scheduling**: freshness policies and asset checks trigger work when data is missing or stale, not merely when the clock ticks.

Ops and jobs (the legacy task-centric API) still exist for imperative workflows, but new projects should default to assets.

## Core Concepts

### Assets and Asset Graphs

An asset is a persistent object (a warehouse table, a Parquet file, an ML model) plus the function materializing it. Assets group into *asset groups* or *domains* by team or storage system. Multi-assets let one computation yield several tables atomically (e.g. a CDC batch producing both a raw and a cleaned table).

### Declarative Automation

Schedules, sensors, and *automation conditions* declare when assets materialize: cron schedules for batch cadences, sensors polling external state (file arrival, Kafka lag, dbt Cloud job completion), and declarative conditions like "run when all parents are newer than me" that replace hand-written sensor logic.

### I/O Managers and Resources

- **I/O managers** handle how asset values are stored and loaded: the default in-memory manager suits tests, while production uses warehouse-backed managers (Snowflake, BigQuery) or object-store managers (S3 pickle/Parquet). Swapping managers moves a pipeline from laptop to cloud without touching asset code.
- **Resources** inject external clients (database connections, API sessions, Spark contexts) with lifecycle management and per-environment configuration, keeping credentials out of asset logic.

### Asset Checks and Freshness

Asset checks are data-quality assertions attached to assets (null-rate below threshold, row-count within bounds, primary-key uniqueness), evaluated on each materialization and surfaced in the UI. Combined with freshness policies ("this asset must be newer than 2 hours"), they turn the orchestrator into a continuous data-quality monitor rather than a blind scheduler.

## Dagster Versus Airflow

| Dimension | Dagster | Airflow |
|-----------|---------|---------|
| Primary abstraction | Data assets | Tasks and DAG order |
| Lineage | Native from asset graph | Via provider extras |
| Local development | `dagster dev` full UI locally | Needs full stack or stubs |
| Partial rerun | Native asset selection | Manual task clearing |
| Ecosystem | Younger, growing fast | Largest provider library |

Choose Dagster when lineage, local iteration speed, and data-aware triggering dominate; choose Airflow when you need its vast provider catalog or an established team skill base. Both orchestrate [[apache-spark|Spark]] jobs, dbt builds, and [[stream-processing|streaming]] tasks rather than replacing those engines.

## dbt Integration

The `dagster-dbt` package loads a dbt project manifest and creates one Dagster asset per dbt model, seed, and snapshot, so the warehouse layer appears inside the same asset graph as ingest and ML steps. Practical consequences: a single lineage view from raw API extract through dbt marts, upstream ingest failures blocking dbt runs automatically, and dbt tests surfacing as Dagster asset checks.

## Deployment Shape

Dagster separates *code locations* (user servers exposing asset definitions) from the *webserver/daemon* (UI, scheduler, sensors) and *run launchers* (where compute happens: local process, Docker, Kubernetes, or serverless). This split lets platform teams host the control plane once while product teams deploy code locations independently. State lives in PostgreSQL (production) or SQLite (local dev); object storage backs inter-asset artifacts and logs.

## Production Practices

- **Separate dev and prod**: branch deployments materialize assets to prefixed schemas so a feature branch never overwrites production tables.
- **Backfills with partitioning**: partition assets by date or key, then launch bounded backfills with concurrency limits instead of one giant run.
- **Observe asset health**: dashboards on materialization delay, check-pass rate, and sensor tick skip rate catch drift before stakeholders do.
- **Test assets as functions**: because assets are plain functions with injected resources, pytest can call them with fakes, no cluster needed.

## References

- Dagster documentation: https://docs.dagster.io/
- Related: [Apache Airflow](/en/concepts/data-engineering/apache-airflow), [[etl-vs-elt|ETL vs ELT]], [[stream-processing|Stream Processing]]
