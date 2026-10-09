---
title: "When History Fails You, Borrow from Geography"
description: Sequential geographic recovery signals and Bayesian prior propagation for corridor forecasts when local data is scarce
tags: [source, airbnb, forecasting, bayesian, hierarchical-models, data-science]
locale: en
source_url: "https://medium.com/airbnb-engineering/when-history-fails-you-borrow-from-geography-915a72b91b5c"
blog: airbnb
date: 2026-06-02
---

# When History Fails You, Borrow from Geography

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-06-02 · **Author**: Harrison Katz (Finance Data Science & Strategy)

## Problem: Shocks Break the Core Forecasting Assumption

Every forecaster assumes the future resembles the past — under unprecedented shocks the model "fails confidently," with precise intervals around the wrong answer. COVID's acute phase (early–late 2020) was only the start; **late 2020–2022 was worse**: overlapping asynchronous changes — staggered vaccine rollouts, country-timeline border reopenings, variant-driven reclosures hitting origin–destination *corridors* at different moments. Demand rebounded unevenly with no historical precedent and no single governing pattern. Waiting per-market for post-shock data meant forecasting blind for months, exactly when Finance needed reads most.

## Insight: Geography as a Time Machine

Recovery unfolded **sequentially**: Europe's booking-lead-time compression hit February 2020, North America's 4–6 weeks later on the same trajectory; vaccine turnaround came December 2020 in North America vs February–March 2021 in Europe (lead time measured vs a 2019 baseline; compression = shortened planning horizons, then re-lengthening). Once demand's reopening response was observable in one market, it became a genuine — imperfect but immediate — signal for later-reopening analogues (shared drivers: reopened borders, restored routes, lifted entry rules).

## The Math: Bayesian Prior Propagation

Standard hierarchical setup: corridor parameters θ_c drawn from a shared population (hyperparameters φ, similarity weights w(c,c')). Innovation: when change hits corridor c at τ_c and similar c′ later at τ_c′ > τ_c, **the posterior from the early corridor becomes the informative prior for the late one** — propagating observable evidence across space in real time instead of extrapolating from stale time. Transfer weighted by structural similarity (traveler composition, intl/domestic mix, accommodation mix). As local data accumulates in c′, the local likelihood automatically takes over — sharing is heaviest when it matters most, receding gracefully with no manual tuning.

## Practice

Built reactively from mid-2020: manual reference-corridor identification (reopened markets as priors for still-closed similar ones, heavy human judgment) → formalized scaled system. It earned its keep across reopenings, variant reclosures, and uneven vaccine rollouts. Prerequisites (not universal): **geographic breadth + granularity** (enough ahead/behind pairs and genuine analogues — Airbnb's global corridor network) and **fast local updating** once data arrives.

## Takeaways for SW Engineers

- **Sequential rollouts are leading indicators**: reframe "no local data" as "early evidence from analogous units."
- Hierarchical Bayes is the natural tool: shared priors with automatic local takeover.
- Treat crisis-built propagation as **standing infrastructure** — post-2020 disruptions keep arriving with their own geography and timelines.
- Companion: "How we knew COVID was over" (the *removal* side — forgetting stale structure).

## References

- Prior post: What COVID did to our forecasting models; Bayesian hierarchical time-series literature
