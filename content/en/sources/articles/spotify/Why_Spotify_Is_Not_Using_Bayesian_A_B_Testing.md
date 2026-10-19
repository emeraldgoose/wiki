---
title: "Why Spotify Is Not Using Bayesian A/B Testing"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing"
blog: spotify
published_date: 2026-09-08
published: 2026-10-17
---

# Why Spotify Is Not Using Bayesian A/B Testing

**Authors**: Mattias Frånberg (Senior Data Scientist), Mårten Schultzberg (Senior Manager, Staff Data Scientist)
**Source**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing)
**Date**: Sep 8, 2026

## Overview

As commercial experimentation platforms add Bayesian modes marketed as modern, flexible, and easier to interpret, Spotify's experimentation team pushes back: "Bayesian A/B testing" is not one thing but a family of configurations (stopping rule × prior × likelihood), and popular claims about it confuse goals with configurations. Drawing on their paper ([arXiv:2608.12949](https://arxiv.org/abs/2608.12949)), they dissect four claims, show Bayesian and frequentist practice overlap far more than the debate admits, and explain why Spotify stays frequentist.

## Dissecting four claims

- **Peeking.** "Bayes needs no peeking correction" conflates two things: not caring about false-positive control (a goal, justified narrowly by the Likelihood Principle) versus using Bayes-factor stopping, which controls it automatically as a martingale under the null. The platform-default flat prior with posterior-probability thresholds reproduces the false-positive rate of frequentist peeking — no better, just renamed.
- **Multiple metrics.** Automatic handling is real only under a demanding setup: Bayes-factor stopping plus a well-calibrated empirical-Bayes prior with a point-mass null component fitted from the program's own history — a sophisticated multiplicity correction, not its absence. Poor calibration voids the guarantee.
- **Winner's curse.** The least problematic claim: any zero-centered informative prior shrinks estimates and helps. But platform defaults use flat priors, which provide zero shrinkage and suffer the curse exactly like frequentist point estimates. Misspecified historical priors (winner-only archives, pooled heterogeneous programs) performed worse than baseline group sequential testing in the authors' simulations.
- **Decision theory.** For common cost functions the optimal policy is Bayes-factor thresholds — which equal the frequentist mixture sequential probability ratio test, well approximated by group sequential testing. Costs and error rates become two parametrizations of the same rule; many teams could get the value by choosing alpha/beta from cost reasoning without switching frameworks. Only non-Bayes-factor-optimal cost functions (e.g. expected-loss stopping, ~50% false positives under flat priors) genuinely differ.

## Frameworks overlap; Spotify's decision

Under a flat prior and the two-group normal model, Bayesian and frequentist outputs are numerically identical: posterior mean equals MLE, one-sided posterior probability equals one minus the p-value. The genuinely advantageous Bayesian configuration — a maintained, per-metric empirical-Bayes prior — demands a large representative corpus, no cross-program pooling, drift monitoring, and statistician upkeep; for most organizations that cost outweighs the benefit. Spotify additionally values a single shared inference mode: two modes would split planning, monitoring, and interpretation across collaborating teams. Their advice: start from the guarantees your experiment program needs, then ask whether a specific Bayesian configuration beats what you have — for Spotify today, it does not.

## References

- [Why Spotify Is Not Using Bayesian A/B Testing — original article](https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing)
- [Companion paper (arXiv:2608.12949)](https://arxiv.org/abs/2608.12949) (referenced in the post)
- [Spotify on experimental evidence](https://confidence.spotify.com/blog/experimental-evidence) (referenced in the post)
- [Spotify's Experiments with Learning framework](https://engineering.atspotify.com/2025/9/spotifys-experiments-with-learning-framework) (referenced in the post)
