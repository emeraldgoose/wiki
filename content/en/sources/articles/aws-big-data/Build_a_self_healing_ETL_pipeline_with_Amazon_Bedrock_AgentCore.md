---
title: "Build a self-healing ETL pipeline with Amazon Bedrock AgentCore"
description: "A four-agent system on Amazon Bedrock AgentCore corrects failed AWS Glue ETL records against a confidence threshold, writes them back to the data lake with correction metadata, and can open pull requests that fix root causes in upstream code."
tags: [source, aws-big-data, amazon-bedrock, aws-glue, etl, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-a-self-healing-etl-pipeline-with-amazon-bedrock-agentcore"
blog: aws-big-data
published_date: 2026-11-14
---

# Build a self-healing ETL pipeline with Amazon Bedrock AgentCore

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-self-healing-etl-pipeline-with-amazon-bedrock-agentcore) · **Published**: 2026-11-13

## Overview

Extract, transform, and load pipelines break silently. Schema drift, missing fields, and type mismatches corrupt downstream analytics, and the typical fix is manual: detect the error, triage it, patch the record, update the code, redeploy. As data volumes grow, that detect-triage-fix-deploy cycle does not scale. The pattern in this post is a self-healing pipeline built on Amazon Bedrock AgentCore together with AWS Glue: it corrects bad records using domain knowledge, persists the corrections to the data lake, and, optionally, proposes pull requests to prevent the same errors from recurring.

The running example is a hypothetical weather system ingesting National Oceanic and Atmospheric Administration (NOAA) records across 15 schema types, including temperature, precipitation, wind, pressure, humidity, visibility, cloud cover, and solar radiation. An AWS Glue ETL job acts as the quality gate: it validates each record against a dispatcher that maps every schema type to a dedicated validator checking required fields, data types, enum values, and numeric constraints. Records that fail are classified by error type (missing field, type mismatch, schema violation, invalid format) and routed to the agent system instead of a dead-letter queue.

Correction knowledge comes from two complementary sources, and a confidence threshold with a human-notification fallback provides built-in oversight over the autonomous behavior. The post covers the architecture, deployment with the AWS Cloud Development Kit, and a test of the correction workflow with before-and-after record comparisons.

## Key points

- A four-agent system on Bedrock AgentCore handles each error: an orchestrator coordinates the sequential workflow, a data correction agent applies a high-confidence fix, a data persistence agent writes the corrected record back, and a code remediation agent proposes a fix at the source.
- Each agent is a containerized application built with the Strands Agents SDK and deployed as an AgentCore runtime.
- The orchestrator degrades gracefully to a human notification when it cannot correct with confidence of at least 70 percent, and it stops on step failure rather than propagating bad data downstream.
- The correction agent weighs two knowledge sources: Amazon Bedrock Knowledge Bases, a managed RAG service queried in natural language and backed by Amazon S3 Vectors and Amazon Titan Embeddings V2, and a direct S3 Vectors lookup of pre-computed correction strategy files at correction/{schema_type}/{error_type}.json that carry confidence scores, 0.85 in the worked example.
- The agent picks whichever source scores higher (the pre-computed S3 file's 0.85 beat the knowledge base's 0.78) and applies the correction if it clears the default threshold of 0.7; otherwise the orchestrator publishes an Amazon SNS notification for manual review.
- S3 Vectors provide instant, deterministic fixes for known error combinations without model inference, while the knowledge base reasons about novel patterns using domain documents such as NOAA data guides, schema definitions, and error pattern catalogs.
- Corrected records keep their original fields and are annotated with the selected correction strategy, and the persistence agent writes them to both the transformed and corrected zones so downstream consumers and auditors see what was wrong and how it was fixed.
- The S3 data lake is organized in three zones: raw/ holds unmodified originals as an audit trail written by producers, transformed/ holds validated records written by the Glue ETL job plus the persistence agent, and corrected/ holds corrected records with correction metadata written by the persistence agent.
- The code remediation agent reads the repository using credentials stored in AWS Secrets Manager, correlates error type, schema type, and correction applied to find the upstream code, generates a change that preserves existing validation, and submits a pull request through the GitHub MCP Server; without repository credentials it logs that remediation was skipped.
- Deployment is a single cdk deploy with AWS CDK (Python): CodeBuild builds ARM64 container images, the knowledge base is created, and four AgentCore runtime resources are provisioned; knowledge sources populate automatically from the repository's knowledge_base/ folder.
- Prerequisites include Amazon Bedrock model access for Anthropic Claude (agent reasoning) and Amazon Titan Embeddings V2 (knowledge base indexing) in the target Region, the AWS CDK CLI with Python 3.10+, and Finch or Docker for local container builds, with all resources in a single AWS Region.
- Cleanup runs cdk destroy --all, which deletes stacks in reverse dependency order, empties buckets through autoDeleteObjects, removes ECR container images, deletes the S3 Vectors bucket and index, and force-deletes the Secrets Manager secret holding repository credentials.

## Details

### Validation and error routing

The Glue ETL job's dispatcher maps each of the 15 schema types to a dedicated validator. Failures carry an error_type and error_details payload, which is what the orchestrator receives. Because correction happens inline, records keep flowing to consumers instead of waiting in a dead-letter queue for manual triage.

### The correction decision logic

The correction agent queries the knowledge base and the S3 correction files in parallel and compares confidence scores. In the traced example both sources returned a strategy, the S3 Vectors file scored higher at 0.85 against 0.78, the 0.7 threshold was cleared, and the correction was applied. A low-confidence result instead sends an SNS notification with the error details to a configured email address for manual review, and the threshold can be tuned per schema or per error type.

### Code remediation at the source

Recurring errors are fixed at the source rather than only patched in the data lake, so the pipeline's error rate decreases as upstream code improves. The agent creates a branch, commits the proposed change, and opens a pull request with the root cause analysis in the description. The optional repository integration requires the git_repo_url context value at deploy time and a token set through the provided script.

### Design decisions

Four agents enforce separation of concerns: correction strategies can be updated without touching persistence logic, and low-confidence notifications live in the orchestrator independent of correction logic. The two knowledge sources play distinct roles: the knowledge base covers the long tail of unseen error combinations, while S3 Vectors cover common cases at deterministic speed. Applying a wrong correction is treated as worse than no correction, which is what the confidence threshold encodes.
