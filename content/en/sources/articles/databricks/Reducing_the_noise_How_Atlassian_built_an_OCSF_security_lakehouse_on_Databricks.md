---
title: "Reducing the noise: How Atlassian built an OCSF security lakehouse on Databricks"
description: "Atlassian is a global SaaS provider serving 350,000 customers — the product of 20 years of growth and a long list of acquisitions, each of which arrived with its own logging formats."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks"
blog: databricks
published_date: 2026-10-15
---

# Reducing the noise: How Atlassian built an OCSF security lakehouse on Databricks

**Source**: [databricks](https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks) · **Published**: 2026-10-15

## Overview

Atlassian is a global SaaS provider serving 350,000 customers — the product of 20 years of growth and a long list of acquisitions, each of which arrived with its own logging formats. The result was a security data pipeline absorbing 44 billion events per day with no common language across various log sources. "You've got varied timestamps, you've got proprietary schemas, you've got operational drain for anyone trying to organize and structure this information," explained Zachary Schmerber, Senior Security Logging Engineer at Atlassian and a maintainer of the OCSF schema. Analysts were burning time normalizing data after it landed, cross-platform correlation was limited because data lived in different places and shapes, and SIEM pipelines were not keeping pace.

## Key points

- 80% reduction in ingestion cost after standardizing security telemetry on OCSF
- 500+ production threat-detection signals running on a single, unified schema
- 60% increase in analyst productivity — one repeatable process across every tool
- Up to 95% faster queries (from ~45 seconds to 2–3 seconds) using OCSF structure
- 44 billion events per day normalized into a common schema
- Winner of the Databricks 2026 Transformation Award

## References

- Original article: [https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks](https://www.databricks.com/blog/reducing-noise-how-atlassian-built-ocsf-security-lakehouse-databricks)
