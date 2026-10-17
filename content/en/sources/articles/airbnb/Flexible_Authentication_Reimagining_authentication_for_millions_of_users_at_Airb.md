---
title: "Flexible Authentication: Reimagining authentication for millions of users at Airbnb"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://airbnb.tech/uncategorized/flexible-authentication-reimagining-authentication-for-millions-of-users-at-airbnb"
blog: airbnb
published: 2026-10-17
---

# Flexible Authentication: Reimagining authentication for millions of users at Airbnb

## Overview

Airbnb's marketplace has users who log in at irregular intervals — a guest may return months after booking — so a failed login directly means lost bookings. After a decade of organically adding login methods, the team rebuilt authentication around Flexible Authentication: split login into identification then challenge, let the server pick the easiest verification method per user and region, and guarantee every screen offers a fallback path.

## Identify first then Challenge

The core insight reframes login from "prove who you are" to "what is the easiest way for this person to verify their session." The flow has two stages: the user first states their identity (email, phone, or social login), then a configurable policy engine selects the challenge most likely to succeed given account history and context — e.g., WhatsApp OTP in Brazil, Naver login in South Korea — presenting it first with everything else as fallback.

Crucially, the client never decides which challenge to show; the server dictates it and the client merely renders the received screen. This lets the team tune strategy per region and run experiments without shipping new client code across web, iOS, and Android.

## Challenge Picker and server-driven screens

The old system had dead ends: fail a challenge and you were stuck restarting the flow. The new design requires every challenge screen to include a "try another way" escape, backed by a server-driven Challenge Picker that returns the primary challenge plus a ranked list of alternatives ordered by predicted success. Tapping it adapts the flow instead of restarting it.

Each authentication step is a screen defined entirely by a server response, with clients acting as thin renderers using generated type definitions. Moving sequencing and flow logic server-side removed 60% of the code and 100KB from the web bundle, and collapsed experiment turnaround from weeks to days — over 20 experiments ran in the three months after launch.

## Results

Leading with the most-likely-to-succeed challenge cut login time and raised successful authentication by 2.6% across millions of sessions. Duplicate-account creation fell 27% since more users recover their existing accounts, and fewer SMS OTPs sent cut one-time-code costs by about 11%. Outages in one challenge method no longer block users because alternatives are always one tap away.

## References

- Original article: https://airbnb.tech/uncategorized/flexible-authentication-reimagining-authentication-for-millions-of-users-at-airbnb
