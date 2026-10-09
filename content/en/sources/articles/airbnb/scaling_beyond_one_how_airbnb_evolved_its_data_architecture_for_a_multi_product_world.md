---
title: "Scaling Beyond One: How Airbnb Evolved Its Data Architecture for a Multi-Product World"
description: Offline warehouse evolution for Homes + Experiences + Services — separate vs monolithic modeling framework
tags: [source, airbnb, data-engineering, data-modeling, data-mesh, warehouse]
locale: en
source_url: "https://medium.com/airbnb-engineering/scaling-beyond-one-how-airbnb-evolved-its-data-architecture-for-a-multi-product-world-6125645d470c"
blog: airbnb
date: 2026-06-09
---

# Scaling Beyond One: How Airbnb Evolved Its Data Architecture for a Multi-Product World

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-06-09

## Context

The May 2025 Summer Release (app redesign, relaunched Experiences, debut of Services) pushed Airbnb beyond Homes. Data + analytics engineering had to evolve a decade-old **offline warehouse** (analytics-oriented; online serving systems treated separately) to integrate two new product pillars without breaking vital analytics. Fragmentation risk: silos, inconsistent metrics, compounding tech debt.

## The Core Dilemma: Separate vs Monolithic

- **Separate models** per product line: clean, tailored — but duplicated logic.
- **Monolithic** unified tables: reusable, consistent — but unwieldy, poor fit for unique attributes.
- Neither dominates universally; guest data and payments data want different answers. Airbnb chose **centralized principles + decentralized modeling guidelines**: firm boundaries, per-domain choice.

## Three Foundational Principles

1. **No hybrid models** — a domain is *entirely* separate-by-product or *entirely* monolithic; hybrids guarantee future inconsistency.
2. **Consistent identifier naming** — structure follows the choice: separate ⇒ product-specific IDs (`id_experience`, `id_service`); monolithic ⇒ generic `id_product_listing` + `dim_product_type` discriminator. Reliable joins by construction.
3. **Clear namespace organization** — product namespaces for core product-specific tables, a global namespace for cross-cutting monolithic tables, team namespaces for intermediate assets.

## Modeling Guidelines (per-domain decision inputs)

Shared vs unique attributes · future evolution (4th, 5th product?) · upstream online-DB alignment · downstream query patterns · code maintainability · volume/performance · backward/forward compatibility (new-product changes must not endanger Homes models) · business continuity (key-metric accuracy during low-initial-volume + unexpected values).

## How It Played Out

The decisive question was **attribute overlap**:

- **Separate** (user-experience-adjacent domains): Listings (Services introduced *offerings* — many-to-one variants under a parent listing, e.g., a chef's menus — with no Homes/Experiences parallel); Availability (business-hours → discrete bookable slots); Location (radius-based service areas, host-travels-to-guest).
- **Monolithic** (cross-cutting domains like payments/finance-style flows): shared attributes dominate; one model with product-type discrimination.

Two cross-cutting realities: the warehouse is a **translation layer** (raw production shapes are rarely analytics-ready — reshaping is the DE/AE job), and **data debt must be managed while shipping** (legacy Experiences tables with hundreds of downstream consumers need dual-run validation and slow deprecation, not flag-day migration).

## Takeaways for SW Engineers

- "One size fits all" fails at multi-product scale — standardize the *decision framework and invariants* (no-hybrid, ID conventions, namespaces), not the model choice.
- Attribute overlap is the best first discriminator for separate-vs-monolithic.
- Protect the core product's models contractually (compat + continuity) while absorbing new lines.

## Related Concepts

- Data mesh (domain ownership + central standards); warehouse namespace/contract design
