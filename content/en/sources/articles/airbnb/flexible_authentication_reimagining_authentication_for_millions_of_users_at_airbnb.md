---
title: "Flexible Authentication: Reimagining Authentication for Millions of Users at Airbnb"
description: Server-driven Identify-first-then-Challenge auth rebuild — Challenge Picker, +2.6% auth success, -27% duplicate accounts
tags: [source, airbnb, authentication, identity, architecture, experimentation]
locale: en
source_url: "https://medium.com/airbnb-engineering/flexible-authentication-reimagining-authentication-for-millions-of-users-at-airbnb-3a8a4c917137"
blog: airbnb
date: 2026-08-12
---

# Flexible Authentication: Reimagining Authentication for Millions of Users at Airbnb

**Source**: Airbnb Engineering (Medium) · **Published**: 2026-08-12 · **Authors**: Jose Santos, Mike Barry

## Problem: Infrequent Logins Are Structural

Guests book in January and return in summer; hosts check in only on reservations. A failed login = lost booking and lost revenue for both sides. A decade of organic growth (password → social login → email OTP → phone) produced a rigid, client-heavy auth system that couldn't adapt per user, per region, or per experiment.

## Design 1: Identify First, Then Challenge

Old mental model: one question — "can you prove who you are?" New model: "given this session, what is the **easiest** way for this person to verify?"

- A traveler in Brazil with a phone number gets **WhatsApp OTP**, not SMS (penetration).
- A returning host in Korea gets **Naver login**, not Google.
- Flow splits into two stages: (1) identifier (email/phone/social, user's choice), then (2) a **server-side policy engine** picks the challenge most likely to succeed using session + account history.
- **The client never decides which challenge to present** — it renders whatever screen the server returns. Per-region tuning without shipping client code; experimentation becomes trivial.

## Design 2: Challenge Picker — No Dead Ends

Old failure mode: fail the presented challenge ⇒ stuck (password reset was its own journey with its own drop-off). Product principle turned hard requirement: **every auth screen must offer an escape**.

- Server returns the primary challenge **plus a ranked list of alternatives**, ordered by predicted success (past successes, registered methods, platform availability).
- "Try another way" adapts the flow in place instead of restarting it.
- Outages in one challenge stop blocking users — fallbacks are always one tap away.

## Design 3: Fully Server-Driven Screens

Motivation: every improvement waited weeks for app review before an experiment could even start. Solution: **the screen is the fundamental unit of abstraction** — identifier input, challenge, account picker, error recovery are all server-defined; Web/iOS/Android clients are thin renderers with auto-generated type definitions from the server schema (compile-time mismatch detection).

## Results

- **-60% code**, -100KB web bundle (client state management, design-system, and localization simplifications).
- **Velocity**: 20+ experiments in 3 months post-launch; idea → measured result collapsed from weeks to days (most with zero client changes).
- **+2.6% successful authentications** (from an already high base, over millions of sessions); lower time-to-login.
- **-27% duplicate accounts** (returning users find existing accounts; trip history intact).
- **~11% OTP cost reduction** (fewer SMS sends as journeys resolve via completable challenges).

## Takeaways for SW Engineers

- **Move the decision boundary off the client** for any flow where context determines the right experience — server-driven UI buys per-region/per-experiment/per-person adaptability.
- "No dead ends" as an architectural invariant, not a UX nicety: ranked fallbacks computed server-side.
- Thin renderers + schema-generated types preserve safety while centralizing logic.

## References

- Risk-based/step-up auth, passkeys, device trust, behavioral signals literature
