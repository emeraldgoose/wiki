---
title: "Implement least-privilege access with designations in Amazon SageMaker Unified Studio"
description: "When teams move data and AI work to production in a shared environment, one question quickly becomes unavoidable: who can do what? Amazon"
tags: [source, aws-big-data, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published: "2026-10-30"
---

# Implement least-privilege access with designations in Amazon SageMaker Unified Studio

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio)
**Date**: 2026-10-30


## Overview

When teams move data and AI work to production in a shared environment, one question quickly becomes unavoidable: who can do what? Amazon SageMaker Unified Studio now answers it with designations, which are named permission sets that give administrators granular control over the actions each member can perform within a project. Administrators define a designation once, then assign it to project members. A member might sign in through an AWS Identity and Access Management (IAM) role, an IAM user, or an AWS IAM Identity Center user or group. In each case, designations help you give each persona  In this post, we walk through why differentiated permissions matter, how designations work, and how to create and assign your first designation using the console and the AWS Command Line Interface (A

## Key points

- Controlling access to Notebooks: Grant members full access, read-only access, or no access to notebooks within a project, so compute-intensive interactive work is available only to the roles responsible for it. This help
- Separating exploration from production: Grant exploratory users read and explore access while production service accounts run scheduled workflows, all within the same project.
- Supporting governance workflows: Assign specific personas responsibility for data stewardship, subscription approval, and metadata management, which helps prevent other members from bypassing your review process.
- Define once: A domain administrator creates a designation by selecting granular permissions. For example, publish an asset, create data products, or approve subscriptions. Permissions are grouped into categories such as 
- Assign per project: Within a project, the project owner assigns one designation to each member. When a member performs an action through the portal or the API, SageMaker Unified Studio evaluates the assigned designation.
- Owner – Full control over all project resources, including project member management.

## Source outline

- Assign a designation to a project member
- Automate the full lifecycle with the AWS CLI and infrastructure as code (IaC)
- Update designations as your needs evolve

## References

- Original article: [https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio)
