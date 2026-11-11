---
title: "Build a multi-team AI and analytics environment on Amazon SageMaker Unified Studio with Terraform"
description: "A Terraform module for building a governed, multi-team data and AI environment on Amazon SageMaker Unified Studio with per-team project profiles, shared domain, and centralized access control."
tags: [source, aws-big-data, terraform, sage-maker, unified-studio, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform"
blog: aws-big-data
published_date: 2026-11-12
---

# Build a multi-team AI and analytics environment on Amazon SageMaker Unified Studio with Terraform

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform) · **Published**: 2026-11-11

## Overview

Platform engineers who support data and AI teams face a recurring challenge: analytics, machine learning (ML), and AI developer teams each need different tools. When each team operates its own tools and infrastructure, governance becomes fragmented. Organizations face duplicated effort and limited collaboration. Data engineers, data scientists, and AI developers might all work with the same underlying data, yet they navigate separate consoles, manage distinct AWS Identity and Access Management (IAM) configurations, and lack a shared view of each other’s work. Amazon SageMaker Unified Studio brings these capabilities together in one governed workspace. Every practitioner gets access to the tools they need: SQL editors, JupyterLab notebooks, and the Amazon Bedrock IDE. At the same time, they share a common business data catalog, security model, and project structure, all governed centrally within Amazon SageMaker Unified Studio.

Teams collaborate within projects while access to data, compute, and development artifacts is managed centrally. A shared domain holds three purpose-built project profiles — one per team — plus an initial project to get started. The Amazon SageMaker Unified Studio Terraform module codifies the entire setup so the environment stays repeatable and consistent. Consider a mid-size technology company whose analytics team runs a standalone Amazon Redshift cluster, whose ML team provisions SageMaker notebooks ad hoc, and whose generative AI team experiments with Bedrock through the console: today they have no shared data catalog, no consistent access control, and no central visibility into what is running or its cost.

## Key points

- Dual provider: Uses both the AWS provider and AWS Cloud Control (AWSCC) provider for full Amazon SageMaker Unified Studio resource coverage.
- Service role flexibility: All IAM roles are auto-created with least-privilege policies, or existing roles can be supplied for use by Amazon SageMaker Unified Studio.
- Domain- and project-level access using IAM, single sign-on (SSO) with AWS IAM Identity Center, or both.
- KMS encryption: Optionally encrypt domain metadata with a customer-managed AWS Key Management Service (AWS KMS) key using kms_key_identifier.
- Model governance: The domain module automatically provisions a model governance project for Generative AI administrators, who can enable or disable specific models accessible in the domain.
- Terraform creates the Amazon SageMaker Unified Studio domain with shared IAM roles and networking, enables all required blueprints on the domain (DataLake, Redshift Serverless, Bedrock services, EMR, and more), composes three project profiles, creates a project from the first available profile, and assigns project members as owners or contributors.
- The module follows a layered architecture: domain module, blueprint module, project-profile module, and project/project-membership module.
- After deployment, each team can query data across Amazon S3 and Redshift via SageMaker Lakehouse, manage a shared data catalog with AWS Glue, create and share SQL notebooks and dashboards, run ML experiments with MLflow integration, process data at scale with Amazon EMR Serverless, access Bedrock capabilities, build chat agents and knowledge bases, and evaluate model performance with Bedrock Evaluation.

## Details

Prerequisites include an AWS account with permissions to create and manage Amazon DataZone, IAM, Amazon S3, Amazon EC2, and Amazon VPC resources; AWS CLI configured for the target account and Region; Amazon SageMaker Unified Studio available in the target Region; AWS IAM Identity Center configured (required only for SSO-based project membership); and Terraform variables configured for each team.

Clone the `terraform-aws-sagemaker-unified-studio` module from `https://github.com/aws-ia/terraform-aws-sagemaker-unified-studio`, navigate to the quick-setup example, copy `terraform.tfvars.example` to `terraform.tfvars`, and enable the three project profiles (enable_sql_analytics, enable_generative_ai, enable_all_capabilities). Set the domain name, region, environment, project names, and SSO users/groups. If Identity Center is not used, set `enable_sso = false` and use `iam_users` and `iam_roles` instead.

Run `terraform init` then `terraform apply`. Terraform creates one domain with shared governance, IAM roles, networking, and an S3 tooling bucket; enables all selected blueprints on the domain; creates three project profiles (SQL Analytics, Generative AI, All Capabilities); creates a project from the first profile; and configures project memberships for SSO identities, IAM principals, or both. Verify by opening the domain_url output, confirming the project profiles appear under the domain, and confirming project members can access the project interface. Create additional team projects by adding more project sub-module blocks referencing different profiles.

Team isolation is achieved by assigning users or groups to projects created from the appropriate project profile; each principal type can be used independently or in combination. Identity Center users and groups cover most human access patterns, while IAM roles unlock additional use cases. This is a one-way door decision: changing SSO settings later requires destroying and recreating the domain and all dependent resources.

## References

- Original article: [Build a multi-team AI and analytics environment on Amazon SageMaker Unified Studio with Terraform](https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform)