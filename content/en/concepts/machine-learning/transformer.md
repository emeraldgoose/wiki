---
title: Transformer
description: "Seminar-level concept: Transformer architecture, attention mechanisms, scaling laws, training dynamics"
tags: [concept, machine-learning, transformer, attention, llm, scaling]
locale: en
---

# Transformer

**Read from**: Source articles (Netflix GenRec, Spotify LLM A/B testing, Databricks monitoring, HuggingFace papers: Unified Dynamics, PonderPounce, JIT-Agent)

## Architecture

### Core Components
```
Input → Embedding → [Encoder/Decoder Layers] → Output
```

**Encoder Layer** (BERT-style):
```
Multi-Head Self-Attention → Add & Norm → Feed-Forward → Add & Norm
```

**Decoder Layer** (GPT-style):
```
Masked Multi-Head Self-Attention → Add & Norm
Cross-Attention (to encoder) → Add & Norm
Feed-Forward → Add & Norm
```

### Multi-Head Attention
```
Q = X·W^Q, K = X·W^K, V = X·W^V
Attention(Q,K,V) = softmax(Q·K^T / √d_k) · V
MultiHead = Concat(head_1...head_h) · W^O
```

### Key Properties
- **Parallelizable**: No recurrence (unlike RNN/LSTM)
- **Global receptive field**: Every token attends to all tokens
- **Scalable**: Depth + width + data → predictable improvement

## Scaling Laws (from Sources)

### Netflix GenRec
- Two-phase training: Foundation LLM (Phase 1) → Ranking post-train (Phase 2)
- Verbalization + context engineering instead of feature engineering
- Prefill-only vLLM serving

### HuggingFace: Unified Dynamics (2608.20965)
- Training = parameter-optimizer system evolution with state/memory
- Learning = persistent functional reorganization
- Inference = frozen projection of training-learning dynamics
- Cross-architecture validation: Transformer/Adam, ResNet/SGD, Diffusion/AdamW

### HuggingFace: JIT-Agent (2608.25593)
- Harness intelligence orthogonal to model scaling
- JIT-generated harnesses competitive with OpenCode/Claude Code
- Harness = 4 modules: memory, planning, action protocol, tool orchestration

## Training Dynamics

### Phase 1: Pre-training
- Next-token prediction on massive corpus
- Learn: language, world knowledge, reasoning patterns
- Scaling: loss ∝ compute^(-α) (power law)

### Phase 2: Post-training / Fine-tuning
- Instruction tuning, RLHF, DPO, GRPO
- Task-specific adaptation
- **Context engineering** (Netflix): verbalize history, token budget management

### Phase 3: Alignment / Specialization
- Reward modeling (Netflix: long-term member value)
- Catalog-aware heads (Netflix GenRec)
- System2/System1 decoupling (PonderPounce)

## Key Optimizations (from Sources)

### Memory/Efficiency
- **FlashAttention**: IO-aware exact attention (H100+)
- **KV Cache**: Reuse key/value across decoding steps
- **Quantization**: FP8, INT4, GPTQ, AWQ
- **Prefill-only serving** (Netflix): Avoid decode cost for ranking

### Parallelism
- **Tensor Parallel**: Split layers across GPUs
- **Pipeline Parallel**: Split layers across stages
- **Data Parallel**: Replicate model, shard data
- **Sequence Parallel**: Split sequence length

## When to Use (vs Alternatives)
| Task | Transformer | RNN/SSM | Tree/Graph NN |
|------|-------------|---------|---------------|
| Language modeling | ✅ | | |
| Long-context (>100K) | | ✅ (Mamba, RWKV) | |
| Structured reasoning | | | ✅ |
| Multimodal | ✅ (CLIP, Flamingo) | | |

## Related Sources
- `sources/articles/netflix-techblog.md` (GenRec two-phase)
- `sources/articles/spotify-engineering.md` (LLM A/B testing)
- `sources/papers/Training_Learning_and_Inference.md` (training dynamics)
- `sources/papers/PonderPounce.md` (System2/System1)
- `sources/papers/JIT-Agent.md` (harness intelligence)

## Related Guides
- `guides/ai-engineering/build-rag.md`
- `guides/ai-engineering/build-agent.md`
