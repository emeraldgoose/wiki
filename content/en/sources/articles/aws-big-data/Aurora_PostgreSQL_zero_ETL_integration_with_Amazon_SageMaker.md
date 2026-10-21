---
title: "Aurora PostgreSQL zero-ETL integration with Amazon SageMaker"
description: "Replicate Aurora PostgreSQL data into SageMaker AI as Iceberg tables in near real time with no custom ETL pipelines."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/aurora-postgresql-zero-etl-integration-with-amazon-sagemaker"
blog: aws-big-data
published_date: 2026-09-29
---

# Aurora PostgreSQL zero-ETL integration with Amazon SageMaker

## Overview

Aurora PostgreSQL zero-ETL integration with SageMaker streams operational data into analytics within seconds, with no custom ETL pipelines to build or maintain. Changes replicate automatically into a Glue managed catalog as Apache Iceberg tables, where Athena, Redshift, Spark, BI, and ML tools in SageMaker AI can query them alongside other lakehouse data. This removes pipeline latency, operational overhead, and data silos that slow down decisions.

## How it works

The integration is powered by change data capture: Aurora's enhanced logical replication streams every insert, update, and delete from the write-ahead log to the downstream target, including automatic DDL propagation. The flow is: application writes to Aurora, zero-ETL captures changes, data lands in the Glue managed catalog in near real time, and analysts query it via Athena or Redshift while data scientists train models directly on the Iceberg tables. Because the lakehouse rests on open standards with Glue Data Catalog and Lake Formation governance, one copy of data serves SQL, Spark, BI, and AI/ML.

## Setting up the integration

- **Source database:** create a cluster parameter group enabling logical and enhanced logical replication, apply it to a supported Aurora PostgreSQL cluster version, and reboot so the parameters take effect.
- **Target catalog:** create a Glue managed catalog backed by Redshift managed storage, an IAM role assumable by Glue and Redshift for transfers, Lake Formation data-lake admins plus read-only access for the Redshift service-linked role, then register the catalog as an integration target and add a resource policy authorizing inbound integration from the source cluster ARN.
- **Seed and create:** load baseline rows into the source (they become the historical foundation), then call `create-integration` with a data filter (for example, replicate everything). The integration moves from `creating` to `active`; monitor with `describe-integrations`.
- **Verify:** grant Lake Formation table permissions, then query through the Redshift Data API (`execute-statement` / `describe-statement` / `get-statement-result`). Inserting a new row and re-querying confirms near-real-time replication within seconds.

## Cleanup and next steps

Delete the integration first (replication stops but existing data stays in both places), then the Glue catalog, then the Aurora cluster and parameter group if they were created for the walkthrough. Be aware of limits around supported data types, schema-change handling, and filtering. Natural extensions are adding more zero-ETL sources (RDS for MySQL, DynamoDB) for a centralized near-real-time platform, and combining the replicated data with Redshift ML, large-scale SQL analytics, and federated queries.

## References

- Original post: [Aurora PostgreSQL zero-ETL integration with Amazon SageMaker](https://aws.amazon.com/blogs/big-data/aurora-postgresql-zero-etl-integration-with-amazon-sagemaker)
