---
title: "Governance compliance beyond the catalog in Amazon SageMaker Unified Studio"
description: "An AWS pattern that turns SageMaker Unified Studio's governance signals — metadata forms, data quality scores, glossary terms, subscriptions — into a daily enrichment pipeline computing a weighted compliance score per asset, written as an S3 Table snapshot consumed by Athena, QuickSight dashboards, and EventBridge alerts, with a consumption-weighted risk matrix to prioritize ungoverned data."
tags: [source, aws-big-data, data-governance, catalog, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/governance-compliance-beyond-the-catalog-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-11-14
---

# Governance compliance beyond the catalog in Amazon SageMaker Unified Studio

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/governance-compliance-beyond-the-catalog-in-amazon-sagemaker-unified-studio) · **Published**: 2026-11-11

## Overview

A data catalog typically answers what exists: asset names, schemas, ownership. As the catalog grows, the harder question is which assets actually meet the organization's governance standards. Amom Luiz, Guilherme Monte, and Brenda Medeiros de Florenco build on SageMaker Unified Studio's governance building blocks — metadata form definitions, data quality scores, glossary associations, subscription data, and a daily catalog export queryable through SQL — to construct a governance enrichment pipeline that computes a weighted compliance score for every asset and publishes it as a queryable table.

The pipeline runs daily and joins five sources through an enrichment Lambda: the SageMaker asset metadata export (the base inventory, stored as an S3 Table), a Form Policy Config JSON in S3 that defines organization-level required forms per project and asset type, the Search/GetListing API (glossary terms, attached metadata forms, data quality summary per asset), the GetAssetType API (complete data quality rules count), and the ListSubscriptions API (active consumer subscriptions per published asset). The result — one enriched compliance record per asset, including a weighted score — lands as a daily snapshot partition in the governance_metadata.asset_compliance S3 Table, which is itself an asset in the SageMaker catalog, queryable inside SageMaker Unified Studio alongside all domain assets. Downstream consumers are Amazon Athena queries, an AWS QuickSight compliance dashboard, and Amazon EventBridge compliance alerts.

The compliance score combines five dimensions with configurable weights: form coverage at 50% (required forms present versus policy), data quality score at 20% (pass/fail percentage), data quality rule coverage at 10% (actual rules versus a minimum expected), glossary presence at 10% (at least one glossary term), and description at 10% (a business or resource description). Required is treated as a two-level concept: SageMaker Unified Studio's own enforcement rules (mandatory metadata forms at the asset-type level, read from GetAssetType's formsOutput required flag) plus custom organization requirements that lack enforcement rules — for example a project requiring a DataClassificationForm on every Glue table — stored in the S3 policy file. The pipeline takes the union of both layers.

The article emphasizes that the key takeaway is the pattern, not the specific weights: once the signals are in one place, your team defines what "compliant" means for your context. Four role-based questions illustrate the payoff — a data owner asks which assets are missing a required metadata form, a data steward which assets have no glossary terms, a platform team whether compliance is improving since new governance rules were published, and a chief data officer which departments need to work on more reliable data products.

## Key points

- Solution shape: daily enrichment pipeline (Lambda) joining five sources — asset metadata export (S3 Table asset_metadata.asset), S3 Form Policy Config JSON, Search/GetListing, GetAssetType, and ListSubscriptions APIs — writing a daily snapshot to the governance_metadata.asset_compliance S3 Table.
- Enabling the export: aws datazone put-data-export-configuration --domain-identifier DOMAIN_ID --region REGION --enable-export, once per domain; the export is readable as an S3 Table within 24 hours. The pipeline uses asset_id (join key), extended_metadata['owningEntityId'] (per-project policy lookup), and business_description/resource_description (description signal).
- Two-level "required": Level 1 — SageMaker Unified Studio metadata enforcement rules at the asset-type level (GetAssetType, required boolean in formsOutput); Level 2 — custom organization requirements without native enforcement (per-project required forms) stored in an S3 JSON policy file with default and per-project required_forms lists; the pipeline unions both.
- Compliance score dimensions and weights (configurable): form coverage 50%, data quality score 20%, data quality rule coverage 10%, glossary presence 10%, description 10%; weights and the minimum data-quality-rules threshold are tunable per organization.
- Compliance bands for interpreting scores: 80-100 fully governed; 60-79 mostly governed; 40-59 partially governed; 20-39 data quality only; 1-19 minimally documented; 0 ungoverned.
- SQL answers on the enriched table: assets missing required forms; per-project scorecard (total assets, average compliance score, assets with form gaps, assets passing data quality); daily compliance trend since a governance policy publish date.
- Alerting: EventBridge Scheduler plus Lambda sends weekly (or daily) reports and alerts when compliance drops below a threshold, routed to SNS, SES, or a Slack webhook; the sample query counts non-compliant assets per project.
- Dashboard: QuickSight connects directly to Athena over the enriched table (grant the aws-quicksight-service-role-v0 role Lake Formation DESCRIBE/SELECT); a Python script in the aws-samples repository creates the data source, datasets, and dashboard, and QuickSight's natural-language Build feature generates the visualizations from plain-language prompts (average compliance score by project, compliance-band pie, score trend by snapshot date, form-gap stacked bars, glossary-coverage KPI, average DQ rules by project).
- Consumption-weighted risk: subscription counts from ListSubscriptions (projects with approved subscriptions per published asset) combine with compliance scores into a risk matrix — gold standard (score ≥ 80, high adoption, no action), over-invested (≥ 80, zero subscriptions, review), backlog (< 50, zero subscriptions, plan over time), critical (< 50, two or more subscriptions, act now); a CASE-based query tags assets CRITICAL/MEDIUM_RISK/OK and orders them by subscriptions and score, turning the dashboard into a prioritization engine based on downstream impact.
- Data products: SageMaker Unified Studio lets producers group related assets into versioned, self-contained data products that consumers subscribe to in one request; compliance rolls up to the data-product level via an asset_id-to-product mapping built by iterating over all projects (total assets, product compliance score, total subscriptions, assets with form gaps per product).
- Worked example: 20 published Glue tables across three projects at different governance maturities — the project with metadata forms, glossary terms, and data quality rules leads the scorecard, the others trail with only basic data quality checks.
- Scalability and cost: in the test domain (29 published Glue Table assets, three projects) the enrichment Lambda finished in about 30 seconds; for production scale, parallelize enrichment calls, raise Lambda memory, or fan out with AWS Step Functions. Deployment is via the sample-smus-asset-scorecard CDK repository (enrichment Lambda, S3 policy bucket, EventBridge Scheduler rule, IAM roles, S3 Table namespace); Lake Formation governs both the export and the enriched table, requiring DESCRIBE/SELECT grants for the Lambda and service roles. Estimated effort about two hours; estimated cost under $5/month for a small test domain.

## Details

### Why enrichment rather than another catalog view

The metadata export already tells you which form fields are filled, but "filled" is not "required," and requirement has two sources in this design: platform enforcement rules and organizational policy that the platform does not enforce. The pipeline's policy layer therefore unions GetAssetType's per-asset-type required flags with the S3-defined per-project form requirements, so a project can mandate, say, a DataClassificationForm on every Glue table without waiting for platform-level support. Everything else — glossary terms, data quality summaries, subscription counts — arrives through catalog APIs because the export does not carry them.

### From scorecard to prioritization

The most interesting design move is weighting by consumption. A compliance score alone ranks assets by their own maturity; adding the approved-subscriber count per published asset produces quadrants where an ungoverned asset with many consumers ("critical": score < 50, subscriptions ≥ 2) outranks a pristine asset nobody uses ("over-invested"). The risk query's CASE logic (CRITICAL, MEDIUM_RISK, OK) is deliberately simple, and the article positions this as the difference between a passive scorecard and a prioritization engine that tells asset teams where to focus based on compliance gaps and downstream impact together.

### Rolling up to the consumer's level

Because data products are the unit data consumers actually subscribe to, the pattern also aggregates compliance at that level: an asset_id-to-data-product mapping is built by iterating over all projects, and a rollup query reports total assets, product compliance score, total subscriptions, and form-gap counts per product. Unassigned assets surface as an "(unassigned)" group, so nothing hides in the aggregation. This keeps executive views aligned with the level at which access and accountability are actually granted.
