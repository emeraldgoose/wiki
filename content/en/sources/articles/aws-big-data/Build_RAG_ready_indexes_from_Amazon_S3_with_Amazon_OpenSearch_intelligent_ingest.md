---
title: "Build RAG-ready indexes from Amazon S3 with Amazon OpenSearch intelligent ingestion"
description: "Amazon OpenSearch intelligent ingestion turns documents stored in Amazon S3 into searchable indexes without manual parsing and embedding pipelines."
tags: [source, aws-big-data, search, rag, opensearch, en]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion"
blog: aws-big-data
published_date: "2026-10-23"
---

# Build RAG-ready indexes from Amazon S3 with Amazon OpenSearch intelligent ingestion

**Source**: [aws-big-data](https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion) · **Published**: 2026-10-23

## Overview

Much of an organization's most valuable knowledge sits in documents such as contracts, product manuals, research reports, support runbooks and financial filings. This content is stored in Amazon S3 as structured data (JSON, NDJSON and JSON arrays) and unstructured data (PDF, Word, text and Markdown). Generative AI applications, RAG assistants and enterprise search experiences are only as good as their access to this content, yet it is often the hardest data to make discoverable and searchable. To extract this data, customers typically run separate parsing, chart interpretation, chunking, embedding and indexing pipelines, each with its own infrastructure, scaling decisions and failure modes.

Amazon OpenSearch intelligent ingestion addresses this by letting users go from raw documents to semantic search without manual pipelines.

## Key points

- Extract text while preserving layout, reading order and tables with a document parser.
- Interpret charts, diagrams and screenshots inside documents.
- Chunk and embed extracted text, then write results into a vector index.
- Ingest PDF, Word and Markdown files with layout and tables intact into indexes ready for semantic and hybrid search.
- Make visual content searchable by generating text descriptions of charts, diagrams, screenshots and photos with a vision-language model.
- Ingest structured data such as JSON, NDJSON and CSV and apply transformations during ingestion, with optional semantic search enrichment.

## Details

Traditionally, each layer of document processing brings separate infrastructure and complexity; many organizations spend weeks making end-to-end pipelines work. Intelligent ingestion consolidates these steps so teams can prepare enterprise documents for semantic and hybrid search with less manual work.

By parsing documents, handling visual content and supporting structured data transformations within ingestion, the feature helps organizations make PDF, Word, Markdown, JSON and CSV content stored in Amazon S3 discoverable for RAG and search.

## References

- Original article: [https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion](https://aws.amazon.com/blogs/big-data/build-rag-ready-indexes-from-amazon-s3-with-amazon-opensearch-intelligent-ingestion)
