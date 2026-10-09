---
title: Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data
description: HuggingFace Daily Papers — 2026-08-31 — Harvard University
tags: [source, paper, huggingface, harvard-university]
locale: en
arxiv_id: 2608.31082
---

# Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data

**arXiv**: 2608.31082 | **Published**: 2026-08-31 | **Organization**: Harvard University | **Submitted by**: Milad Rezaei Hajidehi | **Upvotes**: 3

**Authors**: Milad Rezaei Hajidehi, Qitong Wang, Stratos Idreos

## Abstract

Valuable data remains embedded in unstructured sources: web pages, reports, contracts, filings, earnings calls, and PDFs. The big bet in enterprise AI is deploying LLM agents that reason over this data to answer complex questions for every knowledge worker. Agents can do this today, but at prohibitive cost. Each question repeatedly opens large documents to recover scattered evidence, consuming up to a million tokens. However, if the data were already structured, the same question would reduce to a cheap database lookup. For example, on FanOutQA benchmark, reasoning over an ideal pre-structured store is 28X cheaper, and the gap grows to orders of magnitude as questions fan out over more documents. Yet structuring everything in advance is not viable: documents hold vastly more possible structure than any workload will use, and the useful structure and documents are unknown until queries arrive. We propose agentic data cracking, a method that structures unstructured data adaptively and speculatively as a byproduct of reasoning itself. Structuring is adaptive because observed queries decide when it happens and what matters, and speculative because it goes beyond the current question. Whenever the agent opens a document to answer, a cracking sub-agent forks from the already-loaded context at marginal cost and extracts grounded structure likely to serve related future queries. Over time, an increasing share of queries is fully covered by structured data and answered without opening a document, keeping agentic accuracy at close to RAG cost. On FanOutQA, extended with merely one related question per test question, cracking cuts cost by 53% while preserving accuracy. Agentic data cracking is a first step toward next-generation data infrastructure for agentic reasoning over unstructured data: a shared substrate beneath the model where knowledge that reasoning already paid to uncover accumulates.

## Key Contributions

- Propose agentic data cracking for adaptive/speculative structuring of unstructured data during reasoning
- Structuring is adaptive: observed queries decide when and what structure to create
- Structuring is speculative: goes beyond current question to serve related future queries
- Cracking sub-agent forks from loaded context at marginal cost
- On FanOutQA with one related question per test question: 53% cost reduction while preserving accuracy
- Framework for next-generation data infrastructure: shared substrate beneath the model

## Methodology

Agentic data cracking: when agent opens a document, a cracking sub-agent forks from loaded context at marginal cost and extracts grounded structure. Structuring is adaptive (queries decide when/what) and speculative (goes beyond current question). Over time, structured data covers increasing share of queries, allowing answers without opening documents. FanOutQA benchmark used to evaluate cost/accuracy tradeoff.

## Results

On FanOutQA with one related question per test question: 53% cost reduction while preserving accuracy. Extended with more questions, gap grows to orders of magnitude versus pre-structured store (28X cheaper ideal). Agentic accuracy maintained at close to RAG cost.

## Relevance to Software Engineers

For SW engineers, agentic data cracking addresses the costly problem of LLM agents repeatedly opening large unstructured documents. The adaptive/speculative structuring approach means structure is created only when needed and for future queries too, keeping costs close to RAG while approaching pre-structured database efficiency. The marginal-cost cracking sub-agent model provides a pattern for building efficient data infrastructure. This is relevant for any agentic system that reasons over unstructured corporate data (confluence pages, SharePoint, S3 documents, etc.). The 53% cost reduction on FanOutQA with just one related question per test question is a concrete, measurable improvement.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2608.31082
- HuggingFace: https://huggingface.co/papers/2608.31082
