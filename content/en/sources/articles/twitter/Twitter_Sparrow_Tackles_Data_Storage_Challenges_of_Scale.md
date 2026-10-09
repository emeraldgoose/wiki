---
title: Twitter Sparrow Tackles Data Storage Challenges of Scale
description: Project Sparrow — redesigning Twitter's event pipeline from hourly batch to streaming, cutting latency from hours to seconds
tags: [source, twitter, x, streaming, beam, dataflow, pubsub, bigquery, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/twitter-sparrow-tackles-data-storage-challenges-of-scale"
blog: twitter
date: '2022-06-28'
---

# Twitter Sparrow Tackles Data Storage Challenges of Scale

## Summary

Twitter logs trillions of events daily from tens of thousands of microservices (every click, swipe, and scroll), historically through a batch log-ingestion pipeline optimized for throughput — billions of events per minute — at the cost of **hours** of end-to-end latency before data was consumable. **Project Sparrow**, started as a 2020 Hack Week project by Lohit Vijayarenu, Zhenzhao Wang and team, redesigned the pipeline streaming-first, cutting latency to **minutes and seconds** while preserving batch access for historical processing. The work was published as *"Twitter Sparrow: Reduce Event Pipeline latency from hours to seconds"* (IEEE BigData 2021).

## Architecture: Before and After

- **Before**: services → batched aggregation (Flume/Kafka-era on-premise stages, HDFS/Tez/Mesos) → hours-late delivery to fixed destinations; no cloud-origin support.
- **After (streaming-first)**: a **Streaming Event Aggregator** collects log events and publishes to Kafka or Google Pub/Sub (with on-the-wire compression and a unified client library transparent across on-prem and cloud, plus pluggable metadata management); a **Streaming Event Processor** layer (one Apache Beam job + subscription per dataset) reads the queue, applies transformations/format conversions (thrift → Avro → TableRow, with UDF/SQL support for light ETL so users avoid writing full Dataflow/MR jobs), and streams into **BigQuery, GCS, and Kafka/PubSub** — serving both real-time and historical consumers. Airflow orchestrates the processor fleet.

## Operating at Twitter Scale on Google Cloud

Sparrow's throughput targets (≈3–5B events/min with ~50% YoY growth; single datasets at 10–18 GB/s and tens of millions of events/sec; single Beam jobs up to ~20 GB/s) pushed past what Google Cloud components handled out of the box. Optimizations included removing shuffle from the BigQuery IO connector (−80–86% Beam resources, joint work with the Dataflow team), compressing data before Pub/Sub processing (~−20% worker usage), and streamlining nested thrift→Avro→TableRow schema conversion. Guardrails added along the way: PDP (private-data-protection) compliance, chargeback support, and cost estimators, as a managed no-maintenance service with transparent migration for existing customers.

## Results

A low-latency streaming ingestion pipeline in GCP enabling near-real-time questions (e.g. live user-behavior analysis) that were previously unaskable — with batch semantics retained for long-window reporting.

## Relevance to SW Engineers

- Throughput-optimized batch pipelines accrue a latency debt that eventually blocks product iteration ("move at the speed of Twitter"); repay it with a streaming-first redesign that still serves batch consumers from the same events.
- At extreme scale, managed-cloud components need co-engineering (custom IO connectors, compression placement, schema-conversion tuning) — budget for joint optimization with the provider.
- Give users function/SQL-level ETL hooks instead of forcing full pipeline jobs for light transforms; it removes the biggest adoption barrier for migration.
- Ship compliance (PDP), chargeback, and cost estimation as part of the platform, not follow-ups — they determine whether a migration is actually shippable.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/twitter-sparrow-tackles-data-storage-challenges-of-scale (Daniel Templeton, 28 Jun 2022)
- Paper: Lohit VijayaRenu et al., *Twitter Sparrow: Reduce Event Pipeline latency from hours to seconds*, IEEE BigData 2021, https://doi.org/10.1109/bigdata52589.2021.9671438
- Related: `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-kafka.md`
