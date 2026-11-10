---
title: "Introducing the Workday Data Cloud integration with AWS"
description: "AWS and Workday ship bi-directional, zero-copy access to Workday's governed people and money data from AWS analytics and AI services, federating the Workday Iceberg REST Catalog through AWS Glue so no ETL copies are needed."
tags: [source, aws-big-data, data-lake, iceberg, governance, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws"
blog: aws-big-data
published_date: 2026-11-11
---

# Introducing the Workday Data Cloud integration with AWS

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws) · **Published**: 2026-11-09

## Overview

AWS has announced an integration between Workday Data Cloud and AWS that gives AWS analytics and AI services bi-directional, zero-copy access to Workday's governed people and money data. The problem it targets is familiar: connecting enterprise systems to analytics platforms usually means building brittle pipelines, duplicating data, and losing the governance and business context that make the data trustworthy. Workday Data Cloud is described as an open, secure, headless data platform that exposes Workday data in the tools developers already use while keeping semantic definitions, permission models, metric logic, and audit controls intact. It offers a curated view through the Workday Data Lake, bi-directional zero-copy access through Workday Data Connect over Apache Iceberg, and near real-time SQL access for applications and agents through Workday Live Data Query.

The integration is bidirectional, so neither side has to copy: each platform queries the other's data in place and respects the governance controls already defined on both sides. Workday's Iceberg REST Catalog is registered as a federated catalog in AWS Glue, which makes Workday datasets discoverable through any service that reads the Glue Data Catalog — Amazon Athena, Amazon Redshift, Amazon EMR, and Amazon SageMaker AI — without extra configuration. The reverse direction works the same way, with the Iceberg REST Catalog endpoint of the AWS Glue Data Catalog registered as an external catalog in Workday Data Cloud so Workday users can browse and query Apache Iceberg tables stored on Amazon S3 in near real time.

The AWS side of the stack maps onto this as follows. Amazon SageMaker Unified Studio is the unified development environment where developers connect to Workday Data Cloud, explore datasets interactively, run SQL, and build models. Amazon Athena provides serverless SQL over Iceberg tables backed by Amazon S3, and Amazon Redshift can incorporate Workday people and money data through Glue Data Catalog federation for cross-domain analytics without data movement. AWS Lake Formation supplies the fine-grained permission layer on the AWS side, letting administrators scope each analyst or application to specific databases, tables, rows, or columns, complementing the governance Workday applies at its own data layer.

## Key points

- Two access patterns cover different freshness needs. Workday Live Data Query executes SQL directly against live Workday datasets from SageMaker Unified Studio, Athena, EMR, or AWS Glue, with the query running inside Workday's governed environment and results flowing back in near real time — aimed at operational AI agents and dashboards where freshness is critical.
- The second pattern suits larger-scale work: registering the Workday Iceberg REST Catalog in the Glue Data Catalog or Lake Formation makes every Workday dataset appear as a standard Iceberg table, with compute running in the customer's AWS account (Athena, Redshift, EMR, or SageMaker AI) while the data itself stays in Workday Data Cloud.
- Governance is layered rather than merged: federation uses OAuth 2.0 authentication, AWS Lake Formation defines which databases and tables the Workday connection may read, and Workday's Configurable Security controls which Workday principals can access the federated tables.
- The article's example combines both directions — an AI agent doing workforce planning in Workday pulls revenue forecasts from an Iceberg table on AWS and combines them with headcount data to produce hiring recommendations for HR planners.
- The stated payoff is removing ETL: organizations no longer build and maintain pipelines just to land Workday data in an analytics environment, so data silos disappear without duplication and data teams spend their time on analytics and ML applications instead of monitoring freshness and reconciling duplicates.
- Business context travels with the data. Because the semantic meanings, permission model, and calculation logic come along, developers spend less time reverse-engineering business logic or rebuilding permission models for agents and models.

## Details

A workforce-analytics walkthrough illustrates the intended workflow: connect to Workday Data Cloud from AWS Glue with the pre-built Workday connector; explore compensation, tenure, engagement, and performance datasets with job levels, org hierarchies, and tenure calculations already defined; join that people data with market compensation benchmarks and recruiting pipeline data stored as Iceberg tables on Amazon S3 using standard SQL in Athena or SageMaker AI notebooks; train an attrition-risk model in SageMaker AI; and deploy an agent that flags high-risk attrition patterns for HR business partners, using Live Data Query for near real-time signals and batch Iceberg access for historical trends. The authors stress that no data leaves its governed environment, no custom pipelines need maintaining, and every step stays auditable.

The integration is generally available. SageMaker Unified Studio users can connect to Workday Data Cloud through either the Workday Live Data Query connector or the Workday Iceberg REST Catalog connector; Live Data Query connections can also be created in the AWS Glue console so that live Workday data is queryable from Athena, Amazon EMR, and Glue ETL jobs; Glue and Lake Formation users can register the Workday Iceberg REST Catalog as a federated catalog; and Workday users who want to query AWS data can register their Glue Data Catalog Iceberg REST endpoint as an external catalog in Workday Data Cloud.

## References

- Original article: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws)
