---
title: "Announcing Spark Connect on Amazon EMR on EKS: Interactive PySpark development, anywhere"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-eks"
blog: aws-big-data
published_date: 2026-09-29
published: 2026-10-17
---

# Announcing Spark Connect on Amazon EMR on EKS: Interactive PySpark development, anywhere

## Overview

Spark Connect is now supported on Amazon EMR on EKS, starting from EMR 7.14 (Spark 3.5.8) and emr-spark-8.1 (Spark 4.1.1). You build, test, and debug Spark from VS Code, PyCharm, Jupyter, or SageMaker Unified Studio while full-scale operations run on EKS. The client-server split removes environment drift between laptop and cluster: you develop locally, and operations route to scalable Spark server pods. The same code validated interactively deploys unchanged as a batch `StartJobRun`.

## How it works

The architecture has four parts: a lightweight PySpark client (no Spark install needed), a secure gRPC/TLS channel to an EMR-managed endpoint, server pods in your EMR-on-EKS namespace (minimum two executors, autoscaling), and Arrow-encoded result batches streamed back. On endpoint creation, EMR launches the server and returns an ELB-backed endpoint plus a short-lived token — no manual server or networking setup. The server inherits your node types, container images, and Spark configs.

First use on a cluster also provisions two shared components: a managed Envoy authentication-proxy router (three replicas by default, NLB-fronted, handling TLS termination and token validation) and a Secret Agent pod managing short-lived session credentials. Both are created automatically, shared across endpoints, and persist after individual endpoints are deleted so new ones start within a minute.

## Why use it

- **Interactive development on shared clusters:** iterate cell-by-cell in notebooks or IDEs against the same engine as batch jobs, reusing EKS RBAC, network policies, autoscaling, and observability (Prometheus, Grafana, CloudWatch Container Insights).
- **Embedded Spark:** the compact client embeds into web services, dashboards, scripts, or backend APIs; heavy work stays on EKS.
- **Governed multi-tenancy:** each session carries its own IAM execution role and cost tags; virtual clusters give namespace isolation, and Kubernetes quotas plus EKS split-cost allocation enable chargeback.
- **Reusable images and scheduling:** custom container images work for both batch and interactive sessions; pod templates, dynamic allocation, Spot, and GPU pools tune placement and cost.
- **Multi-cluster and hybrid reach:** the client only needs endpoint reachability, simplifying cross-account, cross-Region, or on-premises Kubernetes analytics without data duplication.

## Getting started

Six steps: create EMR namespaces on EKS, create a security configuration, create a session-enabled virtual cluster, create a SPARK_CONNECT managed endpoint, obtain a session token, and connect with a remote `SparkSession`.

- **Prerequisites:** EKS cluster with AWS Load Balancer Controller, AWS CLI 2.x and recent boto3, matching `pyspark[connect]` client, and a job execution IAM role.
- **Security note:** tokens are short-lived (15 minutes default, up to 12 hours); refresh via `get-managed-endpoint-session-credentials` for long sessions.
- **Session behavior:** endpoints survive client disconnects for a configurable idle timeout (default 60 minutes), preserving cached data and temp views; reconnect with a fresh token to resume.
- **Validation:** check endpoint status via the EMR Containers API, inspect driver/executor pods with `kubectl`, and port-forward the driver for the live Spark UI.
- **Cleanup:** delete the endpoint, virtual cluster, security configuration, and namespaces; shared router and Secret Agent are removed once the last session-enabled virtual cluster goes away.

Available in all EMR-on-EKS Regions except GovCloud and China, at no extra charge beyond underlying EKS resources. For cost efficiency, use Karpenter/Cluster Autoscaler, On-Demand for persistent session pods, Graviton, cost-allocation tags, and a single shared router.

## References

- Original post: [Announcing Spark Connect on Amazon EMR on EKS: Interactive PySpark development, anywhere](https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-eks)
