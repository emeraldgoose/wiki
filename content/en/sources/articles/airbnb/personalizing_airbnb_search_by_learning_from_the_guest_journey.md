---
title: "Personalizing Airbnb Search by Learning from the Guest Journey"
description: JourneyFormer — Transformer sequence model over guest history; +3.78% NDCG, +0.55% bookers online
tags: [source, airbnb, recommendation, personalization, transformer, ranking]
locale: en
source_url: "https://medium.com/airbnb-engineering/personalizing-airbnb-search-by-learning-from-the-guest-journey-bcefd1915624"
blog: airbnb
date: 2026-07-21
---

# Personalizing Airbnb Search by Learning from the Guest Journey

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-07-21 · **Authors**: Daochen Zha, Chun How Tan, Xin Liu, Bin Xu, Han Zhao, et al. (Search/Relevance team). Deep version: KDD '26 *JourneyFormer* paper.

## Problem: Trips Aren't Single Sessions

A guest browses dozens of listings over days; over years they accumulate bookings, reviews, cancellations. Legacy ranking compressed this into hand-crafted aggregates (total bookings, avg price — hundreds of features): unscalable and inexpressive. Goal: learn guest-preference representations directly from the event sequence.

Three challenges: (1) sequences dominated by listing views (up to hundreds of thousands per guest — intractable raw); (2) **Airbnb optimizes booking conversion, not engagement** — bookings are rare/deliberate, views are noisy; generalizing from sparse noisy signals differs fundamentally from social-media modeling; (3) training on hundreds of millions of search-label pairs is expensive.

## Solution

**Sequence design** — split into two capped streams (thresholds cover all but the longest 2%):
- **Long-term** (7 years): bookings, reviews, cancellations — cap 80 events.
- **Short-term** (21 days): listing views — cap 200 events.
Shared feature pool with a **unified embedding table** for high-cardinality IDs (listing, host, hierarchical geo).

**Training efficiency (~4x throughput)**:
1. **Search batching**: with a causal mask, one encoder pass serves multiple searches — the embedding at position T=3 represents history for the search at T=4, etc. Three searches share one forward pass.
2. **Length bucketing** to cut padding waste; 3. **sparse search computation** to drop padded searches from the ranker.

**Serving**: sequence encoder runs as a **daily batch job** writing embeddings for guests with new events; the live ranker fetches the stored embedding + query and scores candidates — full history depth at low query-time latency.

**Three-stage rollout** (each 3-week A/B, business + guardrail metrics): long-term sequence alone → + short-term views → + **setwise ranker** co-trained with the encoder (scores candidate *sets* jointly, reasoning about relative differences, vs pointwise independence).

## Results (0.3% NDCG is "significant" at Airbnb scale)

| Stage | Offline NDCG (booking labels) | Online A/B |
|-------|-------------------------------|------------|
| Long-term only | +0.44% | +0.31% uncanceled bookers, +0.38% views |
| + short-term views | +1.48% total | +0.55% bookers, +0.82% nights, +0.90% views |
| + setwise ranker | +3.78% total | +0.28% bookings, +0.32% requesters |

Signal generalized beyond search to promotional emails. Next: near-real-time embedding updates, wishlists/map interactions, target-aware and generative recommenders.

## Takeaways for SW Engineers

- **Split sequences by timescale**, not uniform modeling, when event densities differ by orders of magnitude.
- **Causal-mask batching** turns multi-query sequences from O(queries × seq) into one pass — the dominant win.
- **Decouple representation freshness from serving latency**: batch-encoded user embeddings + real-time scoring.
- Setwise (listwise-context) ranking unlocks gains pointwise scorers can't reach once representations are rich.

## References

- Coleman et al., "Unified embedding" (NeurIPS 2023)
- Tang et al., "Learning to Comparison-Shop" (CIKM 2025); Haldar et al., "Beyond Pairwise Learning-To-Rank" (CIKM 2025)
- Zha et al., "JourneyFormer" (KDD 2026): https://arxiv.org/abs/2606.19108
