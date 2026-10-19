---
title: "Introducing Funke: Native HL7v2 Parsing on Databricks"
description: Promoted on 2026-10-17
tags: [source, article, en, en]
locale: en
source_url: "https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks"
blog: databricks
published_date: 2026-10-08
published: 2026-10-17
---

# Introducing Funke: Native HL7v2 Parsing on Databricks

**Source**: [Databricks Blog](https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks) · **Published**: 2026-10-08

## Overview

HL7v2 still runs healthcare messaging, but its nested delimiter-encoded structure forces teams into lossy FHIR conversions or third-party flattening engines. Funke ("spark" in German), the Python/PySpark successor to the 2021 Scala library Smolder, parses every HL7v2 message type directly into native Spark types — preserving the full segment/field/component/subcomponent hierarchy — and ships as a deployable asset bundle with a runnable demo.

## How the pipeline works

Deployed as a Declarative Pipeline on the medallion pattern, Auto Loader lands raw HL7 files from a Unity Catalog volume into a `raw_messages` bronze table with tracking metadata, then a parser step adds a native `hl7` column (segment map addressable by field, repetition, component, subcomponent, honoring MSH-declared separators and escapes) in silver. Analysts query any element with plain SQL or accessor helpers like `get_value`, and build their own gold tables — the demo derives an ADT history, a CDC-maintained live census, and bed-utilization metrics with a control-room app tracing messages end to end.

## Scope and getting started

Funke is a parser and ingestion accelerator, not an interface engine: it delivers complete, governed, queryable messages, while mapping segments to business meaning remains clinical domain work. Deploy by cloning the repo into a workspace, clicking Deploy in the bundle editor (or the Databricks CLI), dropping HL7 files in the landing volume, and running the pipeline — minutes from nothing to a streaming clinical feed.

## References

- [Introducing Funke: Native HL7v2 Parsing on Databricks](https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks)
