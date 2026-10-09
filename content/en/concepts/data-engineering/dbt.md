---
title: "dbt: Data Build Tool"
description: "SQL-first transformation framework: models, tests, snapshots, incremental builds, mesh, and semantic layer"
tags: [concept, data-engineering, dbt, sql, transformation, elt]
locale: en
published: 2026-09-07
---

# dbt: Data Build Tool

> Read this page in Korean: [/ko/concepts/data-engineering/dbt](/ko/concepts/data-engineering/dbt)

**dbt (data build tool)** is a SQL-first transformation framework: analysts and engineers write `SELECT` statements (templed with Jinja), and dbt compiles them into DDL/DML, manages run order from a dependency graph, tests outputs, and documents everything. It owns the Transform inside ELT (see [[etl-vs-elt|ETL vs ELT]]), running inside the warehouse rather than on separate compute.

## Why dbt Won the Warehouse

Before dbt, warehouse SQL lived in stored procedures, BI-tool extracts, or orchestration scripts: untested, unordered, undocumented. dbt applies software-engineering discipline to that SQL:

- **Modularity**: every transformation is a versioned file with explicit `ref()` dependencies; dbt topologically orders execution.
- **Testability**: schema and data tests run in CI on every pull request.
- **Documentation**: descriptions in schema YAML compile into a browsable docs site with lineage.
- **Environment parity**: the same project builds `dev_yourname` schemas on branches and production schemas on merge, so review happens against real query results.

## Core Concepts

### Models

A model is a `.sql` file with a single SELECT; dbt materializes its result as a relation. Materialization strategies:

| Strategy | What it does | Use when |
|----------|--------------|----------|
| `view` | Creates a view | Tiny, always-fresh logic |
| `table` | Full rebuild CTAS | Small to medium dimensions |
| `incremental` | Appends or merges new rows only | Large fact tables, event streams |
| `ephemeral` | Inlines as CTE into dependents | Intermediate logic, no persistence |
| `snapshot` | Type-2 slowly-changing-dimension history | Auditing dimension changes |

Incremental models carry a predicate like "only rows newer than the current max timestamp" plus a merge strategy; getting the unique key and merge behavior right is the single highest-leverage dbt skill.

### Refs, Sources, and Seeds

- `ref('stg_orders')` points at another model; dbt resolves schema names per environment and builds the DAG.
- `source('shop', 'orders')` declares raw upstream tables with freshness checks, separating what you own from what you inherit.
- `seeds` load small CSVs (country codes, mappings) as versioned tables; `snapshots` implement type-2 SCD with timestamp or check strategies.

### Tests

Schema tests (`unique`, `not_null`, `accepted_values`, `relationships`) declare invariants in YAML; singular tests are custom SQL returning violating rows (zero rows means pass). Run tests in CI per PR and as a production job after the build; store test failures as queryable artifacts so data-quality incidents start from evidence.

### Jinja and Macros

Jinja templating adds loops, conditionals, and variables over SQL (pivot generation, environment-aware logic). Macros package reusable SQL patterns (a cents-to-dollars cast, a surrogate-key generator) into tested libraries; the `dbt_utils` package supplies a battle-tested standard set. Discipline matters: heavy Jinja obscures the query plan, so keep generated SQL explainable.

## Layered Project Shape

The conventional layering keeps dependencies flowing one way:

1. **Staging** (`stg_`): 1:1 with sources, renames and type casts only, no joins.
2. **Intermediate** (`int_`): joins, pivots, and complex logic broken into auditable steps.
3. **Marts** (`fct_`/`dim_`): Kimball-style facts and dimensions, the BI contract.
4. **Exposure**: documented dashboards and reverse-ETL consumers pinned to mart versions.

Selectors (`dbt build --select marts+`) then rebuild exactly one layer and its ancestors.

## Advanced Surface

- **Mesh**: multi-project setups where a core project publishes *public* models under contracts, and domain projects consume them as cross-project refs with enforced versioning.
- **Semantic layer**: MetricFlow definitions (metrics, entities, dimensions) compile to governed SQL, so "revenue" means one thing in every dashboard.
- **State-aware CI**: `dbt build --select state:modified+` on pull requests rebuilds only changed models and their children against production-comparable data, keeping CI minutes bounded as projects grow past thousands of models.

## Orchestration and Compute Fit

dbt is not a scheduler: production runs trigger from [Airflow](/en/concepts/data-engineering/apache-airflow), Dagster, or dbt Cloud jobs, ordered after ingest completes (often signaled by CDC streams or file sensors). Compute stays in the warehouse ([[apache-spark|Spark]] SQL and Trino cover non-warehouse engines), so dbt cost management equals warehouse cost management: incremental discipline, partition pruning, and retiring unused marts.

## Production Practices

- Enforce `unique` plus `not_null` tests on every mart primary key; a mart without a tested key is a rumor.
- Require contracts (`contract: {enforced: true}`) on public models so breaking column changes fail CI instead of dashboards.
- Keep full-refresh runs exercised (weekly on a clone) so the day you need one, it works.
- Version and pin adapter and package releases; dbt minor versions move fast.

## References

- dbt documentation: https://docs.getdbt.com/
- Related: [[etl-vs-elt|ETL vs ELT]], [Apache Airflow](/en/concepts/data-engineering/apache-airflow), [[apache-iceberg|Apache Iceberg]]
