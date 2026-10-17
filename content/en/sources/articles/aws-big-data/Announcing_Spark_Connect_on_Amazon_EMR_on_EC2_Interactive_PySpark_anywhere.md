---
title: "Announcing Spark Connect on Amazon EMR on EC2: Interactive PySpark anywhere"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-ec2-interactive-pyspark-anywhere"
blog: aws-big-data
published_date: 2026-09-23
published: 2026-10-17
---

# Announcing Spark Connect on Amazon EMR on EC2: Interactive PySpark anywhere

## Overview

Amazon EMR on EC2 now supports Spark Connect with the AWS runtime for Apache Spark (emr-spark-8.0, Spark 4.0.2 and later). You can develop and debug PySpark interactively from SageMaker Unified Studio Data Notebooks or your own IDE (VS Code, PyCharm, Kiro, Jupyter) while Spark itself runs on a dedicated EMR cluster. Python runs locally, so breakpoints and DataFrame inspection work against full-size data. Each session is isolated with its own permissions, so a whole team can share one cluster.

Previously, EMR development meant a cluster-bound notebook or packaging code as a job before seeing results, with local/cluster version mismatches discovered only through a slow deploy-and-check loop.

## How Spark Connect works

Spark Connect splits the application from the engine. A lightweight PySpark client in your notebook or IDE sends DataFrame and SQL operations over a gRPC/TLS channel to a Spark Connect Server on the cluster, which executes them and returns results. Your machine needs no Spark install and no workload-sized resources.

When you start a session, EMR launches the server as a YARN application and returns an endpoint plus a short-lived token — no server to provision. Because the server runs on a cluster you already operate, sessions inherit its instance types, libraries, bootstrap actions, and Spark configuration, so what you debug is what runs as a batch job.

## One cluster for the whole team

Each session is a separate resource with its own execution role, tags, and lifecycle. A single cluster supports up to 1,000 concurrent sessions and 1,000 concurrent execution roles (service maximums; real concurrency depends on cluster size). Sharing one cluster gives:

- **On-demand Spark without extra clusters** — no idle per-person clusters.
- **Consistent environments** — one Spark version, libraries, and security config to patch and monitor.
- **Isolation and attribution** — per-session roles and tags scope data access, track cost per user, and let you stop one session without disturbing others.
- **Visibility and control** — active sessions in the Spark UI, finished ones in History Server, managed via console, API, CLI, or SDK.

## Getting started

Three steps: create a session-enabled cluster, start a session, connect.

- **Prerequisites:** EMR release emr-spark-8.0.0+ with sessions enabled, Spark installed, local Python 3.9+ with a `pyspark[connect]` version matching the cluster, plus `StartSession`/`ListSessions`/`GetSession`/`GetSessionEndpoint`/`TerminateSession` and `iam:PassRole` permissions.
- **Create the cluster** with session support, wait for WAITING state, then start a session and poll until IDLE.
- **Connect:** fetch the endpoint and token, build an `sc://host:443/` URL with the token and session ID, and create a remote `SparkSession`. Note `spark.stop()` only closes the local connection — terminate the session explicitly or rely on the idle timeout (60 minutes default, up to 24 hours).
- **Two entry points:** SageMaker Unified Studio handles attachment and session creation for you (create or attach a cluster in the Compute panel), while local IDEs use the CLI flow plus breakpoints and stepping.

Key limits: local PySpark must match the cluster Spark version, only DataFrame/SQL APIs (no RDDs), tokens expire after 1 hour, and multi-primary HA clusters, Trusted Identity Propagation, and Lake Formation fine-grained access are not supported in this release. There is no extra charge beyond the EC2 instances.

## References

- Original post: [Announcing Spark Connect on Amazon EMR on EC2: Interactive PySpark anywhere](https://aws.amazon.com/blogs/big-data/announcing-spark-connect-on-amazon-emr-on-ec2-interactive-pyspark-anywhere)
