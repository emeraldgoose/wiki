---
title: Vector Search
description: "Seminar-level concept: Vector search algorithms, indexes, quantization, billion-scale deployment"
tags: [concept, ai-engineering, vector-search, hnsw, diskann, quantization]
locale: en
---

# Vector Search

**Read from**: Netflix Embedding Store, Databricks monitoring, Uber Hudi, PonderPounce, JIT-Agent

## Problem
Given query vector q ∈ ℝ^d, find top-K nearest neighbors in dataset X ∈ ℝ^(N×d). N = millions to billions.

## Algorithm Families

### Graph-Based (HNSW, NSW)
- **NSW**: Navigable Small World graph; greedy walk
- **HNSW**: Hierarchical NSW; multi-layer (express lanes + local search)
- **Complexity**: O(log N) search, O(N log N) build
- **Memory**: High (graph edges + vectors in RAM)

### Disk-Based (DiskANN, SPANN, FreshDiskANN)
- **Key idea**: Graph in RAM, vectors on SSD
- **PQ (Product Quantization)**: Compress vectors for RAM; refine from SSD
- **Complexity**: O(log N) search, ~10× lower RAM than HNSW
- **Best for**: Billion-scale on commodity hardware

### Quantization
| Method | Compression | Recall Loss | Search Speed |
|--------|-------------|-------------|--------------|
| None (FP32) | 1× | 0% | Baseline |
| FP16 / BF16 | 2× | ~0% | 2× |
| PQ (8-bit) | 4× | 1-3% | 4-8× |
| PQ (4-bit) | 8× | 3-8% | 8-16× |
| Scalar Quantization | 4× | 0.5-2% | 4× |

### Filtering + Hybrid
- Pre-filter by metadata (category, date, tenant) → smaller candidate set
- Post-filter for exact constraints

## Production Architecture (from Sources)

### Netflix Embedding Store
- Decoupled store: same embeddings at training + serving
- Cross-modal: CLIP (artwork), SeqCLIP/MediaFM (video)
- Invariant to crop/resize → single model across canvases

### Databricks Hydra
- High-cardinality metrics → Delta tables
- PromQL-to-SQL for Grafana (not pure vector search)

### Uber Hudi
- Column stats in metadata table → file pruning
- Not vector search but similar: metadata-first, data-second

## Seminar-Level Design Decisions

### Scale → Index Choice
| Scale | Vectors | Recommended |
|-------|---------|-------------|
| < 1M | Any | HNSW (RAM) |
| 1M - 100M | HNSW + PQ or DiskANN |
| 100M - 1B+ | DiskANN / SPANN + PQ |

### Latency Requirements
| Latency Budget | Approach |
|----------------|----------|
| < 10ms (p99) | HNSW (RAM) |
| < 50ms (p99) | DiskANN + PQ |
| < 200ms (p99) | DiskANN + aggressive PQ |

### Update Frequency
| Update Rate | Strategy |
|-------------|----------|
| Static / batch | Rebuild index periodically |
| Low (< 1%/day) | Incremental HNSW inserts |
| High (> 1%/hour) | DiskANN (better incremental) + merge |

## Key Seminar Points

1. **HNSW = gold standard for RAM**; **DiskANN = gold standard for disk**
2. **PQ (Product Quantization)** essential for billion-scale (4-8× compression)
3. **Hybrid search** (vector + keyword + filters) required for production quality
4. **Index rebuild vs incremental** trade-off based on update rate
5. **Observability**: recall@K, latency p50/p99, index size, build time

## Related Sources
- `sources/articles/netflix-techblog.md` (Embedding Store)
- `concepts/machine-learning/embedding.md` (embedding types)
- `concepts/ai-engineering/rag.md` (retrieval in RAG)

## Related Guides
- `guides/ai-engineering/vector-search.md`
