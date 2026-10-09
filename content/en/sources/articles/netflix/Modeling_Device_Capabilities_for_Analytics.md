---
title: "Modeling Device Capabilities for Analytics"
description: Cumulative and histogram tables modeling device capabilities (codecs, DRM, display, RAM) to drive feature rollout decisions
tags: [source, article, netflix, data-engineering, data-modeling, analytics, devices]
locale: en
source_url: "https://netflixtechblog.com/modeling-device-capabilities-for-analytics-e7607acebde8"
blog: netflix
published: 2026-07-31
---

# Modeling Device Capabilities for Analytics

Authors: Aarti Laddha, Richard Diaz-Cool, Rishika Idnani, Venkatesh Selveraj. Netflix ships features from 4K and spatial audio to live streaming and cloud gaming across a vast device ecosystem — but hardware (RAM, CPU, display, platform support) means not every feature runs on every model. Deep device-capability understanding, fused with internal feature flags, enables granular feature management, bottleneck diagnosis, and faster innovation.

## Background: why a capability model

Without a unified model, feature-penetration questions ("which devices block 4K rollout?") require ad-hoc joins across telemetry and flag systems. A comprehensive, analytics-ready capability data model turns them into routine queries.

## Methodology

**Cumulative table for latest state.** Per-device latest capabilities (screen resolution, supported video profiles, surround sound, RAM, etc.) are maintained in a cumulative table — e.g. `{"Screen Height": ["720"], "Screen Width": ["1280"], "Video Profiles": ["playready", "hevc"]}` — ideal for point-in-time analytics and reporting.

**Histogram table for distributions.** A 28-day-active-device histogram broken down by model and software version records how many devices support each capability, enabling distribution analysis — e.g. all streaming sticks support HD (playready) but only ~20% support UHD (hevc) — directly informing codec/display rollout decisions.

**Analytical products.** These datasets power feature-reach views (4K Ultra HD, spatial audio, cloud gaming, latest UI), so enablement decisions per device rest on data rather than guesswork, balancing performance and reliability.

## Results

Data-driven per-device feature enablement: informed rollout scoping, bottleneck identification in feature penetration, and accelerated innovation pace across the device landscape.

## Limitations / open questions

- Capability inference from user-agent/telemetry is approximate for long-tail models; taxonomy maintenance is ongoing work.
- 28-day-active histograms underrepresent rarely-used devices.
- The post reports approach, not quantified rollout wins.

## Relevance to SW engineers

- Cumulative (latest-state) + histogram (distribution) is a reusable analytics pattern: one table answers "what is X now", the other "how is X distributed".
- Gate feature rollouts on measured capability reach, not device-model folklore.
- Fuse static capability data with dynamic feature flags for granular, reversible management.

## Related concepts

- `concepts/data-engineering/data-modeling.md` (cumulative/histogram patterns)
- `concepts/data-engineering/stream-processing.md` (telemetry pipelines)
