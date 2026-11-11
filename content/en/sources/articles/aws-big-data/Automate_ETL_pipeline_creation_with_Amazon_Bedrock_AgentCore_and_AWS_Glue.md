---
title: "Automate ETL pipeline creation with Amazon Bedrock AgentCore and AWS Glue"
description: "Agentic AI automates ETL pipeline setup: source analysis, schema mapping, code generation, testing and AWS Glue job deployment with approval gates and quality checks."
tags: [source, aws-big-data, bedrock, agentcore, glue, automation, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue"
blog: aws-big-data
published_date: 2026-11-12
---

# Automate ETL pipeline creation with Amazon Bedrock AgentCore and AWS Glue

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue) · **Published**: 2026-11-11

## Overview

Building and maintaining ETL pipelines is time-consuming. Data engineers often spend days mapping fields, writing PySpark code, and testing against changing schemas — and the work must be repeated when schemas evolve. Agentic Data Ingestion automates this process with AI. Point the agent at a source file or database table, and foundation models (FMs) propose field mappings and write the transformation code. The agent tests the generated code on Apache Spark before deploying it as an AWS Glue job, and an approval gate pauses the workflow for human review at key steps.

The entire pipeline runs on AWS managed services. AWS Bedrock provides the foundation models; Amazon Bedrock AgentCore hosts and operates the AI agents built with the open-source Strands Agents SDK; AWS Step Functions orchestrates the 10-step workflow; and AWS Glue runs the generated data integration jobs. The solution is deployed via AWS Cloud Development Kit (CDK). Before starting, review the prerequisites.

## Key points

- The solution architecture spans from data source sign-in through agent orchestration, Step Functions workflow, and Glue job deployment to targets like Amazon S3 Tables, Amazon S3, or relational databases. An interactive React dashboard shows each run's progress and approval status. When a user uploads a source file to Amazon S3, the stream passes through EventBridge and SQS to a Lambda trigger that starts a 10-step Step Functions workflow.
- The workflow runs with two explicit approval gates: one after schema mapping (when FM-confidence scores fall below a threshold or field names don't match) and one after code testing. A mapping skips review only when every field pair has high confidence and a name match is corroborated; otherwise the mapping goes to review by default.
- Code generation delegates to the FM only the transformation block (typically 5–15 lines), not the full Glue script (500+ lines). The scaffold is a human-written Jinja2 template per target type, and the generated code is checked against an allowlist of permitted constructs before job creation. The rendered code is resolved with `getResolvedOptions` and all required parameters must be present, or the job creation is refused.
- Testing runs in an AWS Glue interactive session on the same Spark version as the target job, against a 100-row sample of the source. Output is checked for record counts, nulls, and schema compliance. Database sources are tested on schema-generated rows, since the test session has no database access.
- If a test fails, the workflow can retry with a larger worker or regenerated code. A self-healing agent attempts one new run after schema/type errors or OOM conditions, but skips retry when duplication is possible or the error is unrecoverable (e.g., permissions problem). The run stays failed with the agent's diagnosis displayed.
- A run left waiting at a gate for 72 hours fails, and both approvals and rejections are recorded with the reviewer's identity.
- Customer case: Montai Therapeutics uses the same pattern for scientific data. Embedding the parser-generation agent into their existing ingestion app reduced lead time to onboard new assays from days or weeks to 5–10 minutes per parser generation and output check. The biggest business impact is the proportion of experimental data now landing in the data lake instead of in inboxes, fueling drug specificity and efficacy predictive models.

## Details

Customer sign-in is through Amazon Cognito with MFA required by default. The dashboard serves through Amazon CloudFront behind two WAF web ACLs (managed rules plus rate limiting) with a second WAF ACL for API requests through CloudFront. By default signed-in users have full dashboard access, though the solution does not include identity federation or role-based access (listed as next steps for production in the README's hardening section).

Usage costs include an idle deployment of about $15–20 per month (about $14 from the two WAF ACLs and their rules, up to $5 from CloudWatch monitoring, and storage plus one secret adding about $1). A run at sample scale costs about $0.10–0.25, where AI cost depends on the number of fields rather than rows — prompts carry schemas and at most 100 sample rows are used. A scheduled pipeline repeats most AI steps on each run and skips only the mapping call when the schema is unchanged.

The pipeline creates IAM roles scoped to the single pipeline, bounded by a permissions boundary, with separate roles for agent runtimes. Data is encrypted at rest and in transit, and JDBC credentials are referenced only by their Secrets Manager ARN so they never appear in job arguments.

The test session runs in an interactive Glue session against a 100-row source sample, checking record counts, nulls, and schema compliance. For database sources, tests run on rows generated from the schema rather than querying the database directly. Data quality rules, default-on for file uploads into Amazon S3 Tables (Iceberg), quarantine failing rows before the job writes.

Results are visualized on a React dashboard served through CloudFront with WAF protection. The solution is extensible: Hardening for real data lists identity federation and role-based access as next steps, and the solution's separate agents handle complex mappings and self-healing after failures.

## References

- Original article: [Automate ETL pipeline creation with Amazon Bedrock AgentCore and AWS Glue](https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue)