---
title: Configure Custom Domain Name for Amazon MSK
description: Custom advertised listener hostnames for Amazon MSK Provisioned clusters (ZooKeeper and KRaft) via NLB, DNS, and ACM — two-phase rollout without client reconfiguration.
date: 2026-08-25
tags: [aws, kafka, msk, networking, dns]
locale: en
blog: aws
---

# Configure Custom Domain Name for Amazon MSK

**Published**: Aug 25, 2026 · **Source**: AWS Big Data Blog (original URL no longer listed; split from the legacy aggregate `sources/articles/aws-bigdata.md`)

> Note: no source URL is available for this entry — it predates the current blogwatcher feed. The summary below is preserved from the aggregate file. URLs are never fabricated.

## Problem

Amazon MSK advertises broker endpoints with AWS-generated hostnames. Enterprises that put Kafka behind corporate DNS conventions, private certificate authorities, or firewall allow-lists need **custom domain names** on the advertised listeners, so clients connect to `kafka.corp.example.com` instead of opaque broker hostnames — without reconfiguring every producer and consumer on rotation.

## Solution path

- **NLB + DNS + ACM certificate**: place a Network Load Balancer in front of the brokers, map custom DNS records to it, and terminate TLS with an AWS Certificate Manager certificate for the custom domain.
- **Advertised listener change**: set the per-broker custom advertised listener configuration (the modern equivalent of the legacy `custom.advertised.listeners` CLI override) so brokers tell clients to reconnect via the custom hostname.
- **Two-phase rollout**: (1) establish the networking path (NLB, DNS, certificate) first; (2) flip the advertised listener so cutover is automatic for clients.
- **Same behavior on ZooKeeper and KRaft**: the mechanism works identically on both metadata modes.
- **Scaling and failover safe**: automatic broker scaling and broker replacement re-apply the configuration, so the custom name survives topology changes.
- **Availability**: supported on all MSK Provisioned clusters (Standard and Express brokers).

## Takeaways for the seminar

- Rolling networking first and config second makes the cutover hitless — clients never need simultaneous reconfiguration.
- Custom advertised listeners are a prerequisite pattern for corporate Kafka adoption (mTLS identity, DNS policy, audit), and they compose with the in-place ZooKeeper-to-KRaft upgrade path rather than conflicting with it.

## Related concepts

- `concepts/data-engineering/stream-processing.md`, `concepts/infrastructure/kubernetes.md`
