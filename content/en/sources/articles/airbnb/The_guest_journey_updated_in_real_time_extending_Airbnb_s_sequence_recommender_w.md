---
title: "The guest journey, updated in real time: extending Airbnb's sequence recommender with Chronon"
description: "Airbnb adds Push Mode and near-real-time model transform to Chronon, cutting guest embedding staleness from two days to seconds."
tags: [source, airbnb, ml, recommendation, chronon, streaming, en]
locale: en
source_url: "https://airbnb.tech/ai-ml/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon"
blog: airbnb
published: "2026-09-23"
---

# The guest journey, updated in real time: extending Airbnb's sequence recommender with Chronon

## Overview

Airbnb's Transformer-based sequence encoder personalizes search ranking from each guest's bookings, reviews, and browsing history, but it ran as a nightly batch job — embeddings could lag real behavior by nearly two days. The team closed the gap with two general-purpose additions to Chronon, their open-source feature platform: Push Mode (event-driven notifications when streaming features update) and near-real-time Model Transform (running deployed models inside the streaming pipeline).

## Why batch was not enough

Staleness had two sources — the once-daily schedule and the job's own processing lag — so running batches more often would not suffice; the pipeline had to react to activity as it happened. The encoder was also built for full-day snapshots, not per-event invocation, and guest signals (page views, searches) arrive as independent streams that must merge with long-term profile state so embeddings stay comparable with batch output.

## Push Mode and near-real-time model transform

Push Mode extends Chronon's streaming jobs to publish a lightweight notification as soon as a new feature value commits, turning a polling step into an event-driven trigger. Near-real-time Model Transform lets Chronon call an already-deployed model — here the same Transformer encoder — directly inside the streaming flow and write the result back as an immediately servable feature. Combined, a guest's page view or search merges with existing sequence state, triggers the encoder, and lands a fresh embedding in the same low-latency store the batch job and ranking model already use. Both capabilities live in the platform (and are open-sourced), so other teams can reuse them for different real-time use cases.

## Results

Embedding freshness dropped from roughly two days to typically 10–30 seconds, so listings viewed minutes ago shape the very next search. Offline ranking quality improved +1.67% NDCG over the batch baseline — large for a decade-refined system — and online A/B tests showed about +0.33% uncancelled bookings, confirming freshness itself is a meaningful quality source.

## References

- Original article: https://airbnb.tech/ai-ml/the-guest-journey-updated-in-real-time-extending-airbnbs-sequence-recommender-with-chronon
- Chronon: https://github.com/airbnb/chronon
