---
title: "Real-time fraud detection with Feature Views"
description: "Feature Views unify feature definitions for training and serving to reduce skew in real-time fraud detection."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/real-time-fraud-detection-feature-views"
blog: databricks
published_date: "2026-11-07"
---

# Real-time fraud detection with Feature Views

**Source**: [Databricks Blog](https://www.databricks.com/blog/real-time-fraud-detection-feature-views) · **Published**: 2026-11-05

## Overview

Real-time fraud detection must combine recent customer activity, normalized spending behavior, and current transaction details within a short decision window. Feature Views in Databricks Feature Store address the risk of training-serving skew and data leakage by defining a feature once for both point-in-time training data and managed serving pipelines.

The article demonstrates this through a streaming payment scenario. Features include five-minute transaction counts, ten-minute totals, thirty-day averages and standard deviations, and request-time comparisons between a live payment and the customer's baseline. Historical, streaming, and on-demand capabilities all run from the same feature definitions under Unity Catalog.

By keeping feature logic consistent across training and serving, models receive inputs matching what they learned, while streaming and on-demand computation keeps customer context current. This improves fraud detection timeliness without separate preprocessing pipelines.

## Key points

- Real-time fraud models need recent activity, spending baselines, and transaction context.
- Training-serving skew arises when features are computed differently in training and production.
- Point-in-time correct features prevent data leakage.
- Feature Views define one feature for both historical training and serving.
- Rolling windows and Sawtooth windows maintain short-term and long-term baselines.
- On-demand features compare a live transaction with stored customer baselines.

## Details

The walkthrough explains ingestion from Kafka, managed offline storage for training, Unity Catalog governance, and Model Serving at request time. It also uses Databricks Apps for live transaction monitoring and visualization.

## References

- Original article: [Databricks Blog](https://www.databricks.com/blog/real-time-fraud-detection-feature-views)
