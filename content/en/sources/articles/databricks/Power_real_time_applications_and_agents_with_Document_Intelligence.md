---
title: "Power real-time applications and agents with Document Intelligence"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence"
blog: databricks
published: 2026-10-17
---

# Power real-time applications and agents with Document Intelligence

**Source**: [databricks](https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence)
**Date**: 2026-10-14

> Draft summary auto-extracted from the original article. Condensed here — see the original for full detail.
> Original: [https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence](https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence)

## Overview

At Databricks, our enterprise customers receive millions of documents every single day. These messy, unstructured documents hold critical context about operations, customers, and finances that power key downstream decisions across the business. Yet when a document arrives, putting that enterprise context to work is surprisingly tedious. For example: These are distinct workflows, but they share the same bottleneck: before customers can use the valuable data inside the documents for business analytics or decision-making, someone has to read each document and pull out what matters. That manual step slows everything downstream, and the bottleneck and costs explode as the incoming document volume grows.

## Key points

- Document workflows are traditionally built around asynchronous batch pipelines, delaying the operational context needed for immediate downstream decisions in interactive or human-in-the-loop settings.
- With Document Intelligence real-time REST APIs, your application can read and act on documents as they arrive. Call ai_parse_document, ai_decide, ai_classify, and ai_extract when a file is uploaded, so you can understand
- Build interactive document workflows with Databricks Apps or custom agents. Embed the REST APIs in applications or agentic workflow automations so documents can turn into business decisions in real-time.
- A contract lands in an inbox. A legal team member opens it, hunts for the parties, effective date, and renewal terms, then enters them into the system to track the agreement for years.
- An invoice arrives. An accounts payable specialist finds the vendor, PO number, and total, then enters them into the system so the invoice can go through approval and audit.
- An insurance claim shows up in a portal with a stack of attachments, and an adjuster reads all of it just to decide where the claim should be routed to.

## Source outline

- Process documents in real-time with synchronous REST APIs
- Integrate real-time document intelligence into your Apps and Agents

## References

- Original article: [https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence](https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence)
