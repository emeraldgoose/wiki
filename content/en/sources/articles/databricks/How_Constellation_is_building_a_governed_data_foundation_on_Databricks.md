---
title: "How Constellation is building a governed data foundation on Databricks"
description: "Constellation, operator of the largest US nuclear fleet, is building a governed Enterprise Data Platform on Databricks: conformed business entities and a semantic knowledge layer, Unity Catalog as the ownership-and-lineage model, one governed foundation across workspaces, and first AI use cases in nuclear engineering, outage planning, and sales."
tags: [source, databricks, data-governance, enterprise-architecture, en]
locale: en
source_url: "https://www.databricks.com/blog/how-constellation-building-governed-data-foundation-databricks"
blog: databricks
published_date: 2026-11-14
---

# How Constellation is building a governed data foundation on Databricks

**Source**: [Databricks Blog](https://www.databricks.com/blog/how-constellation-building-governed-data-foundation-databricks) · **Published**: 2026-11-12

## Overview

Constellation operates the largest nuclear fleet in the United States and is the nation's largest producer of clean, reliable energy, with generating capacity equivalent to the needs of 27 million homes and roughly 2.5 million retail customer accounts. Data pours in from asset management, supply chain, commercial and trading systems, and fleet operations, feeding everything from near-real-time market models to nuclear telemetry. In that setting, Renee Voves and Herman Lombard report, one of the hardest parts of preparing for AI was not choosing models — it was agreeing on what the data means.

The problem statement is a single question with no single answer: "How many customers do we have?" Retail keys on the billing meter, wholesale on the counterparty, and the CRM on an account or user — three correct answers with three different meanings. Strong data capabilities had grown within each domain, but cross-domain questions required extra effort to reconcile definitions, and data sat in dozens of places with no shared semantic layer. Acquisitions compounded it: Calpine, acquired in 2026, brought 79 power plants across 22 states and 27 GW of capacity on a completely separate stack with its own definitions, warehouses, and modeling conventions, so the Enterprise Data Platform (EDP) suddenly had to absorb an entity roughly Constellation's own size.

Constellation's answer is a governed EDP built on Databricks, chosen after a decision process that took only weeks. Databricks won because it left room to experiment, grow, and mature incrementally, and — just as importantly — because it could interoperate with the existing architecture instead of forcing a rip-and-replace. Three architectural pillars stand out. First, shared meaning as conforming semantics: the EDP team works with business leaders to define governed, conformed entities (what "customer" means across retail, wholesale, gas, and CRM) and replicates those definitions enterprise-wide, then maps business relationships — customer, contract, asset — in a semantic knowledge layer, using Data Vault selectively for critical, reusable entities that must flex as systems change (not every dataset is vaulted; the choice depends on whether an entity will be reused, audited, or evolved). Second, governance as an ownership model rather than mere access control: Unity Catalog provides lineage, fine-grained access, and a single permission model, with Unity Catalog metric views simplifying shared metrics, while internal approvals and governance act as the trust anchor — answering who owns the meaning. Third, multi-workspaces on one governed foundation: the same governed datasets surface across separate workspaces, so business semantics are defined once and consumed many times.

On that foundation, three early AI use cases show the range: a nuclear engineering assistant built with Databricks Genie and governed through Unity Catalog to help engineers find and use approved technical information; planned nuclear outage (maintenance) planning, where scheduling, work execution, and asset health data come together to help planners coordinate large crews and many work orders on a tight schedule while decisions remain with the outage teams; and sales intelligence for opportunity prioritization and next-best-action recommendations. Looking forward, Constellation is exploring Genie Ontology, a self-learning knowledge graph that adds business context, and Unity Catalog Pages, which centrally manages business definitions.

## Key points

- Constellation profile: largest US nuclear fleet and largest producer of clean, reliable energy; capacity equivalent to 27 million homes; about 2.5 million retail customer accounts; data from asset management, supply chain, commercial and trading systems, and fleet operations, up to near-real-time market models and nuclear telemetry.
- The core problem: high-quality per-domain data with no shared semantics — "How many customers do we have?" has three correct answers (billing meter for retail, counterparty for wholesale, account/user for CRM), data in dozens of places, no cross-domain semantic layer.
- Acquisition pressure: Calpine (2026) added 79 power plants in 22 states and 27 GW of capacity on a separate stack with its own definitions, warehouses, and modeling conventions — an entity roughly Constellation's own size for the EDP to absorb.
- Platform decision took weeks; Databricks chosen for room to experiment, grow, and mature, and for interoperability with existing architecture (no rip-and-replace).
- Pillar 1 — conforming semantics: governed, conformed entities defined with business leaders and replicated enterprise-wide; a semantic knowledge layer maps customer/contract/asset relationships across domains; Data Vault modeling applied selectively to critical, reusable, evolvable entities.
- Pillar 2 — governance as ownership: Unity Catalog for lineage, fine-grained access, and a single permission model; Unity Catalog metric views for shared metrics; internal approvals as the trust anchor; different data domains get different access and governance controls.
- Pillar 3 — multi-workspaces on one foundation: the same governed datasets surfaced across separate workspaces; semantics defined once, consumed many times.
- Use case 1: nuclear engineering assistant on Databricks Genie, governed via Unity Catalog, to ease finding and using approved technical information.
- Use case 2: planned outage (nuclear maintenance) management — refueling, major maintenance, regulatory inspections, equipment work; planning data from scheduling, work execution, and asset health systems brought together in Databricks; decisions stay with the outage teams.
- Use case 3: sales intelligence — consistent, accessible customer and commercial information for opportunity prioritization and next-best-action, on the same governed foundation with data guardrails.
- Forward look: Genie Ontology (self-learning knowledge graph adding business context) and Unity Catalog Pages (central management of business definitions) extend the semantic layer.
- The stated lesson: an enterprise data platform is as much about meaning and governance as technology; with Unity Catalog the data becomes trusted and discoverable, and data scientists can build ML and agentic AI (Genie One, Genie Agents) on top.

## Details

### Why semantics before AI

Constellation's framing is that in a safety-and-reliability-first business, getting definitions and governance right drives every architectural choice. Domains had each built strong capabilities, but the value of those capabilities stopped at domain boundaries; cross-domain questions needed manual reconciliation. The EDP therefore targets the meaning layer first: conformed entities are negotiated with business leaders rather than imposed, and the semantic knowledge layer expresses how customers, contracts, and assets connect across domains.

### Data Vault, selectively

The modeling choice is deliberately non-uniform. Data Vault is applied to critical, reusable entities that need to flex as systems change; datasets that will not be reused, audited, or evolved do not get vaulted. This mirrors the conformed-semantics approach: consistency is required where meaning must survive system change, not everywhere.

### Governance as an ownership question

The article stresses that Constellation's decisive criterion was a platform that could convey semantic meaning to stakeholders, not just enforce access. Unity Catalog's lineage, fine-grained access, and single permission model answered the technical half; the organizational half — who owns the meaning — was settled through internal approvals and governance structures that became the trust anchor for everything built on the platform. Metric views then make shared business metrics consistent across domains.

### Where AI fits

Because the governed foundation provides a controlled environment, the AI use cases could be built on the same substrate: a Genie-based engineering assistant, outage-planning analytics with decision authority kept with the outage teams, and sales intelligence with guardrails. The forward-looking pieces (Genie Ontology, Unity Catalog Pages) extend the same thesis — make the business context machine-usable and centrally defined so analytics and AI scale beyond a single domain.
