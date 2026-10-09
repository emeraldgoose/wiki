---
title: Accelerating Spark queries with Iceberg materialized views
description: How automatic query rewrite with Iceberg materialized views reduces Apache Spark query execution time without changing SQL, using precomputed results from the AWS Glue Data Catalog.
date: 2026-09-10
tags: [aws, data-engineering, spark, iceberg, materialized-views, query-optimization]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/"
blog: aws
---

# Accelerating Spark queries with Iceberg materialized views

**Authors**: AWS Big Data Blog · **Published**: Sep 10, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/)

## Query modification approach comparison

| Approach | Stored results | Refreshes | Modification to existing queries |
|---|---|---|---|
| Standard views in AWS Glue | No (re-runs each time) | n/a | Required |
| Custom ETL pipeline | Yes | Manual | Required |
| Hand-rolled rewrite | Yes | Manual | Required |
| Materialized views with automatic rewrite enabled | Yes | Automatically through AWS Glue Data Catalog on a schedule when configured | Not required when supported |

## Prerequisites

To use automatic query rewrite with Iceberg materialized views, you need:

* Amazon EMR release 7.12.0 or later, or AWS Glue 5.1 or later.
* Source tables in Apache Iceberg or Parquet format, registered in the AWS Glue Data Catalog, in the same AWS Region and account as the materialized view. Parquet source tables are supported for automatic query rewrite starting with Amazon EMR 7.14.0 and AWS Glue 8.1.
* An Amazon Simple Storage Service (Amazon S3) Tables bucket, or an S3 general purpose bucket, for the materialized view data.
* Permissions for the definer role. You can use AWS Identity and Access Management (IAM) policies or AWS Lake Formation.
* Automatic query rewrite turned on in your Spark session: `--conf spark.sql.optimizer.answerQueriesWithMVs.enabled=true`.
* For Parquet source tables, set `spark.sql.materializedView.v1SourceTables.enabled=true` and `spark.sql.materializedView.v1ETagVersioning.enabled=true`.

## How it works

* **You define a SQL query** with aggregations, joins, or filters across your supported source tables.
* **AWS Glue Data Catalog stores the precomputed results** as an Apache Iceberg table in your [Amazon S3](/s3/) bucket. You can store it in a general purpose S3 bucket or in [Amazon S3 Tables](/s3/features/tables/). Any Apache Iceberg-compatible query engine can read the materialized view, including [Amazon Athena](/athena/), Amazon EMR, AWS Glue, [Amazon Redshift](/redshift/), and Iceberg-compatible third-party query engines. Automatic query rewrite is available on the AWS optimized Spark runtime in Amazon Athena, Amazon EMR, and AWS Glue. Other engines can query the materialized view directly, but they don't rewrite queries to use it automatically.
* **Automatic refresh keeps the MV current** on a schedule that you define, for example `SCHEDULE REFRESH EVERY 1 DAY`. You set it at creation time or later with `ALTER MATERIALIZED VIEW ... ADD SCHEDULE REFRESH`. At that scheduled time, the refresh process checks the current Apache Iceberg snapshot ID or Parquet file ETags and refreshes the MV when it detects source-table changes.
* **Automatic query rewrite redirects matching queries to** the MV at query optimization time. Automatic query rewrite in Apache Spark uses two matching strategies:
  + **Structural rewrite** (adapted from Amazon Redshift) handles an MV defined as a single SELECT-FROM-WHERE-GROUP-BY block over INNER joins. The optimizer can roll up an MV's aggregates to a coarser grain and pull extra query predicates up onto the MV scan.
  + **Exact-match rewrite** handles MVs defined as other shapes, such as window functions and outer joins, by matching a canonicalized form of the MV body against subtrees of the query plan.

When the optimizer evaluates a query, it consults a metadata cache of MVs from the configured catalogs and chooses the best match. It also checks MV staleness during optimization. It skips stale MVs, so rewrite won't return stale results. If no MV matches, the original query runs unchanged.

## Example: One query with three potential MVs

Consider a typical analytics query: **"Top 100 preferred US customers by total store spending."** It joins fact and dimension tables, applies two selective filters on the customer dimension, aggregates per customer, ranks the result with a window function, and keeps only the top 100:

```sql
SELECT c_customer_id, total_revenue, num_transactions, avg_purchase, revenue_rank FROM ( SELECT cust.c_customer_id, SUM(sales.ss_quantity * sales.ss_sales_price) AS total_revenue, COUNT(*) AS num_transactions, AVG(sales.ss_quantity * sales.ss_sales_price) AS avg_purchase, RANK() OVER (ORDER BY SUM(sales.ss_quantity * sales.ss_sales_price) DESC) AS revenue_rank FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_birth_country = 'UNITED STATES' AND cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id ) ranked WHERE revenue_rank <= 100 ORDER BY revenue_rank;
```

**Query 1**: The original query. Top 100 preferred US customers by total store spending, before any materialized view.

Three MV designs cover progressively more of this query, from a single-table pre-aggregate to the full query body itself:

### Tier 1: Pre-aggregate store_sales only, no join, no filter.

This tier is a single-table aggregate of `store_sales` at customer-surrogate-key grain. The query still must join the `customer` table, apply both filters, re-aggregate at `c_customer_id` grain, and run the window function.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_1 AS SELECT ss_customer_sk, SUM(ss_quantity * ss_sales_price) AS sum_revenue, COUNT(ss_quantity * ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales GROUP BY ss_customer_sk;
```

*Tier 1 MV: Single-table pre-aggregate of store_sales by customer surrogate key (no join, no filter).*

**Plan comparison:**

*Plan 1: Original plan.* Scans the large store_sales table.

*Plan 2: Rewritten plan (Tier 1).* Reads the pre-aggregated customer_tier_1 MV. The optimizer rolls up aggregates from the MV and applies residual filters.

### Tier 2: Pre-join store_sales x customer, pre-apply one filter (c_preferred_cust_flag = 'Y').

The middle tier pre-joins both tables and bakes in the preferred-customer filter. The query still must apply the country filter as a residual on the MV scan and run the RANK() window function.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_2 AS SELECT cust.c_customer_id, cust.c_birth_country, SUM(sales.ss_quantity * sales.ss_sales_price) AS sum_revenue, COUNT(sales.ss_quantity * sales.ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id, cust.c_birth_country;
```

*Tier 2 MV: Pre-joins store_sales and customer, with the preferred-customer filter applied.*

**Rewritten query plan:** Country filter applied as a residual on the MV scan.

### Tier 3: Full query pre-join with both filters.

This tier pre-joins both tables and applies both filters, so the query only needs to run the window function on the pre-filtered result.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_3 AS SELECT cust.c_customer_id, cust.c_birth_country, SUM(sales.ss_quantity * sales.ss_sales_price) AS sum_revenue, COUNT(sales.ss_quantity * sales.ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_birth_country = 'UNITED STATES' AND cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id;
```

*Tier 3 MV: Full pre-join with both country and preferred-customer filters.*

**Rewritten query plan:** Only the window function runs on the residual data.

## Key benefits

* **Single job**: No need to manage multiple coordinated jobs or orchestration infrastructure.
* **Automatic dependency resolution**: SDP resolves execution order from dataset references.
* **Unified data catalog**: All datasets land in Glue Data Catalog, queryable via Athena.
* **Reduced operational complexity**: No manual DAG wiring, retry logic, or checkpoint management.

## Getting started

1. Launch an Amazon EMR 7.12.0+ cluster or an AWS Glue 5.1+ job.
2. Create an MV over your most expensive repeating query using `CREATE MATERIALIZED VIEW` in the AWS Glue Data Catalog.
3. Turn on automatic query rewrite by setting `spark.sql.optimizer.answerQueriesWithMVs.enabled=true` in your Spark session configuration.
4. Verify the rewrite by inspecting the optimized query plan for an MV scan node, or by checking INFO-level logs on Amazon EMR 7.14.0+.

Queries with multi-table joins, heavy aggregations, or window functions over large fact tables are strong initial candidates. Start with one high-cost, frequently executed query. Validate the speedup, then expand to broader MVs as you identify shared patterns across your workload.

## References

* [Using materialized views with Amazon EMR](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-materialized-views.html).
* [Using materialized views with AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/materialized-views.html).
* [Querying materialized views in Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-gdc-mv.html).
* [Introducing Apache Iceberg materialized views in AWS Glue Data Catalog](/blogs/big-data/introducing-apache-iceberg-materialized-views-in-aws-glue-data-catalog/).
* [Materialized views in AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/materialized-views.html).
* [How to use streamlined permissions for Amazon S3 Tables and Iceberg materialized views](/blogs/big-data/how-to-use-streamlined-permissions-for-amazon-s3-tables-and-iceberg-materialized-views/).

## About the authors

### Resources

* [Amazon Athena](/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon EMR](/blogs/big-data/category/analytics/amazon-emr?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Kinesis](/blogs/big-data/category/analytics/amazon-kinesis?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon MSK](/blogs/big-data/category/analytics/amazon-managed-streaming-for-apache-kafka/)
* [Amazon QuickSight](/blogs/big-data/category/analytics/amazon-quicksight?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Redshift](/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [AWS Glue](/blogs/big-data/category/analytics/aws-glue?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

### Follow

* [Twitter](https://twitter.com/awscloud)
* [Facebook](https://www.facebook.com/amazonwebservices)
* [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
* [Twitch](https://www.twitch.tv/aws)
* [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)