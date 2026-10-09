---
title: Build RAG System — Guide (Seminar Level)
description: "Execution guide: build production RAG system (retrieval, generation, evaluation, deployment)"
tags: [guide, ai-engineering, rag, retrieval, generation, production]
locale: en
---

# Build RAG System — Execution Guide

**Synthesizes**: `concepts/ai-engineering/rag.md`, `concepts/ai-engineering/vector-search.md`, `concepts/machine-learning/embedding.md`, `sources/articles/netflix-techblog.md`, `sources/articles/databricks-engineering.md`

## Architecture Overview
```
Query → [Hybrid Retrieval] → [Rerank] → [Context Assembly] → [LLM Generation] → Answer
         ↑                    ↑              ↑                   ↑
    Vector + BM25        Cross-encoder   Token budget      Prefill-only/
    + metadata                                              Citations
```

## Step 1: Data Preparation

### Chunking Strategy
```python
# Semantic chunking (preserve meaning)
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,          # tokens
    chunk_overlap=64,        # overlap for continuity
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Or: Document structure aware (headers, tables, code blocks)
```

### Embedding
```python
# Production: E5 / BGE / instructor-xl
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-large-en-v1.5")  # 1024-dim
embeddings = model.encode(chunks, batch_size=64, show_progress_bar=True)
```

### Index (HNSW for <100M, DiskANN for >100M)
```python
import faiss  # or hnswlib, diskann

# HNSW (RAM)
index = faiss.IndexHNSWFlat(1024, 32)  # M=32
index.hnsw.efConstruction = 200
index.add(embeddings)

# DiskANN (billion-scale)
# Use diskann library or managed service (Pinecone, Weaviate, Qdrant)
```

## Step 2: Hybrid Retrieval

```python
def hybrid_search(query, top_k=100, alpha=0.7):
    # Dense
    query_vec = model.encode([query])[0]
    dense_scores, dense_idx = index.search(query_vec.reshape(1,-1), top_k)
    
    # Sparse (BM25)
    sparse_scores, sparse_idx = bm25_search(query, top_k)
    
    # Combine
    combined = {}
    for i, idx in enumerate(dense_idx[0]):
        combined[idx] = combined.get(idx, 0) + alpha * dense_scores[0][i]
    for i, idx in enumerate(sparse_idx):
        combined[idx] = combined.get(idx, 0) + (1-alpha) * sparse_scores[i]
    
    # Top-K
    top_idx = sorted(combined, key=combined.get, reverse=True)[:top_k]
    return [chunks[i] for i in top_idx]
```

## Step 3: Reranking

```python
# Cross-encoder reranker
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-large")
pairs = [[query, chunk] for chunk in candidates]
rerank_scores = reranker.predict(pairs)
reranked = [c for _, c in sorted(zip(rerank_scores, candidates), reverse=True)]
```

## Step 4: Context Assembly (Context Engineering)

```python
def assemble_context(reranked_chunks, token_budget=4000):
    context = ""
    citations = []
    tokens_used = 0
    
    for i, chunk in enumerate(reranked_chunks):
        chunk_tokens = estimate_tokens(chunk)
        if tokens_used + chunk_tokens > token_budget:
            # Summarize or truncate
            chunk = summarize(chunk, token_budget - tokens_used)
            chunk_tokens = estimate_tokens(chunk)
        
        context += f"[{i+1}] {chunk}\n\n"
        citations.append({"id": i+1, "source": chunk.metadata})
        tokens_used += chunk_tokens
        
        if tokens_used >= token_budget:
            break
    
    return context, citations
```

## Step 5: Generation with Citations

```python
prompt = f"""System: You are a helpful assistant. Answer using ONLY the provided context. Cite sources inline like [1], [2].

Context:
{context}

Query: {query}

Answer:"""

# Prefill-only for ranking/classification; full generation for answers
response = llm.generate(prompt, max_tokens=512, temperature=0.1)
```

## Step 6: Evaluation (RAGAS)

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision

dataset = {
    "question": [...],
    "answer": [...],
    "contexts": [...],
    "ground_truth": [...]
}

results = evaluate(dataset, metrics=[
    faithfulness,      # Answer supported by context?
    answer_relevancy,  # Addresses query?
    context_recall,    # Relevant context retrieved?
    context_precision  # Retrieved context relevant?
])
```

## Production Patterns (from Sources)

### Netflix GenRec
- **Prefill-only vLLM** for ranking (no decode)
- **Context engineering**: token budget, high-signal retention
- **Verbalization**: user history + metadata → text

### Databricks Hydra
- **PromQL-to-SQL** conversion (retrieval = SQL generation)
- **Direct Delta access** for deep analysis
- **Unified semantics** across paths

### Uber Software Factory
- **3,600+ agent skills** as RAG patterns
- **Benchmark-driven model selection** per skill
- **Cost equation optimization**

## Deployment Checklist
- [ ] Hybrid retrieval (dense + sparse + filters)
- [ ] Cross-encoder reranker (top-100 → top-10)
- [ ] Context assembly with token budget + citations
- [ ] RAGAS evaluation pipeline (CI/CD)
- [ ] Latency p99 < 2s (retrieval + rerank + generation)
- [ ] Hallucination rate < 2% (faithfulness > 0.95)
- [ ] Monitoring: recall@K, latency, token usage, error rate

## Related Concepts
- `concepts/ai-engineering/rag.md`
- `concepts/ai-engineering/vector-search.md`
- `concepts/machine-learning/embedding.md`

## Related Guides
- `guides/ai-engineering/vector-search.md`
- `guides/ai-engineering/build-agent.md`
