---
title: "Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS"
description: "CUDOS 5.10 adds an Amazon Redshift RA3-to-RG section that estimates migration savings, tracks the instance-generation mix, and quantifies the efficiency already gained on Graviton-based RG."
tags: [source, aws-big-data, data-engineering, finops, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos"
blog: aws-big-data
published_date: 2026-11-10
---

# Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS

**Source**: [Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS](https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos) · **Published**: 2026-11-09

## Overview

Graviton-based RG instances, launched on 12 May 2026, give every Amazon Redshift RA3 customer a migration path with a better price-performance profile: up to 2.2x faster for data warehouse workloads and up to 2.4x faster for data lake workloads, at 30% lower price per vCPU than RA3, with full feature parity and no per-TB scan charges for Redshift Spectrum. Manual snapshot storage is now also metered on the unique data blocks stored across cluster snapshots. The catch is organizational rather than technical — running a measurable migration across many accounts and teams requires visibility into what you could save, how far adoption has progressed, and what has already been gained.

The post shows how CUDOS, the Cost and Usage Dashboard Operations Solution within the open-source Cloud Intelligence Dashboards (CID) framework, answers those three questions. CID dashboards are built entirely from the AWS Cost and Usage Report, and CUDOS is the granular, recommendation-driven member of the family: it pairs executive summaries with drill-down to resource level on Quick Sight SPICE datasets, organized into tabs such as Executive summaries, Compute, Databases, Storage, AI/ML, Analytics, Security and Data Transfer, with spend trends, idle-resource waste, Reserved Instance and Savings Plans tracking, and a Taxonomy Explorer for tag and account-mapping views.

Version 5.10 introduces a dedicated Amazon Redshift RA3-to-RG section structured as "What could we save?", "How is our migration progressing?" and "What have we already gained?".

## Key points

- A headline KPI, Monthly Cost Savings Opportunities with Migration to Redshift RG over the last 30 days, gives the total estimated monthly saving if eligible RA3 resources moved to RG; a companion resource-level table expands it into account, cluster, purchase type and line-item hierarchy.
- The estimate is built from three columns — Current Cost on RA3, Estimated Cost on RG and Estimated Savings on RG — with a total row that ties back to the KPI; as with all list-price-based estimates, actual savings vary and exclude performance, data-transfer and other usage-specific factors.
- Adoption is tracked with a 100% stacked column chart of cost share across instance generations month over month, showing leadership how the mix shifts from RA3 to RG as migration proceeds.
- Realized benefit is charted separately: a column chart of achieved monthly efficiency gains on RG with the 4xlarge node-decrease ratio from the RA3-to-RG migration best-practices post applied, so it quantifies the return on migration rather than the opportunity ahead.
- Two in-place filters tune the model to the environment: a Purchase Option menu that can model On-Demand or Reserved pricing (Reserved is informational only, because changing a node type does not move existing Reservations — those must go through Billing Support or the account team), and an Incremental Snapshot Size slider for the share of data that changes between manual snapshots.

## Details

Deployment runs through AWS CloudFormation or the CID Terraform module, and AWS recommends a dedicated data collection account separate from the management or payer account. The first step creates the CUR destination in the data collection account — an S3 bucket with a policy allowing AWS Data Exports to write to it, plus the AWS Glue and Athena tables — with destination account ID and source account IDs configured, and takes 5–15 minutes. The second step launches a stack in every source account to create CUR 2.0 pointing at that destination, about 5 minutes each, though the first Data Exports delivery typically takes around 24 hours and up to 72; Billing support can backfill up to 14 months of history. The third step deploys the dashboards in the data collection account, which requires Amazon Quick Sight setup (sign-up, correct Region, roughly 40 GB of SPICE capacity) and lets you select CUDOS and optionally the Cost Intelligence and KPI dashboards.

Hands-on effort is roughly 15–30 minutes with the automation, while the first CUR refresh can take up to 24 hours to appear. Every stack must be deployed in the same Region to avoid cross-Region data-transfer charges, and existing CUDOS installations can be updated to 5.10 by following the Update Dashboards guide.

## References

- Original article: [Assess and track your Amazon Redshift RA3 to RG modernization with CUDOS](https://aws.amazon.com/blogs/big-data/assess-and-track-your-amazon-redshift-ra3-to-rg-modernization-with-cudos)
