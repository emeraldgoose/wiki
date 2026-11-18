---
title: "What is Real-Time Mode in Apache Spark?"
description: "Real-Time Mode is a Spark Structured Streaming trigger that processes each record as it arrives (millisecond end-to-end latency) on the same engine and APIs — fraud detection, personalization, and real-time AI features without a second stream-only engine."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/what-is-real-time-mode"
blog: databricks
published_date: "2026-11-19"
---

# What is Real-Time Mode in Apache Spark?

**Source**: [databricks](https://www.databricks.com/blog/what-is-real-time-mode) · **Published**: 2026-11-13

## Overview

Real-Time Mode is a trigger for Apache Spark Structured Streaming that processes each record as soon as it arrives instead of waiting for the next micro-batch. It brings Spark streaming from seconds down to milliseconds of end-to-end latency, on the same engine and the same APIs you already use for batch and micro-batch streaming. Before Real-Time Mode, teams that needed sub-second responses often added a second, stream-only engine; Real-Time Mode removes that requirement for most workloads. You change the trigger on an existing query, and Spark runs it continuously.

## Key points

- Enabling Real-Time Mode is a one-line trigger change; the source, transformations, and checkpoint stay the same, so no rewrite is needed.
- Use it for fraud detection, personalization, and real-time AI features — workloads that used to require Apache Flink-class engines.
- DraftKings uses Real-Time Mode with `transformWithState` for fraud detection in live sports betting.
- MakeMyTrip serves personalized hotel results with 44 ms P50 latency.
- The same pipeline computes features for model training and online inference, keeping AI agents supplied with the latest events.

## Details

Real-Time Mode targets the gap between Spark's micro-batch model (seconds of latency) and the sub-second requirements of interactive and AI-facing use cases. It runs inside Spark Structured Streaming, so existing knowledge, code, and operations carry over: same DataFrame/Dataset APIs, same checkpointing model, same operational tooling. Stateful processing through `transformWithState` is supported, which is what enables DraftKings-style fraud scoring on live event streams.

The FAQ in the original article covers operational questions: which Spark versions support Real-Time Mode, whether it runs on serverless or Free Edition, stateful operation support, and how it compares to Apache Flink and to the earlier continuous-processing experimental mode. The article also situates Real-Time Mode within Databricks' "agentic AI playbook" positioning — millisecond feature freshness for online inference and agent context.

## References

- Original article: [What is Real-Time Mode in Apache Spark?](https://www.databricks.com/blog/what-is-real-time-mode)
