---
title: "Eclipse Aerospace simplifies flight-data ingestion with Databricks"
description: "Eclipse Aerospace wrapped its Rust flight-data decoders in an Arrow-native PySpark custom data source, reading nearly 20 years of proprietary telemetry directly on Databricks Serverless — no Lambda hop, no Avro copies, no always-on dedicated compute."
tags: [source, databricks, data-engineering, pyspark, aerospace, en]
locale: en
source_url: "https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks"
blog: databricks
published_date: 2026-11-13
---

# Eclipse Aerospace simplifies flight-data ingestion with Databricks

**Source**: [Databricks Blog](https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks) · **Published**: 2026-11-12

## Overview

As data-intensive industries modernize, sensor, telemetry, and scientific data piles up in specialized or proprietary formats that mainstream analytics engines cannot read directly, forcing a choice between slow memory-intensive custom transformations, maintained connectors, or extra decoding stages. Eclipse Aerospace, a very light jet manufacturer and operator, faced exactly this: nearly 20 years of flight data — more than 3TB spanning over a million flight hours, sourced from near-real-time satellite telemetry, bulk uploads of full flight histories, and external data sources — all stored in proprietary file formats that already had custom decoders written in Rust and Scala.

Before PySpark custom data sources arrived in Databricks Runtime 15.4 LTS, the team had three workable options, each flawed. Loading files as binary and splitting them with Python UDFs trades performance for readability and posed a real risk of running out of memory on variable-length messages. Implementing a native Data Source v1/v2 from the existing Scala decoder required dedicated compute — and keeping that compute always on cost more than the alternatives. That left decoding files into an intermediary format (Avro) via a Rust-based decoder on AWS Lambda, which introduced multi-hop latency, duplicated schema logic between the Lambda decoder and the downstream Spark jobs, and a second copy of every flight stored.

The chosen design was an Arrow-native PySpark custom data source: a thin Python DataSource wrapping the existing Rust decoder, passing records through Apache Arrow so file-reading logic runs inside Spark itself on serverless compute. Python handles control flow while Rust and Arrow handle high-performance decoding and data transfer — no dedicated always-on compute, no intermediary pipeline. The results: records process within a minute of file upload including startup time, large multi-gigabyte batches commonly process in parallel in under two minutes, an entire infrastructure tier disappeared, and the schema now lives in one versioned connector next to the decode logic instead of two drifting codebases.

## Key points

- The three pre-existing options and why each failed: Python UDFs over binary (out-of-memory risk on variable-length messages), a Scala native Data Source on dedicated compute (always-on cost), and Lambda-based decoding to Avro (multi-hop latency, duplicated schema logic, duplicated storage).
- The pattern: keep the domain-specific Rust decoder, wrap it in a thin Python DataSource, pass records through Apache Arrow, and let Spark on Databricks Serverless handle partitioning, execution, observability, and downstream processing.
- Speed: records are processed within a minute of file upload including startup time; large multi-gigabyte batches commonly process in parallel in under two minutes, so large flight histories are analyzed in minutes.
- Cost: removing the Lambda hop and the Avro intermediary eliminated a whole tier of infrastructure to run, monitor, and pay for — no more storing two copies of every flight (original binary plus Avro conversion), which across almost two decades of retained history is a meaningful amount of duplicated storage.
- Storage posture: the majority of files remain in AWS Glacier, with easily repeatable decodes if the original data is ever needed again.
- Observability: because decoding happens inside Spark, it appears in the Spark UI and standard job metrics like any other stage; custom badRecordsPath settings (mimicking the CSV/JSON loader) capture misformatted data, and data-quality pipelines capture statistics directly from the decoder.
- Engineering time: schema logic used to be defined twice — in the Lambda decoder producing Avro and again in the consuming Spark jobs — so every message-format change meant syncing two codebases; now a single versioned connector defines the schema once, next to the decode logic.
- Reusability: the same architectural pattern — a thin Python DataSource wrapping a Rust decoder — applies to the other proprietary formats Eclipse Aerospace supports, rather than being reinvented per format.
- Availability: PySpark custom data sources are in Databricks Runtime 15.4 LTS and above, or serverless environment version 2.

## Details

- A PySpark custom data source is a user-defined Spark data source implemented in Python, letting teams read specialized file formats as part of a standard Spark workflow without building a separate JVM connector.
- Databricks Serverless is the fully managed compute layer that makes the design economical: workloads run without provisioning infrastructure, with compute allocated, scaled, and optimized automatically — exactly what a fast-turnaround upload-and-view workflow needs.
- The connector uses PySpark custom data sources to run file-reading logic inside Spark on serverless compute; proprietary files are read directly, without always-on dedicated compute or an intermediary Avro pipeline.
- The duplicated-schema problem is worth restating: the old design encoded the message format once in the Lambda decoder that produced Avro and again in every downstream Spark job that consumed it, with the two definitions drifting apart over time.
- The takeaway for teams with proprietary or industry-specific formats: expose the decoding logic you already trust through a PySpark custom data source instead of building a separate ingestion platform around the format.
