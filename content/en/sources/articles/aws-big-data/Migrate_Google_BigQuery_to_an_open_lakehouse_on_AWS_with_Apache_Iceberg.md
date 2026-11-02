---
title: "Migrate Google BigQuery to an open lakehouse on AWS with Apache Iceberg"
description: "Why an open lakehouse on AWS is the next step for BigQuery-based organizations, plus migration patterns and target architecture."
tags: [source, aws-big-data, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg"
blog: aws-big-data
published_date: 2026-11-03
---

# Migrate Google BigQuery to an open lakehouse on AWS with Apache Iceberg

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg) · **Published**: 2026-11-02

## Overview

Enterprises are increasingly measuring their readiness for AI by the readiness of their data, which often means moving to an open lakehouse where data stays open and portable. A tightly coupled, single-engine cloud data warehouse begins to hold organizations back. An open lakehouse on AWS combines Amazon S3 storage with Apache Iceberg tables so teams can choose the engines and models that fit each workload without re-architecting their platform.

## Key migration patterns

- Bulk migration: use BigQuery's EXPORT DATA to export tables to Google Cloud Storage in Parquet, then move data with AWS DataSync.
- Zero-ETL: land SaaS and operational sources such as Google Analytics, Salesforce, SAP, ServiceNow, and HubSpot directly into the lakehouse.
- Change data capture: stream row-level changes from operational stores with Debezium on Amazon MSK Connect.
- Streaming: use Amazon Kinesis Data Streams and Amazon MSK to feed real-time data into the raw layer.
- Medallion layers: Bronze/Raw data lands as Apache Iceberg; Silver/Trusted data is refined with AWS Glue or Amazon EMR Spark into query-ready tables.

## Architecture

Storage, consumers, and cross-cutting layers are separated. Amazon S3 with Apache Iceberg provides the storage layer, while multiple compute engines, dashboards, and AI workloads read the same tables. The case study in the post describes a global technology leader completing a zero-downtime GCP exit at petabyte scale.

## References

- Original article: [Migrate Google BigQuery to an open lakehouse on AWS with Apache Iceberg](https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg)
