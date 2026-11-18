---
title: "Analyze Anthropic usage, spend, and access with AWS Glue, Amazon S3 Tables, and AWS Quick"
description: "How AnyCompany Retail brings Anthropic Admin API usage and cost data into Amazon S3 Tables with the native AWS Glue connector, joins it with business data through Glue materialized views, and answers spend, value, and API-key-ownership questions in AWS Quick."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick"
blog: aws-big-data
published_date: "2026-11-19"
---

# Analyze Anthropic usage, spend, and access with AWS Glue, Amazon S3 Tables, and AWS Quick

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick) · **Published**: 2026-11-16

## Overview

Finance teams want to allocate AI spend to the business units that use it. Engineering leaders want to know what that spend delivers. Security teams want to know who owns each API key and whether any belong to former employees. Anthropic exposes detailed usage and cost visibility through Claude Code usage analytics and the Anthropic Admin API, but taking that data into an AWS-based analytics stack has meant building and maintaining a custom integration with the Admin API.

AWS Glue now offers a native connector for Anthropic — one of 100 new native SaaS connectors AWS Glue added — so no custom code is required. You store an Anthropic API key in AWS Secrets Manager, reference it from an AWS Glue connection, and the connector handles API calls and schema mapping. The post walks through the fictional retailer AnyCompany Retail, which loads Anthropic data into Amazon S3 Tables (fully managed Apache Iceberg tables), joins it with its own business data using AWS Glue materialized views, queries the result with Amazon Athena, and publishes a weekly AWS Quick dashboard for leadership.

## Key points

- **Connector setup**: store Anthropic API keys in AWS Secrets Manager; create a Glue connection that references the secret; run an AWS Glue ETL job that reads entities such as usage reports, cost reports, users, and workspaces through the Admin connection (plus message batches/files through workspace connections) and writes them unchanged to a raw namespace.
- **Lakehouse layout**: the ETL script (`anthropic_usage_etl.py`) flattens usage/cost reports into daily fact tables, converts cost from cents to US dollars, builds API-key/user/workspace dimension tables in a curated namespace, and writes everything to Amazon S3 Tables as Apache Iceberg tables that AWS analytics services (and other Iceberg engines) can read natively.
- **Business-context joins**: Anthropic data shows what each workspace and key spends, but not which business unit owns a workspace, what the spend produced, or whether a key's creator still works there. AnyCompany supplies three reference datasets from its own CSV exports in S3 — `workspace_business_unit` (workspace→unit mapping), `support_outcomes_daily` (conversations, completed resolutions, QA score per business unit per day), and `hr_directory` (email, employment_status active/departed) — loaded into a reference namespace.
- **Materialized views**: AWS Glue materialized views (stored as Iceberg tables) join the curated Anthropic tables with the reference datasets to produce the spend, value, and access fact sets; the Glue role needs Secrets Manager read, S3 read for scripts/reference data, table-bucket read/write in the Data Catalog, and `iam:PassRole` on its own ARN because Glue stores the role with each view and uses it to refresh the view.
- **Answers and visualization**: Amazon Athena (SQL) answers leadership's three questions — which business units drive AI spend, what the spend delivers (e.g., completed resolutions and QA scores vs. spend), and who owns each API key (including keys held by departed employees) — and AWS Quick presents the results via natural-language prompting or a dashboard that leadership reviews weekly.
- **Adjust to your data**: if your datasets or columns differ, update `REFERENCE_DATASETS` in the ETL script and the materialized-view definitions to match.

## Details

The solution is delivered in three parts. Part 1 sets up the Glue connector for Anthropic (secrets, connection, and permissions). Part 2 builds the AI-usage lakehouse: upload the three reference CSVs to S3 under a common prefix (one folder per dataset), grant the IAM role the permissions above, upload and run the ETL job to populate raw/reference/curated namespaces in the S3 Tables bucket, then create the Glue materialized views that combine them. Part 3 covers Quick: allow Quick to access the table bucket, create datasets from the materialized views, and build the dashboard.

Example rows shown in the post illustrate the grain of each dataset: `support_outcomes_daily` records 2026-10-30 for Customer Service with 1,216 conversations, 990 completed resolutions, and a 96% QA score; `hr_directory` flags e.g. jane.doe@example.com as `departed`. Cost values arrive in cents and are converted to dollars by the ETL job. Table creation is automatic — the script creates missing tables and adds columns when the schema evolves.

Operationally, this turns AI usage into just another governed domain in the data lakehouse: the same Iceberg tables are queryable from Athena today and from any Iceberg-aware engine later, and the materialized views refresh through the Glue-stored role rather than a human process. Security-relevant wins include identifying API keys owned by former employees from the `hr_directory` join and attributing spend to business units via `workspace_business_unit`.

**Note**: the article is a walkthrough using sample data; figure details and exact script contents live in the original post. The ETL script and materialized-view SQL are downloaded separately from the article.

## References

- Original article: [Analyze Anthropic usage, spend, and access with AWS Glue, Amazon S3 Tables, and AWS Quick](https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick)
