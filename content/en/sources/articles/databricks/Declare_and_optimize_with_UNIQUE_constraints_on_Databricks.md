---
title: "Declare and optimize with UNIQUE constraints on Databricks"
description: "Databricks UNIQUE constraints let teams declare multiple uniqueness guarantees and use them for optimization."
tags: [source, databricks, data-engineering, sql, en]
locale: en
source_url: "https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks"
blog: databricks
published_date: 2026-11-04
---

# Declare and optimize with UNIQUE constraints on Databricks

**Source**: [databricks](https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks) · **Published**: 2026-11-03

## Overview

Data teams often maintain uniqueness guarantees in their pipelines, but without a flexible way to represent all of them in table schema, neither users nor tools can discover them and the query optimizer cannot safely leverage them. Business entities often have more than one value, or combination of values, known to be unique. Databricks already supports PRIMARY KEY and FOREIGN KEY constraints, but a table can have only one primary key and its columns must be non-nullable. UNIQUE constraints extend this model by allowing multiple nullable or composite uniqueness guarantees.

Teams can declare these guarantees with NORELY by default, validate them, and then use RELY to let the optimizer eliminate redundant joins and DISTINCT aggregations. In 10 TB TPC-DS benchmarks, UNIQUE with RELY removed over 99.99% of shuffle and delivered up to 12 times faster queries. UNIQUE constraints can also be referenced by foreign keys.

## Key points

- UNIQUE constraints support multiple nullable or composite uniqueness guarantees.
- PRIMARY KEY remains limited to one non-nullable identifier per table.
- Constraints can be declared with NORELY without paying validation cost on every write.
- Validated constraints can use RELY to enable optimizer simplifications.
- Foreign keys can reference UNIQUE constraints.
- Benchmarks show major shuffle reduction and faster queries with RELY.

## Details

The article explains how to put pipeline uniqueness guarantees into schema metadata. Declaring them separately from primary keys supports richer data models while keeping validation explicit. Once data is validated, RELY lets the optimizer use the guarantee safely, avoiding redundant join and DISTINCT operations. This separates correctness bookkeeping from query optimization and gives teams control over when each constraint becomes trusted.

## References

- Article: [Declare and optimize with UNIQUE constraints on Databricks](https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks)
