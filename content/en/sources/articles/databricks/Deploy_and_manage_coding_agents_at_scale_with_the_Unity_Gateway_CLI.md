---
title: "Deploy and manage coding agents at scale with the Unity Gateway CLI"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli"
blog: databricks
published_date: 2026-09-24
published: 2026-10-17
---

# Deploy and manage coding agents at scale with the Unity Gateway CLI

**Source**: [Databricks Blog](https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli) · **Published**: 2026-09-24

## Overview

Frontier coding models turn over every few days, forcing platform teams to choose between standardizing on one provider and scattering access, budgets, and logs across many. The Unity Gateway CLI (`ug`) resolves the tension: admins configure approved models, MCP tools, skills, and spending policies centrally, while developers launch any approved agent (e.g. `ug claude`, `ug codex`) with those settings applied automatically.

## Central configuration, familiar developer workflow

Admins manage agent defaults, MCP servers, skills, Smart Routing, and spending policies under Unity Gateway Govern, then publish one configuration change that every developer's CLI picks up on next launch — including cohort-based rollouts of new models. Organizations can distribute `ug` through device management so everyone starts from the same locked-down setup, with identity-level attribution on every request.

## Cost controls: Smart Routing, budgets, and tracing

Coding tasks vary in difficulty, so Smart Routing matches cheap models to simple work and capable models to hard work (about 35% savings on Databricks' internal coding benchmark). Budget-aware defaults steer new launches to lower-cost options as thresholds are hit, and `ug usage` shows spend per developer. Tracing captures agent tool calls into the lakehouse unified trace table, where Genie analysis found wasted tokens — Databricks' own team fixed seven MCP tool bugs this way for roughly $1.2M/year in recovered spend.

## References

- [Deploy and manage coding agents at scale with the Unity Gateway CLI](https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli)
