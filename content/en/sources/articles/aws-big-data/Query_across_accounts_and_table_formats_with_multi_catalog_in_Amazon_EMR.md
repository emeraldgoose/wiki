---
title: "Query across accounts and table formats with multi-catalog in Amazon EMR"
description: "EMR 8.1's RedirectingSessionCatalog unifies Iceberg, Delta, Hudi, and Hive tables across accounts behind one Spark catalog with query-time auto-discovery."
published: "2026-10-06"
source_url: "https://aws.amazon.com/blogs/big-data/query-across-accounts-and-table-formats-with-multi-catalog-in-amazon-emr"
blog: aws-big-data
locale: en
tags: [source, aws-big-data, emr, glue, en]
---

# Query across accounts and table formats with multi-catalog in Amazon EMR

## Overview

Spark's default catalog accepts only one format extension at a time, and its V1 metastore binds to a single account's Glue catalog — so mixed-format lakes and cross-account meshes needed per-format catalogs plus Lake Formation/RAM/resource-link workarounds. EMR 8.1's opt-in `RedirectingSessionCatalog` (RSC) removes both constraints: set it as the Spark default and it detects each table's format from Glue metadata and routes to the right handler, joins across accounts' Glue catalogs without copying data, and auto-discovers remote catalogs at query time.

## The three capabilities

Multi-format support collapses one-catalog-per-format configuration into a single property, letting unprefixed `db.table` references and cross-format joins work in one statement. Multi-catalog access declares a named RSC catalog pointing at a remote account's Glue catalog ID, joining local and remote tables directly — each named instance gets its own metastore delegate, ending the V1 singleton limit. Auto-wiring goes further: EMR fills in format handlers automatically, and the opt-in `GlueCatalogResolver` registers undeclared catalogs on first reference via the Glue GetCatalog API, supporting cross-account Glue catalogs, S3 Tables, and Redshift Managed Storage.

## Trying it and choosing configuration

A walkthrough in the aws-emr-utilities repo creates one table per format through the same catalog, runs a four-way cross-format join, and extends to a cross-account join with bootstrap scripts for consumer and producer accounts. Rule of thumb: mixed-format lake → RSC as default (Delta/Hudi need session extensions); data in another account → named catalog; many accounts with zero upfront config → enable the resolver; all of the above compose. Cross-account reads still require the underlying Lake Formation grants, Glue resource policy, S3 bucket policy, and KMS key policy.

## References

- [Original post: Query across accounts and table formats with multi-catalog in Amazon EMR](https://aws.amazon.com/blogs/big-data/query-across-accounts-and-table-formats-with-multi-catalog-in-amazon-emr)
- [Walkthrough code: aws-emr-utilities](https://github.com/aws-samples/aws-emr-utilities)
