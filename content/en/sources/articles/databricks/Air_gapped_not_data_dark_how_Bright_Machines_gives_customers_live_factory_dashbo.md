---
title: "Air gapped, not data dark: how Bright Machines gives customers live factory dashboards without opening the plant"
description: "Bright Machines streams PostgreSQL changes out of air-gapped factories with Debezium into Apache Iceberg over a single auditable outbound path, and reads them in Databricks in place through Unity Catalog federation — one governed platform replacing a nine-service pipeline."
tags: [source, databricks, data-engineering, unity-catalog, manufacturing, en]
locale: en
source_url: "https://www.databricks.com/blog/air-gapped-not-data-dark-how-bright-machines-gives-customers-live-factory-dashboards-without"
blog: databricks
published_date: 2026-11-13
---

# Air gapped, not data dark: how Bright Machines gives customers live factory dashboards without opening the plant

**Source**: [Databricks Blog](https://www.databricks.com/blog/air-gapped-not-data-dark-how-bright-machines-gives-customers-live-factory-dashboards-without) · **Published**: 2026-11-11

## Overview

Bright Machines builds software-defined, automation-first production lines inside its customers' plants — and those plants are locked down by design: no inbound access, minimal outbound, zero tolerance for risk. Every line runs an on-premises stack (in-house MES, customer MES integrations, operator screens, robot workflow orchestrators, assembly dashboards) persisting to PostgreSQL on the factory cluster, feeding KPI dashboards, finance reporting, operations, quality, vendor component quality, NCR tracking, genealogy, OEE, and downtime and cycle-time analysis. The problem was that customers standing in front of the assembly dashboard wanted the data behind it — yield by station, cycle-time trends, downtime by cause, batch genealogy — and the only way to share it was reports rerun on-prem and sent by email, with each new report costing hours to days of ETL engineering.

The first attempt — rebuilding a cloud copy of each factory database from application events across nine loosely coupled services — worked on the factory floor but failed everywhere else: it broke when schemas changed, failures went unnoticed, and it had no real access controls. The redesign starts from the security model instead of the pipeline. Changes are captured at the factory edge with Debezium change data capture and written as Apache Iceberg, then pushed out over a single auditable outbound path with edge buffering so a WAN blip never becomes a production database incident. Databricks reads the Iceberg tables in place through Unity Catalog federation with AWS Glue — zero inbound ports stay open to the plant. One governed platform now serves role-based AI/BI Dashboards integrated with Bright Machines' SSO federation, plus OpenSharing access that publishes zero-copy governed silver tables to customers with Databricks accounts; bronze views, silver models, the job, the dashboards, and the shares all deploy from one Databricks Asset Bundle.

The numbers are the argument for the redesign. A row committed on the line is queryable in Databricks in one to two minutes at steady state, silver models and dashboards refresh every ten minutes, and a heartbeat check detects a broken pipeline in under thirty minutes instead of days. The proof of concept took about six weeks with two engineers, and the first customer-visible dashboard went live about two months after kickoff. Next on the roadmap is making the governed data accessible to AI: natural-language analytics with Genie, custom AI agents for operations via Databricks Apps or Agent Bricks (so a line lead can ask "Why did station 4 have higher downtime this shift?" against the same governed silver data), and predictive analytics on factory data.

## Key points

- The old architecture shared factory data by rebuilding a cloud copy from application events across nine loosely coupled services — fragile on schema changes, silent on failures, and without real access controls.
- The new edge path is minimal and auditable: Debezium CDC plus a local object store plus one sync component, pushing Apache Iceberg tables out over a single auditable egress with zero inbound ports to the plant.
- Databricks never copies the data: Unity Catalog federation reads the Iceberg tables from AWS Glue in place, so one governed platform replaces the nine-service pipeline.
- The five lessons for sharing data from locked-down sites: start from the security model you already have; design the one path out first and buffer behind it; keep control of when a table moves forward with a catalog hop you own and a guard on the pointer; build the data once and let permissions do the rest; assert freshness on a heartbeat, not on row counts.
- The heartbeat principle matters because no new rows only means the line is idle — no new heartbeat is what means the pipeline is broken.
- Freshness: line commits are queryable in Databricks in 1–2 minutes; silver models and dashboards refresh every 10 minutes; operators needing true real-time views keep the on-prem assembly dashboards.
- The catalog hop with a pointer guard means the lakehouse only ever sees a table version the team has validated.
- Portability: only the edge sync target, cross-account replication, and the catalog hop are AWS-specific; everything on the Databricks side is identical on any cloud.
- Deployment is unified: bronze views, silver models, the job, dashboards, and shares ship from a single Databricks Asset Bundle.

## Details

- The air-gapped constraint is absolute by design: no inbound access, one tightly controlled route out, and role-based access rules restricting access from inside as well.
- Customer sharing now has two layers: AI/BI Dashboards with role-based permissions integrated with Bright Machines' SSO federation, and OpenSharing access that publishes zero-copy governed silver tables to customers with their own Databricks accounts.
- The monitoring change is about semantics, not tooling: row-count-based freshness checks confuse an idle line with a broken pipeline, so the team asserts freshness with a heartbeat that detects a broken pipeline in under 30 minutes.
- The AI roadmap builds on the same governed silver data: Genie for natural-language analytics, custom operational agents through Databricks Apps or Agent Bricks for non-SQL users (operators, quality engineers, maintenance techs), and predictive analytics to turn factory data into forward-looking decisions.
- Timeline: proof of concept in about six weeks with two engineers; first customer-visible dashboard live about two months after kickoff.
