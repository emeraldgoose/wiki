---
title: "Implement least-privilege access with designations in Amazon SageMaker Unified Studio"
description: "Designations are reusable named permission sets in Amazon SageMaker Unified Studio that let admins grant each persona only the access its responsibilities require, complementing IAM controls within a single project."
tags: [source, aws-big-data, data-governance, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-10-30
---

# Implement least-privilege access with designations in Amazon SageMaker Unified Studio

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio) · **Published**: 2026-10-30

## Overview
When data and AI workloads move from experimentation to production in a shared environment, the question of who can do what quickly becomes unavoidable. Amazon SageMaker Unified Studio answers it with designations: named permission sets that give administrators granular control over the actions each member can perform inside a project. A designation is defined once and assigned to project members regardless of whether they sign in through an AWS IAM role, an IAM user, or an AWS IAM Identity Center user or group. The pragmatic outcome is least-privilege access per persona while the underlying data stays unified in a single project rather than being fragmented across duplicates. Designations integrate with AWS CloudFormation and incur no additional charge beyond the SageMaker Unified Studio usage they run on. Effective access still depends on identity and resource policies, service control policies, permission boundaries and group memberships, so designations are intended to complement existing IAM controls rather than replace them.

## Key points
- A domain administrator defines a designation by selecting granular permissions grouped into Catalog, Project, Subscriptions, Connections and Notebooks categories, backed by the Cedar policy language.
- Within a project, the project owner assigns one designation per member; when a member acts through the portal or API, SageMaker Unified Studio evaluates the assigned designation before permitting the action.
- Members may inherit designations through SSO group membership; where direct assignment and group inheritance overlap, the union of both permission sets applies, so SSO group assignments must be reviewed regularly to avoid excess access.
- Authorization runs in two layers: IAM decides whether the principal may invoke the API at the AWS boundary, then the designation decides whether the assigned permission set grants the specific action within the project, and an IAM Deny blocks the call regardless of what the designation permits.
- Every domain ships with two managed designations, Owner (full control including member management) and Contributor (full access except member management and project deletion), so teams can begin immediately.
- Because a designation is defined once and assigned per project, permissions stay consistent across every project without recreating policies, which suits scenarios such as scoping notebook access, separating exploration from production pipelines and supporting governance workflows like data steward subscription approval.

## Details
A single SageMaker Unified Studio project often brings together data engineers, data stewards, analysts and machine learning engineers with very different access needs. In a financial services example, engineers build and schedule ETL pipelines while a steward approves subscription requests, analysts query curated tables for dashboards and ML engineers iterate on models in notebooks. Before designations, teams commonly either granted everyone the same broad project role or split the work across separate projects; both workarounds either risk accidents such as deleting a connection that disrupts a production workload, or fragment data across project boundaries while adding provisioning and member-management overhead.

Designations separate policy definition from member assignment, so the policy can be reused wherever it is needed. Adoption does not require rewriting legacy IAM policies because authorization happens in two layers. For example, the AmazonSageMakerDomainExecution role might hold the IAM permission datazone:CreateListingChangeSet to publish a data asset, but publication succeeds only when the member's designation also includes the Manage Asset Publishing permission, and an IAM Deny blocks publish unconditionally. IAM continues to scope principals at the AWS API boundary while designations add a consistent authorization layer across every principal type the studio supports, including SSO users and groups that cannot receive IAM policies directly inside it. SwissLife Germany summarizes the operational value of consistent personas from day one, and the guidance concludes that teams should keep IAM at least-privilege even as designations simplify in-project control.

## References
- Original article: [Implement least-privilege access with designations in Amazon SageMaker Unified Studio](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio)
