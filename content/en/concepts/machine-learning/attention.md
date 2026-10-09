---
title: Attention
description: "Seminar-level concept: Attention mechanisms, variants, FlashAttention, KV cache, scaling"
tags: [concept, machine-learning, attention, transformer, flash-attention]
locale: en
---

# Attention

**Read from**: Transformer concept, HuggingFace Unified Dynamics paper, PonderPounce System2/System1, JIT-Agent

## Core Attention

### Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

**Complexity**: O(N²) time/space for sequence length N

### Multi-Head Attention
```
head_i = Attention(Q·W_i^Q, K·W_i^K, V·W_i^V)
MultiHead = Concat(head_1...head_h) · W^O
```

### Attention as Organizational Condition (from Unified Dynamics)
- "Component gating and rollback show causal recruitment"
- "Non-additive combination of query-conditioned support formed during training"
- Organizational conditions realized by **Attention**

## Variants & Optimizations

### FlashAttention (IO-Aware)
- **Problem**: Standard attention materializes N×N matrix in HBM
- **Solution**: Tiling + recomputation; never materialize full matrix
- **Result**: 2-4× speedup, linear memory, exact (not approximate)

### FlashAttention-2 / 3
- Better parallelism, lower shared memory usage
- Hopper (H100) tensor core utilization
- FP8 support

### KV Cache (Decoding)
- Store K, V for previous tokens
- **Memory**: 2 × layers × heads × dim × seq_len × bytes
- **Optimization**: PagedAttention (vLLM), prefix caching

### Sparse / Linear Attention
| Variant | Complexity | Approximation | Use Case |
|---------|------------|---------------|----------|
| Longformer | O(N·w) | Local + global | Long docs |
| BigBird | O(N·√N) | Random + local + global | Long docs |
| Performer | O(N) | Kernel approx | Long context |
| Linear / RWKV | O(N) | Recurrent | Infinite context |

## Attention in Sources

### Netflix GenRec
- Prefill-only vLLM serving (no decode)
- Catalog-aware scoring head on top of attention output

### PonderPounce (System2 MLLM)
- **Causal context** = MLLM's native KV cache as episode memory
- Ponder accumulates observations in causal context
- Pounce receives compressed cognition token (single token + age)

### Unified Dynamics (2608.20965)
- Attention realizes "organizational conditions" for support recruitment
- Frozen inference projection recruits training-formed support
- Cross-architecture: Attention structure preserved in Transformer/Adam

## Key Seminar Points

1. **Attention is the bottleneck** for long-context scaling (O(N²))
2. **FlashAttention** makes exact attention feasible at 100K+ tokens
3. **KV cache** = working memory; prefix caching = semantic memory
4. **System2/System1** (PonderPounce): Slow deliberation builds context; fast action uses compressed token
5. **Harness intelligence** (JIT-Agent): Attention over tool/action space via planning module

## Related Concepts
- `concepts/machine-learning/transformer.md` (full architecture)
- `concepts/ai-engineering/agent.md` (System2/System1, KV cache as memory)

## Related Guides
- `guides/ai-engineering/build-rag.md` (retrieval + attention)
- `guides/ai-engineering/build-agent.md` (agent attention patterns)
