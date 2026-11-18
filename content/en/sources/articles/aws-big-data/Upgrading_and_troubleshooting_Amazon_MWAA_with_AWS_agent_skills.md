---
title: "Upgrading and troubleshooting Amazon MWAA with AWS agent skills"
description: "AWS publishes four MWAA agent skills (author/test/debug/upgrade) in the aws-data-analytics plugin of the Agent Toolkit for AWS — Airflow 2.x→3.x upgrades with a 2.11.x stepping-stone, blue/green or in-place, confirmation-gated changes."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills"
blog: aws-big-data
published_date: "2026-11-19"
---

# Upgrading and troubleshooting Amazon MWAA with AWS agent skills

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills) · **Published**: 2026-11-16

## Overview

Amazon Managed Workflows for Apache Airflow (Amazon MWAA) simplifies provisioning and upgrading the managed Airflow runtime, but keeping DAGs current is the hard part: Airflow keeps moving, teams fall behind, upgrades break code, and the 2.x→3.x jump in particular brings breaking changes, a Python transition, and a required stepping-stone version. Standard automation is often trained on stale Airflow syntax and mixes concepts across versions. AWS now ships MWAA agent skills in the open-source Agent Toolkit for AWS: instruction packages your coding assistant (Kiro, Claude Code, Cursor, Codex, …) loads to plan, execute, and debug MWAA upgrades with steps authored by AWS.

## Key points

- **Four skills in the `aws-data-analytics` plugin**: `authoring-mwaa-workflow` (author/deploy provisioned-environment Python DAGs and MWAA Serverless YAML workflows), `testing-mwaa-workflow` (trigger a deployed DAG/workflow, monitor to completion, retest after fixes, call debug/author skills on failure), `debugging-mwaa-workflow` (root-cause failed runs and tasks, missing DAGs, import errors, worker OOM, IAM permission errors), `upgrading-mwaa-environments` (upgrade a provisioned environment incl. 2.x→3.x via blue/green or in-place; updates and tests DAG code; for sources older than 2.11.x it plans the route through the latest 2.11.x as a bridge to in-place Airflow 3). The first three also work with MWAA Serverless.
- **How they work**: skills follow the open Agent Skills standard; they run AWS CLI commands against your resources and use the AWS MCP Server (bundled with the plugin) to fetch current AWS documentation at runtime and run CLI commands with sandboxed execution and audit logging. The assistant loads the right skill automatically from your prompt — you don't name it.
- **Agents make changes, not just recommendations**: depending on the task they can edit and deploy DAG files. Try on a development environment first, keep DAGs in version control, and verify every proposed change.
- **Prerequisites**: an AWS account with an existing MWAA provisioned environment (walkthrough starts at Airflow 2.11.x); an Agent-Skills-compatible assistant; IAM permissions scoped to the `airflow` (provisioned + REST API) and `airflow-serverless` (Serverless workflows/runs) action namespaces; least-privilege credentials (write access only for confirmed change steps).
- **Install**: Option A (Claude Code/Codex) — update the marketplace first (`/plugin marketplace update claude-plugins-official`) then `/plugin install aws-data-analytics@claude-plugins-official` (installing without the update can yield "Plugin not found"; the Anthropic directory may list an older version). Option B (Kiro) — add the AWS MCP Server to `~/.kiro/settings/mcp.json` (set AWS_REGION to your environment's Region) and run `npx skills add aws/agent-toolkit-for-aws/skills`, or `aws configure agent-toolkit` for auto-detection.
- **Walkthrough 1 — 2.x→3.x upgrade (confirmation-gated)**: the skill computes the ordered version path (inserting the 2.11.x stepping-stone and Python-transition when crossing 2.x→3.x); selects a strategy (new-environment blue/green, rehearsed in-place validated on a test copy, or direct in-place) based on whether run history and the same environment URL/ARN must be kept; validates DAGs with Ruff scanning, deprecation-warning log scans, and Docker validation; deploys and switches over, saving a resumable multi-session plan. It never creates an environment, changes a version, or modifies your environment without per-action confirmation, and confirms each version jump individually.
- **Walkthrough 2 — failed DAG**: the debugging skill walks common MWAA failure modes to root cause; then you fix manually or ask the authoring skill to update the DAG, and the testing skill re-runs it.
- **Sample prompts**: "Upgrade envname from Airflow 2.7.2 to the latest 3.x. We don't need the run history." · "Upgrade envname from 2.10.3 to 2.11.x. We must keep run history and the same URL. It has a large number of DAGs." · "Upgrade envname from 2.11.0 to 3.2.1 in place. Skip the test copy. Some DAGs import airflow.datasets and one runs 'airflow db clean' in a BashOperator."

## Details

The lifecycle pain is the upgrade loop: escape the break-fix cycle by upgrading incrementally with the 2.11.x bridge instead of jumping 2.x→3.x directly. The skills keep the assistant current with Airflow/MWAA behavior where generic automation fails. Example session: start with "What AWS Regions are available?" (confirms MCP connectivity) and "What can MWAA Skills help me with?" (confirms skill visibility), then drive the upgrade with the sample prompts above. During walkthroughs the skill emits structured plans and gates every mutating step behind confirmation; the saved plan lets a multi-session upgrade pause and resume.

All four skills support provisioned environments; authoring/testing/debugging also cover MWAA Serverless (YAML workflows). Follow Getting started in the Agent Toolkit for AWS User Guide and Using agent skills in MWAA in the Amazon MWAA User Guide for per-assistant setup.

## References

- Original article: [Upgrading and troubleshooting Amazon MWAA with AWS agent skills](https://aws.amazon.com/blogs/big-data/upgrading-and-troubleshooting-amazon-mwaa-with-aws-agent-skills)
