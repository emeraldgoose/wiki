---
title: "Choose the right streaming ingestion path for Apache Iceberg tables on AWS"
description: "Compares five AWS streaming ingestion paths into Apache Iceberg tables — streaming tables for Apache Iceberg, MSK Connect with the Iceberg sink connector, Amazon Data Firehose, Amazon Managed Service for Apache Flink, and Spark Structured Streaming on Amazon EMR — across eight technical criteria, with production caveats and a two-question decision framework."
tags: [source, aws-big-data, streaming, iceberg, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/choose-the-right-streaming-ingestion-path-for-apache-iceberg-tables-on-aws"
blog: aws-big-data
published_date: 2026-11-14
---

# Choose the right streaming ingestion path for Apache Iceberg tables on AWS

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/choose-the-right-streaming-ingestion-path-for-apache-iceberg-tables-on-aws) · **Published**: 2026-11-13

## Overview

Writing real-time data into Apache Iceberg tables is a key step in building low-latency data lakes that feed AI agents, operational dashboards, and analytics. Iceberg gives all of these workloads one shared table format, but reducing ingestion latency depends on which streaming path carries the data into the table. The authors frame the choice as a trade-off between operational and technical requirements, and warn that these decisions are expensive to reverse because they live in your pipeline code, IAM model, and operational runbooks rather than in the table itself.

The post compares five AWS ingestion paths: streaming tables for Apache Iceberg (native delivery from Amazon MSK and Amazon Kinesis Data Streams), Amazon MSK Connect with the Apache Iceberg sink connector, Amazon Data Firehose, Amazon Managed Service for Apache Flink, and Apache Spark Structured Streaming on Amazon EMR. Each is evaluated against eight technical criteria: upsert behavior, table maintenance, schema evolution, message serialization, source and destination support, scalability and performance, fan-out to multiple tables, and in-flight transformation. Four operational questions come first: do you want a fully managed solution, do you prefer configuration or application code, do you require sub-minute data freshness, and do you need a portable open source solution.

The post is explicitly a live document that the authors plan to evolve as new features ship. It closes with a decision framework built on two questions — is your write pattern append-only or does it need row-level updates and deletes, and who owns compaction, the service or your team — which usually narrows the field to one or two options.

## Key points

- Streaming tables for Apache Iceberg are a native delivery capability of Amazon MSK Express brokers and Amazon Kinesis Data Streams On-Demand mode; delivery costs up to 60% less than a self-managed pipeline, and optimally sized files cut downstream query costs by up to an additional 30%.
- Streaming tables validate records against a schema registered in AWS Glue Schema Registry, compact inline into optimized Parquet, route failed records to a dead-letter queue in Amazon S3, and are append-only and read-only to user engines.
- The Apache Iceberg sink connector on Amazon MSK Connect scales by adding tasks as topic partitions grow, creates destination tables automatically, and fans out one topic to several Iceberg tables — but supports insert-only writes (no UPDATE or DELETE) and has no embedded compaction.
- Amazon Data Firehose has the broadest source support (Amazon MSK, Kinesis Data Streams, and Direct PUT), applies inserts, updates, and deletes without code using JQ expressions, and enforces table-level and column-level access control through AWS Lake Formation; input must be JSON and output is always Parquet.
- Firehose trades throughput against partition count, produces many small files that demand an external compaction strategy from day one, incurs Amazon S3 PUT charges per update (a delete file plus a data file), and does not support Amazon MSK Serverless as a source.
- Amazon Managed Service for Apache Flink is the only option that requires writing and maintaining an application, but it delivers full CDC with equality deletes, first-class event-time semantics with watermarks, exactly-once commits aligned with Flink checkpoints, and embedded compaction with the Iceberg 1.10 or later sink.
- Apache Spark Structured Streaming on Amazon EMR offers full MERGE INTO support and the complete set of Iceberg Spark procedures (rewrite_data_files, expire_snapshots, remove_orphan_files); records must be deduplicated before every MERGE, which the authors call a correctness requirement, not a performance optimization.
- Only Managed Service for Apache Flink and Spark Structured Streaming on Amazon EMR support sub-minute data freshness while also managing the compaction that sub-minute workloads need.
- Spark creates one task per source partition (one per Kinesis shard or MSK topic partition), so an under-partitioned source caps throughput no matter how many executors you add.
- Firehose scales automatically to match throughput for insert-only workloads when the AppendOnly flag is set to true on CreateDeliveryStream.
- The recommendation is short: append-only workloads wanting the lowest operational effort start with streaming tables; CDC with updates and deletes points toward Managed Service for Apache Flink.

## Details

### Eight criteria and the five-stage reference architecture

The eight technical criteria decide feasibility before preference: upsert behavior (append-only logging and IoT versus CDC mirroring source state), table maintenance (Amazon S3 Tables compacts files, expires snapshots, and removes orphan files automatically, or you run maintenance in the sink pipeline), schema evolution, message serialization (JSON, Avro, or Protobuf and which schema registry), source and destination support (fully managed Amazon S3 Tables versus self-managed Iceberg in your own S3 bucket catalogued through the AWS Glue Data Catalog), scalability, fan-out, and data transformation and analytics. The reference architecture is a five-stage pattern: stream sources (SDK applications, log files, IoT events, database CDC), stream storage (Amazon MSK or Kinesis Data Streams, or Direct PUT straight to Firehose), stream processing (one of the five options), stream sink (Iceberg tables in S3 Tables or a general-purpose S3 bucket), and analytics with Amazon Athena.

### Streaming tables: managed delivery with inline compaction

You select a topic or stream, point delivery at a registered schema, and choose an S3 table bucket; the service buffers to the configured freshness interval, validates and converts each record, compacts inline into optimized Parquet files, and commits. Write coordination and exactly-once delivery are built in, eliminating the concurrent-writer conflicts that otherwise surface as failed commits. On MSK, delivery runs on the Express broker backend, uses none of your broker's read capacity, and adds no cross-Availability Zone transfer charges; on Kinesis it does not consume read limits or enhanced fan-out. When Iceberg is not required, the same delivery can write to general-purpose S3 buckets in the source format for archival, backup, or ML training data. The caveats: it is append-only and read-only, with no CDC and row removal only through the record expiration job.

### Configure-first paths: MSK Connect and Data Firehose

MSK Connect's Iceberg sink connector fits teams already running Kafka Connect: Avro, JSON, and Protobuf through standard Kafka Connect converters with schema registry support, automatic schema propagation, and content-based fan-out. Limits are significant — only Simple Message Transformations are available (no joins, aggregations, or stateful logic), no writes to Iceberg branches, Kafka sources only, and continuous commits produce many small files, so query performance degrades without an aggressive compaction schedule. Firehose is the serverless path with the widest source range; it routes records with JQ expressions and can invoke an AWS Lambda function to transform records in flight. Column names and types must match the target table exactly, extra fields are skipped, mismatches land in the S3 error bucket, and schema evolution is additive-only — renames, deletions, and type changes need manual intervention, with no schema registry enforcement.

### Application-code paths: Flink and Spark on EMR

Flink processes records one at a time rather than in micro-batches, so a windowed aggregation keyed on event time produces the same result regardless of arrival order. The checkpoint interval controls commit frequency and file size and is the setting that most affects downstream query performance; even with embedded maintenance, small files still accumulate between compaction cycles. Teams without Flink experience should plan ramp-up on state, watermarks, and backpressure, and the Managed Service for Apache Flink Agent Skill generates idiomatic application code to shorten that. Spark on EMR suits teams that already run Spark, need MERGE semantics, and accept minutes-scale latency; batch and streaming share the same DataFrame API, so one transformation codebase serves a nightly reprocessing job and a continuous pipeline. But MERGE INTO with duplicate keys in a source batch is ambiguous — Spark may apply one row non-deterministically or fail with a multiple matching rows error — so deduplicate or rank records, for example by event timestamp within each key. Micro-batch latency in the tens of seconds to minutes, higher cost than an equivalent Flink application at comparable throughput, and self-managed in-pipeline compaction complete the picture.
