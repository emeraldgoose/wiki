---
title: "Personalization without user identity"
description: "Airbnb's Proximity Features group nearby users into buckets to personalize search and recommendations for logged-out cold-start traffic."
tags: [source, airbnb, ml, personalization, privacy, en]
locale: en
source_url: "https://airbnb.tech/infrastructure/personalization-without-user-identity"
blog: airbnb
published: "2026-09-29"
---

# Personalization without user identity

## Overview

Much of Airbnb's acquisition traffic — visitors from ads or organic search — arrives logged out with no history, leaving ranking models with sparse features (the cold-start problem), worsened by GDPR consent rules and third-party-cookie deprecation. The team's answer is Proximity Features: group geographically nearby users into buckets of roughly 1,000 and aggregate their collective behavior into features, so any user whose IP can be geo-located gets personalization with no login or persistent identifier.

## The proximity key and adaptive clustering

The underlying hypothesis is geographic correlation: users browsing from the same city tend to search similar destinations and price ranges. A proximity key — a quantized lat/long tile plus, in dense areas, an IP hash bucket — identifies a neighborhood rather than a person, and works as a drop-in aggregation key wherever a model currently conditions on `user_id`.

Bucketing must handle wildly uneven density, so a two-phase adaptive algorithm subdivides dense coordinates with IP hash buckets while progressively coarsening sparse rural tiles until each bucket holds about 1,000 users. The partition has stayed stable since 2023 with daily refreshes. At serving time the IP resolves to a key and features are fetched from a key-value store as a soft dependency — a timeout simply means the model scores without them, never blocking the request.

## Privacy design

Privacy is structural: every feature reflects a group, never an individual. Clustering input excludes users without consent, coordinates are coarse and population-centered rather than address-level, and the pipeline integrates consent management and deletion controls end to end.

## Production impact

Proximity Features now serve multiple surfaces. Marketing landing pages went from static cards to personalized recommendations for cold-start traffic. Homepage AutoSuggest replaced its global fallback list (Paris, Barcelona, London, Rome) with location-aware suggestions — a new user in Beijing now sees Hong Kong and Tokyo — with gains concentrated among never-booked and dormant users and new regional diversity (Kuala Lumpur, Dubai, Jeju Island appearing where relevant). The same serving layer is being extended to personalized engagement emails. Full details appear in the team's KDD 2026 TSMO workshop paper.

## References

- Original article: https://airbnb.tech/infrastructure/personalization-without-user-identity
- Paper: https://arxiv.org/abs/2607.12246
