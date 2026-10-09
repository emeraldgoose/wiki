---
title: Twitter's Blobstore Hardware Lifecycle Monitoring and Reporting Service
description: How Twitter manages bare-metal lifecycle (allocated, managed, maintenance, repair) for Blobstore photo/video storage at scale
tags: [source, twitter, x, blobstore, storage, hardware, sre, tier-2]
locale: en
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/twitters-blobstore-hardware-lifecycle-monitoring-and-reporting-service"
blog: twitter
date: '2023-02-23'
---

# Twitter's Blobstore Hardware Lifecycle Monitoring and Reporting Service

## Summary

[Blobstore](https://blog.twitter.com/engineering/en_us/a/2012/blobstore-twitter-s-in-house-photo-storage-system) is Twitter's low-cost, high-performance, scalable in-house storage system for photos, videos, and other binary large objects. Most of it runs on bare-metal servers in on-premise data centers. This article describes the hardware lifecycle management service the Blobstore team built after years of operating with almost no visibility: hosts drifted between states with only ad-hoc manual queries, machines sat indefinitely in a given state with no alerting, and physical capacity had no alerting at all — impending capacity crunches were discovered via unrelated alerts or manual intervention.

## Goals

1. Improve Blobstore service health and infrastructure monitoring.
2. Reduce manual toil.
3. Increase response and recovery speed during provisioning crises.
4. Gain insight into bare-metal server health.
5. Facilitate bare-metal management in Blobstore.
6. Detect and prevent capacity crunches and lifecycle issues.

## The Four Lifecycle States

Blobstore models every host with four fundamental states:

- **Allocated** — freshly allocated from the Capacity Management team, or returning from repair after a re-image.
- **Managed** — host configuration matches the expected in-production state; the host serves traffic.
- **Maintenance** — host needs a kernel/firmware update, or shows early signs of trouble.
- **Repair** — host has critical errors (e.g. bad disk with I/O errors); owned by the Site Operations team. After successful repair the host is wiped and returns to **allocated**, completing the cycle.

## Key Mechanisms

### Provisioning (allocated → managed)

A provisioner service runs every 24 hours on each host at a randomly scheduled time. It validates that the host was correctly built after re-image/allocation, formats data disks (new UUIDs, FAT files, top-level files/directories), runs Puppet to converge software, then flips the state to **managed** and adds the host to the data center.

### Firmware/kernel compliance via Airflow (managed → maintenance → managed)

Twitter uses Airflow and Airflow-Compliance as scheduler/operation components that scan for hosts on outdated firmware or kernel. The host's monitoring alerts are silenced, it moves to **maintenance**, firmware is upgraded, and on completion it returns to **managed**, is unsilenced, and released. Failures are reported to Blobstore over Slack; a host that fails an update always releases its lease (to avoid false alerts) and the failure is picked up by other automation or manual inspection.

### Lifecycle metrics pipeline

Lifecycle metrics were added to Blobstore's agents: hosts provisioned, hosts in **allocated**, hosts sent to/already in **repair**, hosts moved to **managed**, rebooted hosts. Because Twitter's metrics library unreliably collects stats from cron jobs shorter than two minutes, a short-lived Python service on each machine publishes via CuckooScribePublisher to a local Scribe daemon, which routes over the network to Cuckoo for dashboards.

### Disk remediation automation (managed → repair)

Broken hosts are moved to **repair** automatically: a list of failed, unused nodes is collected from Blobstore's mapping service; hosts in **maintenance** or with an existing repair ticket are excluded. A heuristic decides reboot vs. repair — e.g. more than 6 bad statuses in a month, more than 3 in a week, or more than 2 in a day sends the host to **repair** (silenced, ticket created, history cleared); otherwise the host is rebooted and its history pruned. The tool also counts dead disks fleet-wide, takes hosts out of production, and rate-limits how fast hosts are sent to Site Operations. This replaced a manual process and mattered especially because the fleet lacks hot-swappable disks.

## Results and Takeaways

- Toil dropped: provisioning, compliance upgrades, and repair triage run on schedules/automation instead of ad-hoc queries.
- Visibility: dashboards over lifecycle states give early warning of capacity crunches and stuck hosts.
- Failure handling discipline: silencing during maintenance, lease release on failure, and exclusion of in-maintenance hosts prevent alert storms and accidental reboots.

## Relevance to SW Engineers

- Model fleet hardware as an explicit finite-state machine (allocated/managed/maintenance/repair) rather than implicit status flags — it makes automation, dashboards, and ownership boundaries crisp.
- Short-lived cron telemetry needs a push-based side channel (here: local Scribe daemon → Cuckoo) when the metrics library only samples long-running processes.
- Rate-limit repair submissions and use escalating heuristics (day/week/month windows) so a single bad batch of disks cannot stampede the repair queue.

## References

- Source: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/twitters-blobstore-hardware-lifecycle-monitoring-and-reporting-service (Taylor Olson, Ashwin Poojary, 23 Feb 2023)
- Related: `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/delta-lake.md`
