---
title: Kerberizing Hadoop Clusters at Twitter
description: How Twitter added Kerberos authentication to tens of Hadoop clusters with zero HDFS downtime
tags: [source, twitter, x, hadoop, kerberos, security, sre, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/kerberizing-hadoop-clusters-at-twitter"
blog: twitter
date: '2023-02-23'
---

# Kerberizing Hadoop Clusters at Twitter

## Summary

Twitter runs one of the largest Hadoop installations in the world: tens of clusters, thousands of nodes, hundreds of petabytes of logical storage, tens of thousands of MapReduce/Spark jobs per day, serving search, AI/ML, metrics, ads, and spam prevention. Authorization (HDFS Unix-like permissions over LDAP identities) and accountability (HDFS audit logs) were in place from day one, but strong *authentication* was missing. This article explains how the team kerberized all Hadoop clusters without HDFS downtime, despite constraints that rule out the textbook rollout.

## Why It Was Hard: Four Constraints

1. **Any change amplifies.** A battle-tested platform serving hundreds of teams means every change is high-risk.
2. **Customer code changes don't scale.** Hundreds of teams and thousands of daily jobs must all be Kerberos-ready *before* services are kerberized — an all-or-none cutover per cluster, since kerberized services drop unauthenticated clients.
3. **Embedded clients.** Microservices with thousands of instances embed the Hadoop client library; each needs a keytab distributed to every host plus a coordinated restart (sometimes days of work). A single "flag day" is infeasible.
4. **Cross-cluster dependencies are cyclic.** Tens of clusters with replication jobs (destination-cluster jobs reading the source cluster) and ViewFS multi-cluster paths mean kerberizing one cluster breaks jobs spanning a kerberized/non-kerberized pair. The dependency graph had cycles, so no safe ordering existed.

Rejected alternatives: "fail-open"/whitelisted users (defeats strong auth, invites circumvention, not a Hadoop feature); standing up a parallel set of kerberized clusters (long-tail migration plus CapEx/OpEx, and cross-cluster use cases still break); proxying all Hadoop RPC through an authenticating gateway (merely moves the auth problem, cross-cluster issue remains).

## Building Blocks

- **KDC scale-out.** Tens of thousands of new service principals, thousands of client principals, and hundreds of extra auth QPS — absorbed with master-KDC tuning plus replicas.
- **Keytab generation and secure distribution services** built with the platform security team, with APIs for per-host keytabs and a self-service web UI.
- **NameNode principal design.** Per-host principals everywhere to limit blast radius — *except* the HA NameNode pair, which shares one service principal (e.g. `namenode/hadoopClusterOne@DOMAIN`), so a failover with thousands of connected clients does not flood the KDC with service-ticket requests for the newly active NN.

## The Rollout Strategy

The key enabler was Hadoop's built-in `ipc.client.fallback-to-simple-auth-allowed=true`: with it set on both clients and services, kerberized clients can still talk to non-kerberized clusters, so clusters can be kerberized **one at a time** without breaking cross-cluster jobs in one direction (DistCp launched in the kerberized cluster reading from a non-kerberized source keeps working). The reverse direction (job in a non-kerberized cluster reading a kerberized one) fails because HDFS delegation tokens — renewed by the ResourceManager so tasks avoid re-authenticating against the KDC — cannot be obtained across the boundary; the team added a `FileSystem.getTargetFileSystem(Path)` API and resolved input/output filesystems explicitly so tokens are fetched from the right cluster.

Additional tactics: auto-login from keytab (wrapping `UserGroupInformation.loginUserFromKeytab` so hundreds of thousands of user applications need no code change beyond the client library), kerberizing in the order *client applications → DataNodes/NodeManagers → NameNodes/ResourceManager/History servers* (the reverse order causes huge downtime), using HDFS audit logs to find the last un-kerberized stragglers (usually fewer than 10 teams), and always having a rollback plan.

## Results

All Hadoop clusters kerberized with zero HDFS downtime and minimal YARN disruption (in-flight jobs at ResourceManager cutover fail but auto-retry and succeed). Strong authentication now covers one of the company's largest sensitive-data platforms.

## Relevance to SW Engineers

- For fleet-wide auth migrations, prefer *fallback-compatible* intermediate states over flag days; order the rollout clients-first, servers-last.
- Shared service principals for HA pairs trade a slightly larger blast radius for KDC survival during failover storms — a deliberate, documented tradeoff.
- Delegation tokens (not just Kerberos tickets) are the second auth system you must design for in Hadoop; cross-realm token renewal is where mixed-mode rollouts break.
- Audit logs double as a migration tracker: query who still connects without credentials and chase owners directly.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/kerberizing-hadoop-clusters-at-twitter (Ashwin Poojary, Sampath Kumar, Santosh Marella, 23 Feb 2023)
- Related: `concepts/data-engineering/apache-kafka.md`, `concepts/infrastructure/kubernetes.md`
