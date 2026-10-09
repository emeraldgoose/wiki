---
title: Retrieval-Augmented Generation (RAG)
description: "Seminar-level concept: RAG architecture, retrieval, generation, evaluation, production patterns"
tags: [concept, ai-engineering, rag, retrieval, generation, llm]
locale: en
---

# Retrieval-Augmented Generation (RAG)

**Read from**: Netflix GenRec (context engineering), Databricks Hydra (PromQL-to-SQL), Uber software factory (agent skills), PonderPounce (System2 reasoning), JIT-Agent (harness intelligence)

## Core RAG Pipeline
```
Query → Retrieval (vector/keyword/hybrid) → Top-K Context → Generation (LLM) → Answer
```

## Retrieval Strategies

### Dense Retrieval (Vector Search)
- Query → embedding → ANN search (HNSW/DiskANN) → top-K passages
- Best for: semantic similarity, paraphrase tolerance

### Sparse Retrieval (BM25/Keyword)
- Query → token weights → inverted index → top-K passages
- Best for: exact match, entity names, technical terms

### Hybrid Retrieval (Production Standard)
```
score = α × dense_score + β × sparse_score + γ × metadata_filters
```
- α, β tuned per domain; metadata filters (date, source, category) applied pre-search

### Multi-Stage Retrieval
1. **Candidate generation**: Broad recall (BM25 + dense, k=100-1000)
2. **Reranking**: Cross-encoder / LLM reranker (k=10-20)
3. **Deduplication**: Remove near-duplicate passages
4. **Context assembly**: Fit into token budget (context engineering)

## Generation

### Prompt Construction
```
System: You are a helpful assistant. Use only provided context.
Context: [passage_1] [passage_2] ... [passage_k]
Query: {user_query}
Answer:
```

### Context Engineering (from Netflix GenRec)
- **Token budget management**: Retain high-signal, omit low-signal, summarize repetitive
- **Ordering**: Most relevant first (primacy effect) or last (recency effect)
- **Citation**: Require inline citations [1], [2] for verifiability

### Generation Patterns
| Pattern | Description | Use Case |
|---------|-------------|----------|
| Single-pass | One LLM call | Simple QA |
| Iterative | Retrieve → Generate → Refine | Complex reasoning |
| Self-RAG | LLM decides when to retrieve | Adaptive |
| Corrective RAG | Verify → Correct → Re-generate | High accuracy |

## Evaluation (Seminar Level)

### Retrieval Metrics
- **Recall@K**: % relevant in top-K
- **MRR**: Mean Reciprocal Rank
- **nDCG**: Normalized Discounted Cumulative Gain

### Generation Metrics
- **Faithfulness**: Answer supported by context? (LLM-as-judge)
- **Answer Relevance**: Addresses query?
- **Hallucination Rate**: Unsupported claims / total claims

### End-to-End
- **RAGAS**: Retrieval + Generation combined
- **Human eval**: Side-by-side comparison

## Production Patterns (from Sources)

### Netflix GenRec
- **Context engineering** over feature engineering
- Verbalized user history + item metadata as context
- Prefill-only vLLM for cost efficiency

### Databricks Hydra
- PromQL-to-SQL conversion (retrieval = SQL generation)
- Direct Delta table access for deep analysis
- Unified metric semantics across TSDB + Lakehouse paths

### Uber Software Factory
- 3,600+ agent skills = retrieval + generation patterns
- Benchmark-driven model selection per skill
- Cost equation optimization

### PonderPounce
- System2 (Ponder) retrieves/reasons over full episode context
- System1 (Pounce) receives compressed cognition token

### JIT-Agent
- Harness synthesis = retrieval of relevant skill modules
- Self-evolving archive of (task, harness, performance) tuples

## Key Seminar Points

1. **Retrieval quality > generation quality** for factual accuracy
2. **Hybrid search + reranking** is production baseline
3. **Context engineering** (token budget, ordering, citation) critical
4. **Evaluation must cover both retrieval + generation** (RAGAS)
5. **Agentic RAG**: Retrieval as a tool/skill in agent harness

## Related Sources
- `sources/articles/netflix-techblog.md` (GenRec context engineering)
- `sources/articles/databricks-engineering.md` (Hydra PromQL-to-SQL)
- `sources/papers/PonderPounce.md` (System2 context)
- `sources/papers/JIT-Agent.md` (harness as retrieval)

## Related Guides
- `guides/ai-engineering/build-rag.md`
- `guides/ai-engineering/vector-search.md`
