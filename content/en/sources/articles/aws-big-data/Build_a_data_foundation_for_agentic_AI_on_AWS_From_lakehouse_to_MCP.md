---
title: "Build a data foundation for agentic AI on AWS: From lakehouse to MCP"
description: "A four-pillar framework for an AI-ready data foundation on AWS: unified lakehouse with zero-ETL, context engineering, multi-agent interoperability via MCP and open protocols, and data/AI governance."
tags: [source, aws-big-data, agentic-ai, bedrock, lakehouse, mcp, governance, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp"
blog: aws-big-data
published_date: 2026-11-12
---

# Build a data foundation for agentic AI on AWS: From lakehouse to MCP

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp) · **Published**: 2026-11-11

## Overview

Building a data foundation ready for agentic AI is becoming a priority for organizations deploying AWS. The foundation relies on a unified lakehouse and interoperability protocols such as the Model Context Protocol (MCP). Teams can move from prototype to production. Yet many struggle to know where to start.

Gartner reports that more than 40 percent of agentic AI projects will be cancelled by 2027 for failing to deliver expected value; the root cause the authors identify is lack of governance and inconsistent data.

The post walks through four pillars for building an agentic-AI-ready data foundation on AWS.

## Four pillars for an agentic AI data foundation

### Pillar 1: Unified lakehouse with zero-ETL

The foundation starts with where the data lives and how it is queried. A lakehouse combines the flexible storage of a data lake (open formats, raw data on Amazon S3) with the governance of a data warehouse (ACID transactions, high-performance SQL). Amazon SageMaker Lakehouse requires no full migration; Amazon S3 Tables provides native Apache Iceberg support so data can be read and written from Spark, Athena, EMR, or Redshift.

For agents, a lakehouse needs three capabilities: zero-ETL ingestion (no pipeline management needed), a federated catalog (unified view of tables across S3, Redshift, Snowflake, or Databricks), and query federation (interrogate multiple sources without duplicating data). AWS Glue connectors bring in operational sources like Amazon Aurora, DynamoDB, and RDS, plus SaaS sources like Salesforce, ServiceNow, and SAP, and streaming sources like Amazon MSK and Kinesis.

### Pillar 2: Context engineering for high-performing AI agents

A lakehouse makes data accessible, but agents need curated, relevant context to act on it. LLMs remain stateless with a finite context window; long-context research shows a lost-in-the-middle effect where information away from the prompt's start or end is ignored. Context engineering addresses this with a context manager built on knowledge bases, session state/history, and data tools.

For knowledge bases, AWS offers vector store options including Amazon OpenSearch, Aurora PostgreSQL, and Neptune; Amazon S3 Vectors lets raw data and indexed embeddings share the same governed foundation. AgentCore memory automates the agentic-memory process (extraction module identifies key terms and writes them into long-term storage).

### Pillar 3: Multi-agent interoperability with MCP and open protocols

After agents retrieve the right context, the challenge is collaboration. Two open protocols address it: Agent2Agent (A2A) for agent-to-agent communication, and the Model Context Protocol (MCP) for connecting agents to systems.

MCP standardizes how agents access data and tools through resources, tools, and prompts; Amazon Bedrock AgentCore Gateway centralizes this access, enforcing authentication and audit logging in one place.

### Pillar 4: Data and AI governance for trust and compliance

Agents now communicate and act through MCP, so the underlying data must be trustworthy. Governance is the true differentiator; the authors argue foundation models are widely accessible, so data management is what sets agents apart.

Amazon SageMaker Data Catalog provides discovery, governance, and collaboration; it auto-generates summaries, glossaries, lineage, and quality indicators. Governance follows a publish-and-subscribe model.

## Key points

- Four pillars form the AI-ready foundation: unified lakehouse with zero-ETL, context engineering, interoperability via MCP/open protocols, and data/AI governance.
- Gartner: more than 40% of agentic AI projects will be cancelled by 2027 for under-delivering expected value; lack of governance and inconsistent data are the root causes.
- Zero-ETL ingestion removes pipeline management; federated catalog + query federation unify multi-source data views.
- Context engineering mitigates lost-in-the-middle (long-context) behavior via knowledge bases, session memory, and data tools.
- A2A handles agent-to-agent communication over HTTP/JSON; MCP standardizes agent-to-system tool access.
- Governance uses publish-and-subscribe with full access, row-level, or column-level filtering; SageMaker Unified Studio adds a generative AI assistant for querying.

## Details

The lakehouse combines data lake and warehouse approaches without a full migration; S3 Tables adds native Iceberg support. Context engineering uses vector stores (OpenSearch, Aurora PostgreSQL, Neptune, S3 Vectors) plus AgentCore memory.

The authors caution that LLMs have finite context windows; context engineering via context manager (knowledge bases, session state, data tools) mitigates lost-in-the-middle. AgentCore Gateway adds semantic search so agents query in natural language and receive only permission-scoped relevant tools.

Governance includes the SageMaker Data Catalog (discovery, governance, collaboration), auto-generated metadata (summaries, glossaries, lineage, quality), and publish-and-subscribe access. SageMaker Unified Studio adds a generative AI assistant to turn natural language into SQL/Python/viz cells.

The full technical walkthrough is a recorded AWS Summit Paris session video.

## References

- Original article: [Build a data foundation for agentic AI on AWS: From lakehouse to MCP](https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp)