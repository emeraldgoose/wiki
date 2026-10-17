---
title: "Genie One MCP: Give any AI Agent the Right Business Context"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context"
blog: databricks
published_date: 2026-09-22
published: 2026-10-17
---

# Genie One MCP: Give any AI Agent the Right Business Context

**Source**: [Databricks Blog](https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context) · **Published**: 2026-09-22

## Overview

General-purpose assistants can reach enterprise data yet still fumble questions like "why did net revenue drop 8%?" — terms differ across teams, sources conflict, and permissions vary by user. Genie One MCP solves this by exposing Genie One, grounded in the governed Genie Ontology context layer, as a tool to any MCP-compatible assistant (ChatGPT, Claude, Copilot, coding agents), so teams define business meaning once and reuse it everywhere.

## Why direct data access is not enough

Wiring an agent straight to tables provides access without shared meaning, creating four problems: uncertain accuracy (which sources, definitions, joins are approved?), higher cost and latency from repeated schema inspection, inconsistent governance across connections, and divergent answers per client or session. Genie Ontology instead combines approved metrics, definitions, relationships, ownership, and access policies with context inferred from trusted assets, letting Genie One pick authoritative sources and enforce the caller's permissions.

## How Genie One MCP works

The server exposes five tools — ask, poll-response, full-result fetch, cancel, and an MCP-Apps interactive view — plus a warehouse-pinning parameter. Identity flows through on-behalf-of-user OAuth so Unity Catalog privileges, row filters, and column masks apply per caller; two users asking the same question get appropriately scoped answers. Managed servers appear under Agents > MCPs with audit logs, query history, and billing telemetry. Production guidance: tune Genie in Databricks rather than client prompts, prefer single-domain Genie Agent MCP servers where they fit, register one OAuth app per client, and validate governance by impersonating different groups.

## References

- [Genie One MCP: Give any AI Agent the Right Business Context](https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context)
