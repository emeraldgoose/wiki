---
title: "Clean data was never enough: How IFS Copperleaf taught AI its business with Databricks Genie One"
description: "IFS Copperleaf built IONA, a company-wide AI assistant on Databricks Genie One, answering across ~30 governed source systems; 70% activation since July 2026 launch and running costs covered within four months."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0"
blog: databricks
published_date: "2026-11-19"
---

# Clean data was never enough: How IFS Copperleaf taught AI its business with Databricks Genie One

**Source**: [databricks](https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0) · **Published**: 2026-11-16

## Overview

IFS Copperleaf is a leading global provider of Asset Investment Planning (AIP) software, helping asset-intensive organizations make better investment decisions, balance risk and value, and maximize capital impact. With more than 25 years of experience, IFS Copperleaf pioneered the AIP category and is now part of IFS, a global leader in enterprise cloud and Industrial AI software. In the fall of 2025, Misagh Jebeli, IFS Copperleaf's Enterprise Data Architect, and Lisa Richter, Director of Technology and AI, made the time to ask what working with data would look like in two years. Their bet: by 2027, people would stop looking for reports — the tools they use every day would understand the business, answer in plain language, and act on their behalf.

That bet became IONA, a company-wide AI assistant built on Databricks Genie One.

## Key points

- **IONA on Genie One**: anyone at IFS Copperleaf can ask plain-English questions across governed data from nearly 30 systems, including Salesforce, HubSpot and M365.
- **Clean data wasn't enough**: each team defined metrics like "active customer" differently. IONA answers on raw data, and business teams teach it what the data means through Skills, built on Genie Ontology and governed context.
- **Results**: ~70% activation rate since the July 2026 launch, with running costs covered within four months.
- **Comparison baseline shifted**: users judged IONA not against legacy reports but against the AI-native tools they use daily — wanting context memory, follow-up drafting, and action across systems.
- **Data in one place ≠ meaning in one place**: asking three leaders how many active customers the company had could still yield three numbers; AI could read every table yet not know a downsell from churn.
- **IONA shows its work**: when an answer looks off, it points the user to the data owner for that system — people fix the source instead of giving up on the tool.
- **Partnership, not just procurement**: the team shared prototypes and feedback that shaped Genie One, Genie Agents and Genie Ontology features.

## Details

The team expected the hard part to be data quality; it turned out to be meaning. Like most enterprises, IFS Copperleaf runs on many systems — CRM, marketing, support, contract and finance tools, each owned by a different part of the business. A cross-functional answer used to mean manual exports into a spreadsheet versioning abyss, reconciliation, and a meeting about whose number was right.

**First pivot — stop modeling everything.** The textbook approach says every table must be cleaned and modeled before querying. With nearly 30 source systems and tens of thousands of tables, that queue would never empty. The team flipped it: finance and the marketing-to-sales funnel, where stakes are highest, are fully modeled; for everything else, IONA answers directly on raw data. Data became useful months sooner, and modeling effort went where accuracy matters most.

**Second pivot — the business teaches the AI.** Unlike generic AI tools that either fabricate confident answers or stall without context, IONA — built on Genie and grounded in Genie Ontology — is designed to self-improve and prompt for more information when needed. Business teams encode what the data means (what counts as "active customer", how the business tells a downsell from churn) as Skills, so the meaning lives with the data rather than in people's heads.

User reaction surprised the team: people compared IONA to the best AI they had ever used, expecting remembered context, drafted follow-ups, and cross-system action — not just a chart back. And because IONA surfaces its reasoning and names the responsible data owner when an answer looks wrong, the organization fixes data at the source instead of routing around bad answers.

## References

- Original article: [Clean data was never enough: How IFS Copperleaf taught AI its business with Databricks Genie One](https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0)
