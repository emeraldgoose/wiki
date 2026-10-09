---
title: "How United Airlines Uses Amazon Redshift and Glue Data Catalog Federation to Query Databricks-Managed Data"
description: "United Airlines federation chain from Databricks Unity Catalog through Glue federated catalog and Lake Formation to Redshift Serverless, with resource-link pattern and measured cost impact."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/how-united-airlines-uses-amazon-redshift-and-aws-glue-data-catalog-federation-to-query-databricks-managed-data/"
blog: "AWS Big Data"
locale: "en"
tags: [aws, redshift, glue, lake-formation, databricks, unity-catalog, iceberg, federation]
---

# How United Airlines Uses Amazon Redshift and Glue Data Catalog Federation to Query Databricks-Managed Data



**Authors**: Vaibhav Agrawal (AWS), Ankit Aggarwal and Raja Kalluri (United Airlines) · **Published**: 2026-09-15 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-united-airlines-uses-amazon-redshift-and-aws-glue-data-catalog-federation-to-query-databricks-managed-data/)

## Problem

United Airlines curates petabytes through a medallion (bronze→silver→gold) architecture on S3; the user-interaction gold layer alone is double-digit terabytes of near-real-time streamed data. Tables are cataloged in Databricks Unity Catalog, invisible to Amazon Redshift Serverless where ~100 analysts work. Without federation the only path was duplicating data into Redshift Managed Storage plus sync pipelines — expensive and drift-prone.

## Solution overview

Glue Data Catalog federation bridges the platforms at the metadata layer with a four-layer chain:

1. **Unity Catalog** exposes tables via its Iceberg REST API (Delta tables use UniForm for Iceberg compatibility).
2. **Glue federated catalog** (`databricks-federated-catalog`) connects to Unity Catalog — metadata visible in AWS, no data movement.
3. **Resource-link database** (`databricks_federated_db_link`) in the default Glue catalog points at the federated database — required because Redshift resolves `CREATE EXTERNAL SCHEMA` only against the default catalog.
4. **Redshift Serverless external schema** references the resource link; at query time Redshift traverses the link, Glue Federation calls the Unity REST API, Lake Formation vends scoped S3 credentials, and Redshift reads Iceberg files directly from S3.

The six-step query flow: analyst SQL → external schema resolution → federated catalog REST call → namespace IAM role calls `lakeformation:GetDataAccess` → policy evaluation and credential vending → direct S3 read. The Graviton-based Serverless engine (up to 2x faster lake queries per the linked post) is purpose-built for this Iceberg-direct pattern. Rollout is phased: 30 tables in production, 70 rolling out, several hundred planned.

## Implementation

**Prerequisites**: Databricks workspace with Unity Catalog + catalog/schema/table (UniForm on); AWS account with Glue/Lake Formation/Redshift Serverless/IAM rights; provisioned Serverless workgroup+namespace; Lake Formation admin; AWS CLI. Phase 1 (Unity-side setup) follows the companion post on accessing Unity Catalog via federation.

1. **Lake Formation**: add a data lake admin; confirm `databricks-federated-catalog` is registered.
2. **Resource link** (the key detail — a pointer, not a copy):
   ```bash
   aws glue create-database --database-input '{"Name": "databricks_federated_db_link", "TargetDatabase": {"CatalogId": "<account-id>:databricks-federated-catalog", "DatabaseName": "databricks_federated_db"}}'
   ```
3. **Namespace IAM role**: attach Glue metadata reads (`GetDatabase(s)`, `GetTable(s)`, `GetPartitions`, `GetCatalog(s)`) plus `lakeformation:GetDataAccess`. Scope `Resource` down in production. Associate the role under Namespace → Security and encryption → Manage IAM roles.
4. **Lake Formation grants** (Grant-on-Target pattern): `DESCRIBE` on the resource-link database to the namespace role, plus `SELECT, DESCRIBE` on the *target* tables in the federated catalog (granting SELECT only on the link is the common failure).
5. **External schema** (connect as superuser, e.g. Query Editor v2):
   ```sql
   CREATE EXTERNAL SCHEMA databricks_schema FROM DATA CATALOG
   DATABASE 'databricks_federated_db_link' IAM_ROLE '<arn>' REGION '<region>';
   ```
   Convention: federated schemas named `{domain}_iceberg`; analyst views use `WITH NO SCHEMA BINDING` so each execution resolves fresh schema.
6. **Verify**: `SELECT * FROM SVV_EXTERNAL_TABLES WHERE schemaname='databricks_schema';` then `SELECT * FROM databricks_schema.<table> LIMIT 10;`. SAML users connect via the IdP JDBC plugin with `ssl=true`.

## Results and business impact

| Area | Before | After | Impact |
|---|---|---|---|
| Data access | Delta and Redshift siloed | Real-time federated access | ~100 analysts unblocked with zero new pipelines |
| DR | Redshift snapshots every 3h (RPO 3h+) | S3 cross-Region replication, near-continuous RPO; DR workgroup federates to same S3 data | More resilient, less snapshot/copy cost |
| Architecture | Dual processing + manual catalog sync, drift-prone | Processing consolidated in Databricks; Redshift as query engine | Single source of truth, zero sync pipelines |
| Infra cost | Dedicated Redshift ETL cluster + RMS + snapshots | Redshift as query engine only | ~$30K/month redundant ETL cost removed |

Security: unified identity via Azure AD groups mapped on both sides (Redshift SAML + Unity schemas); Lake Formation fine-grained control; least-privilege namespace role; short-lived vended credentials per query; TLS everywhere. Requirements: UniForm on Delta tables; well-partitioned, regularly compacted sources since federated performance reflects write-time layout.

## Takeaways for the seminar

- The resource-link indirection is the whole trick: Redshift can only see the default catalog, so the link is the addressable path to the federated catalog.
- Grant-on-Target (SELECT on federated tables, DESCRIBE on the link) is the permission shape to memorize.
- Federation reframes Redshift Serverless as a stateless query engine over open storage — the $30K/month figure is the cost of refusing that reframing.

## Related concepts

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/delta-lake.md`, `concepts/data-engineering/trino.md`

## References

- [Access Databricks Unity Catalog data using catalog federation](https://aws.amazon.com/blogs/big-data/access-databricks-unity-catalog-data-using-catalog-federation-in-the-aws-glue-data-catalog/)
- [Achieve 2x faster data lake query performance with Apache Iceberg on Amazon Redshift](https://aws.amazon.com/blogs/big-data/achieve-2x-faster-data-lake-query-performance-with-apache-iceberg-on-amazon-redshift/)
- [Catalog federation service limitations](https://docs.aws.amazon.com/lake-formation/latest/dg/catalog-federation.html#catalog-federation-limitations)
