---
title: "Building an LLM-powered DAG failure analysis plugin for Amazon MWAA"
description: "Add an on-demand Analyze Task button to Airflow on MWAA that uses Amazon Bedrock to diagnose failed tasks with code-level context."
tags: [source, aws-big-data, mwaa, airflow, bedrock, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/building-an-llm-powered-dag-failure-analysis-plugin-for-amazon-mwaa"
blog: aws-big-data
published_date: 2026-09-29
---

# Building an LLM-powered DAG failure analysis plugin for Amazon MWAA

## Overview

As Airflow fleets grow to hundreds of DAGs spanning Glue, EMR, Athena, and Redshift, diagnosing one failed task means digging through logs, DAG configs, and error messages by hand. This post builds a custom Airflow plugin for Amazon MWAA that integrates Amazon Bedrock (Claude) to produce on-demand root-cause analysis with actionable fixes. Full source is in the `sample-aws-mwaa-llm-powered-plugin` repository, with example DAGs simulating failures across operator types.

## How it works

From the Airflow UI you select a failed task and choose **Analyze Task**. Behind that button the plugin: pulls task metadata from the Airflow metadata DB; collects logs, DAG source, and the operator's actual code or query; sends the enriched context to Bedrock; and renders a structured report with root cause, step-by-step resolution, and prevention advice. AWS calls authenticate through the `aws_default` connection, which on MWAA resolves to the execution role — no static keys.

The differentiator is operator-aware enrichment: for Glue and EMR operators it resolves the job definition and reads the PySpark script from S3; for Athena, Redshift, Bash, Python, and dbt operators it reads the query or command inline from rendered template fields. Smart fetching skips the S3 lookup for infrastructure errors (for example timeouts) and only fetches code for code-relevant error patterns.

## Plugin design

- **Registration:** on Airflow 3.x the web UI registers as a FastAPI app under `/task-analyzer` via `fastapi_apps`, with an external `Analyze Task` view on task-instance pages. Files ship inside `plugins.zip`, extracted to the plugins folder — no extra registration call.
- **Analysis engine:** the `POST /api/analyze-task` endpoint assembles context, enriches it per operator type, builds the prompt from `prompts.py` templates, invokes Bedrock, and returns the report. Model IDs are Airflow Variables, so switching models needs no redeploy.
- **Prompt and safety:** prompts bundle task metadata, error text, logs, DAG source, and operator script; the model returns root cause, resolution steps, and prevention. Before sending anything, the plugin redacts credentials, truncates to fit context windows, blocks path traversal on file reads, and optionally adds a Comprehend PII-detection pass for regulated logs. Results cache by error-context hash to avoid repeat inference charges.

## Deploy, test, and operate

Package `plugins/` as `plugins.zip`, upload it to the MWAA S3 bucket, and update the environment with the archive's version ID (takes 10–30 minutes; no `requirements.txt` needed since FastAPI and Boto3 are preinstalled). Override the Region via the `aws_default` connection extras if needed, then confirm the plugin appears under Admin > Plugins. Copy the sample DAGs to the DAGs folder, trigger an intentional failure, and check the analysis completes in seconds with file/line references.

For production: scope IAM to `bedrock:InvokeModel` on chosen models and `s3:GetObject` on script paths, keep secrets in Secrets Manager rather than DAG files, rely on Airflow auth for the endpoints (plus tag-based DAG permissions at scale), and add retries, circuit breakers, and CloudWatch alarms around Bedrock calls. Natural extensions are SNS/Slack notifications, a Bedrock Knowledge Bases RAG layer over past analyses, custom-operator handlers, and automated remediation for known failure patterns.

## References

- Original post: [Building an LLM-powered DAG failure analysis plugin for Amazon MWAA](https://aws.amazon.com/blogs/big-data/building-an-llm-powered-dag-failure-analysis-plugin-for-amazon-mwaa)
