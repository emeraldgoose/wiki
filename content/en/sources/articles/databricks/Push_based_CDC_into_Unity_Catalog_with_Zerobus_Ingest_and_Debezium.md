---
title: "Push-based CDC into Unity Catalog with Zerobus Ingest and Debezium"
description: "Capture database changes with Debezium and land them in Unity Catalog Delta tables through Zerobus Ingest, without a Kafka cluster as transport."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium"
blog: databricks
published_date: 2026-11-06
---

# Push-based CDC into Unity Catalog with Zerobus Ingest and Debezium

**Source**: [databricks](https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium) · **Published**: 2026-11-05

## Overview

Operational database changes often need to reach the lakehouse for analysis, but source databases frequently sit in private corporate networks or restricted subnets whose policies block inbound connections from external services. Teams need faithful capture of inserts, updates, and deletes without polling, an ordering signal that reconstruction downstream can replay in source order, minimal load on the source database, outbound connectivity from locked-down environments, no Kafka cluster operated solely as transport, and landed data in a lakehouse-queryable form.

Debezium provides the capture side: an open-source log-based change data capture platform that tails transaction logs such as PostgreSQL's write-ahead log instead of polling tables, issuing structured change events. Zerobus Ingest provides the destination side: a serverless, push-based ingestion service that writes records directly into Unity Catalog Delta tables without a message broker. The Debezium Server Zerobus sink connects the two, landing change events directly into Databricks. It was built jointly by engineers at NVIDIA and Databricks and contributed to the open-source Debezium project, and it ships in Debezium Server 3.7.

Debezium has two operating models: a Kafka Connect plugin where Kafka is the canonical event bus, or the standalone Debezium Server that runs on ordinary compute and pushes events to non-Kafka destinations such as Zerobus Ingest. Zerobus Ingest is append-only, so once the change stream lands in a Delta table the downstream step is to build a Type-1 dimension table through a merge for the latest version of each key. The sink supports two table contracts; in envelope mode the full Debezium change event lands with idempotency keys and durable acknowledgment before source offsets advance.

## Key points

- Debezium captures inserts, updates, and deletes by reading transaction logs, preserving source ordering with minimal source load.
- Zerobus Ingest is push-based and serverless, writing records directly into Unity Catalog Delta tables without a broker.
- The Debezium Server Zerobus sink removes the intermediate Kafka hop between capture and lakehouse.
- The sink was developed collaboratively by NVIDIA and Databricks and ships in Debezium Server 3.7.
- Outbound capture from a private network is practical because Debezium runs next to the database and pushes events outward.
- Zerobus is append-only, so current-state tables are built downstream by merging the landed change stream.

## Details

The article contrasts a traditional message-bus architecture with the Zerobus architecture, where an additional replication job is otherwise needed to move events from Kafka into the lakehouse. Six requirements motivate the pattern: capture all operations including deletes, preserve ordering, avoid polling overhead, work with private networks, avoid Kafka purely as transport, and land lakehouse-ready data. Each Debezium event carries before and after row states, operation code, source metadata, and a timestamp. Envelope mode lands the full event including ordering and idempotency safeguards. Exact connector configuration, target table contracts, and a hands-on local PostgreSQL walkthrough are in the linked source and the companion community how-to blog.

## References

- Source: [databricks](https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium)
