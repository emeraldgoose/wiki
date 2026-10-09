---
title: "Discover and Govern Snowflake Data Using SageMaker Unified Studio"
description: "Federate Snowflake into SageMaker Unified Studio via Glue connection, publish governed assets to SageMaker Catalog, and post Glue Data Quality scores without moving data."
published: "2026-09-16"
source_url: "https://aws.amazon.com/blogs/big-data/discover-and-govern-snowflake-data-using-sagemaker-unified-studio/"
blog: "AWS Big Data"
locale: "en"
tags: [aws, sagemaker, snowflake, glue, data-quality, catalog, governance]
---

# Discover and Govern Snowflake Data Using SageMaker Unified Studio

[한국어 버전](../../../../ko/sources/articles/aws/Discover_and_Govern_Snowflake_Data_Using_SageMaker_Unified_Studio.md)

**Authors**: Marco Duarte López, Diego Ortiz · **Published**: 2026-09-16 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/discover-and-govern-snowflake-data-using-sagemaker-unified-studio/)

## Problem

Many organizations live in a hybrid estate: critical tables in Snowflake, analytics workloads on AWS. Without a connection, cataloging Snowflake data means building extraction pipelines that take days, governance splits across two systems, and discovery friction forces duplicated effort. The post asks: how do you query, catalog, and validate Snowflake data in 5–15 minutes with no replication and no custom ETL?

## Solution overview

SageMaker Unified Studio federates Snowflake through an AWS Glue connection. The federated catalog entry registers in the Glue Data Catalog, governed by Lake Formation, without moving data out of Snowflake. The five-step workflow:

1. **Create the Snowflake connection** in SageMaker Unified Studio (Glue connection, register-in-catalog on).
2. **Federate tables** into the publisher project — tables appear in the project catalog within minutes.
3. **Publish the dataset** to SageMaker Catalog as a governed asset with business metadata.
4. **Validate quality** with Glue Data Quality (DQDL via Visual ETL) and post scores to the catalog asset.
5. **Consume**: publisher-project users query via SQL analytics (Athena pushdown); consumer projects discover and subscribe via SageMaker Catalog.

Federated queries run through Athena: Athena reads the table definition from Glue Catalog, connects to Snowflake, pushes the query down, and returns only results. Nothing is copied to S3.

## Implementation

**Prerequisites**: Snowflake account with admin access and a database/schema with tables; a SageMaker Unified Studio domain plus a producer project; an S3 bucket for Glue assets; IAM permissions (`datazone:SearchListings`, `GetListing`, `ListDomains`, `GetDomain`, `PostTimeSeriesDataPoints`, `GetAsset`, `ListAssetRevisions`). Add the Glue job role as a domain user and as project member with Owner.

**Connection details** (Project → Data → Add → Add Connection → Snowflake): name `snowflake-connection`, host `<account>.snowflakecomputing.com`, port 443, database/warehouse/schema, username/password, check **Register in AWS Glue Data Catalog**, choose case-conflict handling. Wait a few minutes, then search confirms federated objects.

**Publish to catalog**: Manage → Data Sources → Create Data Source → AWS Glue, check Import data lineage, connection `project.default_lakehouse`, catalog `snowflake-connection`, database name, table selection `*` or specific table. Run the source to extract metadata, open Assets, optionally Generate Descriptions (business description, column definitions, glossary suggestions), then **Publish Asset**.

**Data quality pipeline** (Glue Studio Visual ETL):

1. Copy `post_dq_results_to_datazone.py` and `post_dq_results_to_datazone.json` from aws-samples into `s3://aws-glue-assets-<account>-<region>/transforms/` to register the **Datazone DQ Result Sink** custom transform.
2. New Visual ETL job: Snowflake source (reuse the connection, pick schema/table) → **Evaluate Data Quality** transform with DQDL rules → **ruleOutcomes** → **Datazone DQ Result Sink** (domain ID, table/schema, ruleset name, max results).
3. Job parameters: `--additional-python-modules = boto3>=1.34.105`. Save and run.
4. Verify in SageMaker Catalog → Assets → Data Quality tab (example in the post: overall score 100, ruleset `movies` Passed 1/1).

## Why it matters

- **No data movement**: query and validate in place; 5–15 minutes instead of days of pipeline work.
- **Centralized governance**: one discovery and quality surface (SageMaker Catalog) across Snowflake and AWS, Lake Formation access control.
- **Trust at discovery time**: consumers see quality scores before subscribing, without Snowflake access or their own validation runs.
- **Unified collaboration**: publisher/consumer project split with lineage import keeps ownership clear.

## Takeaways for the seminar

- Federation beats replication when the source of truth must stay put: metadata travels, data stays.
- The sharp edges are IAM (Glue role as domain user + project Owner, `datazone:` actions) and the custom-transform wiring (`transforms/` folder + boto3 module pin).
- Quality-as-metadata (posting DQ results to the catalog asset) turns a technical check into an organizational trust signal.

## Related concepts

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/data-modeling.md`

## References

- [Cross-account lakehouse governance with Amazon S3 Tables and SageMaker Catalog](https://aws.amazon.com/blogs/big-data/cross-account-lakehouse-governance-with-amazon-s3-tables-and-sagemaker-catalog/)
- [Get started with AWS Glue Data Quality dynamic rules for ETL pipelines](https://aws.amazon.com/blogs/big-data/get-started-with-aws-glue-data-quality-dynamic-rules-for-etl-pipelines/)
- [AWS Glue DQDL documentation](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html)
