---
title: "What makes a catalog open? Unity Catalog Advances the Open Lakehouse"
description: "While almost every platform now supports open formats, what makes a catalog truly open?"
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse"
blog: databricks
published_date: 2026-10-19
---

# What makes a catalog open? Unity Catalog Advances the Open Lakehouse

**Source**: [databricks](https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse) · **Published**: 2026-10-19

## Overview

While almost every platform now supports open formats, what makes a catalog truly open? An open catalog keeps your data in storage you own, gives you the best features there, and supports data portability: the ability to move your tables to another catalog while keeping the data in place. Portability is a core tenet of an open lakehouse, and it’s where most catalogs fall short. As the first catalog to support both REGISTER and UNREGISTER from the Apache Iceberg™ REST catalog spec, Unity Catalog in Databricks' Open Lakehouse expands what an open catalog means: your tables can move existing Iceberg tables in or out without any data movement. Databricks contributed UNREGISTER to the Iceberg REST catalog spec, making this an open standard. Read Unlocking Data Portability.

## Key points

- Customer-owned storage: Unlike other platforms with native tables in managed storage, Unity Catalog managed tables in customer-owned storage allow portability without data copy.
- Unity Catalog is the most open catalog: As the first catalog to support the Apache Iceberg REST catalog spec for REGISTER and UNREGISTER, Unity Catalog allows you to move tables between catalogs without data duplication.
- Best features available on tables you own: Open catalogs like Unity Catalog deliver all advanced table features on tables in your storage, not only on tables a provider stores for you.
- Fail-safe data protection. Snowflake and other platforms reserve fail-safe recovery for tables in their own storage. By contrast, Unity Catalog managed tables in customer-owned storage support data recovery: you can quer
- Automatic optimizations. In Snowflake, data compaction is costlier in provider-controlled storage. For other platforms, table maintenance and V-order apply to tables stored in customer-owned storage, rather than data rea
- Storage costs. Snowflake doesn't delete orphaned files from Iceberg tables in your own bucket, such as files left behind by failed writes, which means you keep paying for files no table uses. On Unity Catalog managed tab

## References

- Original article: [https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse](https://www.databricks.com/blog/what-makes-catalog-open-unity-catalog-advances-open-lakehouse)
