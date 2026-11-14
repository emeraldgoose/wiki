---
title: "OpenAI and Databricks: Enterprise AI on your governed data"
description: "Databricks lays out three adoption patterns for the OpenAI partnership, a multi-year agreement started in September 2025: business users answering governed questions in ChatGPT through the Genie plugin, engineers running Codex through Unity Gateway with budgets and audit logs, and custom agents built with GPT models, Model Serving and Databricks Apps under Unity Catalog. OpenAI is one of Databricks' largest customers, and every Databricks engineer is getting access to Codex."
tags: [source, databricks, openai, genie, unity-gateway, en]
locale: en
source_url: "https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data"
blog: databricks
published_date: 2026-11-14
---

# OpenAI and Databricks: Enterprise AI on your governed data

**Source**: [Databricks Blog](https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data) · **Published**: November 13, 2026

## Overview

Greg Brockman, co-founder and president of OpenAI, has a one-line diagnosis of AI deployed without company data: it is like hiring someone with 20 PhDs and never inviting them to a meeting. The OpenAI and Databricks partnership exists to fix exactly that. OpenAI contributes the frontier models, Codex and ChatGPT that people use every day; Databricks contributes the context those tools need to work inside a company — governed data, business definitions and access rules. Genie Ontology is named as the context layer holding those definitions, so ChatGPT using Genie knows what "revenue" or "active customer" means at your company before it starts working.

The post organizes enterprise adoption into three patterns: accelerating work for business users with ChatGPT and the Genie plugin, coding with enterprise-level governance through Codex and Unity Gateway, and transforming business processes with GPT models, Model Serving and Databricks Apps. Behind them sits one multi-year agreement, started in September 2025, in which each company is a customer of the other.

A recorded conversation between Databricks co-founder and CEO Ali Ghodsi and Brockman, on the shift from chatbots to autonomous agents, accompanies the announcement — and Databricks promises a separate post on each pattern over the next few weeks, with architecture details, setup steps and customer lessons.

## Key points

- The Genie plugin lets employees ask data questions directly in ChatGPT — for example, how weekly active user adoption tracks against target by plan tier — with Genie understanding the metric definitions, finding the relevant data, running the query in Databricks and returning visual graphs and charts.
- The plugin runs on the Genie MCP; Genie applies the company's own approved metrics and definitions from Genie Ontology, so revenue in ChatGPT matches revenue in the finance reports.
- Users see only data they already have permission to see, and each answer links to its sources in Databricks.
- ChatGPT Work can recommend next steps and who should be involved, share findings through Slack or email, and carry out approved actions through connected tools.
- Codex signs in with a Databricks credential while the OpenAI key stays inside Unity Gateway; every request is logged, and engineering leaders set budgets, review spend by team, and pick which GPT model handles which task.
- Getting started with pattern two is short: install the Unity Gateway CLI and run ug codex.
- On Databricks, OpenAI frontier models run next to governed data under Unity Catalog; when Databricks serves the model there is no external API key to manage.
- Teams can build and evaluate agents in Agent Bricks, or write them with the OpenAI Agents SDK and deploy them as Databricks Apps from the workspace template.
- The partnership is multi-year, started September 2025, and mutual: OpenAI is one of Databricks' largest customers, and every Databricks engineer is getting access to Codex.
- Databricks gets early access to new OpenAI models, and OpenAI models lead on OfficeQA, a Databricks benchmark for real document work.
- Model Serving runs GPT models next to company data for calls from SQL, notebooks and agents, and Lakebase, a managed Postgres database, keeps memory and state for agents.
- Available models include the GPT-6 family and the open-weight gpt-oss models, callable from SQL, notebooks and agents.

## Details

### Pattern 1: ChatGPT plus the Genie plugin

Historically, employees who needed numbers to make decisions could not write SQL, so they looped in analysts or pasted data into AI tools that did not know the company's definitions — waiting slowed decisions, and answers built on wrong definitions led to wrong decisions. Now a product manager asks in ChatGPT; Genie reads the approved metric definitions, finds the relevant data, runs the query in Databricks and returns graphs and charts. Setup is deliberately light: install the plugin, a Databricks admin turns on Genie, and each user connects it to ChatGPT, seeing only the data they are allowed to see.

### Pattern 2: Codex through Unity Gateway

AI coding agents usually spread one team at a time, and leaders lose track of who uses them, what they cost, and where code and data end up. Unity Gateway is offered as the rollout path: developers use Codex as they do today, sign-in is a Databricks credential, the OpenAI key never leaves the Gateway, and every request is logged. Around it sit related integrations — the Neon plugin for Codex creates Neon serverless Postgres projects, runs SQL and manages migrations from Codex, while Databricks Agent Skills teach Codex the Databricks CLI and SDKs.

### Pattern 3: GPT models with Model Serving and Databricks Apps

Agents that could change core business processes often stall before production, because the data they need sits behind strict security and governance rules. On Databricks, the frontier models run next to that data under Unity Catalog governance. Agent Bricks covers building and evaluating agents; the OpenAI Agents SDK route deploys as Databricks Apps via the workspace's Agent template. Databricks Model Serving hosts the GPT models so calls come from SQL, notebooks and agents without a separate API key.

### The wider integration map

Two more plugins round out the picture: the Codex Data Science plugin runs Codex data science workflows on the Lakehouse, and the ChatGPT Data Analyst plugin creates and edits dashboards in ChatGPT over data connected through Genie. A one-click ChatGPT connection links ChatGPT to Databricks without admin setup and applies each user's existing permissions. Across every pattern the same Unity Catalog permissions and Unity Gateway cost controls apply, and Databricks points teams that already live in ChatGPT and Codex to the Genie plugin and Unity Gateway as the starting moves.
