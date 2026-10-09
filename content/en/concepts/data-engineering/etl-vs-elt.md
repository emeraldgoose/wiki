---
title: ETL vs ELT
description: "Extract-Transform-Load versus Extract-Load-Transform: definitions, trade-offs, and when to use each"
tags: [concept, data-engineering, etl, elt, data-warehouse]
locale: en
published: 2026-09-07
---

# ETL vs ELT



**Summary:** ETL (Extract-Transform-Load) transforms data **before** loading it into the warehouse, while ELT (Extract-Load-Transform) loads raw data **first** and transforms it inside the destination platform. ETL fits strict schemas, legacy warehouses, and regulated pipelines; ELT fits cloud warehouses and lakehouses where storage is cheap and compute is elastic. The choice shapes cost, latency, debuggability, and who can change the logic.

## Definition

- **ETL:** Extract data from sources, Transform it in a dedicated processing engine (clean, join, aggregate, conform to a schema), then Load the finished tables into the warehouse. The warehouse receives curated data only.
- **ELT:** Extract data from sources, Load it raw (or near-raw) into the destination (cloud warehouse, data lake, lakehouse), then Transform it there with SQL or SQL-based tools. The raw layer is preserved.
- **The real difference** is *where* transformation compute happens and *whether raw history survives*. ETL discards raw detail at the gate; ELT keeps it and transforms on demand.
- **Related variants:** EtLT (light staging transform, then main transform in-warehouse), reverse ETL (warehouse → operational SaaS tools), and zero-ETL (federated/query-in-place integrations sold by cloud vendors).

## Why It Matters

- **Cost structure.** ETL pays for a separate transformation cluster (always-on Informatica, SSIS, or Spark jobs). ELT shifts that spend to warehouse compute, which scales per query — cheaper at low volumes, spiky at high ones.
- **Agility.** In ELT, adding a column means re-running a SQL model over retained raw data. In ETL, it means changing the pipeline, redeploying, and often re-extracting history from sources that may no longer have it.
- **Compliance and privacy.** ETL can mask PII *before* it lands anywhere analysts can query — a hard requirement in some regulated shops. ELT must instead enforce masking through views, policies, or deletion from raw zones.
- **Debuggability.** ELT's raw layer is a replayable audit trail: when a metric looks wrong, you can trace it back to untouched source snapshots. ETL pipelines that drop raw data force you to reproduce bugs from source systems.

## How It Works

### ETL pipeline (concrete example)

Nightly sales reporting from Postgres + a CSV dump into a legacy warehouse:

1. **Extract:** Sqoop or a Python job pulls `orders` changed since yesterday (`WHERE updated_at > :watermark`) plus the partner CSV over SFTP.
2. **Transform (in Spark):** normalize currencies to USD, deduplicate on `order_id`, join to a conformed `dim_customer`, reject rows with null `amount` into a quarantine table.
3. **Load:** bulk-insert finished `fact_orders` into the warehouse; analysts see only the clean table.

```python
# Simplified ETL transform step (runs before anything reaches the warehouse)
clean = (
    orders.dropna(subset=["amount"])
          .drop_duplicates(subset=["order_id"])
          .merge(fx_rates, on="currency", how="left")
          .assign(amount_usd=lambda d: d["amount"] * d["rate"])
)
clean.to_sql("fact_orders", warehouse_engine, if_exists="append", index=False)
```

### ELT pipeline (concrete example)

Clickstream + Postgres into Snowflake/BigQuery with dbt:

1. **Extract + Load:** Fivetran/Airbyte copies raw tables (`raw.orders`, `raw.events`) into the warehouse on a schedule; files land in object storage as JSON/Parquet first if volume is high.
2. **Transform (in-warehouse SQL):** staged dbt models build `stg_orders` (renamed, type-cast), then `marts.fact_orders` (joined, aggregated). Each layer is a view or table *inside* the warehouse.

```sql
-- dbt-style ELT: raw data already in the warehouse, transform with SQL
with stg as (
    select
        id::bigint            as order_id,
        lower(email)          as email,
        (payload:amount)::numeric as amount
    from raw.orders
)
select o.order_id, c.customer_key, o.amount * f.rate as amount_usd
from stg o
left join marts.dim_customer c on c.email = o.email
left join marts.fx_rates f on f.currency = o.currency;
```

### Side-by-side comparison

| Dimension | ETL | ELT |
|-----------|-----|-----|
| Transform location | Outside, before load | Inside the destination |
| Raw data retained | Usually no | Usually yes |
| Best destination | Legacy warehouse, strict schema | Cloud warehouse, lake, lakehouse |
| Schema approach | Schema-on-write | Schema-on-read (flexible) |
| Latency profile | Batch windows, heavier orchestration | Near-real-time possible (micro-batch loads + SQL) |
| Who transforms | Data engineers (Python/Spark/Java) | Engineers + analysts (SQL/dbt) |
| Main risk | Lost history, rigid changes | Runaway compute cost, messy raw sprawl |

## Pitfalls

- **Treating ELT as "no modeling."** Dumping raw tables without staged models produces a swamp of duplicated, conflicting SQL. ELT still needs modeling discipline (see [[concepts/data-engineering/data-modeling|Data Modeling]]).
- **Surprise warehouse bills.** A dbt model with a full-refresh over billions of rows, run hourly by accident, is the classic ELT cost incident. Use incremental models, clustering keys, and cost alerts.
- **PII in the raw zone.** Loading everything raw means emails and card tokens sit in storage before any masking. Pair ELT with column masking policies, short raw retention, or pre-load hashing for sensitive fields.
- **ETL's point of no return.** Aggregating away detail before loading (e.g., daily rollups only) permanently destroys drill-down ability. Keep a raw archive even in ETL designs.
- **Vendor "zero-ETL" hype.** Federated queries still move data and still cost; they just hide the pipeline. Measure the query bill before deleting your loaders.

## Related Concepts

- [[concepts/data-engineering/data-modeling|Data Modeling]] — staging and mart design for the Transform step
- [[concepts/data-engineering/batch-vs-stream|Batch vs Stream]] — latency choices for the pipeline
- [[concepts/data-engineering/orchestration-basics|Orchestration Basics]] — scheduling and dependency management
- [[concepts/data-engineering/cdc-change-data-capture|CDC (Change Data Capture)]] — low-latency extraction for both patterns
- [[concepts/data-engineering/data-quality|Data Quality]] — tests and contracts on transformed outputs

## References

- Ralph Kimball and Margy Ross, *The Data Warehouse Toolkit* (3rd ed., Wiley) — dimensional modeling behind the Transform step.
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly) — batch/stream foundations; see also https://dataintensive.net
- AWS, "What is ETL?": https://aws.amazon.com/what-is/etl/
- Google Cloud, "What is ETL?": https://cloud.google.com/learn/what-is-etl
- Snowflake, "ETL vs ELT": https://www.snowflake.com/guides/etl-vs-elt/
- dbt documentation: https://docs.getdbt.com/
