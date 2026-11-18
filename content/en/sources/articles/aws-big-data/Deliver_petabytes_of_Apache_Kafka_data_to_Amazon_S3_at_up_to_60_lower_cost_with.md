---
title: "Deliver petabytes of Apache Kafka data to Amazon S3 at up to 60% lower cost with Amazon MSK Express brokers"
description: "How Amazon MSK Express brokers deliver Kafka topic data to general purpose S3 buckets natively — no Kafka Connect, pay-per-byte delivery that doesn't consume broker throughput, up to 60% lower ingestion and delivery cost."
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers"
blog: aws-big-data
published_date: "2026-11-19"
---

# Deliver petabytes of Apache Kafka data to Amazon S3 at up to 60% lower cost with Amazon MSK Express brokers

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers) · **Published**: 2026-11-16

## Overview

Many Kafka workloads need a durable copy at rest in Amazon S3 for backup and archive, compliance retention, replay beyond topic retention, AI/ML training data, and staging for scheduled ETL. The classic pattern — an S3 sink connector on Kafka Connect — leaves you running two systems: Kafka brokers you must size, patch, and over-provision, and a delivery pipeline you must build, secure, and pay for around the clock.

Amazon MSK Express brokers now deliver topic data directly to general purpose Amazon S3 buckets. Because Express brokers handle both ingestion and delivery, ingestion plus delivery costs drop by up to 60% versus self-managed alternatives. There is no connector or infrastructure to manage, you pay only for data delivered (billed per byte), and delivery does not consume broker throughput — archiving no longer competes with real-time consumers.

## Key points

- **Broker management, simplified**: Express brokers include pay-as-you-go storage that scales automatically (no storage to size or monitor; charges fall when traffic falls), automatic recovery of failed brokers, AWS-managed cluster/topic configurations for availability and performance, no maintenance windows, and partition rebalancing in minutes when you add brokers — so you stop sizing for peak.
- **No Kafka Connect to run**: create a delivery channel on a topic and MSK runs the delivery. No connector to find, security-approve, deploy, or patch; MSK handles retries and backpressure, and records that fail processing go to a dead-letter-queue (DLQ) bucket with identifiers and error context while delivery continues.
- **Cost model**: no peak-sized capacity to pay for; you pay per byte delivered, one charge on top of standard S3 charges, with no worker fees, no broker-egress charge for delivery, and no DLQ charge. Low traffic means low delivery cost.
- **No contention**: the channel reads the topic without consuming broker throughput, so the archive doesn't compete with real-time applications, and multiple channels can be added to one topic without added broker load. Scaling and version upgrades happen without delivery gaps.
- **Delivery format and control**: you choose compression (NONE, GZIP, ZSTD), storage class (S3 Standard, S3 Intelligent-Tiering, S3 Glacier Instant Retrieval), and an output key template (e.g., date-based prefixes with partition and offset). Records keep their producer format — JSON, UTF-8 strings, or raw bytes — with no schema registry required; JSON/String records are validated, failures route to the DLQ.
- **Beyond buckets**: Express brokers also deliver to streaming tables — continuously materialized Apache Iceberg tables on Amazon S3 Tables registered automatically in AWS Glue Data Catalog (queryable from Athena, Redshift, Spark), with inline compaction cutting downstream query cost by up to 30%. One topic can feed both an S3 bucket and a streaming table since delivery adds no broker load.
- **Getting started**: create a channel on the MSK console (Channel tab, destination = general purpose S3), or manage channels via `aws kafka create-channel` / the MSK APIs through IaC. The open-source `managing-amazon-msk` Agent Skill (Agent Toolkit for AWS) guides agents through IAM role/trust setup, key-template rules, DLQ setup, and delivery verification. When migrating from an existing connector, run both until delivered data overlaps.

## Details

The two hard parts of Kafka-to-S3 archiving are broker operations and the delivery pipeline; the post addresses each. On the broker side, Express removes storage sizing, failed-broker recovery, configuration management, and maintenance windows, and MSK Replicator plus the migrate-to-MSK Agent Skill help move self-managed or third-party Kafka into an Express cluster with right-sized recommendations before you start. On the pipeline side, the channel model eliminates the Connect tier entirely.

Architecturally, producers write unchanged; the channel reads, batches, and writes objects to your bucket in the source format, with validation for JSON/String records and DLQ routing on failure. Delivery logs and metrics surface through CloudWatch (Logs, metrics) with optional delivery to S3 or Data Firehose; troubleshooting happens in one place via the channel's CloudWatch metrics and logs. Compliance and audit retention is satisfied by keeping raw events for years in S3; replay outliving topic retention comes free since the archive is at rest in S3.

Migration note: check the Amazon MSK Developer Guide for supported Regions, accounts, and configurations ("Requirements and supported configurations") before planning, and keep the old connector running until overlap is confirmed.

## References

- Original article: [Deliver petabytes of Apache Kafka data to Amazon S3 at up to 60% lower cost with Amazon MSK Express brokers](https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers)
