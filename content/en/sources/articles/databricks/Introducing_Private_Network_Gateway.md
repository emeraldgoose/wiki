---
title: "Introducing Private Network Gateway"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/introducing-private-network-gateway"
blog: databricks
published: 2026-10-17
---

# Introducing Private Network Gateway

**Source**: Databricks Blog, 2026-10-14

**Lead**: Databricks Private Network Gateway (PNG) replaces per-resource private endpoints, load balancers, and proxy VMs with a single managed gateway. Configure one subnet delegation, and serverless workloads gain access to everything your network already reaches—databases, Kafka clusters, internal APIs, on-premises systems—using your existing routes, DNS, and firewall rules.

## The Serverless Networking Challenge

Databricks serverless compute runs in a Databricks-managed network, removing operational overhead but requiring explicit paths to private resources. For cloud-managed services (S3, ADLS), Serverless Private Link works. But for **self-hosted resources** (databases, Kafka, internal APIs), the per-resource approach meant:
- Separate private endpoint + load balancer + proxy VM per resource
- Coordination between Databricks admin, cloud admin, network security team
- Bottleneck when accessing dozens of resources across VNets, peered networks, on-prem

> 75% of customers said network configuration complexity was the main reason workloads stayed on classic compute.

## How PNG Works

**Setup**: Delegate one subnet in your VNet/VPC to Databricks. PNG establishes a managed, encrypted gateway from serverless into that subnet. Configure inside a Network Connectivity Configuration (NCC)—the same account-level object used for serverless networking.

**No gateway VMs to deploy, patch, or scale**—Databricks runs it. You keep network control.

### You Keep Control of the Network Boundary

- **Dedicated gateway**: Your path, not shared with other customers; isolation via encapsulation and security rules
- **Workspace-level access controls** enforced before traffic leaves the gateway
- **Your route tables, NSGs, DNS, security appliances** decide what's reachable beyond the subnet—same as rest of your network

### Two Traffic Modes

1. **`specific_destinations`**: Only listed FQDNs route through PNG; other traffic keeps normal path. For precise control.
2. **`all_traffic`**: All outbound routes through your network (except more-specific Private Link paths). For firewall inspection or consistent source IP.

PNG is additive—sits alongside existing private connectivity/egress controls, can enable/remove without affecting existing setup.

## Use Cases Enabled

- **Lakeflow Connect on serverless**: Ingest from private databases across VNet/VPC and on-prem
- **AI agents to private services**: Call private MCP servers you host
- **Private package repos**: Install from private PyPI, Artifactory, Nexus inside your network
- **Egress through your firewall**: Filter/log with your own tools
- **Consistent customer-owned source IP**: SaaS apps see your IP

## Availability

- **Public Preview on Azure** — [Azure docs](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/private-network-gateway)
- **Private Preview on AWS** — Contact Databricks account team
- **Google Cloud** — In development

## Relevance to Software Engineers

For teams adopting **serverless compute but blocked by networking**: PNG eliminates the per-resource networking tax. One subnet delegation replaces dozens of coordinated deployments. Your existing network policies (routes, DNS, firewall) become the single source of truth for serverless access—no duplicate rule sets to maintain.

## References

- Original article: [https://www.databricks.com/blog/introducing-private-network-gateway](https://www.databricks.com/blog/introducing-private-network-gateway)
- What's new in Databricks Platform security: [Data+AI Summit 2026](https://www.databricks.com/blog/whats-new-databricks-platform-security-and-compliance-data-ai-summit-2026)