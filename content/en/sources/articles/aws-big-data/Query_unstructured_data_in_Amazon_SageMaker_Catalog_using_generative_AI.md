---
title: "Query unstructured data in Amazon SageMaker Catalog using generative AI"
description: Promoted on 2026-10-17
published: 2026-10-17
source_url: "https://aws.amazon.com/blogs/big-data/query-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai"
blog: aws-big-data
locale: en
tags: [source, article, en, en]
---

# Query unstructured data in Amazon SageMaker Catalog using generative AI

## Overview

This is the consumer-side follow-up to a series whose first part enriched unstructured documents (Textract extraction plus Claude summarization) and published them to SageMaker Catalog. Here, a data consumer searches the catalog for the enriched asset, subscribes with producer approval, and queries the documents two ways: a no-code chat agent for analysts, and Bedrock model inference from a notebook for engineers embedding NLQ into applications.

## Subscribing to the asset

From the SageMaker Unified Studio consumer project, search the catalog with a keyword from the AI-generated README, open the asset to review its business metadata and glossary terms, and request a subscription with a reason. The producer approves in their own project, after which the asset appears under the consumer's subscribed assets with governed access intact throughout.

## Two query paths

Option one registers the subscribed S3 location in the project, builds a knowledge base over the PDFs, and chats against it through the Bedrock chat agent app — plain-English questions answered from ingested documents, with Guardrails available for sensitive domains. Option two opens a JupyterLab notebook from the subscribed asset and runs Bedrock inference programmatically, returning grounded answers that can be wired into external chat or BI tools. Both paths keep analysts and engineers on governed data without knowing where files live.

## References

- [Original post: Query unstructured data in SageMaker Catalog using generative AI](https://aws.amazon.com/blogs/big-data/query-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai)
- [Part 1: Improve discoverability of unstructured data in SageMaker Catalog](https://aws.amazon.com/blogs/big-data/improve-the-discoverability-of-your-unstructured-data-in-amazon-sagemaker-catalog-using-generative-ai/)
