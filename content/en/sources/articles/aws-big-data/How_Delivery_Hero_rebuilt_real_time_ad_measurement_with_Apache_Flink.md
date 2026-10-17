---
title: "How Delivery Hero rebuilt real-time ad measurement with Apache Flink"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/how-delivery-hero-rebuilt-real-time-ad-measurement-with-apache-flink"
blog: aws-big-data
published_date: 2026-09-24
published: 2026-10-17
---

# How Delivery Hero rebuilt real-time ad measurement with Apache Flink

## Overview

Delivery Hero — a Berlin-based delivery platform spanning ~65 countries with 1.5M+ partners and an ad business nearing EUR 1.5B in 2025 — moved ad measurement from hourly batch to real time on Amazon Managed Service for Apache Flink. Every impression and click must be billable-accurate and fresh enough for the ad server to act on; the new pipeline cut costs ~57% while reaching data quality the old system could not.

## Legacy problems

Five structural issues accumulated as traffic (tens of thousands of messages/sec, billions of events/day) grew: events were bucketed by processing time rather than event time (91% of impressions lacked reliable timestamps), widening error on time-sensitive metrics like ROAS, with an average 61-minute event-to-record gap; enrichment ran as blocking per-event API calls with no backpressure, so spikes cascaded into billing, serving, and reporting; a document database built for occasional access suffered per-event read/write amplification, cost growth, and peak-load outages; reprocessing was a per-system project (hand-rolled billing replay, daily Airflow reporting replay, no replay at all for some event types); and best-effort enrichment silently wrote through malformed events, leaving 30–40% missing session IDs and 5% missing customer IDs that corrupted downstream ML features.

## Why Managed Flink

Three non-negotiables drove the choice: fault-tolerant processing with no data loss, stateful stream processing holding multi-day history in cheap low-latency storage, and fully managed infrastructure. Flink supplies the first two natively — event-time watermarks placing late events correctly and a RocksDB state backend holding large keyed state off-heap — while the managed service removes JobManager/TaskManager and checkpoint operations. Kinesis Data Streams (two streams: user actions and orders) beat MSK on cost for this topology; DynamoDB serves reference data via Async I/O; Secrets Manager holds decryption keys; S3 stores Avro event logs and incremental checkpoints; EventBridge Pipes bridged SQS to Kinesis codelessly in the MVP, saving two weeks.

## Pipeline and results

The Java pipeline has five stages: decrypt ad tokens, deduplicate over a 30-hour RocksDB window (~20 GB, audit copies kept in S3), enrich concurrently from DynamoDB, attribute via multi-day keyed interval joins (~100 GB state) emitting attributed orders to S3, and aggregate metrics upserted to the reporting DB every 5 minutes — with CPM/CPC billing events emitted to Kafka for the ad server and budget service. At-least-once transport plus the dedup stage yields effectively exactly-once billing, and checkpoints to S3 restore state after failures.

Results: event-to-record gap fell from 61 minutes to 1.2 seconds; monthly costs dropped ~57%; async enrichment sustains 20K messages/sec peaks without backpressure leaking upstream; raw-event persistence in S3 plus 7-day Kinesis retention makes replay deterministic instead of a cross-team project. Data quality gaps closed dramatically — missing sessions 30–40%→0%, missing customer IDs 5%→0.8%, missing impression timestamps 91%→0.2% — feeding complete session context to ranking, conversion, and anomaly-detection models. Next steps extend the architecture to more ad formats, sub-second budget pacing, and live streams for personalization and LLM recommendations.

## References

- Original post: [How Delivery Hero rebuilt real-time ad measurement with Apache Flink](https://aws.amazon.com/blogs/big-data/how-delivery-hero-rebuilt-real-time-ad-measurement-with-apache-flink)
