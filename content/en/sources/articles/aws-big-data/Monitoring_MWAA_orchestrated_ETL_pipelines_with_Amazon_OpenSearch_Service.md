---
title: "Monitoring MWAA-orchestrated ETL pipelines with Amazon OpenSearch Service"
description: "Stream MWAA, Glue, and EC2 logs into OpenSearch via CloudWatch subscription filters and query failures in natural language through a Bedrock-backed MCP server."
published: "2026-10-06"
source_url: "https://aws.amazon.com/blogs/big-data/monitoring-mwaa-orchestrated-etl-pipelines-with-amazon-opensearch-service"
blog: aws-big-data
locale: en
tags: [source, aws-big-data, mwaa, opensearch, en]
---

# Monitoring MWAA-orchestrated ETL pipelines with Amazon OpenSearch Service

## Overview

When an MWAA-orchestrated pipeline spans Glue jobs, EC2 scripts, and Airflow DAGs, each component logs to its own CloudWatch group and failure triage becomes a scavenger hunt across tools. This solution streams all of those logs in real time into Amazon OpenSearch Service and puts an AI agent in front: engineers ask in natural language why a job failed and get root-cause analysis with remediation steps, cutting mean time to resolution.

## Architecture

MWAA (provisioned and serverless) orchestrates the pipeline while Glue jobs and EC2 Python scripts emit logs to CloudWatch through native integration, default log configuration, and the unified CloudWatch agent. Subscription filters on each log group stream events through a Lambda function that decompresses, enriches, and bulk-indexes them into OpenSearch indices per source plus a unified ETL index. Inside OpenSearch, the ML Connector framework calls Claude on Bedrock for semantic understanding, and an OpenSearch MCP server on Bedrock AgentCore exposes index discovery and search tools to AI assistants — no hand-written DSL required.

## Deployment

Three CloudFormation stacks deploy in order: `opensearch-cfn` (domain, SageMaker AI notebook, IAM roles), `etl` (VPC, MWAA environment, Glue job, EC2 instance, streaming pipeline), and `agentcore-mcp-server` (Bedrock AgentCore MCP runtime with Cognito auth). A notebook then wires credentials, creates the Lambda-backed subscription filters, triggers the demo DAGs (provisioned or serverless via a flag), registers the Claude connector in OpenSearch, and spins up the ETL analysis agent either locally or against AgentCore.

## Using and extending it

Once logs flow, prompts like "show me ERROR level logs" or "why did the Glue job fail at 3 AM" return correlated findings across sources. Natural extensions are OpenSearch alerting to SNS on error thresholds, more log sources via additional subscription filters, dashboards for error rate and trigger-to-completion latency, and prompt tuning with the index mapping. Cleanup is a stack delete per template.

## References

- [Original post: Monitoring MWAA-orchestrated ETL pipelines with Amazon OpenSearch Service](https://aws.amazon.com/blogs/big-data/monitoring-mwaa-orchestrated-etl-pipelines-with-amazon-opensearch-service)
- [Sample code: sample-etl-troubleshooting-using-genai](https://github.com/aws-samples/sample-etl-troubleshooting-using-genai)
