---
title: "Connect SageMaker Unified Studio to Power BI Part 2 - IAM-Based Domains"
description: "Direct Power BI to SageMaker Unified Studio for IAM-based domains via Athena ODBC SageMakerIam auth: SSO permission set, DSN and DSN-less wiring, gateway IAM role."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/"
blog: "AWS Big Data"
locale: "en"
tags: [aws, sagemaker, athena, power-bi, odbc, iam, iam-identity-center, bi]
---

# Connect SageMaker Unified Studio to Power BI Part 2 - IAM-Based Domains



**Authors**: Ramesh H Singh, Krishna Atluru, Armando Segnini, Saushthav Saxena, Gaurav Sharma · **Published**: 2026-09-15 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/)

## Problem

Part 1 of this series wired Power BI to SageMaker Unified Studio for IAM Identity Center (IDC)-based domains, where the Athena ODBC driver 2.2.0+ can authenticate through the browser (`SageMakerBrowserIdc`). IAM-based domains have no IDC browser flow: the driver must obtain AWS credentials some other way. UC Irvine's spotlight quote frames the stakes — analysts live in Power BI, governed data lives in Unified Studio projects, and the old path required third-party ODBC-JDBC bridge software with extra licensing. This post (Part 2 of 2) builds the same direct Power BI connection for IAM-based domains using `SageMakerIam` authentication sourced from the default credential provider chain.

## Solution overview

Architecture is identical to Part 1: Power BI Desktop → Athena ODBC → SageMaker Unified Studio project (governance boundary) → Athena/Glue Catalog/S3; an on-premises data gateway on EC2 bridges to Power BI Service for report viewers. What changes is authentication and setup:

| | Part 1 (IDC domains) | Part 2 (IAM domains, this post) |
|---|---|---|
| Auth modes | `SageMakerBrowserIdc` + `SageMakerIam` | `SageMakerIam` only |
| Credential source | Browser SSO via Identity Center | Default credential chain (here: IAM Identity Center permission set via `aws configure sso`) |
| Extra admin setup | None beyond project membership | Permission set + SSO profile + project membership for the SSO role |
| Gateway auth | `SageMakerIam` (EC2 instance role) | `SageMakerIam` (EC2 instance role) — same |

Both connection methods are covered: **Method 1 (DSN-based)** via the Athena connector (DirectQuery + Import) and **Method 2 (DSN-less)** via the ODBC connector with a connection string (Import only). Because the gateway runs as a Windows service with no browser, both methods converge on `SageMakerIam` at the gateway.

Demo dataset is the same PUDL EIA-860 generators table (`core_eia860__scd_generators`): a stacked bar of `capacity_mw` by `technology_description` stacked on `operational_status`.

## Implementation

**Prerequisites** (Part 1's plus): latest AWS CLI on the Windows machine; a SageMaker Unified Studio IAM-based domain with Identity Center SSO enabled.

**Administrator setup — credential plumbing via Identity Center:**

1. **Permission set** `SageMakerDataAnalyst` in IAM Identity Center with a metadata-only inline policy (`datazone:GetConnection/ListConnections/GetDomain/GetProject`, `sts:GetCallerIdentity` on `Resource: "*"` — required because these actions are not resource-scoped). This grants no data access; project membership remains the data gate. The project IAM role supplies Athena/S3 permissions separately.
2. **Assign** SSO users/groups to the target account with that permission set.
3. **SSO profile** on the machine: `aws configure sso` (session name e.g. `smus`, start URL, region, `sso:account:access` scope), producing a `~/.aws/config` with the `sso_session` block. Day-to-day refresh is just `aws sso login`; verify with `aws sts get-caller-identity`.
4. **Project membership**: add the IAM identity that feeds the driver (e.g. `AWSReservedSSO_SageMakerDataAnalyst_…`) as a member of the Unified Studio project. Gather the domain ID, project ID, Region, and Athena workgroup from Project → ⋯ → Project details → JDBC and ODBC details.

**Method 1 — DSN (`pbi-iamdomain`)**: System DSN with the Athena ODBC driver — Region, Catalog `AwsDataCatalog`, Database `default`, workgroup; auth `SageMakerDomainId` (`dzd-…`), `SageMakerProjectId`, `SageMaker Region`, type `SageMakerIam`. Test (browser Allow Access). Power BI: Get Data → Amazon Athena → DSN → DirectQuery → Use Data Source Configuration → `AwsDataCatalog` → generators table → Load → publish as `generation-iamdomain`.

**Method 2 — DSN-less**: copy the **Using IAM auth** ODBC connection string from the project overview, e.g. `Driver={Amazon Athena ODBC (x64)};AwsRegion=…;Catalog=AwsDataCatalog;Schema=default;Workgroup=…;SageMakerDomainId=…;SageMakerProjectId=…;SageMakerDomainRegion=…;AuthenticationType=SageMakerIam;`. Power BI: Get Data → ODBC → (None) → Advanced → paste → Default or Custom → Load → publish as `generation-iamdomain-dsnless`. If the machine already has credentials elsewhere in the default chain, the whole admin SSO setup can be skipped.

**Gateway + Service**: create `pbi-gateway-role` (EC2 trust, same inline policy), attach to the gateway EC2, add as domain user + project member. Method 1: replicate the **System** DSN on the gateway box with the identical DSN name. Method 2: nothing on the box; configure in Service. Service: workspace → semantic model ⋯ → Settings → Gateway and Cloud Connections → add connection (matching DSN name or exact connection string) → Auth **Anonymous** → Maps to → Apply → open the report.

## Why it matters

- **No bridge tax on IAM domains either**: native `SageMakerIam` auth removes third-party licensing for the domain type most enterprises already run.
- **Governance preserved**: the `Resource: "*"` policy looks broad but is metadata-scoped; actual reads are gated by project membership plus Lake Formation, with short-lived credentials per session.
- **Automatable**: the post points to ENGIE's automation of Athena data sources on Power BI and to a self-service blueprint (`ProjectMembership` resource) so project owners auto-add the gateway role at creation instead of manual member adds.

## Takeaways for the seminar

- IAM domains collapse the Part 1 auth matrix to a single mode: `SageMakerIam` everywhere, Desktop and gateway alike.
- Credential source is composable — Identity Center SSO profile today, EC2 instance role on the gateway, any default-chain source tomorrow; the ODBC parameters don't change.
- Gateway rules carry over unchanged: System DSN (not User), names/strings must match Desktop exactly, Anonymous auth in Service.

## Related concepts

- `concepts/data-engineering/trino.md`, `concepts/data-engineering/data-modeling.md`

## References

- [Part 1 - IDC-based domains](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/)
- [Power up your analytics with Unified Studio integration](https://aws.amazon.com/blogs/big-data/power-up-your-analytics-with-amazon-sagemaker-unified-studio-integration-with-tableau-power-bi-and-more/)
- [Athena ODBC v2 driver docs](https://docs.aws.amazon.com/athena/latest/ug/odbc-v2-driver.html)
- [How ENGIE automates Athena data sources on Power BI](https://aws.amazon.com/blogs/big-data/how-engie-automates-the-deployment-of-amazon-athena-data-sources-on-microsoft-power-bi/)
