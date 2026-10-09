---
title: "Accelerating Spark queries with Iceberg materialized views"
source_url: "https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/"
blog: "AWS Big Data"
published: "2026-09-10"
locale: "en"
---

# Accelerating Spark queries with Iceberg materialized views

In this post, you learn how to reduce [Apache Spark](https://spark.apache.org/) query execution time with [Apache Iceberg](https://iceberg.apache.org/) materialized views without changing a single SQL query.

Organizations running analytical workloads on their data lakes often hit a common wall: queries that are slow and costly, yet difficult to rewrite by hand. Multi-table joins, heavy aggregations, and window functions over large fact tables all drive up execution times, but the SQL behind them often can’t be changed. It might come from [business intelligence (BI)](/what-is/business-intelligence/) dashboards, packaged independent software vendor (ISV) applications, or legacy reports, where editing the source introduces regression risk that outweighs the performance gain.

Starting with [Amazon EMR](/emr/) 7.12.0 and [AWS Glue](/glue/) 5.1, you can accelerate these queries without rewriting them. Automatic query rewrite analyzes the logical plan of each incoming query and compares it against a metadata cache of available MVs. When the optimizer finds a [materialized view (MV)](/what-is/materialized-view/) that satisfies all or part of a query, it rewrites the plan to read from that MV instead of the base tables. Matches can be structural (aggregations and joins) or exact (more complex patterns like window functions). If no MV matches, the original query runs unchanged with no impact on correctness.

If you have previously tried to speed up slow analytical queries, you might have considered one of the following alternatives. Here is how automatic query rewrite compares:

| **Query modification approach** | **Stored results** | **Refreshes** | **Modification to existing queries** |
|---|---|---|---|
| Standard views in AWS Glue | No (re-runs each time) | n/a | Required |
| Custom ETL pipeline | Yes | Manual | Required |
| Hand-rolled rewrite | Yes | Manual | Required |
| Materialized views with automatic rewrite enabled | Yes | Automatically through [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) on a schedule when configured | Not required when supported |

In this post, we:

- Give a high-level overview of how automatic query rewrite works in Apache Spark.
- Walk through a concrete example, showing how the same query can benefit from MVs at different levels of coverage.
- Discuss the trade-offs so you can choose the right MV shape for your workload.

## Prerequisites

To use automatic query rewrite with Iceberg materialized views, you need:

- Amazon EMR release 7.12.0 or later, or AWS Glue 5.1 or later.
- Source tables in Apache Iceberg or Parquet format, registered in the AWS Glue Data Catalog, in the same AWS Region and account as the materialized view. Parquet source tables are supported for automatic query rewrite starting with Amazon EMR 7.14.0 and AWS Glue 8.1.
- An Amazon Simple Storage Service (Amazon S3) Tables (a capability of Amazon S3) bucket, or an S3 general purpose bucket, for the materialized view data.
- Permissions for the definer role. You can use AWS Identity and Access Management (IAM) policies or AWS Lake Formation.
- Automatic query rewrite turned on in your Spark session: `--conf spark.sql.optimizer.answerQueriesWithMVs.enabled=true`.
- For Parquet source tables, set `spark.sql.materializedView.v1SourceTables.enabled=true` and `spark.sql.materializedView.v1ETagVersioning.enabled=true`.
For more Spark configurations, see [Introducing Apache Iceberg materialized views in AWS Glue Data Catalog](/blogs/big-data/introducing-apache-iceberg-materialized-views-in-aws-glue-data-catalog/).

## How it works

Here is how MVs and automatic query rewrite work together:

- **You define a SQL query** with aggregations, joins, or filters across your supported source tables.
- **AWS Glue Data Catalog stores the precomputed results** as an Apache Iceberg table in your [Amazon S3](/s3/) bucket. You can store it in a general purpose S3 bucket or in [Amazon S3 Tables](/s3/features/tables/). Any Apache Iceberg-compatible query engine can read the materialized view, including [Amazon Athena](/athena/), Amazon EMR, AWS Glue, [Amazon Redshift](/redshift/), and Iceberg-compatible third-party query engines. Automatic query rewrite is available on the AWS optimized Spark runtime in Amazon Athena, Amazon EMR, and AWS Glue. Other engines can query the materialized view directly, but they don’t rewrite queries to use it automatically.
- **Automatic refresh keeps the MV current** on a schedule that you define, for example `SCHEDULE REFRESH EVERY 1 DAY`. You set it at creation time or later with `ALTER MATERIALIZED VIEW ... ADD SCHEDULE REFRESH`. At that scheduled time, the refresh process checks the current Apache Iceberg snapshot ID or Parquet file ETags and refreshes the MV when it detects source-table changes.
- **Automatic query rewrite redirects matching queries to** the MV at query optimization time. Automatic query rewrite in Apache Spark uses two matching strategies:
  - **Structural rewrite** (adapted from Amazon Redshift) handles an MV defined as a single SELECT-FROM-WHERE-GROUP-BY block over INNER joins. The optimizer can roll up an MV’s aggregates to a coarser grain and pull extra query predicates up onto the MV scan.
  - **Exact-match rewrite** handles MVs defined as other shapes, such as window functions and outer joins, by matching a canonicalized form of the MV body against subtrees of the query plan.
When the optimizer evaluates a query, it consults a metadata cache of MVs from the configured catalogs and chooses the best match. It also checks MV staleness during optimization. It skips stale MVs, so rewrite won’t return stale results. If no MV matches, the original query runs unchanged.

Note that automatic query rewrite is opt-in: set `spark.sql.optimizer.answerQueriesWithMVs.enabled=true` when creating the Apache Spark session.

## Example: One query with three potential MVs

An MV doesn’t need to cover an entire query to help it. Automatic query rewrite in Apache Spark operates on subtrees: when an MV matches a portion of your query plan, the rewriter substitutes that subtree and lets the rest of the query run on the rewrite output unchanged. The same query can therefore be served by many possible MV designs, each making a different trade-off between per-query speedup, storage cost, and reuse across other queries.

To make this concrete, consider a typical analytics query: **“**Top 100 preferred US customers by total store spending**.”** It joins fact and dimension tables, applies two selective filters on the customer dimension, aggregates per customer, ranks the result with a window function, and keeps only the top 100:

*Query 1: The original query. Top 100 preferred US customers by total store spending, before any materialized view.*

Three MV designs cover progressively more of this query, from a single-table pre-aggregate to the full query body itself:

**Tier 1: Pre-aggregate store_sales only, no join, no filter.** This tier is a single-table aggregate of `store_sales` at customer-surrogate-key grain. The query still must join the `customer` table, apply both filters, re-aggregate at `c_customer_id` grain, and run the window function.

*Tier 1 MV: Single-table pre-aggregate of store_sales by customer surrogate key (no join, no filter).*

The following plans compare the original query plan to the rewritten plan:

```
Window, filter, Sort
+- Aggregate by c_customer_id
:  total_revenue = SUM(ss_quantity * ss_sales_price)
:  num_transactions = COUNT(*)
:  avg_purchase = AVG(ss_quantity * ss_sales_price)
+- Project
   +- Join Inner ON ss_customer_sk = c_customer_sk
      :- BatchScan store_sales <- reads the large store_sales table
      +- Filter c_birth_country='UNITED STATES' AND c_preferred_cust_flag='Y'
         +- BatchScan customer
```

*Plan 1: Original plan. Scans the large store_sales table.*

```
Window, filter, Sort
+- Aggregate by c_customer_id <- rolls up pre-aggregated sums
:  total_revenue = SUM(sum_revenue) <- sum of sum_revenue
:  num_transactions = SUM(num) <- sum of num
:  avg_purchase = SUM(sum_revenue) / SUM(count_revenue) <- sum of sum_revenue / sum of count_revenue
+- Project
   +- Join Inner ON ss_customer_sk = c_customer_sk
      :- BatchScan customer_tier_1 <- reads pre-aggregated MV
      +- Filter c_birth_country='UNITED STATES' AND c_preferred_cust_flag='Y'
         +- BatchScan customer
```

*Plan 2: Rewritten plan (Tier 1). Reads the pre-aggregated customer_tier_1 MV.*

**Tier 2: Pre-join store_sales x customer, pre-apply one filter (c_preferred_cust_flag = ‘Y’).** The middle tier pre-joins both tables and bakes in the preferred-customer filter. The query still must apply the country filter as a residual on the MV scan and run the `RANK()` window.

*Tier 2 MV: Pre-joins store_sales and customer, with the preferred-customer filter applied.*

Rewritten query plan:

```
Window, filter, Sort
+- Aggregate by c_customer_id <- rolls up pre-aggregated sums
:  total_revenue = SUM(sum_revenue) <- sum of sum_revenue
:  num_transactions = SUM(num) <- sum of num
:  avg_purchase = SUM(sum_revenue) / SUM(count_revenue) <- reads pre-aggregated MV
+- Filter c_birth_country='UNITED STATES' [residual filter on MV scan]
   +- BatchScan customer_tier_2 <- reads pre-aggregated MV
```

*Plan 3: Rewritten plan (Tier 2). Country filter applied as a residual on the MV scan.*

**Tier 3: Match the entire query, including the window function and top N filter.** This is the most specific tier. The MV body is the target query verbatim (minus the top-level `ORDER BY`, which is meaningless for a stored set). The MV stores the top-ranked rows the query asks for (rank ≤ 100).

*Tier 3 MV: Stores the exact ranked output of the query (exact-match path).*\n\nThis tier exercises the **exact-match rewrite path**: the rewriter canonicalizes the MV body and matches it against the query’s logical plan.\n\nRewritten plan:\n\n```\nSort revenue_rank ASC\n+- BatchScan customer_tier_3 <- reads around 100 stored rows\n```\n\n*Plan 4: Rewritten plan (Tier 3). Reads around 100 stored rows.*\n\n### The trade-off\n\nThe three tiers trade per-query speedup against reuse and storage. In our testing on [TPC-DS](https://www.tpc.org/tpcds/) 3 TB, we observed the following:\n\n| **MV design** | **Pre-computed** | **Reuse** | **Per-query speedup** | **MV size** |\n|---|---|---|---|---|\n| Baseline (no MV) | nothing | n/a | 1x | n/a |\n| Tier 1: store_sales agg by customer surrogate key | aggregate of all sales per customer | broadest: any per-customer aggregation | ~5x faster | 0.07% of store_sales for TPC-DS 3 TB |\n| Tier 2: store_sales x customer agg, one filter pre-applied | join + aggregate, preferred customers only | medium: any country filter, preferred customers | ~10x faster | 0.04% of store_sales for TPC-DS 3 TB |\n| Tier 3: entire query body verbatim (exact-match) | exact ranked output of this query | narrowest: only this exact query shape | 20x+ faster | negligible (only 100 rows) |\n\n[... middle omitted — see footer ...]\n\n\nTurning on automatic query rewrite has overhead: it introduces trade-offs that might affect some queries negatively:\n\n1. **Optimization overhead.** Enabling rewrite adds processing time during query optimization as the optimizer evaluates MV candidates against the query plan. This overhead applies to every query in the session, including those that ultimately don’t match any MV.\n2. **Reduced task parallelism.** Reading from an MV instead of the original base table might produce fewer tasks or introduce data skew, depending on the MV’s data layout. This reduces parallelism compared to a direct scan of the larger, more evenly distributed source table.\n\n## Conclusion\n\nIn this post, we showed how automatic query rewrite can accelerate your existing Apache Spark workloads. It uses Apache Iceberg materialized views in the AWS Glue Data Catalog, without changing a single line of SQL. By storing precomputed results as managed Apache Iceberg tables, the AWS Glue Data Catalog lets the Apache Spark optimizer transparently substitute matching query plans. You get the performance benefit of pre-aggregation without the application-level rewiring. BI dashboards, ISV-generated reports, and legacy pipelines all benefit the moment a matching MV exists.\n\nWe walked through three MV designs for the same analytical query, each striking a different balance between per-query speedup, storage footprint, and reuse across your workload. As the trade-off table shows, our testing found that a narrow, exact-match MV delivered 20x+ acceleration for a single query shape. A broader pre-aggregate served an entire family of queries at a more modest ~5x gain. The right choice depends on how many queries share the same join-and-aggregate pattern and how frequently your source data changes.\n\nTo get started:\n\n1. Launch an Amazon EMR 7.12.0+ cluster or an AWS Glue 5.1+ job.\n2. Create an MV over your most expensive repeating query using `CREATE MATERIALIZED VIEW` in the AWS Glue Data Catalog.\n3. Turn on automatic query rewrite by setting `spark.sql.optimizer.answerQueriesWithMVs.enabled=true` in your Spark session configuration.\n4. Verify the rewrite by inspecting the optimized query plan for an MV scan node, or by checking INFO-level logs on Amazon EMR 7.14.0+.\nQueries with multi-table joins, heavy aggregations, or window functions over large fact tables are strong initial candidates. Start with one high-cost, frequently executed query. Validate the speedup, then expand to broader MVs as you identify shared patterns across your workload.\n\nSpecial thanks to everyone who contributed to the automatic query rewrite feature and this blog: Andre Hernich, Leon Lin, Yiyang Chen, Geeta Krishna Panda, Ashok Chintalapati, Muhammad Malik, Rishabh Bhatia, and Giovanni Fumarola.\n\n## References\n\nFor more detail, see the following resources:\n\n- [Using materialized views with Amazon EMR](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-materialized-views.html).\n- [Using materialized views with AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/materialized-views.html).\n- [Querying materialized views in Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-gdc-mv.html).\n- [Introducing Apache Iceberg materialized views in AWS Glue Data Catalog](/blogs/big-data/introducing-apache-iceberg-materialized-views-in-aws-glue-data-catalog/).\n- [Materialized views in AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/materialized-views.html).\n- [How to use streamlined permissions for Amazon S3 Tables and Iceberg materialized views](/blogs/big-data/how-to-use-streamlined-permissions-for-amazon-s3-tables-and-iceberg-materialized-views/).\n\n---\n\n## About the authors\n\n──────── [TRUNCATED] ────────\nShowing 11,075 chars (head) + 3,722 chars (tail) of 19,548 total clean characters.\nFull text saved to: /opt/data/cache/web/aws.amazon.com-142c38b343.md\nTo read the omitted middle: read_file path=\"/opt/data/cache/web/aws.amazon.com-142c38b343.md\" offset=138 limit=200  (the file is the complete page; raise/lower offset to page through it).\n─────────────────────────────