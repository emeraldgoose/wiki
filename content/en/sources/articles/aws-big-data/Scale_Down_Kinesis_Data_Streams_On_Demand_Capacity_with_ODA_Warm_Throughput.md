---
title: "Scale Down Kinesis Data Streams On-Demand Capacity with ODA Warm Throughput"
description: "New warm-throughput scale-down for Kinesis on-demand Advantage streams: release post-burst shard capacity, safeguard on last-hour peak, and monitor via CloudWatch."
published: "2026-09-14"
source_url: "https://aws.amazon.com/blogs/big-data/scale-down-kinesis-data-streams-on-demand-capacity-with-oda-warm-throughput/"
blog: "AWS Big Data"
locale: "en"
tags: [aws, kinesis, streaming, serverless, cost-optimization, cloudwatch]
---

# Scale Down Kinesis Data Streams On-Demand Capacity with ODA Warm Throughput

[한국어 버전](../../../../ko/sources/articles/aws/Scale_Down_Kinesis_Data_Streams_On_Demand_Capacity_with_ODA_Warm_Throughput.md)

**Authors**: Pratik Patel, Varsha Palepu, Priyanka Chaudhary · **Published**: 2026-09-14 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/scale-down-kinesis-data-streams-on-demand-capacity-with-oda-warm-throughput/)

## Problem

Kinesis on-demand mode auto-scales up on bursts (shard splits) but retained the elevated capacity after transient spikes — flash sales, batch migrations, IoT firmware bursts. The post's example: a 100 MB/s stream (100 shards) spikes +50 MB/s → 150 shards. After the spike the 150 shards remain. With a Lambda consumer at parallelization factor 2, invocations jump 200→300 (+50%) against quota and cost while processing small batches; KCL consumers eat extra DynamoDB leases (one per shard: scan/renew/checkpoint every heartbeat). Before this launch the only escapes were switching to provisioned mode (losing autoscaling) or accepting the excess.

## Solution: warm throughput scale-down

On-demand Advantage (ODA) streams now support lowering warm throughput to trigger a capacity reduction, at no extra cost. Resulting capacity = max(requested warm throughput, capacity needed for peak ingest in the last hour) — a safeguard against under-provisioning live traffic. After scale-down, reactive scaling still expands on new growth. Warm throughput is now bidirectional: scale up ahead of forecast events (existing), scale down after transients (new).

## Implementation

**Prerequisites**: existing on-demand stream, ODA mode on, AWS CLI, `kinesis:UpdateStreamMode`.

```bash
aws kinesis update-stream-mode \
  --stream-arn arn:aws:kinesis:us-east-1:111122223333:stream/my-stream/my-stream \
  --warm-throughput-in-mb 50
```

**Monitoring** (CloudWatch): `IncomingBytes` (Sum, aggregate throughput), `IncomingRecords` (traffic pattern/burst frequency), `WriteProvisionedThroughputExceeded` (non-zero after scale-down = target too low). Shard count is *not* a CloudWatch metric — poll `DescribeStreamSummary` (`OpenShardCount`) or the console, optionally via a Lambda-backed custom metric. Expected timeline: steady state (e.g. ~67 open shards at 20 MiB/s) → burst (splits, `OpenShardCount` + `IncomingBytes` rise) → post-burst plateau (traffic back, shards still high — stream holds ~2x recent peak) → post-scale-down merge (shards fall toward request, floored by the one-hour peak).

## Best practices

1. **Analyze 24h of `IncomingBytes`/`IncomingRecords`** before choosing a target; know baseline first.
2. **Target at or above steady-state peak, not the average** — on-demand accommodates ~2x observed peak, so keep headroom for normal variance.
3. **Watch `WriteProvisionedThroughputExceeded`** for hours after; scale back up on throttling (automatic recovery exists but monitoring shortens impact).
4. **Use after known transients** (migrations, marketing events, backfills); avoid during uncertain/growing traffic.
5. **Lean on the one-hour safeguard** when unsure — set a low value and let the peak floor prevent under-provisioning.

## Why it matters

- **Consumer cost control**: shard count drives Lambda concurrency and KCL/DynamoDB overhead, so warm-throughput tuning is downstream-compute tuning.
- **Elasticity made symmetric**: on-demand finally releases as well as acquires, keeping autoscaling benefits without the residue.
- **Operational simplicity**: one CLI value instead of a provisioned-mode migration.

## Takeaways for the seminar

- Remember the formula: final capacity = max(your request, last-hour peak need).
- Shard count is the hidden cost lever; `OpenShardCount` via API is the metric to plot, not just bytes.
- Scale-down is a post-mortem action for identified transients, not a routine dial.

## Related concepts

- `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-kafka.md`

## References

- [Amazon Kinesis Data Streams launches on-demand Advantage](https://aws.amazon.com/blogs/big-data/amazon-kinesis-data-streams-launches-on-demand-advantage-for-instant-throughput-increases-and-streaming-at-scale/)
- [On-demand capacity mode in the Developer Guide](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html)
- [DescribeStreamSummary API](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_DescribeStreamSummary.html)
