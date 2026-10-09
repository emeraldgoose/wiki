---
title: Apache Flink
description: Stateful stream processing engine with event-time semantics, exactly-once guarantees, and unified batch/stream API
tags: [concept, data-engineering, stream-processing, flink, real-time]
locale: en
---

# Apache Flink

**Apache Flink** is a distributed stream processing engine designed for stateful computations over unbounded and bounded data streams. It provides event-time processing, exactly-once guarantees, and a unified API for batch and streaming.

## Core Philosophy

### Streaming-First, Batch as Special Case
- **Bounded streams** = batch processing (finite input)
- **Unbounded streams** = real-time processing (infinite input)
- Same APIs, operators, and runtime for both

### Event-Time Processing
- Processes events based on **when they occurred**, not when processed
- Handles late/out-of-order events via watermarks
- Enables correct results regardless of processing delays

### Exactly-Once Semantics
- **End-to-end exactly-once**: Source → Flink → Sink with transactional sinks
- **Checkpointing**: Periodic distributed snapshots of operator state (Chandy-Lamport)
- **Savepoints**: Manual snapshots for upgrades, migrations, A/B testing

## Architecture

### Runtime Components
```
JobManager (Cluster Coordinator)
    ├── Resource Manager (slot allocation)
    ├── Dispatcher (REST API, job submission)
    └── JobMaster (per-job: scheduling, failover, checkpoints)

TaskManagers (Worker Nodes)
    ├── Task Slots (resource units)
    └── Operators (subtasks with state)
```

### Execution Model
- **Pipelined execution**: Data flows continuously between operators (network shuffle)
- **Operator chaining**: Fuse compatible operators into single task (reduces serialization/network)
- **Async I/O**: Non-blocking external service calls (databases, APIs)

### State Backends
| Backend | Storage | Use Case |
|---------|---------|----------|
| **HashMap** | Heap | Small state, low latency |
| **EmbeddedRocksDB** | Local disk (RocksDB) | Large state (TB), incremental checkpoints |
| **Changelog** | Remote (Kafka/Pulsar) | Disaggregated state; fast recovery |

## Key APIs

### DataStream API (Java/Scala)
```java
// Event-time window with watermark
DataStream<Event> stream = env.addSource(kafkaSource)
    .assignTimestampsAndWatermarks(WatermarkStrategy
        .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
        .withTimestampAssigner((e, ts) -> e.getTimestamp()));

stream.keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .reduce((a, b) -> a.add(b))
    .addSink(icebergSink);
```

### Table API / SQL (Unified Batch + Stream)
```sql
-- Streaming aggregation with window TVF
SELECT user_id, COUNT(*) AS cnt,
       window_start, window_end
FROM TABLE(
  TUMBLE(TABLE events, DESCRIPTOR(event_time), INTERVAL '5' MINUTE)
)
GROUP BY user_id, window_start, window_end;
```

### Python API (PyFlink)
Full parity with Java/Scala APIs; popular for ML preprocessing pipelines.

## Connectors (Sources & Sinks)

### Sources
- **Kafka** (exactly-once, consumer groups, partition discovery)
- **Kinesis** (enhanced fan-out, checkpointing)
- **Pulsar** (transactions, geo-replication)
- **File Systems** (S3, HDFS, local — continuous file monitoring)
- **JDBC/CDC** (Debezium for MySQL/Postgres/Oracle → Flink)

### Sinks
- **Kafka** (transactional, exactly-once)
- **Iceberg** (dynamic sink, schema evolution, branching)
- **JDBC** (upsert, batch writes)
- **File Systems** (rolling files, partitioning, compaction)
- **OpenSearch/Elasticsearch** (bulk indexing)

## Advanced Features

### Complex Event Processing (CEP)
- Pattern detection on event streams (e.g., "A followed by B within 5min then C")
- NFA-based pattern matching; supports loops, alternation, time constraints

### Stateful Functions (Cloud-Native)
- **Embedded mode**: Functions as Flink operators
- **Remote mode**: Functions as independent services (gRPC/HTTP)
- Enables serverless-style event-driven architectures

### SQL on Streaming
- **Dynamic tables**: Streams as append-only tables; changelog streams as updating tables
- **Temporal joins**: Versioned table joins (lookup at event time)
- **Window TVFs**: TUMBLE, HOP, CUMULATE, SESSION
- **CDC ingestion**: `CREATE TABLE ... WITH ('connector' = 'mysql-cdc')`

## Operational Concerns

### High Availability
- **JobManager HA**: ZooKeeper/Kubernetes leader election
- **TaskManager failure**: Automatic rescheduling on healthy TMs
- **State recovery**: From latest checkpoint/savepoint (seconds for RocksDB incremental)

### Scaling
- **Parallelism**: Set per operator; change via savepoint + restart
- **Reactive scaling** (K8s): KEDA/HPA based on backlog/latency metrics
- **Predictive scaling**: ML-based load forecasting (Netflix, Uber)

### Monitoring & Debugging
- **Metrics**: Latency, throughput, backpressure, checkpoint duration, state size
- **Web UI**: Job graph, timeline, flame graphs, backpressure visualization
- **Queryable state**: Expose operator state via REST for external lookups

## Flink on Kubernetes

### Deployment Modes
| Mode | Description |
|------|-------------|
| **Session Cluster** | Long-running cluster; multiple jobs share TMs |
| **Job Cluster** | Dedicated cluster per job; isolates resources |
| **Application Cluster** | Job + Flink runtime in single container (native K8s) |

### Kubernetes Operator
- **FlinkDeployment** CRD manages JobManager + TaskManager pods
- **Savepoint/Upgrade**: Automated rolling upgrades via savepoints
- **Autoscaling**: Integrated with KEDA for reactive scaling

### Managed Services
- **Amazon Managed Service for Apache Flink** (KDA)
- **Google Dataflow** (Flink runner)
- **Azure Stream Analytics** (Flink-compatible)
- **Ververica Platform** (Enterprise Flink on K8s)

## Iceberg Integration (Streaming Lakehouse)

### Dynamic Sink (Flink 1.18+, Iceberg 1.5+)
```sql
CREATE TABLE events (
  event_id STRING,
  event_time TIMESTAMP(3),
  payload STRING,
  event_type STRING
) PARTITIONED BY (event_type)
WITH (
  'connector' = 'iceberg',
  'catalog-type' = 'rest',
  'catalog-uri' = 'https://polaris.example.com/api/catalog',
  'warehouse' = 's3://bucket/warehouse',
  'format-version' = '2'
);

-- Streaming insert with schema evolution
INSERT INTO events SELECT ... FROM kafka_source;
```

### Capabilities
- **Schema evolution**: Add columns, change types without pipeline restart
- **Automatic table creation**: New event types → new partitioned tables
- **Exactly-once**: Two-phase commit with Iceberg spec
- **Format v2/v3**: v3 supports row-level deletes (MERGE INTO)

## Key References
- [Flink Documentation](https://nightlies.apache.org/flink/flink-docs-master/)
- [Flink SQL Reference](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sql/overview/)
- [Flink on Kubernetes](https://nightlies.apache.org/flink/flink-docs-master/docs/deployment/resource-providers/kubernetes/)
- [Iceberg Flink Integration](https://iceberg.apache.org/docs/latest/flink/)
- [Ververica Blog](https://ververica.com/blog/) — Flink engineering insights

## Related Concepts
- `concepts/data-engineering/stream-processing.md`
- `concepts/data-engineering/apache-iceberg.md`
- `concepts/data-engineering/apache-kafka.md`
- `concepts/infrastructure/kubernetes.md`