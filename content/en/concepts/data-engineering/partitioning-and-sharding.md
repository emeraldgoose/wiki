---
title: Partitioning and Sharding
description: Partition pruning, bucketing, strategies, skew, examples in Spark/Iceberg/BigQuery, pitfalls, and references
tags: [concept, data-engineering, partitioning, sharding, spark, iceberg, bigquery]
locale: en
published: 2026-09-07
---

# Partitioning and Sharding

**Partitioning** and **sharding** are techniques to distribute data across storage nodes or files, enabling parallelism, query optimization, and scale-out. While related, they operate at different levels: partitioning typically organizes data within a single system, while sharding distributes data across independent compute clusters. See also `[[apache-spark|Spark]]` and `[[iceberg|Iceberg]]` for distributed table examples.

## Partition Pruning

Partition pruning is an optimizer optimization that skips reading partition files that cannot satisfy a query's `WHERE` clause. By pruning irrelevant partitions, query latency drops dramatically and I/O decreases.

### How It Works

- Each partition is associated with a range, list, or hash key.
- The query optimizer evaluates `WHERE` column references against partition metadata.
- Partitions whose key space does not intersect the query predicates are eliminated from the scan.

### Example: Range Partitioning in Spark

```sql
-- Table range-partitioned by sale_date
CREATE TABLE sales (
  sale_id BIGINT,
  amount DECIMAL(10,2),
  sale_date DATE
)
PARTITIONED BY (sale_date);

-- Query prunes 2023 partitions when filtering 2024 only
SELECT SUM(amount) FROM sales WHERE sale_date >= '2024-01-01';
-- Only 2024 partitions are scanned; 2023 partitions are pruned.
```

### Example: Iceberg Hidden Partitioning

Iceberg's hidden partitioning means partition values are derived from data columns but not stored explicitly. The manifest files track partition stats, and the optimizer prunes based on those stats:

```sql
SELECT * FROM sales
WHERE sale_date = DATE '2024-03-15';
-- Iceberg reads manifest stats; if 2024-03-15 is not in any manifest's partition bounds, that partition is pruned.
```

## Bucketing

**Bucketing** (also called hashing) co-locates rows with the same key value in the same file bucket. Bucketed tables enable map-side joins, faster aggregation, and more efficient sampling.

### Bucket vs Partition

| Aspect | Partition | Bucket |
|--------|-----------|--------|
| **Purpose** | Prune groups of files per query | Co-locate same-key rows for map-side ops |
| **Key type** | Often high-cardinality (date, region) | Often join key (user_id, product_id) |
| **Granularity** | Coarser (days, regions) | Finer (hash buckets) |
| **Implementation** | `PARTITIONED BY (col)` | `CLUSTERED BY (col) INTO N buckets` |

### Example: Bucketed Table in Spark

```sql
CREATE TABLE orders (
  order_id BIGINT,
  customer_id INT,
  amount DECIMAL(10,2)
)
CLUSTERED BY (customer_id) INTO 32 BUCKETS
ROW FORMAT DELIMITED
STORED AS PARQUET;
```

Bucketed tables work with `SKEW JOIN` hints and `bucket_map_join` optimization to perform hash joins without shuffling the entire dataset.

## Sharding Strategies

**Sharding** distributes data across independent compute clusters or nodes. Each shard owns a disjoint subset of the data, and queries fan out to all shards, aggregating results.

| Strategy | Key Choice | Use Case |
|--------|-----------|----------|
| **Hash sharding** | `hash(key) % N` | Even distribution; no natural ordering required |
| **Range sharding** | Numeric or temporal ranges | Range queries, time-series, inequality filters |
| **Directory sharding** | Manual assignment per folder/prefix | Object storage (S3/GCS) with path-based routing |

### Hash Sharding

The most common approach. A hash function maps each key to one of N shards, guaranteeing uniform distribution (assuming a good hash function and high-cardinality key).

```python
# Pseudocode: assign order to shard based on order_id
shard_index = hash(order_id) % num_shards
```

### Range Sharding

Effective when query workload frequently filters on range conditions (e.g., `WHERE date >= '2024-01-01' AND date < '2024-04-01'`). Time-series data is the classic example.

**Risk:** skew if the data distribution is uneven (e.g., most events occur in a narrow time window).

### Directory Sharding (Cloud Object Storage)

Each shard corresponds to a prefix path in S3/GCS. Queries route to specific prefixes based on key prefixes. Common in Iceberg tables on cloud storage, where `optimize` writes to partitioned directories.

## Skew

**Skew** occurs when a subset of partition or bucket keys receives disproportionately more traffic or data volume than others.

### Partition Skew

- A few dates or categories dominate (e.g., `sale_date = '2024-12-25'` or `region = 'North America'`).
- Result: those partitions experience hot-spotting, slower queries, and executor memory pressure.

### Bucket Skew

- A few join keys have vastly more rows (e.g., `customer_id = 1` has 10M rows vs. average 100K).
- Result: skew join tasks spill to disk or fail; `SKEW JOIN` in Spark mitigates this by partitioning the build side.

### Mitigations

| Technique | Description |
|-----------|-------------|
| **Salting** | Add a random prefix to the join key to distribute hot keys across buckets (e.g., join on `rand(10) || customer_id`). |
| **Dynamic partitioning** | Adjust the number of partitions/buckets at runtime based on key distribution. |
| **Skew join hint** | In Spark, `/*+ SKEW_JOIN(t1.customer_id) */` to handle the build side specially. |
| **Increase bucket count** | More buckets reduce the row count per bucket, alleviating memory pressure. |

## Examples in Spark / Iceberg / BigQuery

### Spark SQL Partitioning

```sql
-- Create a range-partitioned table
CREATE TABLE sales_by_date
PARTITIONED BY (sale_date AS DATE)
USING PARQUET
AS SELECT * FROM raw_sales;
```

### Iceberg Table Evolution

Iceberg's `ALTER TABLE` evolves the partition spec without rewriting data:

```sql
-- Change from daily to monthly partitioning
ALTER TABLE sales SET PARTITION SPEC sale_date = month(sale_date);

-- Query continues to work; new writes use the new spec; old manifests are retired.
```

### BigQuery Partitioned Tables

BigQuery natively partitions by ingestion time or a `DATE` column:

```sql
-- Partition by ingestion date (_PARTITIONTIME)
SELECT * FROM `project.dataset.sales`
WHERE _PARTITIONTIME = DATE '2024-03-15';

-- Partition by a DATE column
CREATE TABLE `project.dataset.sales`
PARTITION BY DATE(sale_date)
CLUSTER BY customer_id
AS SELECT * FROM raw_sales;
```

BigQuery also supports **clustering**, which organizes data within each partition by the clustered columns, enabling pruning within partitions without separate bucketing.
