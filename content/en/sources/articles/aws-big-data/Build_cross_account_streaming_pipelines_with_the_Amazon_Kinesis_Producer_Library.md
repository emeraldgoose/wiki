---
title: "Build cross-account streaming pipelines with the Amazon Kinesis Producer Library and Kinesis Client Library"
description: "A three-account reference architecture shows how to run KPL producers and KCL 3.5 consumers against a central Kinesis stream with cross-account IAM roles, resource-based policies, customer-managed KMS keys, and Enhanced Fan-Out, deployed via CloudFormation."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library"
blog: aws-big-data
published_date: 2026-10-12
---

# Build cross-account streaming pipelines with the Amazon Kinesis Producer Library and Kinesis Client Library

**Source**: AWS Big Data Blog, 2026-10-12

**Lead**: Multi-account deployments give streaming pipelines security isolation and cost attribution, but producers and consumers must then cross account boundaries — coordinating IAM policies, KMS keys, and CloudWatch observability. This post walks through the most isolated configuration, with the KPL producer, the Kinesis data stream, and the KCL consumer each in a separate AWS account, and provides CloudFormation templates plus sample Java applications for every step.

## Background

Amazon Kinesis Data Streams ingests millions of records per second at sub-second latency and integrates natively with Lambda, Data Firehose, and Managed Service for Flink, where cross-account access typically flows through Kinesis resource policies. Custom applications instead use two open-source libraries: the Kinesis Producer Library (KPL — record aggregation up to 1 MB, exponential-backoff retries, rate limiting, per-instance CloudWatch metrics) and the Kinesis Client Library 3.5 (automatic shard discovery, DynamoDB-coordinated leases, checkpointing, load balancing, graceful lease handover on resharding, Enhanced Fan-Out). Both support Java; KCL adds other languages via MultiLangDaemon.

## Challenges with multi-account streaming

- **Account boundary enforcement**: access is denied by default, so producer-write and consumer-read paths must each be granted explicitly, plus KMS key access on both sides for encrypted streams.
- **Policy complexity**: three policies must agree — a resource-based policy on the stream, identity-based policies on producers/consumers, and KMS key sharing.
- **Encryption**: streams encrypted with AWS-managed keys cannot be shared cross-account; a customer-managed KMS key is required.
- **Observability**: producer throughput, stream utilization, and consumer lag metrics live in different accounts, needing cross-account observability.

## Deployment patterns

| Pattern | KPL (producer) | Stream | KCL (consumer) |
|---------|----------------|--------|----------------|
| All-in-one | A | A | A |
| Cross-account consumer | A | A | B |
| Cross-account producer | A | B | B |
| Full separation (walkthrough) | A | B | C |

## Solution architecture

- **Account A (Producer)**: KPL app on EC2 with `KPLProducerRole`; at startup it calls `sts:AssumeRole` on `KinesisProducerCrossAccountRole` in Account B (with external ID) and uses the temporary credentials for `PutRecords`. CloudWatch metrics publish locally to Account A.
- **Account B (Stream)**: owns the stream, the customer-managed KMS key, the producer's cross-account role, a resource-based policy granting the consumer `GetRecords`/`GetShardIterator`/`DescribeStream`/`ListShards`, and a pre-registered Enhanced Fan-Out consumer (dedicated 2 MB/s per shard, ~70 ms via `SubscribeToShard`, shared by consumer ARN).
- **Account C (Consumer)**: KCL 3.5 app reading with its local `KCLConsumerRole` — no role assumption, authorized purely by the stream's resource policy — with its own DynamoDB lease table and CloudWatch metrics.

## Deployment walkthrough

Prerequisites: three AWS accounts with CLI profiles, CLI v2, Java 11+ with Maven, and the companion repo (`aws-samples/sample-kinesis-cross-account-kpl-kcl`).

1. **Stream stack (Account B)**: deploy `stream-account-stack.yaml` with producer/consumer account IDs; record `StreamArn`, `KMSKeyArn`, `ProducerCrossAccountRoleArn`, `EFOConsumerArn`.
2. **Producer stack (Account A)**: deploy `producer-account-stack.yaml` with the role/stream/key ARNs; then via SSM build and run `CrossAccountKPLProducer` with stream ARN, region, and role ARN.
3. **Consumer stack (Account C)**: deploy `consumer-account-stack.yaml` with stream/EFO-consumer/key ARNs; then via SSM build and run `CrossAccountKCLConsumer` with local credentials.
4. **Verify**: start the producer, start the consumer, and confirm end-to-end flow plus CloudWatch metrics in each account.

## Relevance to Software Engineers

- **Prefer role assumption for writes, resource policies for reads**: the post's asymmetric pattern (producer assumes a role; consumer relies on the stream policy) is a reusable template for cross-account data planes.
- **Customer-managed keys are non-negotiable**: any cross-account encrypted stream design must provision shared CMKs up front — AWS-managed keys silently block sharing.
- **Pre-register EFO consumers**: `SubscribeToShard` needs a separately authorized, pre-registered consumer ARN; plan fan-out topology before deploying readers.
- **Lease tables per consumer account**: KCL's DynamoDB checkpointing stays local to the consumer, so failure recovery never depends on the stream-owning account.

## References

- Original article: [https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library](https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library)
- Companion repo: `aws-samples/sample-kinesis-cross-account-kpl-kcl` (linked from the original post)
