---
title: "Scaling beyond one: How Airbnb evolved its data architecture for a multi-product world"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://airbnb.tech/uncategorized/scaling-beyond-one-how-airbnb-evolved-its-data-architecture-for-a-multi-product-world"
blog: airbnb
published: 2026-10-17
---

# Scaling beyond one: How Airbnb evolved its data architecture for a multi-product world

## Overview

The May 2025 Summer Release added Services and relaunched Experiences alongside Homes, forcing Airbnb's decade-old offline data warehouse to absorb two new product pillars without breaking analytics. Rather than mandating one modeling style, the data organization set three centralized principles and let each domain team choose separate or monolithic models using shared guidelines — balancing consistency with domain-specific flexibility.

## Three foundational principles

First, no hybrid models: each domain must be fully separate by product or fully monolithic, avoiding inconsistent half-combined states. Second, consistent identifier naming tied to the choice — separate models use product-specific IDs (e.g., `id_experience`, `id_service`), monolithic models use a generic descriptor (e.g., `id_product_listing`) plus a product-type column. Third, clear namespace organization: product-specific tables in dedicated product namespaces, cross-cutting tables in a global namespace, plus team namespaces for intermediate assets.

Decision guidelines covered shared vs. unique attributes, future product extensibility, upstream online-schema alignment, downstream query patterns, maintainability, volume and performance, compatibility with existing Homes models, and business continuity for key metrics.

## Separate vs. monolithic in practice

The decisive question was whether product lines share attributes. User-facing domains chose separate models: Listings (Services introduced nested offerings under a parent listing), Availability (flexible business hours translated into bookable slots), Location (radius-based service areas vs. fixed listing addresses), and Guests (distinct high-volume funnels per product). Foundational domains chose monolithic models: Messaging (threads can span products and support), Payments (product-agnostic transactions and payouts), and Customer Support (cases spanning multiple bookings need one unified view).

## Challenges and takeaway

Two realities complicated rollout: upstream online schemas optimized for app speed rather than analytics clarity, making the warehouse a crucial translation layer into a reliable source of truth; and legacy tables with hundreds of downstream consumers requiring careful dual-run migration and slow deprecation. The lesson: at scale the answer is rarely one-size-fits-all — central consistency plus empowered domain choice, with discipline to address data debt alongside new builds.

## References

- Original article: https://airbnb.tech/uncategorized/scaling-beyond-one-how-airbnb-evolved-its-data-architecture-for-a-multi-product-world
