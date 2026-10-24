---
title: "Running Apache Spark experiments in my sleep (and on a plane)"
description: "As one of Netflix’s largest and critical data pipelines, member-sessionizer consolidates tens of billions of hourly client events, encompassing user taps, playbacks, and engagement signals, into individual viewing..."
tags: [source, netflix, data-engineering, en]
locale: en
source_url: "https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8"
blog: netflix
published_date: 2026-10-14
---

# Running Apache Spark experiments in my sleep (and on a plane)

**Source**: [netflix](https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8) · **Published**: 2026-10-14

## Overview

As one of Netflix’s largest and critical data pipelines, member-sessionizer consolidates tens of billions of hourly client events, encompassing user taps, playbacks, and engagement signals, into individual viewing sessions per profile. A quick two-week tuning effort spiraled into two months when standard approaches hit a wall. Because the failures only happened at full production scale, each test took hours, limiting me to just three or four attempts daily. The turning point was changing the goal: instead of trying to speed up a single run, I built a way to run and monitor multiple tests at once and track every result.

## Key points

- Field types and Option boxing: The session ID changed from an 8-byte Long to a UUID string. Worse, wrapping fields in Scala Option forced Spark to deserialize typed Datasets into JVM objects (Some wrappers), driving up o
- Bloated string attributes: Low-value fields (e.g., referrer URLs, test allocations) added several hundred bytes per event. Multiplying these strings across collect_list wasted terabytes per hour, even though downstream t
- Unboxed primitives: Removing Option wrappers from non-nullable fields dropped peak executor memory from 112% to 58% of the slot with zero disk spill.
- Slimmed event bags: Dropped unused per-event attributes and hoisted session-invariant metadata (app version, country) up to the session header.
- Finding 1: Narrowing rows can trigger faster OOMs. Slimming our table dropped its size below Spark’s auto-broadcast threshold, prompting the query planner to switch from shuffle joins to broadcast joins. Because broadcas
- Finding 2: Broadcast hash joins were silently draining memory. Adaptive Query Execution (AQE) rewrote nine sort-merge joins into broadcast hash joins at runtime. While each join stayed under our 400 MB broadcast limit in

## References

- Original article: [https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8](https://netflixtechblog.com/running-apache-spark-experiments-in-my-sleep-and-on-a-plane-588816b6b5f8)
