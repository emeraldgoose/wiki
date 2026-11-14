---
title: "Optimizing PySpark UDFs on AWS Glue 6.0 with native Arrow UDFs"
description: "A parameterized AWS Glue 6.0 benchmark across 10M, 50M, and 100M rows shows the native Arrow UDF (arrow_udf, Apache Spark 4.1) is the fastest UDF approach — about 4.4× faster than a standard Python UDF on a compute-heavy workload — and that Arrow's benefit comes from the vectorized DataFrame execution path, not transport alone."
tags: [source, aws-big-data, glue, pyspark, performance, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/optimizing-pyspark-udfs-on-aws-glue-6-0-with-native-arrow-udfs"
blog: aws-big-data
published_date: 2026-11-14
---

# Optimizing PySpark UDFs on AWS Glue 6.0 with native Arrow UDFs

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/optimizing-pyspark-udfs-on-aws-glue-6-0-with-native-arrow-udfs) · **Published**: 2026-11-13

## Overview

Python UDFs in PySpark can degrade performance because data must be serialized between the Java Virtual Machine (JVM) and the Python runtime. AWS Prescriptive Guidance ranks the remedies: use built-in Spark SQL functions first, implement UDFs in Scala or Java next, and use Apache Arrow-based (vectorized, pandas) UDFs for vectorized workloads. That guidance rests on a small example — a + b over 10 million rows comparing a standard Python UDF, a vectorized UDF, and Spark SQL. This post extends it with the questions customers actually ask: does the ranking hold from 10 million to 100 million rows, does it hold for compute-intensive operations beyond a + b, and where do the two newer options in AWS Glue 6.0 (Apache Spark 4.1.1) fit — the Arrow-optimized Python UDF (useArrow=True) and the native Arrow UDF (arrow_udf, from Apache Spark 4.1.0)?

The authors ran a parameterized benchmark harness as an AWS Glue 6.0 job: generate a Parquet dataset once, write it to Amazon S3, and run every UDF variant against the same files. Measurements span three volumes (10M, 50M, and 100M rows) and three workloads of increasing per-row cost, each under two query shapes — a streaming shape (sum(op(a, b))) that isolates per-row cost, and a stateful shape (GROUP BY on about one million groups) that adds a shuffle and hash aggregation.

The verdict is consistent across volumes and shapes: the ranking matches the AWS Prescriptive Guidance recommendation, and among UDFs the native Arrow UDF is fastest whenever the logic maps onto PyArrow compute kernels. A controlled 2×2 experiment adds the key explanation: the benefit comes from Apache Arrow integrated into the vectorized DataFrame execution path, not from Arrow transport in isolation.

## Key points

- AWS Glue 6.0 runs Apache Spark 4.1.1 with Python 3.13 and Scala 2.13; the benchmark used 10 G.1X executors plus the driver in the US East (N. Virginia) Region (us-east-1), over a Parquet dataset with two bigint columns.
- Five approaches compared: standard Python UDF (Pickle transport, per-row Python), Arrow-optimized Python UDF (Arrow transport, per-row Python), vectorized pandas UDF (Arrow transport, NumPy per batch through a pandas conversion), native Arrow UDF (arrow_udf — Arrow transport, PyArrow compute per batch, no pandas conversion), and Spark SQL (no crossing, runs on the JVM).
- On mathheavy (sqrt(x² + y²) · sin(x) + ln(y)) at 100M rows: Spark SQL 1.22s, native Arrow UDF 3.13s, vectorized UDF 3.83s, Arrow-optimized Python UDF 11.01s, standard Python UDF 13.82s — the native Arrow UDF ran about 18 percent faster than the vectorized UDF.
- On the same workload, the gap between the native Arrow UDF (3.13s) and the standard Python UDF (13.82s) was about 4.4× for identical output; because Glue bills by the second, the difference translates directly into spend on every run.
- On arith (a + b) at 100M rows: Spark SQL 0.99s (11.8× faster than baseline), native Arrow UDF 2.81s (4.2×), vectorized UDF 3.13s (3.7×), Arrow-optimized Python UDF 8.94s (1.3×), standard Python UDF 11.68s (baseline).
- The vectorized-over-standard advantage widens with volume, from about 2.2× at 10M rows to 3.7× at 100M on arith, because per-row serialization cost grows with row count.
- On pyheavy (a bounded Collatz-style loop, at most 1,000 iterations per row), Spark SQL and the native Arrow UDF don't apply; the vectorized UDF is the best option, about 2.2× faster than the standard Python UDF at 10M and about 3.8× at 100M.
- Stateful query shape gives the same ranking (mathheavy at 100M: Spark SQL 1.59s, vectorized 4.22s, Arrow-optimized 11.02s, standard 14.33s), running somewhat slower due to shuffle and hash aggregation.
- In the controlled experiment, reproducing NumPy computation with Pickle transport via RDD.mapPartitions was slowest of all — 21.07 seconds at 100M, worse than the standard Python UDF's 13.82 seconds.
- Methodology mattered: a cached DataFrame made Spark SQL look slower than UDFs because the plan pruned per-row work; clearing the cache, re-reading Parquet every iteration, and using sum(...) restored the expected ranking. A UDF benchmark whose timings don't scale with row count is likely measuring the cache.
- A rewrite pays off when per-row work is non-trivial and data is large or the job runs often; for a trivial operation on a small, infrequent dataset the standard Python UDF may be perfectly adequate.

## Details

### How each variant crosses the JVM–Python boundary

The five approaches differ in transport and computation. The vectorized UDF and the Arrow-optimized Python UDF both use Apache Arrow for transport, so both show ArrowEvalPython in the physical plan; the difference is that a vectorized UDF receives a pandas.Series batch and computes with NumPy in native code, while the Arrow-optimized variant is still a scalar UDF receiving one value per call. The native Arrow UDF, introduced with the arrow_udf decorator in Apache Spark 4.1 and available in AWS Glue 6.0, receives and returns a pyarrow.Array and computes with PyArrow compute kernels directly on Arrow data, with no pandas conversion. Spark SQL never crosses the boundary at all. The code shapes mirror this: useArrow=True wraps a scalar lambda, pandas_udf wraps a batch function over pandas.Series, and arrow_udf composes PyArrow kernels such as multiply, sqrt, add, and sin.

### Benchmark design: three workloads, two query shapes

Three per-row operations of increasing cost were chosen deliberately. arith (a + b) isolates transport cost because computation is trivial. mathheavy (sqrt(x² + y²) · sin(x) + ln(y)) adds real computation that maps onto SQL, PyArrow compute kernels, NumPy, and scalar Python, so all five approaches compete. pyheavy is a data-dependent Collatz-style iterative loop — derivable from columns a and b, halving when even, otherwise 3n + 1, bounded at 1,000 iterations — that maps onto neither SQL nor PyArrow kernels, so only the Python-based UDFs apply. Each workload ran under the streaming shape (sum(op(a, b)), a full scan reduced to one value) and the stateful shape (GROUP BY cast(op(a, b) AS bigint) % 1,000,000, about one million groups), for every approach and volume. One warm-up iteration was discarded and the best of seven timed iterations reported.

### Results and the controlled transport-versus-computation experiment

The streaming tables above give the numbers; timings scale approximately linearly across 10M, 50M, and 100M and the ranking is stable at every volume. For pyheavy the stateful figures run somewhat slower than streaming (for example, vectorized UDF 2.99s streaming versus 3.01s stateful at 100M), but the order doesn't change. To test whether the vectorized UDF's edge comes from transport or computation, the authors constructed the missing combination — NumPy computation over Pickle transport using RDD.mapPartitions — and it was slowest of all at 21.07 seconds for 100M rows. Forcing Pickle transport means leaving the DataFrame API, which materializes each row as a Python object before a NumPy array can be built and bypasses the optimized DataFrame execution engine. The conclusion: the benefit is Arrow integrated into the vectorized DataFrame execution path, combining columnar transport and NumPy computation; reproducing only the NumPy portion outside that path yields no benefit, so keep vectorized logic in the DataFrame API rather than dropping to RDD operations.

### Practical guidance

When a UDF is required and the logic maps onto PyArrow compute kernels, prefer the native Arrow UDF — fastest in these tests and available in AWS Glue 6.0 (Apache Spark 4.1). Use the Arrow-optimized Python UDF (useArrow=True) when you want a minimal change to an existing scalar UDF; it improves transport but not computation, so vectorized or native approaches win whenever per-row work is non-trivial. Stay in the DataFrame API to keep Arrow's benefit. Weigh the rewrite as a one-time cost against per-second savings that scale with row count and job frequency: a compute-heavy transform over hundreds of millions of rows run daily typically repays itself in the first few runs, while a trivial operation on a small, infrequent dataset may not need a rewrite at all.
