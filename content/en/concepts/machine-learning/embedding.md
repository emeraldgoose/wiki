---
title: Embedding
description: "Seminar-level concept: Embeddings, vector search, multimodal embeddings, Netflix Embedding Store"
tags: [concept, machine-learning, embedding, vector-search, multimodal]
locale: en
---

# Embedding

**Read from**: Netflix MAPS (multimodal embeddings), GenRec (verbalization), Databricks monitoring, Uber Hudi, PonderPounce

## What It Is
Dense vector representation capturing semantic similarity. Maps discrete tokens/images → continuous space where distance = semantic relatedness.

## Types

### Text Embeddings
| Model | Dim | Use Case |
|-------|-----|----------|
| Word2Vec/GloVe | 300 | Classic, static |
| BERT | 768 | Contextual, bidirectional |
| Sentence-BERT | 384/768 | Sentence similarity |
| E5 / BGE | 1024 | Retrieval-optimized |
| LLM hidden states | 4096+ | Rich, task-adaptive |

### Image/Video Embeddings (from Netflix MAPS)
- **CLIP**: Image-text joint embedding (768-dim)
- **SeqCLIP**: Sequential frames for video
- **MediaFM**: Foundation model for media embeddings

### Multimodal (Netflix Embedding Store)
- Single store for: title embeddings, game embeddings, member profiles, multimedia assets
- **Cross-modal transfer**: Artwork preferences transfer to new titles via CLIP space
- **Cold-start solution**: New asset gets embedding at creation → immediate personalization

## Vector Search

### Index Structures
| Index | Build Time | Query Latency | Recall | Memory |
|-------|------------|---------------|--------|--------|
| Flat (brute force) | O(1) | O(N) | 100% | Low |
| IVF (Inverted File) | O(N) | O(√N) | ~95% | Medium |
| HNSW | O(N log N) | O(log N) | ~99% | High |
| DiskANN / SPANN | O(N log N) | O(log N) | ~99% | Low (disk) |

### Hybrid Search
```sql
-- Vector + keyword (BM25) + filters
SELECT * FROM items
WHERE vector_search(embedding, query_vec, k=100)
AND category = 'electronics'
ORDER BY hybrid_score(bm25_score, vector_score)
LIMIT 20
```

## Netflix Embedding Store (from MAPS)
- **Decouples foundation model updates from personalization model deployments**
- Same embeddings at training time AND online inference time → no skew
- Serves exact same embeddings across all personalization models
- Artwork embeddings (CLIP) invariant to crop/resize → single unified model across 5 canvases

## From Sources

### Netflix GenRec
- Verbalization: user history + item metadata → text → LLM embedding space
- Context engineering: token budget management (retain high-signal, omit low, summarize repetitive)

### Databricks Hydra
- High-cardinality metrics → embedding-like representations for troubleshooting

### PonderPounce
- MLLM causal context (KV cache) as episode memory embedding

## Key Seminar Points

1. **Embedding quality > index choice** for recall
2. **Multimodal alignment** (CLIP-style) enables cross-modal transfer
3. **Decoupled store** (Netflix) prevents training/serving skew
4. **Hybrid search** (vector + keyword + filters) for production quality
5. **HNSW/DiskANN** for billion-scale; Flat for <1M

## Related Sources
- `sources/articles/netflix-techblog.md` (MAPS, GenRec)
- `sources/papers/PonderPounce.md` (causal context as memory)
- `sources/papers/JIT-Agent.md` (tool embedding in harness)

## Related Guides
- `guides/ai-engineering/build-rag.md` (embedding + retrieval)
- `guides/ai-engineering/vector-search.md`
