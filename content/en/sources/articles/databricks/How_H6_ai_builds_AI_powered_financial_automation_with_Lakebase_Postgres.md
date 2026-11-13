---
title: "How H6.ai builds AI-powered financial automation with Lakebase Postgres"
description: "AP-automation startup H6.ai gives every customer a dedicated Lakebase Postgres database and uses copy-on-write branching to freeze the exact financial state behind invoice issues, replaying real cases on disposable schema-migrated branches judged by deterministic assertions and an AI-judge panel — without mocks and without touching live data or the ERP."
tags: [source, databricks, ai-agents, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/how-h6ai-builds-ai-powered-financial-automation-lakebase-postgres"
blog: databricks
published_date: 2026-11-14
---

# How H6.ai builds AI-powered financial automation with Lakebase Postgres

**Source**: [Databricks Blog](https://www.databricks.com/blog/how-h6ai-builds-ai-powered-financial-automation-lakebase-postgres) · **Published**: 2026-11-12

## Overview

Traditional accounts-payable and invoice-processing tools force a trade-off: move quickly with AI automation and risk losing control, or keep tedious manual oversight. H6.ai, founded by Benji Borg and Mauro Pirrone to break that trade-off, automates AP on top of a company's existing ERP: it reads each invoice, matches it to a purchase order, assigns its lines to the right accounts, and checks it against the company's own policies — combining AI-assisted understanding with approved, deterministic, and auditable policy execution. The engineering challenge was finding a backend that could support frequent regression testing at scale.

The testing problem is specific to financial data: it never stands still. No two customers look alike — each brings its own ERP, suppliers, purchase orders, chart of accounts, and policies, and invoices range from a one-line service bill to documents with hundreds of lines. Worse, the underlying data moves: an invoice that matches an open purchase order with enough quantity left at 10 AM may face an order that is partly consumed, amended, or closed by the afternoon, so processing the same invoice again changes the answer even though the code has not. When a result changes, the team needs to know whether their change caused it or the customer's data did.

The solution is the Lakebase architecture — storage separated from compute, idle compute scaling to zero, and branching — chosen as the core system of record. Every H6.ai customer gets a dedicated Lakebase Postgres database holding their whole financial context: purchase orders and suppliers synced from the ERP, the chart of accounts and dimensions, past transactions, and H6 policy settings. When the team finds an invoice H6 handled incorrectly, they branch that customer's database and keep the branch as a snapshot: the purchase order that was open stays open in the snapshot with the same remaining quantities and prices, even after the ERP closes it. As the article puts it, they no longer try to recreate the conditions behind an issue — they keep them.

The test harness then runs real invoices against frozen states in four steps: migrate the snapshot forward on its own branch once per code version ("migrate once and fork many times"), fork a short-lived run branch per test, process the original invoice file exactly as production would against that run branch, then judge the result and delete the branch while the snapshot stays untouched. Judging combines deterministic assertions (final document status, matched purchase order, totals) with a panel of AI judges built on models from different providers that reviews the full outcome and returns pass, fail, or inconclusive with reasoning — so the team learns whether the outcome was right, not only whether processing finished.

## Key points

- H6.ai automates accounts payable on top of the customer's existing ERP: read the invoice, match it to a purchase order, assign lines to accounts, and validate against the company's own policies, combining AI-assisted understanding with approved, deterministic, auditable policy execution.
- Why regression testing is hard in this domain: every customer has its own ERP, suppliers, purchase orders, chart of accounts, and policies; invoices span one-line bills to hundreds of lines; and live data changes under the pipeline (open purchase orders get consumed, amended, or closed), so the same invoice can legitimately produce different answers over time.
- Architecture: every customer gets a dedicated Lakebase Postgres database as the multi-tenant platform's isolation boundary, holding ERP-synced purchase orders and suppliers, chart of accounts and dimensions, past transactions, and H6 policy settings.
- Lakebase branching is copy-on-write: a branch is a point-in-time copy that shares storage with its parent and stores only what changes, so creating one copies no data and appears instantly regardless of database size.
- Error forensics: when an invoice is handled incorrectly, the customer's database is branched and the branch kept as a frozen snapshot — an open purchase order stays open with the same remaining quantities and prices even after the ERP closes it; suppliers, accounts, dimensions, history, and policy settings are likewise preserved.
- Test run, four steps: (1) branch the snapshot once and apply current schema migrations, reusing that up-to-date branch for every run of the same code version (the snapshot itself is never modified); (2) fork a short-lived run branch per test; (3) let the candidate pipeline read and write the run branch as if it were the customer's database, processing the original invoice file exactly as in production; (4) judge the result against the expected outcome and delete the run branch.
- A test plan can mix cases from many customers, ERPs, and invoice formats, each against its own preserved database; because every run starts from the same frozen state, the same test gives the same starting point today, next week, and next quarter.
- Data protection: no mocks — isolation does that job. Test writes (review items, validation results, draft documents) land on the run branch and are deleted with it; tests never post to the customer's ERP and never write the live database. Branch management uses dedicated service principals with least-privilege access, and the branching guards refuse to touch a customer's live branch.
- Two-layer judging: deterministic assertions for exactly stateable facts (final status, matched purchase order, totals) plus a panel of AI judges built on models from different providers reviewing the full outcome against expectations and returning pass/fail/inconclusive with reasoning — catching regressions on real customer cases before production and enabling safe model swaps, extraction improvements, cost cuts, and matching/policy engine changes.
- Continuous coverage: every unusual invoice becomes a permanent regression test — its database snapshot, the invoice, and the expected outcome — so test coverage grows with the complexity of the customer base.
- What Lakebase Postgres provides: isolation (one database per customer), frozen state (branches keep the exact financial picture behind an issue), cheap disposable copies (copy-on-write), and schema-safe replays (old snapshots migrate forward on their own branch).
- Looking forward: Lakehouse//RT queries on Lakebase tables for read-only analytical queries without copying data — fresh analytics without a pipeline.
- Context from the FAQ: a lakebase keeps a transactional database's data in durable cloud object storage with a stateless engine (compute scales independently, storage on demand); Lakebase Postgres is a fully managed serverless Postgres on Databricks with autoscaling, scale-to-zero, instant branching, read replicas, instant restore, high availability, and native Unity Catalog integration; multi-tenancy can also use shared tables with PostgreSQL row-level security, with scale-to-zero keeping per-tenant databases cost-efficient.

## Details

### Why frozen state beats re-creation

The recurring failure mode in financial automation testing is trying to reconstruct the world as it was when an error happened: purchase orders have since closed, quantities changed, suppliers updated. Lakebase branches invert that effort — the team branches the customer's database at the moment an issue is found and preserves it. Because a branch shares storage with its parent and captures only deltas, keeping hundreds of such forensic snapshots is cheap, and each is exact rather than an approximation rebuilt from logs.

### Migrate once, fork many times

Schema evolution would normally break old snapshots. H6.ai's harness branches a snapshot once, applies the current migrations to that branch, and reuses the migrated branch for every run of the same code version — the snapshot itself is never modified. Each individual test then forks a short-lived run branch from the migrated copy, writes everything it needs, and is deleted with its branch. This keeps a growing library of historical cases compatible with current code without polluting live systems.

### AI judging as a complement, not a replacement

The article is explicit that deterministic assertions come first for facts that can be stated exactly, and the AI-judge panel covers what they cannot: whether the full outcome — including policy compliance and classification quality — matches expectations. The panel is deliberately built on models from different providers to avoid a single model family grading its own relatives. Together the two layers let H6.ai change models or engines and know, on real customer cases, whether outcomes actually regressed.
