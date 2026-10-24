---
title: "Behind the Scenes: Evolving Netflix’s Ads Event Pipeline for Live — Part II"
description: "In Part 1 of this series, we shared how Netflix built the Ads Event pipeline and approached it as a system design problem: replacing fragmented pipelines with a centralized collection, enrichment, and a standard data..."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb"
blog: netflix
published_date: 2026-10-14
---

# Behind the Scenes: Evolving Netflix’s Ads Event Pipeline for Live — Part II

**Source**: [netflix](https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb) · **Published**: 2026-10-14

## Overview

In Part 1 of this series, we shared how Netflix built the Ads Event pipeline and approached it as a system design problem: replacing fragmented pipelines with a centralized collection, enrichment, and a standard data contract. The result was Ads Event Publisher, the system that collects ad telemetry from client devices, enriches it with the context of the ad that was actually served, and publishes a single, unified stream of ad events to every downstream consumer: frequency capping, metrics, billing, measurement partners, and reporting. Any member viewing or account details that move through t If ad serving is the “brain” and ad events are the “heartbeats” that feed it, then enrichment is what gives each heartbeat its meaning, turning a bare “[Somebody] watched an ad to completion” signal

## Key points

- When the ad server made a decision, it wrote the metadata for that impression into the registry.
- It encoded only reference identifiers into the opaque token returned to the device, keeping the token small.
- Later, when the client fired an event carrying that token, the Ads Event Publisher decoded the token, looked up the metadata in the registry, and stitched the two together into an enriched ad event.
- It was a scaling bottleneck. Every ad and every ad break is a write. Multiply that by tens of millions of concurrent viewers, keep it non-lossy (a dropped write is a dropped ad, and lost revenue), add Live’s spiky on/off
- Fewer dependencies on the critical path. Serving an ad meant a synchronous, must-succeed write to the registry, followed by a wait for its acknowledgment. Every system on the critical path is one more thing that can stop
- It put event freshness at risk. If writing slowed down under load, or lookups timed out, events spilled into retries and dead-letter queues, and enriched ad events were delivered late. Some systems might be fine, but oth

## References

- Original article: [https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb](https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb)
