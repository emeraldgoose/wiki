---
title: How Twitter Uses rasdaemon for Hardware Reliability
description: Replacing deprecated mcelog/edac-utils with rasdaemon as the centralized hardware-error telemetry on hundreds of thousands of hosts
tags: [source, twitter, x, hardware, reliability, linux, rasdaemon, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-twitter-uses-rasdaemon-for-hardware-reliability"
blog: twitter
date: '2023-01-06'
---

# How Twitter Uses rasdaemon for Hardware Reliability

## Summary

Twitter's on-premise data centers hold hundreds of thousands of servers and millions of hardware components. Transient, intermittent hardware faults were hard to root-cause: service owners could see a poorly performing machine but not which component was at fault, so machines cycled through site-operations repair loops — reinstalled, returned to service, failing again — with no diagnosis. Meanwhile every team had written its own fault-detection plugins, leaving service owners with a confusing sprawl of signals. The legacy tools themselves were dying: **mcelog is deprecated in the kernel** and **edac-utils is largely unmaintained**, and kernel changes had made their exported metrics unreliable. The team consolidated all hardware-error telemetry onto **rasdaemon**, the standard Linux open-source RAS (reliability, availability, serviceability) utility, as the one-stop collector, filter, and reporter of kernel hardware-error events.

## Events Covered

- **MC (Memory Controller) events** — corrected, uncorrected, and fatal errors counted and exposed in detail.
- **MCE (Machine Check Exception) events** across platform types — replaces mcelog for CPU-detected hardware failures.
- **Disk/block errors** — EOPNOTSUPP, ETIMEDOUT, ENOSPC, ENOLINK, EREMOTEIO, EBADE, ENODATA, EILSEQ, ENOMEM, EBUSY, EAGAIN, EREMCHG, EIO (supplementing S.M.A.R.T. data).
- **Devlink errors** and **PCIe AER events**.

Side benefits: unblocked CentOS 8/9 migration, higher-fidelity signals (fewer non-actionable alerts generating cross-team overhead), and **page-offlining** used wherever appropriate — offlining bad memory pages instead of pulling whole servers from production, saving real money.

## Migration Discipline

- **Make-before-break**: full feature parity before disabling old plugins.
- Exhaustive codebase search for every mention of edac-utils/mcelog; every service dashboard reviewed so observability never regressed.
- Company-wide communication, extensive canarying, and a slow fleet-wide rollout.
- Result: reduced MTTD/MTTR on hardware and a recommendation of rasdaemon to the industry.

## Relevance to SW Engineers

- Treat deprecated kernel-adjacent tooling (mcelog) as tech debt with a deadline: kernel changes silently degrade its output before it formally dies.
- Consolidate per-team hardware plugins into one pipeline; the cost of N bespoke detectors is paid in every future debugging session.
- Prefer degraded-but-serving responses (page offlining) over whole-host removal when the fault domain allows it.
- "Make before break" plus dashboard-by-dashboard verification is the template for migrating any fleet-wide observability dependency.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-twitter-uses-rasdaemon-for-hardware-reliability (6 Jan 2023)
- Related: `concepts/infrastructure/kubernetes.md`
