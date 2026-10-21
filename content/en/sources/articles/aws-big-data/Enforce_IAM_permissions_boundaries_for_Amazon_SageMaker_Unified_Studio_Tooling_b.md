---
title: "Enforce IAM permissions boundaries for Amazon SageMaker Unified Studio Tooling blueprints"
description: "Attach a custom permissions boundary to Tooling blueprint roles so SCP-governed accounts can adopt SageMaker Unified Studio."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/enforce-iam-permissions-boundaries-for-amazon-sagemaker-unified-studio-tooling-blueprints"
blog: aws-big-data
published_date: 2026-09-28
---

# Enforce IAM permissions boundaries for Amazon SageMaker Unified Studio Tooling blueprints

## Overview

SageMaker Unified Studio now supports custom permissions boundaries on IAM roles created by the Tooling blueprint — the one mandatory blueprint deployed with every project. Regulated organizations whose SCPs require a boundary on every role previously saw project creation fail with an explicit `iam:CreateRole` deny. Setting one `PermissionsBoundaryArn` parameter fixes adoption without weakening the security posture, and additionally gives admins granular control (for example, disabling Data Agent and notebook capabilities while keeping SQL access).

## How it works

The boundary is configured in the Tooling blueprint's regional parameters. Every new project under that blueprint then provisions a CloudFormation stack creating three IAM roles — `datazone_usr_role` (assumed by all project members), `AmazonBedrockServiceRole`, and `AmazonBedrockLambdaExecutionRole` — each carrying the boundary. It applies uniformly to all three roles and to all future projects; existing projects keep their original boundary. An illustrative boundary in the post allows the service namespaces the studio uses while explicitly denying DataZone notebook/cell/conversation and agent messaging actions, acting as an unoverridable ceiling. Treat it as illustration only: validate in a non-production domain, since the boundary must remain a superset of everything the three roles need.

## Configuring the boundary

- **Optional SCP:** in the Organizations management account, create an SCP denying `CreateRole`/`PutRolePermissionsBoundary` without the approved boundary ARN, denying boundary removal, and protecting the boundary policy itself — with a break-glass exception so admins are not locked out. Attach it to the target OU or account.
- **Create the boundary policy** (`SMUSToolingBoundary`) with `create-policy` and note its ARN.
- **Locate IDs:** resolve the domain ID and the managed Tooling blueprint ID via the DataZone list APIs.
- **Read and back up** the current blueprint configuration — `put-environment-blueprint-configuration` overwrites everything, so you must resupply all existing values and add only `PermissionsBoundaryArn` in the regional parameters.
- **Verify** the ARN reads back from the configuration.

## Validating and operating

Create a test project from an enabled project profile and wait for Active status; then list the Tooling stack's IAM roles via CloudFormation and confirm each shows the boundary with `get-role` (also visible in the IAM console). With the illustrative deny-policy, creating a notebook fails on `datazone:CreateNotebook` and the Query Editor agent panel reports no Data Agent access — denied by the boundary. Remember: boundaries are immutable after project creation, the feature covers only the Tooling blueprint (extend via custom blueprints for others), and the policy must exist before provisioning. To roll back test resources, delete the project and re-run the put-configuration without the boundary field using the backed-up values.

## References

- Original post: [Enforce IAM permissions boundaries for Amazon SageMaker Unified Studio Tooling blueprints](https://aws.amazon.com/blogs/big-data/enforce-iam-permissions-boundaries-for-amazon-sagemaker-unified-studio-tooling-blueprints)
