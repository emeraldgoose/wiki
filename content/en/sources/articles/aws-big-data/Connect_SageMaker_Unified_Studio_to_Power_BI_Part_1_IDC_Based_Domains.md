---
title: "Connect SageMaker Unified Studio to Power BI Part 1 - IDC-Based Domains"
description: "Direct Power BI to SageMaker Unified Studio via Athena ODBC 2.2 native auth: SageMakerBrowserIdc and SageMakerIam, DSN and DSN-less methods, gateway wiring, IDC-domain walkthrough."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/"
blog: "AWS Big Data"
locale: "en"
tags: [aws, sagemaker, athena, power-bi, odbc, iam-identity-center, bi]
---

# Connect SageMaker Unified Studio to Power BI Part 1 - IDC-Based Domains



**Authors**: Ramesh H Singh, Krishna Atluru, Armando Segnini, Saushthav Saxena, Gaurav Sharma · **Published**: 2026-09-15 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/)

## Problem

Power BI analysts needing governed SageMaker Unified Studio data previously required third-party ODBC-JDBC bridges — extra components, licensing, and maintenance. UC Irvine's spotlight quote captures it: governed AWS data needed workarounds. Athena ODBC driver 2.2.0+ now authenticates to Unified Studio natively, and this post (Part 1 of 2) wires it for IAM Identity Center (IDC)-based domains.

## Solution overview

Two new Athena ODBC auth modes: **SageMakerBrowserIdc** (browser SSO via Identity Center + external IdP, no local creds) and **SageMakerIam** (default credential chain; here Identity Center-issued creds). Two connection methods:

| | Method 1: DSN-based (Athena connector) | Method 2: DSN-less (ODBC connector) |
|---|---|---|
| Connector | Amazon Athena | ODBC, connection string, no DSN |
| Modes | DirectQuery + Import | Import only (no DirectQuery via ODBC connector) |
| Auth | SageMakerBrowserIdc + SageMakerIam | SageMakerIam only |
| Domains | IAM + IDC | IAM + IDC |
| Best for | Live dashboards | No-DSN or scheduled-refresh scenarios |

Demo scenario: energy analyst querying the PUDL EIA-860 generators dataset through Athena/SageMaker, building a stacked bar of `capacity_mw` by `technology_description` stacked on `operational_status`. Flow: Power BI Desktop → publish → Power BI Service → on-premises data gateway on EC2 (instance IAM role) → Athena → Glue Catalog/S3 under SageMaker project governance. Desktop may run on-prem or on EC2; the gateway always uses SageMakerIam (Windows service, no browser) and must be a project member.

## Implementation (IDC domains)

**Prerequisites**: Athena ODBC ≥2.2.0 (Win64), Power BI Desktop latest, Pro license, gateway on EC2, Unified Studio IDC domain + project with data (EIA-860 preview shown in post).

**Method 1 — DSN (`pbi-idcdomain`)**: add SSO user as project member. Project → ⋯ → Project details → JDBC and ODBC details: copy IDC issuer URL, domain ID (`dzd-…`), project ID, workgroup, Region. System DSN: Region, Catalog `AwsDataCatalog`, Database `default`, workgroup; auth `SageMakerBrowserIdc` + SSO start URL/region + domain/project IDs + domain region. Test (browser Allow Access). Power BI: Get Data → Amazon Athena → DSN → DirectQuery → Use Data Source Configuration → AwsDataCatalog → `core_eia860__scd_generators` → Load → stacked bar → Publish (`generation-idcdomain`).

**Method 2 — DSN-less**: admin creates `SageMakerDataAnalyst` permission set (`datazone:GetConnection/ListConnections/GetDomain/GetProject`, `sts:GetCallerIdentity` on `*` — metadata-only, data still gated by project membership), assigns users, `aws configure sso` + `aws sso login`. Add the SSO role (`AWSReservedSSO_SageMakerDataAnalyst_…`) as domain IAM user + project member. Copy the **Using IAM auth** ODBC connection string from Project Overview, e.g. `Driver={Amazon Athena ODBC (x64)};AwsRegion=…;Catalog=AwsDataCatalog;Schema=default;Workgroup=…;SageMakerDomainId=…;SageMakerProjectId=…;SageMakerDomainRegion=…;AuthenticationType=SageMakerIam;`. Power BI: Get Data → ODBC → (None) → Advanced → paste string → Default or Custom → Load → publish (`generation-idcdomain-dsnless`).

**Gateway + Service**: create `pbi-gateway-role` (EC2 trust, same inline policy), attach to gateway EC2, add as domain user + project member. Method 1: matching **System** DSN on gateway with `SageMakerIam` and identical DSN name. Method 2: nothing on the box; configure in Service. Service: workspace → semantic model ⋯ → Settings → Gateway and Cloud Connections → add connection (DSN name or exact-match connection string) → Auth **Anonymous** → Maps to → Apply → open report (live in the post's Figure 14).

## Why it matters

- **No bridge tax**: native driver auth removes third-party licensing and upkeep.
- **Governance preserved**: project membership remains the data gate; `Resource: *` in the policy is metadata-scoped, not data access.
- **Choice of freshness**: DirectQuery for live versus Import for scheduled, with a clear auth/method matrix.

## Takeaways for the seminar

- Gateway rule of thumb: System DSN (not User), `SageMakerIam` always, names/strings must match Desktop exactly.
- Browser auth never crosses the gateway boundary — that's why Method 2 and the gateway converge on `SageMakerIam`.
- Part 2 covers IAM-based domains; the decision tree here (DSN vs DSN-less, IDC vs IAM) transfers directly.

## Related concepts

- `concepts/data-engineering/trino.md`, `concepts/data-engineering/data-modeling.md`

## References

- [Part 2 - IAM-based domains](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/)
- [Power up your analytics with Unified Studio integration](https://aws.amazon.com/blogs/big-data/power-up-your-analytics-with-amazon-sagemaker-unified-studio-integration-with-tableau-power-bi-and-more/)
- [Athena ODBC v2 driver docs](https://docs.aws.amazon.com/athena/latest/ug/odbc-v2-driver.html)
- [How ENGIE automates Athena data sources on Power BI](https://aws.amazon.com/blogs/big-data/how-engie-automates-the-deployment-of-amazon-athena-data-sources-on-microsoft-power-bi/)
