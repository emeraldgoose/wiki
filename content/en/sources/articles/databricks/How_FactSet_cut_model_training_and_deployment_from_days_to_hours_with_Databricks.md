---
title: "How FactSet cut model training and deployment from days to hours with Databricks AI Runtime"
description: "FactSet’s Text-to-Formula (TTF) system has a deceptively difficult job: take a natural-language request from an investment professional and turn it into the correct FactSet Query Language (FQL) formula."
tags: [source, databricks, data-engineering, en]
locale: en
source_url: "https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime"
blog: databricks
published_date: 2026-10-14
---

# How FactSet cut model training and deployment from days to hours with Databricks AI Runtime

**Source**: [databricks](https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime) · **Published**: 2026-10-14

## Overview

FactSet’s Text-to-Formula (TTF) system has a deceptively difficult job: take a natural-language request from an investment professional and turn it into the correct FactSet Query Language (FQL) formula. FactSet initially built TTF around retrieval-augmented generation (RAG), using retrieval to find relevant examples and information for a given request. But as consumption grew, queries became more specialized and formulas more complex; the approach hit a quality ceiling. FactSet began incorporating fine-tuned open models into its Compound AI architecture, allowing the team to train models on the structure and patterns of FQL rather than relying primarily on retrieval at inference time. In its earlier work on TTF, FactSet found that incorporating fine-tuned models reduced end-to-end latency

## Key points

- FactSet’s Text-to-Formula (TTF) system converts natural-language requests from investment professionals into FactSet Query Language (FQL) formulas. After an initial RAG approach hit a quality ceiling on complex formulas,
- The team retrains models every two to three weeks as new data becomes available, making infrastructure setup and deployment speed important parts of the development cycle.
- With Databricks AI Runtime, FactSet can select serverless GPU compute for each workload and train alongside its existing Lakehouse workflows, reducing the time to set up, train, and deploy a model from days to hours.

## References

- Original article: [https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime](https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime)
