---
title: "Geospatial queries are up to 38X faster with Lakehouse//RT"
description: "Spatial SQL and spatial joins now run on Lakehouse//RT and they're up to 38X faster than traditional cloud data warehouses."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert"
blog: databricks
published_date: 2026-10-15
---

# Geospatial queries are up to 38X faster with Lakehouse//RT

**Source**: [databricks](https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert) · **Published**: 2026-10-15

## Overview

Spatial SQL and spatial joins now run on Lakehouse//RT and they're up to 38X faster than traditional cloud data warehouses. Earlier this year, we brought Spatial SQL to General Availability on Databricks: this included support for the GEOMETRY data type, 100+ spatial functions, high-performance spatial joins, AI/BI maps, Delta Sharing. The GEOMETRY and GEOGRAPHY data types are part of the open lakehouse, available in Apache Spark, and supported in the same underlying parquet files used by Delta and Iceberg v3. Customers across insurance, agriculture, energy, telecom, retail, logistics and more have adopted it to consolidate geospatial workloads onto a single governed platform.

## Key points

- Spatial SQL and spatial joins are now supported on Lakehouse//RT, delivering ultra low latency and high concurrency directly on your governed lakehouse data.
- Benchmarks show Lakehouse//RT delivers 38X faster spatial query performance than a traditional data warehouse with 50 concurrent users.
- No separate geospatial serving layer required. Spatial SQL on Lakehouse//RT combines real-time performance with open formats, Unity Catalog governance, and the full 100+ spatial function library.
- Lakehouse//RT is up to 38X faster, maintaining performance with high-concurrency. Even removing the most significant query improvement; the average speed-up is over 3.5X.
- Lakehouse//RT is up to 20X faster with single-query concurrency. Every spatial benchmark query is faster on Lakehouse//RT.
- No query changes or new licenses required. Spatial workloads are portable on Databricks; the same spatial queries you run on SQL Serverless today can run on Lakehouse//RT with no code changes.

## References

- Original article: [https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert](https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert)
