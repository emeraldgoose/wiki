---
title: "Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work"
description: "AWS Data Analytics 플러그인을 사용하여 ChatGPT Work에서 Amazon Redshift 데이터에 대한 자연어 질의 및 대시보드 생성을 구현하는 방법을 알아봅니다."
source_url: "https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/"
blog: "AWS Big Data"
published: 2026-09-10
locale: "en"
---

# Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work

Data-driven decision-making is often limited by the technical barrier of SQL. While analysts and engineers can easily query data warehouses, business leaders (sales, operations, finance) often rely on pre-built reports, creating a bottleneck. AWS is bridging this gap with the new **AWS Data Analytics plugin** for the **Data agent** in **ChatGPT Work**.

This plugin allows any authorized team member to ask questions in natural language, analyze governed data across Amazon Redshift and data lakes, and create shareable dashboards—all within a conversational interface.



## Concept: Democratizing Data Access

The core concept is **Data Democratization**: moving from a model where data is a specialized resource to one where it is an accessible utility for all roles.

- **Traditional Model**: Analysts write SQL $\rightarrow$ Data is extracted $\rightarrow$ Reports are sent to business teams.
- **Conversational Model**: Business user asks a question in natural language $\rightarrow$ Agent translates to SQL $\rightarrow$ Data is analyzed and visualized instantly.

## Source

- **Title**: Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work
- **Blog**: AWS Big Data
- **URL**: [https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/](https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/)
- **Date**: 2026-09-10

## Guide: How the Plugin Works

The AWS Data Analytics plugin acts as an intelligent bridge between the conversational LLM and the structured data environment of Amazon Redshift.

### 1. Core Capabilities

The Data agent, powered by the plugin, performs several critical tasks:
- **Metadata Discovery**: Automatically identifies schemas, tables, columns, and data types available to the user.
- **NL-to-SQL Translation**: Converts natural language queries into optimized Amazon Redshift SQL.
- **Query Execution**: Runs the generated SQL against the user's existing Redshift environment.
- **Conversational Drill-down**: Maintains context across a chat session, allowing users to ask follow-up questions (e.g., "Why did revenue drop in this region?") to refine analysis.
- **Visualization**: Transforms tabular results into interactive, shareable dashboards.

### 2. Security and Governance

A critical requirement for enterprise data is maintaining existing security postures.
- **Access Controls**: The plugin respects the user's existing **IAM and Redshift access controls**. If a user is not authorized to see a certain table, the agent cannot access it.
- **Governed Datasets**: It works with curated datasets and business definitions already maintained by analytics teams, ensuring that "revenue" is defined consistently across the organization.

### 3. Underlying Technology: Agent Toolkit for AWS

The plugin's intelligence is built using **Amazon Redshift skills** from the **Agent Toolkit for AWS**. These skills provide the agent with:
- Tested, service-specific procedures for metadata exploration.
- Proven workflows for constructing complex, multi-join SQL queries.
- Guidance on interacting with Redshift-specific features.

## Summary for Software Engineers

- **Integration**: Works with both Amazon Redshift provisioned clusters and Serverless workgroups.
- **Extensibility**: Beyond Redshift, the ecosystem supports AWS Glue Data Catalog, Amazon S3 Tables, Amazon Athena, and vector search.
- **Impact**: Reduces the "time-to-insight" for non-technical stakeholders while freeing up analysts to focus on higher-value modeling and architecture.

## References
- [ChatGPT Work Data agent](https://chatgpt.com/plugins/Plugin_fc9843a6fb34819195d6c7802398a8a7)
- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [Amazon Redshift Documentation](https://docs.aws.amazon.com/redshift/)
