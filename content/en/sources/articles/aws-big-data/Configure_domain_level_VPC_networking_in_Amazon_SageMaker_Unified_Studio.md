---
title: "Configure domain-level VPC networking in Amazon SageMaker Unified Studio"
description: "Set one VPC for a SageMaker Unified Studio domain so every new project inherits private subnets, endpoints, and security posture."
tags: [source, article, en, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/configure-domain-level-vpc-networking-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-09-23
---

# Configure domain-level VPC networking in Amazon SageMaker Unified Studio

## Overview

Operations teams supporting dozens of Unified Studio projects otherwise coordinate private connectivity per project — inconsistent subnets, missing endpoints, hard-to-debug failures, and an unauditable posture. Domain-level VPC networking configures the network once (for IAM-based domains), and every new project inherits the VPC settings automatically. This guide covers setup, subnet and security-group selection, migrating existing projects, and validating connectivity from inside a project.

## Prerequisites

You need domain administrator permissions and a same-Region VPC with at least two private subnets in different AZs, DNS hostnames/support enabled, and roughly five free IPs per expected project as a baseline (Glue, EMR, and Redshift Serverless consume more ENIs — prefer /24 or larger for production). Because subnets are private, add VPC endpoints for every service projects touch: the S3 gateway endpoint with route-table associations plus interface endpoints for Glue, SageMaker API/runtime, CloudWatch Logs/monitoring, STS, DataZone, ECR API/DKR, and KMS, all with private DNS enabled. The admin role needs EC2 describe/create plus DataZone permissions; a security group is optional since the studio creates one if omitted. Watch interface-endpoint hourly costs and the per-VPC endpoint and ENI quotas.

## Walkthrough

1. **Navigate:** sign in as the domain login role, open the SageMaker console, launch the IAM-based domain, and go to Domain management.
2. **Add the VPC:** under Settings > Networking in this account, choose Add VPC, pick the VPC, at least two private subnets, and optionally a security group, then save and confirm Ready status. IAM-based domains allow one VPC configuration; new projects now inherit it.
3. **Update existing projects:** projects with no VPC show an update banner and adopt the domain VPC in place. Projects that already have a VPC cannot switch — create a new project, recreate connections, migrate assets, back up data, and delete the old one during a maintenance window.
4. **Validate:** from a project notebook, test S3, Glue, and STS reachability via Boto3 and confirm interface endpoints resolve to private IPs. Note that `AccessDenied` means connectivity works but IAM needs fixing, while timeouts point at missing endpoints, routes, or security-group rules (allow outbound 443; add self-referencing inbound rules for distributed compute).

## Updating and removing the configuration

To change the VPC, subnets, or security group later, use Actions > Update under the same Settings section — but only newly created resources pick it up; existing VPC-backed projects must be recreated, while VPC-less projects update in place. Removing the configuration (Actions > Remove) leaves already-provisioned projects untouched, and new projects get no VPC. As next steps, tighten the auto-created security group toward least privilege, add endpoints as needs evolve, and alarm on subnet `AvailableIpAddressCount` for capacity planning.

## References

- Original post: [Configure domain-level VPC networking in Amazon SageMaker Unified Studio](https://aws.amazon.com/blogs/big-data/configure-domain-level-vpc-networking-in-amazon-sagemaker-unified-studio)
