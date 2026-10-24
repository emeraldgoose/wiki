---
title: "Reducing Qwen training time by 6x on AI Runtime"
description: "Training or finetuning a multi-billion parameter foundation model requires significant compute, often spanning hundreds to thousands of hours of GPU training."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/reducing-qwen-training-time-6x-ai-runtime"
blog: databricks
published_date: 2026-10-14
---

# Reducing Qwen training time by 6x on AI Runtime

**Source**: [databricks](https://www.databricks.com/blog/reducing-qwen-training-time-6x-ai-runtime) · **Published**: 2026-10-14

## Overview

Training or finetuning a multi-billion parameter foundation model requires significant compute, often spanning hundreds to thousands of hours of GPU training. But tuning training performance for an LLM is challenging, and high level metrics, such as GPU utilization may not be showing your actual utilization. In this blog post, we show how to cut through the layers of abstraction, and speed up fine-tuning of the latest Qwen 3.8 27B model on AI Runtime by 6x. Through systematic performance optimization, even with GPU utilization already at 98%, we go from 7 hours 44 minutes to 1 hour 17 minutes  We will provide a deep dive into the techniques behind these improvements, from how to measure what matters, implementation details, and design trade-offs involved in each optimization.

## Key points

- In this blog post we show how we speed up Qwen fine tuning by 6x by installing the correct kernels and making improvements to the data pipeline.
- We get that performance increase despite the fact that the baseline model already showed 98% GPU utilization.
- AIR helps you diagnose performance issues with a standard torch trace of an LLM.
- We apply FSDP2, the latest model sharding technique from torch. This is required to fit the model weights and optimizer state onto the GPUs. A pure distributed data parallel approach would fail to fit the model weights,
- We also enable activation checkpointing, a technique which trades memory space for compute in the backwards pass to allow for a larger batch size per GPU.
- The dataloader is packing 2D batches with a maximum tokens per batch of 8192, padding to the maximum size of the batches example.

## References

- Original article: [https://www.databricks.com/blog/reducing-qwen-training-time-6x-ai-runtime](https://www.databricks.com/blog/reducing-qwen-training-time-6x-ai-runtime)
