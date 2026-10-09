---
title: "How We Knew COVID Was Over (and What Our Models Had to Unlearn)"
description: Airbnb forecasting discipline — refit vs respecify vs hold; forgetting pandemic-era assumptions on purpose
tags: [source, airbnb, forecasting, data-science, bayesian, ml-ops]
locale: en
source_url: "https://medium.com/airbnb-engineering/how-we-knew-covid-was-over-and-what-our-models-had-to-unlearn-c606b9bdb0ab"
blog: airbnb
date: 2026-08-19
---

# How We Knew COVID Was Over (and What Our Models Had to Unlearn)

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-08-19 · **Author**: Harrison Katz (Finance Data Science & Strategy)

## Context: Forecasts That Carry Weight

Airbnb's Forecasting DS team produces demand/booking/cancellation forecasts across thousands of markets that downstream teams plan against. A small persistent bias compounds into bad capacity, staffing, and finance decisions — so a drifting forecast is a **risk question**, not a methods question. One forecast had been missing in the same direction for several quarters despite routine refreshes, prompting this discipline.

## The Core Distinction: Refit vs Respecify vs Hold

"Retrain" conflates three different actions:

1. **Refit** (same model, new data) — cheapest option, right for ordinary drift. But not free: validation/shipping cost, and refitting on an unusual window can degrade a fine model. Default choice when the data-generating process is unchanged.
2. **Respecify** (change the model: add/drop features, alter structure, priors, likelihood) — expensive and frightening on a production forecast, but the **only place real improvement lives**. The tell for misspecification: the model misses the *same way over and over*.
3. **Hold** (deliberately do nothing) — takes the most nerve ("we decided to do nothing" on a watched forecast) yet is often correct. Cadence-driven retraining makes this choice for you in advance — always "refit" — so the three-way decision is rarely made on purpose.

Respecification cuts both ways: **adding** structure (e.g., borrowing across geography after 2020) or **removing** it — retiring an assumption the world outgrew. The second kind is the "unlearning," and teams systematically skip it because adding feels like progress.

## Three Failure Modes

| Failure | Mechanism | Example from the post |
|---------|-----------|----------------------|
| **Chasing noise** | Off-cycle refit absorbs a transient as the new level | A one-quarter event-driven booking spike refit early → next two forecasts biased high until the event aged out |
| **Carrying ghosts** | Crisis-era assumption stays on after the crisis; every refit looks clean | COVID-shifted cancellation-timing assumption persisted post-normalization until someone dug out the baked-in lean and respecified |
| **Respec-as-panic** | Rebuilding under deadline around a transient | FX swing on a major source market → widened priors instead; existing model rode it out, avoiding a fragile regime-tuned replacement |

## The Decision Rule

- **Refit** if the process is the one the model assumes, parameters just drifted.
- **Respecify** if the process changed in ways the model cannot represent no matter the estimation — fresh data can't help a model with no language for the new world.
- **Hold** if the miss is noise within tolerance — and say so explicitly ("Don't just do something; sit there").

Why it's hardest on important forecasts: holding looks like negligence, respecifying is costly/scary (teams under-respecify, ghosts accumulate), and COVID trained the wrong reflex — rebuild fast during the crisis, then leave pandemic assumptions switched on afterward.

## Takeaways for SW Engineers

- **Name the decision**: every refresh should be an explicit refit/respecify/hold call, not a cron job.
- **Monitor direction, not just magnitude**: same-direction misses over quarters ⇒ misspecification ⇒ respecify.
- **Schedule forgetting**: stale-structure removal needs an owner and a deadline like any feature; nobody schedules it by default.
- Companion pieces: COVID's impact on financial models; "When history fails you, borrow from geography" (geographic priors as the *additive* respec).

## References

- https://medium.com/airbnb-engineering/what-covid-did-to-our-forecasting-models-and-what-we-built-to-handle-the-next-shock-ccbf0e1f7fa9
- Bayesian hierarchical forecasting; forecast governance literature
