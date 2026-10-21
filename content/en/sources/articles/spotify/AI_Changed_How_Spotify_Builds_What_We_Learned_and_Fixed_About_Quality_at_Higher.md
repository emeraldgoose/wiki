---
title: "AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at Higher Velocity"
description: "Spotify's data on AI-era quality — merged changes doubled to 17K/month with no AI-attributed incident signature; the bottleneck moved from writing code to verifying it"
tags: [source, article, en, en]
locale: en
source_url: "https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity"
blog: spotify
published_date: 2026-09-16
---

# AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at Higher Velocity

**Author**: Tyson Singer, Head of Technology and Platforms (SVP)
**Source**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity)
**Date**: Sep 16, 2026

## Overview

Spotify runs roughly 3,000 production services serving around 100 million concurrent clients. After ramping up AI-assisted development, quality slipped in places — but the company's incident review found no distinct AI-authored failure signature. The real story is pace: the capacity to produce change grew faster than the controls that verify it. This post walks through four pressure areas, the fixes, and what Spotify's own delivery metrics say about the quality-for-velocity tradeoff.

## Four areas under pressure

**Content processing.** Spotify ingests over 500K new songs, videos, podcasts, and audiobooks daily. Two latent weaknesses — silently masked processing failures and unalerted transcoding queue backlogs — combined with a batch-job conflict, heavier per-episode compute, and a scheduler bug to delay a June 24 podcast-video publish window by hours. Fixes: end-to-end monitoring, scheduler repair, deprioritized batch jobs, more capacity, reworked service tiering, and down-prioritized bad-actor uploads.

**Fleet updates.** The Fleet Management framework applies large-scale automated changes daily, now including agentic migrations (a Java migration across backend services finished in three days). But one automated dependency upgrade passed all checks yet failed in production. Response: stronger safeguards, expanded rollback capacity, and scheduling automated changes during owning teams' working hours.

**Compute shortages.** Industry-wide AI demand erased the spare CPU/GPU headroom Spotify used to rely on, so regional failovers — previously routine — started showing user-visible impact. Spotify doubled reserved edge capacity, accepted that lower service tiers may go unserved during failover, and is extending gradual traffic-shifting controls to edge traffic.

**Mobile app experience.** AI raised the frequency of Spotify's long-standing ship-fast-then-harden quality cycle: individual releases look healthy while small regressions accumulate outside watched signals. The team broadened guardrail metrics and added longer-term trend analysis to release decisions.

## What the delivery data shows

Every major-incident retrospective now asks whether AI-authored code contributed directly and whether change volume stressed verification. So far, no incident blames AI-authored code materially — but several show verification controls lagging change volume. Upstream metrics agree: merged changes more than doubled year over year in August (about 8,100 to 17,000), while the share of code-quality and optimization work rose from 27% to 31% — over twice the absolute quality investment. A rebuilt rework-rate metric (age-weighted, unlike raw churn) shows no rise, diverging from the industry churn spike reported by FAROS. Two watch signals: code complexity and PR size are creeping up, though larger PRs may now reflect human-agent collaboration rather than sloppiness — Spotify is deliberately not recalibrating thresholds yet.

## Takeaway

AI raised the ceiling on how fast Spotify can change its systems; the binding constraint moved to review, testing, rollout, observability, rollback, and failover operating at the same pace. The remediation program treats delivery-system alignment as continuous work, not a one-time fix.

## References

- [AI Changed How Spotify Builds — original article](https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity)
- [Content ingestion and podcast video incident report](https://engineering.atspotify.com/2026/7/content-ingestion-and-podcast-video-incident-report) (referenced in the post)
- [Google Cloud 2025 DORA report](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) (referenced in the post)
- [FAROS 2026 AI acceleration report](https://www.faros.ai/research/ai-acceleration-whiplash) (referenced in the post)
