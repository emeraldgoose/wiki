---
title: Measuring the Impact of Twitter Network Latency with CausalImpact
description: Using Google's CausalImpact (BSTS) package to quantify how edge-latency improvements move engagement and revenue
tags: [source, twitter, x, causal-inference, edge-network, experimentation, data-science, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/insights/2022/measuring-the-impact-of-twitter-network-latency-with-causalimpac"
blog: twitter
date: '2022-10-21'
---

# Measuring the Impact of Twitter Network Latency with CausalImpact

## Summary

Higher network latency degrades the Twitter experience, so the team launched an experiment switching the default edge to a faster public-cloud edge (better geographic coverage) in select countries. The catch: network configuration made it impossible to randomly assign customers to treatment — a classic setting where naive before/after comparisons are contaminated by external shocks and bias. The article presents the framework the team built around **Google's CausalImpact package** (Bayesian Structural Time Series, BSTS) to quantify the causal effect of latency improvement on revenue and customer engagement.

## Method: BSTS and CausalImpact

Causal impact is the gap between the treated group's observed response and its unobserved counterfactual. CausalImpact fits a BSTS model on pre-intervention data (plus control time series from untreated countries) and projects the counterfactual forward; the pointwise and cumulative differences are the estimated effect. Three components do the work: **Kalman filter** (latent state: local trends, seasonality), **spike-and-slab regression** (automatic control-series selection), and **Bayesian model averaging with Gibbs sampling** (posterior uncertainty over the counterfactual). Advantages over Difference-in-Differences and Synthetic Control: flexible accommodation of seasonality/trends/posterior variability, time-varying impact with decay, and counterfactuals without prior knowledge of external covariates.

## The Analysis Framework

1. **Experiment design first.** Schedule away from holidays/seasonality; pick countries by customer-base size, latency baseline, and default-edge share; sequence the rollout so the counterfactual pool (N minus target countries) stays intact; watch neighboring countries for spillover; run at least two months (revenue/engagement lag); pre-register critical metrics (must stay stable) and metrics of interest.
2. **Validate the rollout.** Check p50/p95 content-refresh time (a high-impact, well-logged surface the traffic map optimizes for), focusing on the slowest users who gain most; fall back to Difference-in-Differences on performance, and stop if no significant latency change. Confirm stability of success rate, request volume, and default-edge share.
3. **Filter metrics deliberately.** Four groups — revenue, customer state (leading indicators of monetizable users/lifetime value), engagement, performance — selected for data availability (low sparsity, maintained datasets), sensitivity with short lag (external shocks like the Ukraine war can truncate the post period), alignment with objectives, and interpretability.
4. **Tune and evaluate the model**, checking consistency across runs.
5. **Interrogate counterintuitive results** (significant negative impacts): add more sensitive metrics (smaller customer subsets), check absolute impact vs. base size, vary periods, hunt for external shocks.
6. **Exploit external shocks**: when host degradation reverted latency to baseline, the team attempted a reverse-causality probe (degradation should hurt revenue/engagement) — inconclusive due to a short pre-period, but a useful template: shocks are natural experiments.

## Constraints

Over a year of training history but only ~one month of post-intervention data (Ukraine war truncated it; later network degradation shortened some countries further) — hence the emphasis on sensitive metrics and consistency checks. Future work: cross-validation in model selection, benchmarking BSTS against DiD/synthetic control, customer-subset experiments, and per-country latency thresholds for significant business impact.

## Relevance to SW Engineers

- When randomization is impossible (network routing, infra rollouts), BSTS-based counterfactual modeling is the principled fallback — but only with pre-registered metrics and rollout validation gates.
- Slow business metrics + short post-periods demand *sensitive leading* metrics; topline metrics alone will drown in noise.
- Treat external shocks as data, not just threats: pre/post inversions around degradations can corroborate the original causal claim.

## References

- Source: https://blog.x.com/engineering/en_us/topics/insights/2022/measuring-the-impact-of-twitter-network-latency-with-causalimpac (Widya Salim et al., 21 Oct 2022)
- CausalImpact: https://google.github.io/CausalImpact/CausalImpact.html; BSTS: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41854.pdf
