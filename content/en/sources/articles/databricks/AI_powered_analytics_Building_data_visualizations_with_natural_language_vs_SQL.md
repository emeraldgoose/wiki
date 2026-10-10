---
title: "AI-powered analytics: Building data visualizations with natural language vs. SQL"
description: "Why NL-to-SQL underdelivered for a decade and how a governed semantic layer makes natural-language visualizations trustworthy"
tags: [source, databricks, ai-engineering, semantic-layer, governance, genie, en]
locale: en
source_url: "https://www.databricks.com/blog/ai-powered-analytics-building-data-visualizations-natural-language-vs-sql"
blog: databricks
published: "2026-10-06"
---

# AI-powered analytics: Building data visualizations with natural language vs. SQL

**Source**: [Databricks Blog](https://www.databricks.com/blog/ai-powered-analytics-building-data-visualizations-natural-language-vs-sql)
**Date**: Oct 6, 2026

## Problem

Natural-language querying for visualizations has existed for a decade but never lived up to its promise. Early NL-to-SQL treated the task as language-to-schema translation: map words to columns, emit a query, return a chart. That works for simple lookups and collapses on enterprise reality — competing metric definitions across teams, ambiguous joins, business rules living in people's heads, and no authority signal when two numbers conflict. Models were not the bottleneck; context was. Guessing meaning from table and column names is why the same question could yield two different answers.

## Solution: Governed Semantic Layer

What changed is the layer underneath the model. Before any SQL is generated, the agent must already know what "net revenue" means for this team, which table is certified, how fiscal periods are defined, and which filters always apply. Databricks' Genie Ontology is one implementation: explicitly modeled knowledge (metric views, governed pages, domains, certified sources) combined with context learned from dashboards, queries, and notebooks. Each learned snippet carries an authority score from source, usage, freshness, and certification; at query time a ranker resolves competing snippets on relevance plus authority and delivers only context the user may see.

## Three Trust Requirements

- **Governed data**: clean, consistently categorized records with fine-grained access control, so each user sees only authorized rows and columns.
- **Explicit machine-readable meaning**: governed metric definitions, business terms, key relationships, and certified sources registered where the agent consumes them (e.g. Unity Catalog).
- **Verification layer**: every answer traces back to the definitions, sources, and permissions that produced it, so a business user inspects why the system said it, not just what it said.

## Conversation State

Follow-ups ("break that down by region") require resolving references against prior turns' metric, window, and filters. Genie keeps thread state — metadata, editor instructions, prior turns — asks clarifying questions instead of guessing, and can pull in earlier conversations. Stable ontology definitions prevent meaning drift across turns; relevant-context selection (not naive appending) protects the context window.

## Bringing It to Everyday Tools

Integration paths keep permissions intact: the Genie Conversation API for embedded querying, the Genie One MCP server for assistants like Claude or Copilot, and embeddable Genie Agents running on a SQL warehouse under the author's credentials while Unity Catalog enforces each end user's rights. The recommended pattern is on-behalf-of OAuth, so two people asking the same chatbot the same question get answers scoped to their own data.

## Seminar Takeaways

- NL-to-SQL failed on semantics, not syntax; the fix is a governed meaning layer, not a bigger model.
- Governance must guide every agent decision (tables, joins, definitions, row visibility), not apply after the fact.
- Inspectability (provenance per answer) is what separates a trustworthy system from a faster way to be wrong.
- Per-user enforcement has to survive embedding: OBO auth propagates identity through every integration.

## Related Concepts

- [AI Agent](concepts/ai-engineering/agent.md) (agent-side analyst decisions)
- [RAG](concepts/ai-engineering/rag.md) (grounding generation in retrieved context)
