---
title: "Migrate Apache Solr to Amazon OpenSearch Service with the AI-driven Migration Assistant"
description: "End-to-end Solr 9.6 → Amazon OpenSearch Serverless migration using the AI-driven Migration Assistant for Amazon OpenSearch Service on Amazon EKS: assess, backfill via Reindex-from-Snapshot, validate — with a 600K-document demo catalog."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant"
blog: aws-big-data
published_date: "2026-11-19"
---

# Migrate Apache Solr to Amazon OpenSearch Service with the AI-driven Migration Assistant

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant) · **Published**: 2026-11-16

## Overview

Years of Apache Solr — ZooKeeper quorums, JVM patching, GC tuning, custom plugins — leave organizations eager to move, but the migration itself is what keeps them on aging infrastructure: Solr and OpenSearch schemas differ, application code targets the Solr HTTP API, and custom analyzers are baked in. This post executes a Solr-to-OpenSearch Serverless migration end to end with the Migration Assistant for Amazon OpenSearch Service (AWS Solutions Library), running on Amazon EKS, driven by the Migration Assistant CLI's interactive AI agent mode. The walkthrough uses Apache Solr 9.6 as the source with a 600,000-document synthetic product catalog; the same flow applies to Elasticsearch 5.x+ or self-managed OpenSearch sources. Assessment-only users can run the AI advisor standalone without provisioning infrastructure; the agent mode shows each command before it runs and never stores your credentials.

## Key points

- **Three phases**: (1) Assess — inventory source schema and query patterns, check permissions/accessibility, surface incompatibilities before any data moves; (2) Backfill — snapshot the source into S3, then stream it into the target with Reindex-from-Snapshot (RFS); (3) Validate — compare document counts, mappings, sample query results, and replay consistency between source and target.
- **Architecture**: the Migration Assistant on Amazon EKS runs RFS workers for backfill and capture proxies for live traffic; workflow pods assume a narrowly-scoped role via EKS Pod Identity (snapshot and capture S3 buckets + the target OpenSearch Serverless collection only, not broad account access). CloudFormation creates the VPC, NAT gateway, EKS cluster, IAM roles, ECR repository, and S3 bucket, so the deploying principal needs matching permissions plus `iam:PassRole`.
- **Install**: one-line install from the official Solutions channel — `curl -fsSL https://solutions-reference.s3.us-east-1.amazonaws.com/migration-assistant-for-amazon-opensearch-service/3.98.7/install.sh | bash` (pinned to 3.98.7; review the script first for a safer path — it runs without sudo, drops a binary into ~/.local/bin, and publishes no checksums/signatures, HTTPS is the only protection). Source on GitHub: aws-solutions/migration-assistant-for-amazon-opensearch-service. CLI v2, kubectl, and Helm required; agent mode needs a supported coding assistant.
- **Agent mode in plain language**: you describe the goal ("Assess my Solr 9.6 cluster…" / "Migrate my Solr 8.11 cluster to OpenSearch Serverless"). The agent connects read-only for assessment, deploys the infrastructure, or configures and runs the end-to-end workflow including historical backfill and optional live traffic capture/replay. Data-handling note: agent mode sends Solr schema/solrconfig.xml, sample queries, and endpoints to the third-party model — review what your coding assistant transmits if you have data-handling rules; treat `./migration-assistant-workspace/` (state, logs, assessment report) as credential-adjacent and protect it.
- **Account hygiene**: use a dedicated non-production account or a scoped deployment role with short-lived credentials from IAM Identity Center; point the assistant at a non-production source.
- **Outcome**: a 600K-document Solr catalog migrated to OpenSearch Serverless — assessed, backfilled, and validation-checked — with no ZooKeeper, JVMs, or custom plugins to maintain on the target, plus vector search and native AWS integrations.

## Details

The assessment phase is read-only: the agent connects to the source, analyzes the schema, identifies compatibility gaps (field mappings, analyzers, query-pattern differences), and produces a migration assessment report before anything moves. You supply the source directly in the prompt (SolrCloud endpoint or ZooKeeper connection string, collection name, auth method); the agent asks for what it needs.

The backfill phase snapshots the source to S3 and streams it through RFS into the Serverless collection; for live systems, the capture proxies record traffic for replay-based validation. The validate phase then compares source and target: document counts, mappings, sample query results, and replay consistency — the checks you need before cutting applications over.

This post is the execution companion to the 2024 AWS Big Data Blog planning-level comparison of Solr vs OpenSearch; it pins Migration Assistant 3.98.7 for repeatable results (substitute the latest release), and prompts/responses shown are directional because interactive mode is natural language. Exact prompts vary by version and environment.

## References

- Original article: [Migrate Apache Solr to Amazon OpenSearch Service with the AI-driven Migration Assistant](https://aws.amazon.com/blogs/big-data/migrate-apache-solr-to-amazon-opensearch-service-with-the-ai-driven-migration-assistant)
