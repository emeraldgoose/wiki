---
title: "Accelerate GPU training on Unity Catalog tables with UCDataset"
description: "UCDataset, a beta native PyTorch data loader on Databricks AI Runtime, streams Unity Catalog tables straight to every GPU — 10x faster training than reading an exported Parquet copy in Databricks' benchmark."
tags: [source, databricks, machine-learning, training, en]
locale: en
source_url: "https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset"
blog: databricks
published_date: 2026-11-10
---

# Accelerate GPU training on Unity Catalog tables with UCDataset

**Source**: [Accelerate GPU training on Unity Catalog tables with UCDataset](https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset) · **Published**: 2026-11-09

## Overview

GPUs are usually the most expensive part of a training run and the hardest to keep busy, and the bottleneck is rarely the model — it is getting data from where it lives to the GPU fast enough. Databricks released UCDataset (Unity Catalog Dataset) in Beta on AI Runtime: a native PyTorch data loader that streams Unity Catalog tables directly to every GPU in a training job, with no exports, no copies and no custom loader code.

The post frames three workarounds that teams fall into. Exporting the table to Parquet before every run pays for a second copy, goes stale as soon as new data lands, and falls outside Unity Catalog lineage. Reading the whole table into pandas with `toPandas()` works only for small tables and lands everything on one node, which does not help a job training on 32 GPUs. Streaming through a warehouse is slow because warehouses were not built to feed GPUs and get throttled when many GPUs read at once. On top of that, every GPU and worker needs its own balanced slice of data; teams build that by hand, and a subtle bug can mean duplicated or skipped rows go unnoticed.

UCDataset instead treats Unity Catalog tables as a first-class source for distributed PyTorch training: you describe what to read — a table, the columns you need, a row filter — and it streams training-ready batches. It reads the table's files directly from cloud storage, splits matching rows evenly across every GPU and data loader worker, applies filters and deletion vectors as data is read, picks up newly appended rows on the next run, and enforces Unity Catalog permissions because jobs read data as the identity that runs them.

## Key points

- In a benchmark on a simulated production workload, UCDataset streamed a 300 GB feature table across 8 NVIDIA H100 GPUs to train a recommendation model and cut training time by an average of 10x compared with loading directly from Parquet.
- It plugs into a standard PyTorch training loop: because UCDataset already yields whole batches, it is wrapped in a PyTorch `DataLoader` with `batch_size=None`, and each of the 16 GPUs in the example gets its own share of matching rows, so no sampler or sharding code is written.
- Row filters are pushed into the read, so non-matching rows never reach training code, and because the job reads the live table there is no second copy to store, sync or secure separately.
- Scaling is a configuration change: the job is described in `workload.yaml`, which starts `train.py` with `torchrun` on every node, and training on more GPUs only changes `num_accelerators` — the training code stays the same.
- The package installs from PyPI (`%pip install databricks-uc-dataset`), and the Beta reads Delta tables registered in Unity Catalog, including tables with deletion vectors.
- Two limitations are stated explicitly: in the Beta, UCDataset cannot read tables that have row filters or column masks, and it is scoped to structured tables — unstructured files in Unity Catalog volumes are served by UCVolumeDataset with local caching, while multimodal support via the FILE type is in progress.

## Details

The worked example is a click-through-rate model trained on a `main.recsys.ctr_features` table that receives new impressions daily, using 16 GPUs across two nodes. In `train.py` you select the table, keep the labeled training rows and project only the columns the model needs; `workload.yaml` then runs the script with `torchrun` on each node via the AI Runtime CLI, and the complete files plus a sample table are published in the AI Runtime cookbook recipe for a click-through-rate model on a Unity Catalog table.

The governance story is the direct consequence of skipping the export: training jobs read data as the identity that runs them, and Unity Catalog permissions on the table apply exactly as elsewhere on Databricks, so there is no exported copy with its own access controls to maintain. Databricks asks users to try the Beta, read the UCDataset documentation, start from the cookbook recipe, and send feedback through their account team.

## References

- Original article: [Accelerate GPU training on Unity Catalog tables with UCDataset](https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset)
