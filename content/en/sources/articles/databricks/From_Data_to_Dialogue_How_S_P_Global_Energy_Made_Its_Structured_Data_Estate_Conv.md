---
title: "From Data to Dialogue: How S&P Global Energy Made Its Structured Data Estate Conversational with Databricks Genie Agents and MCP"
description: "S&P Global Energy's three-layer pattern — SME-curated Genie Agents per dataset group, managed MCP servers, and a FastMCP proxy — turned commodity data into conversational endpoints."
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks"
blog: databricks
published_date: 2026-09-25
---

# From Data to Dialogue: How S&P Global Energy Made Its Structured Data Estate Conversational with Databricks Genie Agents and MCP

**Source**: [Databricks Blog](https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks) · **Published**: 2026-09-25

## Overview

S&P Global Energy spans commodities (LNG, chemicals, crude, refined products, gas and power), each a family of datasets spread across Databricks and external sources. Hand-built text-to-SQL and per-use-case APIs kept domain experts behind an engineering backlog. The fix: SME-curated Genie Agents as the semantic layer, managed MCP servers as the integration contract, and a FastMCP proxy composing them into commodity bundles — cutting new conversational data products from months to days.

## Layer 1: narrow, SME-curated Genie Agents

Domain experts pick tables directly from Unity Catalog (or via Lakehouse Federation for external sources, with no new ETL) and create one focused Genie Agent per dataset group — e.g. separate LNG agents for cargo, outages, netbacks, and prices — rather than one giant agent. Inside each, SMEs add the context generic text-to-SQL skips: column descriptions, example queries, trusted assets, and business definitions like floating-storage thresholds. Curation became a domain activity, not an engineering ticket.

## Layers 2–3: managed MCP servers composed by proxy

Each Genie Agent is automatically a governed MCP server exposing an ask-then-poll tool pair, permissioned through Unity Catalog so agents only reach tables the user may see. A FastMCP proxy mounts group-level servers behind one composite endpoint per commodity with namespaced tools, so a question crossing outages and cargo fans out to both and synthesizes the result. One MCP-standard bridge then serves internal agents, customer-facing experiences, and external customers' own assistants.

## Results and practices

Time to market collapsed to days, SMEs became publishers instead of requesters, and Genie Agent Benchmarks keep accuracy measurable with a curate-benchmark-improve loop. Key lessons: keep agents narrow, federate before building pipelines, invest SME time in the semantic layer, namespace composite tools clearly, and track SME agreement with generated SQL as the leading trust metric.

## References

- [From Data to Dialogue: How S&P Global Energy Made Its Structured Data Estate Conversational](https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks)
