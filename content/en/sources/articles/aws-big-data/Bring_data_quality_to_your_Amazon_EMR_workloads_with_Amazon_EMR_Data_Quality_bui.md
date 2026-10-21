---
title: "Bring data quality to your Amazon EMR workloads with Amazon EMR Data Quality built on AWS Glue Data Quality"
description: "Amazon EMR Data Quality brings AWS Glue's DQDL rule engine natively into EMR Spark jobs on EC2, Serverless, and EKS, supporting ad hoc inline validation and Iceberg Write-Audit-Publish promotion gates via managed rulesets in the Glue Data Catalog."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality"
blog: aws-big-data
published_date: 2026-10-12
---

# Bring data quality to your Amazon EMR workloads with Amazon EMR Data Quality built on AWS Glue Data Quality

**Source**: AWS Big Data Blog, 2026-10-12

**Lead**: Bad data slips into EMR pipelines quietly — a null where a value belongs, a malformed timestamp, a dead referential key — and surfaces as wrong dashboards or failed jobs. Teams previously chose between hand-rolled Spark checks (e.g. Deequ, fully custom but self-maintained with no centralized rulesets) and routing data through Glue for managed quality (less code, but a separate engine and step). Amazon EMR Data Quality, bundled in the AWS runtime for Apache Spark (emr-spark-8.1.0+) on EMR on EC2, Serverless, and EKS, offers a third option: run AWS Glue Data Quality rules with the same DQDL syntax directly inside EMR Spark jobs.

## Background

AWS Glue Data Quality centers on the Data Quality Definition Language (DQDL), a declarative syntax for completeness, uniqueness, ranges, referential integrity, and distributions — plus ML-based `DetectAnomalies` rules that learn baselines across runs instead of fixed thresholds. Rules can live inline in a job or as versioned, shareable managed rulesets in the Glue Data Catalog. The evaluator returns per-rule pass/fail plus an overall score that the job can act on: fail the pipeline, quarantine rows, alert, or gate a merge. EMR Data Quality runs this same engine inside Spark, so Glue-authored rulesets work unmodified.

## Prerequisites

- Amazon EMR release with `emr-spark-8.1.0` or later (no bootstrap action needed).
- IAM permissions on the job execution role: `glue:AccessDataQualityRuntimeConfiguration`, `glue:CreateDataQualityRuleset`, `glue:GetDataQualityRuleset`, `glue:GetDataQualityResult`, `glue:PublishDataQuality`, `glue:GetDatabase`/`glue:GetTable`, plus S3 read/write.

## Pattern 1: Ad hoc inline validation

For exploratory or early-stage pipelines, rules live entirely in the job — e.g. validating a vendor CSV before lake ingestion (non-null IDs, non-negative revenue, allowed country codes). The job passes a DataFrame plus a DQDL string to `EvaluateDataQuality.apply()`, which returns a results DataFrame; any `Failed` outcome raises and stops the job, otherwise data is appended:

```python
from awsdataquality.transforms import EvaluateDataQuality

ruleset = """
Rules = [
 RowCount > 0,
 IsPrimaryKey "order_id",
 Completeness "customer_email" >= 0.95,
 ColumnValues "order_status" in ["PENDING","SHIPPED","DELIVERED","RETURNED"],
 ColumnValues "net_amount" between 0.0 and 25000.0
]
"""

dq_results = EvaluateDataQuality.apply(input_df, ruleset, publishing_opts,
                                       additional_opts, additional_sources)
failures = [r for r in dq_results.collect() if r["Outcome"] == "Failed"]
if failures:
    raise RuntimeError(f"Data quality checks failed:\n{failures}")
input_df.writeTo("company_sales.sales_data").append()
```

Sample evaluation output from the article:

| Rule | Outcome | Evaluated metric |
|------|---------|------------------|
| `RowCount > 0` | Passed | RowCount → 50000.0 |
| `IsPrimaryKey "order_id"` | Passed | Uniqueness 1.0, Completeness 1.0 |
| `Completeness "customer_email" >= 0.95` | Passed | Completeness → 0.979 |
| `ColumnValues "order_status" in [...]` | Failed | Compliance 0.996 |
| `ColumnValues "net_amount" between 0.0 and 25000.0` | Failed | Min −2228.87 |

## Pattern 2: Iceberg Write-Audit-Publish with managed rulesets

For production ETL, the article gates promotion on a centrally managed ruleset using the Iceberg Write-Audit-Publish (WAP) pattern for atomic promotion:

1. **Retrieve** the managed ruleset from the Glue Data Catalog (created once via `aws glue create-data-quality-ruleset`, owned and versioned by the governance team).
2. **Write** ETL output to a staging Iceberg branch (branch name carries the Spark application ID so concurrent runs never collide), never directly to `main`.
3. **Evaluate** the branch data with `EvaluateDataQuality` against the catalog ruleset.
4. **Merge or discard**: merge the branch into `main` only if the quality score meets the threshold; otherwise discard and alert.

Rules stay decoupled from pipeline code — governance changes propagate without touching jobs — and `main` readers never see partial or failed writes.

## Relevance to Software Engineers

- **Kill the false choice**: if you maintain Deequ checks today, EMR Data Quality centralizes rulesets and results in the Glue Catalog while keeping execution in your existing Spark jobs.
- **Start ad hoc, graduate to WAP**: inline rules suit evolving pipelines; once a governance team owns standards, switch promotion to branch-gated merges for atomicity.
- **Prefer anomaly detection for drifting metrics**: `DetectAnomalies` replaces hand-tuned thresholds on counts and totals that shift over time.
- **Mind the IAM surface**: cross-service publishing needs six Glue actions plus catalog and S3 rights — scope the execution role per pipeline, not per account.

## References

- Original article: [https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality](https://aws.amazon.com/blogs/big-data/bring-data-quality-to-your-amazon-emr-workloads-with-amazon-emr-data-quality-built-on-aws-glue-data-quality)
- AWS Glue Data Quality documentation (DQDL reference, linked from the original post)
- Related: Build Write-Audit-Publish pattern with Apache Iceberg branching and AWS Glue Data Quality (linked from the original post)
