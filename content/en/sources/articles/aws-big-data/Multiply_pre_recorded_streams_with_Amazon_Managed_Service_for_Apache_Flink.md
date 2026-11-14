---
title: "Multiply pre-recorded streams with Amazon Managed Service for Apache Flink"
description: "A stream multiplier on Amazon Managed Service for Apache Flink replays a sanitized Kinesis recording and emits the original record plus DataFaker variants per input, reaching roughly 176,000 records per second at a 25x factor in the published tests."
tags: [source, aws-big-data, amazon-kinesis, apache-flink, load-testing, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/multiply-pre-recorded-streams-with-amazon-managed-service-for-apache-flink"
blog: aws-big-data
published_date: 2026-11-14
---

# Multiply pre-recorded streams with Amazon Managed Service for Apache Flink

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/multiply-pre-recorded-streams-with-amazon-managed-service-for-apache-flink) · **Published**: 2026-11-10

## Overview

Validating a streaming pipeline beyond its current peak requires production-scale test data, and every existing approach falls short somewhere. Replaying a full-volume pre-recorded stream is faithful but expensive to retain: at 50,000 records per second, a two-hour recording window holds 360 million records, and a recording is needed at every throughput tier. Synthetic generators such as DataFaker emit any rate from a schema but follow configured distributions, not observed ones, so they miss natural skew, micro-bursts, and cross-field dependencies. Canary deployments and shadow pipelines use real production data but cap testing at current production throughput.

The stream multiplier pattern closes that gap. A relatively small sanitized recording from Amazon Kinesis Data Streams is amplified by a single parameter, multiple.factor, which sets how many records each input produces. Fields you do not nominate for replacement keep the distributions of the original recording, while nominated fields are regenerated with DataFaker values, so the amplified stream preserves the statistical shape of real traffic at multiplied volume.

The walkthrough follows AnyCompany Rides, a ride-hailing company whose Apache Flink pipeline ingests approximately 15,000 trip events per second and must sustain 75,000 events per second before a regional expansion. Setting a multiplication factor of 5x on a ten-hour sanitized recording emits the original event unchanged plus four synthetic variants for each record. The multiplier itself is a RichFlatMapFunction running on Amazon Managed Service for Apache Flink, with Amazon CloudWatch collecting throughput, backpressure, checkpoint duration, and heap metrics.

## Key points

- The solution uses three AWS services and one open source library: Amazon Kinesis Data Streams holds the source recording and carries the amplified stream, Managed Service for Apache Flink runs the multiplier, Amazon CloudWatch collects health metrics, and DataFaker produces replacement values driven by faker-config.yaml rather than code.
- Runtime properties drive behavior so one artifact serves any schema: source.type (kinesis for amplification, datagen for pure synthetic), multiple.factor, key.fields, updatable.fields, random.seeds, and rate.limit.per.second.
- In amplification mode each event passes through five steps: read and deserialize, emit the original unchanged, compute a deterministic hash from the key fields plus a per-iteration random seed, generate synthetic values for the fields listed in updatable.fields, and write all records to the sink.
- The application validates multiple.factor at startup and rejects values outside a range of 1 to 100, bounding the damage a mistyped factor could do to sink shard capacity or application heap.
- Key fields are preserved across variants, so a consumer grouping by trip ID still sees a coherent entity; timestamp and any field in neither list pass through untouched.
- The generator is deterministic and repeatable: seeds come from the record key fields and per-iteration seeds, are reseeded for every record, and do not depend on replay order or subtask assignment; values such as wall-clock time or UUID.randomUUID() would break that property.
- Tested versions: JDK 17, sbt 1.9.9, Scala 2.12.20, Apache Flink 2.3.0 on the FLINK-2_3 runtime, aws-kinesisanalytics-runtime 1.2.0, Kinesis connector 6.0.1-2.0, DataFaker 2.7.0, Jackson 2.15.2, and Log4j 2.24.3.
- A factor sweep on 3 KPUs (2 processing, 1 orchestration) with the NYC taxi trip schema averaging about 181 bytes and a 240-shard sink produced roughly 128,000 output records per second at 5x and approximately 176,000 at 25x; CPU sat at 96-100 percent in every row while heap stayed in a 31-38 percent average band, and checkpoints stayed tiny at 17-73 KB completing in 226-460 ms.
- The sink decides real throughput: a Kinesis shard accepts 1,000 records or 1 MB per second on writes, so size the sink at roughly target output rate divided by 1,000 for sub-1 KB records. At 10x, 20 sink shards throttled heavily at about 20,505 records per second with CPU at 16 percent, while 180 shards removed throttling entirely and exposed the compute ceiling of about 143,000 records per second.
- Validate on the Kinesis side, not the application side: the ratio of GetRecords.Records on the source stream to IncomingRecords on the sink should equal the multiplication factor; a 10x run measured 2,056 records per second in against 20,505 out, a ratio of 9.97.
- Switching source.type changes the job graph, so restoring a previous snapshot fails with a KinesisShardSplitSerializer EOFException; start with SKIP_RESTORE_FROM_SNAPSHOT because the multiplier is stateless.
- Cost: the default deployment (3 shards, seven-day retention, 3 KPUs) runs about $0.45 per hour, or about $11 per day; the two-hour 25x run with 240 sink shards used about 1.3 billion PUT payload units ($17.75), 480 sink shard-hours ($7.20), and 6 KPU-hours ($0.66), about $35 including retention.

## Details

### How the fan-out works

The flatMap emits the original followed by N-1 variants, so a multiplication factor of 3 produces the original plus two variants. DataFaker entries in faker-config.yaml pair an expression with a type, for example distance drawn from 0-20 and amount from 5-150, while tripId stays identical on every variant because it is a key field. Because the partition key comes from the record hash rather than the factor, shard load stays even: in the 25x run across 240 open shards, every shard carried between 671 and 678 records per second.

### Throughput and capacity

Output rises with the factor but flattens near 176,000 records per second, because each input carries a fixed read and deserialize cost while each output carries the per-variant field generation cost. CPU is the binding constraint, not memory or state. For capacity planning, size from output per processing KPU: roughly 64,000 records per second at 5x, rising to approximately 88,000 at high factors.

### Sink sizing and resilience

The async KinesisStreamsSink re-queues and retries throttled records. Across the sweep, transient per-attempt failures stayed at 73 or fewer per window against tens of millions of records, with no permanent loss, and write latency held at approximately 40-54 ms with occasional spikes near 1.1 s. Watch WriteProvisionedThroughputExceeded and backPressuredTimeMsPerSecond when output falls below factor times input rate, and use Enhanced Fan-Out with SubscribeToShardEvent.MillisBehindLatest if the source falls behind.

### Limitations and cleanup

Amplification multiplies volume while keeping the sample's timing shape, so bursts carry through at higher amplitude; generated fields are independent of each other, so a 0.5-mile trip can be assigned a $150 fare; ordering is preserved within a partition but not across partitions; and the sample reads and writes JSON only. To clean up, stop the application, wait until it reports READY, and delete the CloudFormation stack; a stack-created AWS KMS key is scheduled for deletion after a 30-day waiting period.
