---
title: "Store and process large strings in Amazon Redshift SUPER columns"
description: "Amazon Redshift SUPER columns now support large strings up to 16 million bytes and in-memory string processing."
tags: [source, aws-big-data, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns"
blog: aws-big-data
published_date: "2026-11-07"
---

# Store and process large strings in Amazon Redshift SUPER columns

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns) · **Published**: 2026-11-06

## Overview

Amazon Redshift expands its SUPER data type so semi-structured data such as JSON and arrays can be ingested, stored, transformed, and analyzed without splitting or truncating large strings. With large string support enabled, SUPER supports individual strings up to 16 million bytes and processes strings beyond the 65,535-byte VARCHAR limit in memory.

The post explains three enhancements. Extended string support lets organizations store complete large JSON documents. In-memory string function processing allows functions such as substring and pattern matching to operate on large strings without truncation. Case-insensitive database compatibility simplifies migrations from legacy databases.

These changes reduce common semi-structured data workflow challenges, especially for large JSON, web logs, IoT telemetry, and application logs. Configuration requires a parameter group with enable_large_strings_opt_in set to Yes and a compatible Redshift maintenance track.

## Key points

- SUPER columns now support individual strings up to 16 million bytes.
- Large string processing happens in memory, avoiding truncation or disk spill.
- Case-insensitive database compatibility eases migration from legacy systems.
- enable_large_strings_opt_in must be enabled in a parameter group or workgroup.
- Detailed examples cover loading, querying, and string operation use cases.

## Details

The article includes SQL examples for turning on large string support, creating orders tables, loading JSON from Amazon S3, querying nested fields, and running LISTAGG and LEN across strings larger than the previous 65,535-byte limit. It also describes behavior for VARCHAR columns, views, UDFs, and stored procedures.

## References

- Original article: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/store-and-process-large-strings-in-amazon-redshift-super-columns)
