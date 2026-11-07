---
title: "Read, don't copy: replacing file and API feeds with OpenSharing - Part 1 (The Why)"
description: "Why SFTP and API customer feeds pile up hidden costs, and how reading a shared Delta or Iceberg table in place through OpenSharing removes them."
tags: [source, databricks, data-engineering, opensharing, en]
locale: en
source_url: "https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why"
blog: databricks
published_date: 2026-11-08
---

# Read, don't copy: replacing file and API feeds with OpenSharing - Part 1 (The Why)

**Source**: [Databricks Blog](https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why) · **Published**: 2026-11-06

## Overview

Customer ingestion has barely changed while the rest of data engineering moved on: most teams still ask for SFTP file dumps, poll a customer API, or reach for a managed connector. Each pattern works, but each carries hidden costs that compound with every new customer, and the authors trace the root of the problem to the copy itself. A copy means a pipeline to build and babysit per customer, bookkeeping of the last processed record, and a second storage of data the customer already maintains.

The evolution from file drops to API pulls to managed connectors traded one failure mode for another. SFTP feeds break when a customer uploads something other than the agreed files. API endpoints typically take a time cursor, and failing to keep track of the last timestamp lets the consumer's copy drift. Managed connectors can fail outright while removing flexibility. Backfills hurt most: without stored raw data, a file feed forces the customer to re-export months of history and an API feed forces chunked re-polling that tends to hit rate limits. Customers carry a burden too, because they must build and babysit an export with its own schedule and failure modes, cannot see whether or when their data was read, and pay to store a duplicate.

OpenSharing is the proposed alternative: read the customer's table in place through an open protocol built on Delta Lake and Iceberg, so the recipient does not have to be on Databricks. A shared table can expose version history for incremental pulls and a change data feed of inserts, updates and deletes, which turns the table that used to track processed records into a checkpoint the pipeline manages. New rows become available the moment the customer writes them, and whole-history shares make backfills a query instead of a favor. Part 2 of the series covers the end-to-end setup.

## Key points

- Traditional customer feeds are cheap to start and expensive to scale: every SFTP drop or API pull adds another pipeline to monitor.
- The article blames the copy, not just the transport: per-customer pipelines, self-managed progress bookkeeping, and duplicate storage all follow from it.
- API feeds drift when the timestamp cursor is mishandled, because a missed timestamp silently duplicates rows or drops a batch.
- Backfills are the worst case, forcing customer re-exports for files or rate-limited chunked re-polling for APIs.
- Customers pay twice: they build an export with its own schedule and failure modes, and they store a duplicate of data they already own.
- OpenSharing reads the shared table in place over an open Delta Lake and Iceberg protocol, so no SFTP endpoint and no per-customer connector.
- Version history and change data feed give incremental reads and explicit inserts, updates and deletes, replacing manual bookkeeping with a checkpoint.
- Adding a recipient is a grant on a table the customer already maintains, and Databricks system tables record when a recipient queried it.

## Details

The argument runs through four sections: how customer ingestion got here, the hidden costs, what OpenSharing changes, and a look at the workflow in action. On the cost side the article stresses that the pain peaks during backfills, and that mismatched bookkeeping is a silent failure that can take hours to debug. It also notes the asymmetry customers live with: they must produce the export, they cannot verify who read it, and both sides keep a copy.

With OpenSharing the consumer stops taking a copy. Because the shared table keeps its own ordered history, a pipeline can follow changes through streaming or the change data feed and no longer track what it has processed. If the customer shares the full history, a backfill is simply a query against the data already needed, with no extra storage and fresh results each time. Providers gain as well: adding a recipient is a grant rather than a new export, reads run against cloud storage with the recipient's own compute instead of the provider's database, and system tables give the provider a readable audit trail of recipient access. The article closes by pointing to Part 2 for setting up a share with a customer from creation through incremental reads.

## References

- Original article: [https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why](https://www.databricks.com/blog/read-dont-copy-replacing-file-and-api-feeds-opensharing-part-1-why)
