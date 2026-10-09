---
title: "Apache Airflow"
description: "Workflow orchestration platform: DAGs, scheduler, executors, operators, sensors, and production practices"
tags: [concept, data-engineering, airflow, orchestration, scheduling, dag]
locale: en
published: 2026-09-07
---

# Apache Airflow

> Read this page in Korean: [/ko/concepts/data-engineering/apache-airflow](/ko/concepts/data-engineering/apache-airflow)

**Apache Airflow** is an open-source workflow orchestration platform for authoring, scheduling, and monitoring data pipelines. Pipelines are defined as directed acyclic graphs (DAGs) in Python, scheduled by a central scheduler, and executed as discrete tasks across workers.

## Core Model: DAGs and Tasks

A DAG is a collection of tasks with dependency edges; Airflow guarantees tasks run only after all upstream tasks succeed (or per configured trigger rules). Key properties:

- **Acyclicity**: no cycles allowed, so execution always terminates and the scheduler can topologically order tasks.
- **Python as configuration**: DAG files are Python code, version-controlled, tested, and reviewed like any software. The TaskFlow API (`@dag`, `@task` decorators) lets return values flow between tasks via XComs without boilerplate.
- **Idempotency by design**: each DAG run carries a logical date (`data_interval`), so backfills and retries recompute deterministic partitions rather than mutating shared state.

A minimal DAG looks like this: an extract task pulls rows from an API, a transform task depends on it, and a load task depends on the transform. If the extract fails, nothing downstream runs, and alerting fires on the failed task specifically.

## Architecture

### Scheduler

The scheduler parses DAG files on a loop, creates DAG runs per schedule, and enqueues runnable tasks. It is the brain but not the muscle: it never runs task code itself. Since Airflow 2.x, the HA scheduler can run multiple replicas, and the 3.x line splits the scheduler from the DAG processor for faster parsing at scale.

### Executors

The executor decides *where* task processes run:

| Executor | Runs tasks | Best for |
|----------|-----------|----------|
| LocalExecutor | Local processes | Single-node, small teams |
| CeleryExecutor | Distributed Celery workers | Classic horizontal scale-out |
| KubernetesExecutor | One pod per task | Elastic, isolated, cloud-native |
| Edge / remote | Remote fleets | Hybrid and edge deployments |

Executor choice is the main scalability lever: moving from Local to Celery or Kubernetes takes a deployment from tens to thousands of concurrent tasks.

### Metadata Database and Webserver

All state (DAG runs, task instances, variables, connections, XComs) lives in a metadata database, usually PostgreSQL. The webserver renders the UI (grid view, Gantt, logs) and the REST API from this database. Keep the metadata DB on fast storage with routine vacuuming; a bloated metadata DB is the most common cause of scheduler slowdowns.

## Building Blocks

### Operators

Operators encapsulate one unit of work: `PythonOperator` for callables, `BashOperator` for shell, provider operators (`S3ToRedshiftOperator`, `BigQueryInsertJobOperator`, `KubernetesPodOperator`) for managed services. Prefer deferrable operators for long waits (API polling, cluster spin-up): they release the worker slot while waiting, dramatically raising effective capacity.

### Sensors

Sensors poke an external condition until true (file landed, table partition ready, API status flipped). Always set `poke_interval`, `timeout`, and `mode="reschedule"` so a stuck sensor frees its slot instead of occupying a worker for hours.

### Hooks, Connections, Variables

- **Hooks** wrap external system clients with retry and connection handling; operators are thin wrappers over hooks.
- **Connections** store credentials and endpoints (prefer a secrets backend such as Vault or cloud secret managers over the built-in store).
- **Variables** hold small JSON config; they are not for large data, which belongs in object storage passed by reference.

### XComs

XComs pass small values (IDs, paths, row counts) between tasks. The default backend stores them in the metadata DB, so never push dataframes or file contents through XCom; push an S3 or GCS URI instead. Custom XCom backends can route values to object storage transparently.

## Scheduling Semantics

- **Data intervals, not wall clock**: a daily DAG with interval starting midnight runs *after* the interval closes, so the run labeled 2026-09-06 processes that day complete data.
- **Catchup and backfill**: `catchup=True` creates runs for every missed interval since `start_date`; for historical reprocessing, trigger explicit backfills with `--rerun-failed-tasks` semantics via the CLI or UI.
- **Timetables**: cron presets plus custom timetables for business calendars, multi-cron, or event-driven triggers. Airflow 3 adds first-class event-driven scheduling so object-store events can trigger runs directly.

## Production Practices

- **SLAs and alerts**: set `sla` on latency-critical tasks plus `on_failure_callback` webhooks (PagerDuty, Slack); distinguish retryable errors (transient API 429) from fatal ones via exception handling inside the callable.
- **Pools and priorities**: pools cap concurrency against fragile sources (e.g. max 3 connections to a legacy ERP); `priority_weight` orders tasks when slots are scarce.
- **Testing**: unit-test task callables with plain pytest; DAG integrity tests assert no import errors, no cycles, and owner/sla conventions across all DAG files in CI.
- **Upgrades**: pin provider packages independently of core; read the breaking-change notes per minor, since operator signatures evolve.

## Airflow Versus Neighbors

- Versus [[stream-processing|stream processors]] like [[apache-flink|Flink]]: Airflow orchestrates batch steps on schedules; Flink processes events continuously. They compose (Airflow triggers Flink jobs) rather than compete.
- Asset-centric orchestrators such as Dagster invert the model (define data assets, derive the DAG); Airflow stays task-centric, which fits ETL sequences with complex branching.
- dbt handles SQL transforms inside the warehouse; Airflow orchestrates everything around dbt (ingest before, QA and reverse-ETL after).

## References

- Apache Airflow documentation: https://airflow.apache.org/docs/
- Related: [[etl-vs-elt|ETL vs ELT]], [[stream-processing|Stream Processing]], [[apache-spark|Apache Spark]]
