---
title: Content Ingestion and Podcast Video Incident Report
description: Spotify's post-mortem of the June 24 podcast video publishing delay — four converging causes and the reliability program for the publishing pipeline
tags: [source, rss, spotify, reliability, incident-report, transcoding, post-mortem]
locale: en
source_url: "https://engineering.atspotify.com/2026/7/content-ingestion-and-podcast-video-incident-report"
blog: spotify
published_date: 2026-07-20
---

# Content Ingestion & Podcast Video Incident Report

Authors: Jim Whitehead (Director, Engineering), Ulrik Mikaelsson (Staff Engineer), John Lagomarsino (Product Manager II), Saunak Jai Chakrabarti (Senior Director, Engineering). Source: Spotify Engineering, Jul 20, 2026.

**Lead**: Over two months, podcast creators hit a series of reliability issues, the worst a June 24 publishing delay that held video episodes for hours. The post-mortem names four converging causes — tight capacity headroom, a competing batch job, a costlier transcoding change, and a scheduling bug wasting ~10% of compute — and kicks off a broader reliability program for the publishing pipeline.

## Background: the publishing pipeline

When a creator publishes an episode, audio and video pass through processing steps — transcoding into the formats Spotify apps need, plus content analysis — before reaching listeners. Video transcoding is the heavy, capacity-sensitive stage, served through priority queues: a medium-priority queue for new episodes and a low-priority queue for updates to older episodes.

## What happened on June 24

Video transcoding infrastructure hit maximum capacity. A backlog built up in both queues; video episodes that normally publish within minutes were delayed for hours. Creators saw episodes missing and, understandably, re-uploaded — adding further load. The report is explicit: that is on Spotify, not the creators; the system should have confirmed receipt and queueing, and it did not.

## Four converging causes

1. **Insufficient headroom for spikes.** The fleet could scale for typical submission volumes (both low-priority backfill and high-priority new content), but had no margin left for large spikes from bulk content delivery.
2. **A competing batch job.** A routine re-processing job — re-transcoding existing episodes for playback-system changes — was consuming capacity alongside new-episode traffic. Harmless earlier in the day, it turned problematic when submissions surged.
3. **A costlier transcoding change.** A recent switch to better quality at lower bitrates raised per-episode time and compute cost — demand the capacity plan had not fully accounted for.
4. **A scheduling bug wasting capacity.** After a migration to more powerful hardware, a resource-scheduling bug underused available compute, cutting throughput by about **10%**.

No single factor would likely have caused the outage; the incident is a textbook convergence of latent conditions released by a demand spike.

## Response and reliability program

The report covers the June 24 delay in full detail and describes a broader reliability program now underway across the publishing pipeline — addressing capacity planning, batch-job isolation, upload acknowledgement UX (confirm receipt and queue position so creators never need to re-upload blind), and scheduling correctness. (Specific program milestones are not detailed in the article.)

## Lessons / takeaways

- Capacity plans must be re-baselined after every quality/cost change to per-item processing — a "better codec" is also a capacity event.
- Batch reprocessing and live publishing must be isolated (separate pools or preemption), so background work cannot starve the publish path.
- Every accepted upload deserves an acknowledgement with queue state; silent ingestion turns a delay into a retry storm.
- Post-migration validation should measure achieved vs. expected throughput, not just successful scheduling — a 10% underuse bug hides behind green dashboards.
- Related: `concepts/infrastructure/kubernetes.md`, `guides/infrastructure/deploy-kubernetes.md`.

## References

- Source article: https://engineering.atspotify.com/2026/7/content-ingestion-and-podcast-video-incident-report
