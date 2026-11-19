---
title: "How Veeva scaled big data with Amazon EMR on EKS"
description: "Veeva Compass moved petabyte-scale Spark batch processing from EMR on EC2 to EMR on EKS with Karpenter, cutting a skewed join stage from 7 hours to 55 minutes and adding four-layer observability, IRSA-based multi-tenant isolation, and Lake Formation/OpenLineage auditing."
tags: [source, article, aws-big-data, emr, spark, life-sciences, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/how-veeva-scaled-big-data-with-amazon-emr-on-eks"
blog: aws-big-data
published_date: 2026-11-19
---

# How Veeva scaled big data with Amazon EMR on EKS

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-veeva-scaled-big-data-with-amazon-emr-on-eks)
**Published**: 2026-11-18

## Overview

Veeva Systems, a leader in cloud software for the global life sciences industry, runs Veeva Compass and the Compass Data Network, unifying prescriptions, in-office procedures, and diagnoses into data products for biopharma customers. Its analytics lake, originally designed for hundreds of terabytes daily, grew exponentially with customer expansion and more data sources/products. Batch job variability caused Spark executors to spill to disk when shuffle stages ran out of memory, adding hours to execution. Veeva revisited its Amazon EMR on EC2 architecture and migrated to Amazon EMR on EKS with Karpenter.

## Key points

- The motivation: orphan therapies were half of U.S. novel drug approvals in 2025, amplifying demand for scalable analytics infrastructure for rare-disease therapies.
- Compass delivered data from suppliers to customers within hours while accelerating analytics and AI workflows, flagging new patient and HCP events earlier so medical reps can engage at the right time.
- Spark tuning: partitioning, continuous compaction, and Adaptive Query Execution (AQE) tuning reduced a skewed join stage from 7 hours to 55 minutes. Reading lookup tables cached in memory (avoiding repeated S3 reads) cut runtime by 20–30% for jobs referencing the same tables multiple times.
- Observability is layered: (1) Spark History Server on EKS with S3-backed event logs for replay and stage-level metrics; (2) Prometheus and Grafana for real-time metrics (executor CPU/memory, pending-pod queue depth, shuffle-spill ratios, Karpenter provisioning latency); (3) CloudWatch Logs Insights aggregating driver/executor logs with automated alerting; (4) OpenTelemetry traces linking Spark jobs to Airflow/Step Functions orchestration.
- Critical alerts: pending pods above threshold (capacity constraints), high shuffle-spill ratios (memory pressure), excessive repartitioning (data skew).
- Security: IRSA gives each Spark job temporary credentials scoped to specific S3 prefixes and Lake Formation permissions (read bronze/silver, write only designated output paths); Kubernetes namespaces with taints/tolerations isolate teams; KMS encryption at rest, TLS in transit, customer-managed keys for S3, Spark built-in shuffle encryption; Lake Formation + OpenLineage for lineage and auditing.
- Migration from EMR on EC2 to EMR on EKS + Karpenter produced measurable improvements across key metrics (see the post for the full bronze→silver table).

## Details

- Veeva Compass unifies prescriptions, procedures, and diagnoses; the Compass Data Network keeps adding closed and open data partners to fill gaps in traditional patient data products.
- The original EMR on EC2 design struggled with variable batch volumes: memory-starved executors spilled shuffle data to disk, adding hours per job.
- EMR on EKS with Karpenter provided elastic compute matched to job variability, avoiding execution slowdowns as data volumes kept growing.
- Details worth noting: lookups cached in memory, skewed-join remediation via AQE, and a four-layer observability stack wired into SLA-driven alerting.
