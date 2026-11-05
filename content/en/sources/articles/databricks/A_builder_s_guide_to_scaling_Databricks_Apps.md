---
title: "A builder’s guide to scaling Databricks Apps"
description: "How to scale Databricks Apps from design to production: latency targets, architecture, state, testing, and instance sizing."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/builders-guide-scaling-databricks-apps"
blog: databricks
published_date: 2026-11-06
---

# A builder’s guide to scaling Databricks Apps

**Source**: [databricks](https://www.databricks.com/blog/builders-guide-scaling-databricks-apps) · **Published**: 2026-11-05

## Overview

A Databricks App often grows from a handful of users to hundreds or thousands across an organization. The intuitive response is more compute, but that only helps once you know where requests spend their time and whether the app can actually use additional capacity. This guide presents scaling as a sequence of four stages: design, build, test and deploy, and operate. The focus is application performance and resiliency at scale, not deployment automation or scaling of other Databricks services that interact with the app.

The design stage starts by defining what users need and where work runs. Teams should agree performance targets such as p95 end-to-end latency, counting UI rendering and handling cold starts separately, plus peak concurrency and growth assumptions. Work that can wait should run outside app compute, for example as a background job, with streamed or polled status in the UI, and untrusted code should run in Databricks Sandbox rather than on instances serving users. App compute should stay focused on serving the UI and coordinating calls. Framework choice also needs scaling in mind: AppKit is recommended for new apps, FastAPI/Flask/Express backends can run multiple workers, while Streamlit or Gradio can be less suitable for multi-instance recovery.

State must be deliberately classified before building. Soft state, such as caches and in-progress work, can be rebuilt; hard state, such as business records, checkpoints, and saved preferences, must survive restarts and be stored durably in Lakebase or Unity Catalog. Because session affinity in Databricks Apps is best-effort and restarts or scaling can move a session, another instance must be able to rebuild a session from hard state. With memory or model-heavy apps, larger instances can help where added instances do not, because each instance loads its own copy.

The build and test stages translate these decisions into code that survives restarts, plus a load-test plan that models bursts, growth, and connection budgets. The operate stage right-sizes instances based on measured memory and CPU, validates session continuity during restarts and scale-out, and adjusts caches and connection pools. The guide illustrates these ideas with a retailer example: 2,000 store managers, 200 peak users, 400 stock checks per minute, 1,200 SQL statements per minute, and 20 statements per second during the busiest hour.

## Key points

- Start scaling work by defining p95 latency, peak active users, growth, and recovery requirements.
- Keep app compute focused on serving the UI and coordinating calls; run heavy and long-running work outside it.
- Separate soft state from hard state, and store durable state in Lakebase or Unity Catalog tables.
- Plan for instance affinity being best-effort, so sessions can be rebuilt after a move or restart.
- Choose frameworks and worker models that match scaling needs; Databricks recommends AppKit for most new apps.
- Load test bursts and growth, budget database connections separately, and size instances by measured limits.

## Details

The four stages are design, build, test and deploy, and operate. State categories include temporary working data, caches, work in progress, business records, checkpoints, and saved preferences. The guide warns that state kept in server memory, such as Streamlit's single-process session handling, needs explicit validation before scale-out. Tasks such as running user- or agent-generated code should be isolated in Databricks Sandbox. Complete sizing formulas, load-test scenarios, monitor setup, and platform commands are in the linked source.

## References

- Source: [databricks](https://www.databricks.com/blog/builders-guide-scaling-databricks-apps)
