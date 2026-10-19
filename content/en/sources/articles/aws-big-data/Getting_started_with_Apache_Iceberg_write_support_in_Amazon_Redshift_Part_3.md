---
title: "Getting started with Apache Iceberg write support in Amazon Redshift – Part 3"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/getting-started-with-apache-iceberg-write-support-in-amazon-redshift-part-3"
blog: aws-big-data
published_date: 2026-09-28
published: 2026-10-17
---

# Getting started with Apache Iceberg write support in Amazon Redshift – Part 3

## Overview

Production tables constantly evolve — columns come and go, types outgrow their precision, and partition layouts stop matching query patterns. In Part 3 of the series (Part 1 created Iceberg tables and inserted data; Part 2 covered DELETE/UPDATE/MERGE), you evolve Iceberg schemas and partitioning with ALTER statements in Redshift as metadata-only operations — no rewrites, no pipeline rebuilds — and share S3 Tables with other engines through Lake Formation resource links under one permission model.

## Schema evolution with ALTER TABLE

Each operation updates only metadata; existing files stay untouched and all readers see the new schema immediately.

- **Add column:** new columns arrive with unique Iceberg field IDs and read NULL for existing rows — demonstrated by adding `loyalty_tier` to `customer` and backfilling it from order totals.
- **Drop column:** the column leaves the current schema while old file data simply becomes invisible (drop any partition field using the column first).
- **Rename column:** renames without touching types or partition specs.
- **Widen type:** safe promotions such as INT→BIGINT or DECIMAL(10,2)→DECIMAL(18,2) without rewriting data — plan types with growth in mind.
- **Set table properties:** compression changes (for example to `zstd`) apply to future writes only, so set them before bulk loads.

## Partition evolution

Iceberg lets the partition spec change without re-partitioning old data: new writes follow the new spec, old files keep their layout, and engines read both transparently.

- **Add a field:** for example adding `bucket(16, customer_id)` alongside day partitioning for high-cardinality distribution.
- **Replace a field atomically:** swapping `DAY(order_date)` for `MONTH(order_date)` in one statement avoids a transient unpartitioned state.
- **Multi-level specs:** add fields one at a time (for example month + bucket + day) with no rewrites, and drop them one at a time to simplify — noting dropped fields lose partition pruning for new data. Available transforms include year, month, day, hour, bucket, truncate, and identity; a column already in a partition field must be dropped or replaced before reuse.

## Cross-engine access and operating guidance

Create a Lake Formation resource link in the default Glue catalog pointing at the S3 Tables database, grant DESCRIBE to the Redshift role, then create an external schema for clean two-part (`schema.table`) queries — preferable for BI tools, Data API, and JDBC/ODBC over three-part notation, which needs IAM federated auth. Schema changes propagate automatically, so an `ALTER` plus `UPDATE` is immediately visible cross-catalog through joins. Operate safely by testing ALTERs in non-production, preferring REPLACE over DROP+ADD, verifying specs with SHOW TABLE, running Glue table optimizers after heavy mutations, applying Lake Formation column/row security, granting schema access to named roles (not PUBLIC), and remembering that dropping a table removes only the catalog entry — S3 files need separate cleanup.

## References

- Original post: [Getting started with Apache Iceberg write support in Amazon Redshift – Part 3](https://aws.amazon.com/blogs/big-data/getting-started-with-apache-iceberg-write-support-in-amazon-redshift-part-3)
