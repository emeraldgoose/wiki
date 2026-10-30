---
title: "Enable cross-Region fine-grained data access with AWS Lake Formation and Trusted Identity Propagation"
description: "Fine-grained, auditable cross-Region data access using AWS Lake Formation and TIP."
tags: [source, aws-big-data, lake-formation, identity-propagation, data-engineering, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation"
blog: aws-big-data
published_date: 2026-10-23
---

# Enable cross-Region fine-grained data access with AWS Lake Formation and Trusted Identity Propagation

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation) · **Published**: 2026-10-23

## Overview

Organizations storing analytics data on AWS often need two things at once: fine-grained access control limiting each person to authorized data, and user-level auditability so every query traces to the actual person rather than a shared IAM role. AWS IAM Identity Center Trusted Identity Propagation (TIP) meets both. A user signs in once, and that identity propagates from client through query engine, Lake Formation, and storage layer, authorizing every request as the actual user and logging queries in CloudTrail.

## Key points

- Identity propagates end to end, enabling fine-grained authorization and user-level auditing.
- Setup spans producer and consumer accounts, IAM Identity Center replication, and permissions across AWS services.
- Lake Formation data catalog settings must clear "Use only IAM access control."
- Trusted identity propagation use cases must be integrated in both accounts across Regions.

## Details

Cross-Region fine-grained access requires consistent identity propagation and catalog configuration, with prerequisites in both producer and consumer environments.

## References

- Original article: [https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation](https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation)
