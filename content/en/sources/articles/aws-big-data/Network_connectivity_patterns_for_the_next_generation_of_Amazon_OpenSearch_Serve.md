---
title: "Network connectivity patterns for the next generation of Amazon OpenSearch Serverless"
description: "Nine private-connectivity patterns for next-gen OpenSearch Serverless over standard PrivateLink endpoints, from single VPC to cross-Region."
published: "2026-09-03"
source_url: "https://aws.amazon.com/blogs/big-data/network-connectivity-patterns-for-the-next-generation-of-amazon-opensearch-serverless"
blog: aws-big-data
locale: en
tags: [source, aws-big-data, opensearch, networking, en]
---

# Network connectivity patterns for the next generation of Amazon OpenSearch Serverless

## Overview

Next-generation OpenSearch Serverless replaces bespoke VPC-endpoint-plus-custom-DNS setup with standard PrivateLink interface endpoints (`com.amazonaws.<region>.aoss-data`) with native private DNS. Collections expose resource-based endpoints on the `on.aws` domain — per-collection hostnames plus a per-account Regional endpoint that multiplexes collections via the `x-amz-aoss-collection-name` header. This post catalogs nine connectivity patterns covering single VPC, multi-VPC, on-premises, cross-account, centralized, multi-business-unit, and cross-Region designs.

## Core mechanics

Creating one interface endpoint with private DNS enabled gives a VPC resolution for every `*.aoss.<region>.on.aws` hostname through the VPC resolver; one endpoint serves all collections in the Region, and a second one in the same VPC conflicts. Access control splits cleanly: network policies authorize endpoint IDs (`SourceVPCEs`), data access policies authorize IAM principals, with cross-account reads via a role in the collection account. Per-account Regional endpoints let many collections share one hostname and connection pool.

## The nine patterns

Single-VPC and multi-VPC access each need only an endpoint per VPC plus policy entries. On-premises variants add a Resolver inbound endpoint, conditional forwarders, and Direct Connect/VPN through Transit Gateway or Cloud WAN. Cross-account access puts an endpoint in each consumer VPC and lists the IDs in the owner's network policy — no peering or transit needed. A centralized variant shares one endpoint over Transit Gateway with Route 53 Profiles carrying DNS (the only pattern requiring managed DNS propagation), including an on-premises flavor. Multi-business-unit designs repeat per-spoke endpoints or one shared networking endpoint. Cross-Region has no built-in endpoint or replication: run independent collections per Region and sync via dual-write, OpenSearch Ingestion pipelines, or S3 replication with re-ingestion.

## Cost guidance

Match the design to scale: Resolver inbound endpoints are only needed for on-premises patterns, and Route 53 Profiles only where a VPC lacks its own endpoint. An endpoint per consumer VPC is usually the simplest and cheapest multi-account option since local DNS adds nothing; centralizing on one endpoint can cost more once transit data-processing charges outweigh endpoint savings. Idle secondary-Region collections scale to zero and bill storage only.

## References

- [Original post: Network connectivity patterns for next-gen OpenSearch Serverless](https://aws.amazon.com/blogs/big-data/network-connectivity-patterns-for-the-next-generation-of-amazon-opensearch-serverless)
- [OpenSearch Serverless documentation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
