---
title: Speculative Decoding
description: Accelerate LLM inference by using a small draft model to generate tokens verified by the target model in parallel
tags: [concept, ai-engineering, llm-inference, speculative-decoding, optimization]
locale: en
---

# Speculative Decoding

**Speculative Decoding** (also called **Speculative Sampling** or **Assisted Decoding**) is an inference acceleration technique where a small, fast **draft model** generates candidate tokens that are verified in parallel by the large **target model**. Accepted tokens are kept; rejected tokens trigger rollback and target model generation.

## Core Idea

```
Traditional:  Target model generates token by token (sequential, slow)
Speculative:  Draft model → generates K tokens fast → Target verifies all K in 1 forward pass
```

- **Draft model**: Small (e.g., 7B), fast, trained to mimic target
- **Target model**: Large (e.g., 70B), slow, high quality
- **Verification**: Single forward pass of target model on draft tokens + context
- **Acceptance**: Sequential from first token; stop at first rejection

## Algorithms

### Standard Speculative Decoding (Chen et al., 2023)
1. Draft model generates γ tokens autoregressively
2. Target model scores all γ tokens in one forward pass (with KV cache)
3. Accept tokens sequentially while `p_target(t) / p_draft(t) ≥ random()`
4. On rejection: sample from corrected distribution `p_target - p_draft` (renormalized)
5. Resume from accepted prefix

### EAGLE (Efficient Accelerated Generation with Lookahead) — Li et al., 2024
- **Insight**: Draft model doesn't need to be a small LLM; can be a lightweight **regression head** on target's hidden states
- **EAGLE-2**: Feature-based drafting; predicts next token from target's last-layer hidden state
- **EAGLE-3**: Adds dynamic draft length; verification-aware training

### Medusa (Cai et al., 2024)
- **Multiple decoding heads** on target model (frozen backbone)
- Each head predicts a different future position (tree-structured draft)
- Verifies multiple branches in parallel; higher acceptance rate

### Lookahead Decoding (Fu et al., 2024)
- **No draft model needed**: Uses n-gram matching or Jacobi iteration on target's own logits
- **Jacobi iteration**: Fixed-point iteration on target's next-token distribution
- Simpler deployment; works with any model

## Key Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Acceptance Length** | Avg tokens accepted per verification round | Higher = better speedup |
| **Acceptance Rate** | Accepted / Drafted | 0.7–0.9 typical |
| **Speedup** | Wall-clock time reduction vs vanilla | 1.5×–3× typical |
| **Quality Preservation** | Output distribution match | Identical to target (theoretically) |

## Training Draft Models

### Distillation-Based
- Train draft to mimic target's next-token distribution (KL divergence)
- Data: Target model generations or shared training corpus
- Challenge: Draft capacity << Target capacity → approximation error

### Verification-Aware Training (VAT) — NAVER AI, 2026
- **Verification Head**: Lightweight classifier predicting if each position survives verification
- **Verification-Adaptive Weighting**: Full weight up to first rejection; decay re-anchored there
- **Result**: 11.4% acceptance length improvement; 8.7% wall-clock speedup

### Self-Speculative (No Separate Draft)
- **Early-exit layers**: Use intermediate layers as draft
- **Skip layers**: Periodically skip layers for draft generation
- Trade-off: Simpler deployment vs lower acceptance rate

## Practical Considerations

### Memory Overhead
- Two models in GPU memory (draft + target)
- KV cache for both during verification
- **Mitigation**: Quantize draft (INT4/INT8); share embeddings; offload draft to CPU

### Quality Guarantee
- **Theoretically exact**: Output distribution matches target exactly (with proper rejection sampling)
- **Practically exact**: Floating-point differences negligible
- **No quality degradation** if implemented correctly

### When It Works Best
- **Large target models** (70B+): Higher absolute speedup
- **Long generations**: Amortizes draft overhead
- **High arithmetic intensity**: Target compute-bound (not memory-bound)
- **Batch size = 1**: Speculative shines at low batch; at high batch, target saturates GPU

### When It Struggles
- **Small targets** (<7B): Overhead not worth it
- **Highly structured output** (code, JSON): Draft may violate constraints
- **Memory-constrained**: Two models may not fit
- **High batch inference**: Target already saturated; speculative adds overhead

## Deployment Patterns

### vLLM Integration
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-70B-Instruct",
          speculative_model="meta-llama/Llama-3-8B-Instruct",
          speculative_draft_tensor_parallel_size=1)

outputs = llm.generate(prompts, SamplingParams(max_tokens=512))
```

### TensorRT-LLM / SGLang
- Native speculative decoding support
- Optimized kernels for verification pass
- Multi-GPU tensor parallelism for both models

## Key References
- Chen et al. (2023): "Accelerating Large Language Model Decoding with Speculative Sampling"
- Leviathan et al. (2023): "Fast Inference from Transformers via Speculative Decoding"
- Li et al. (2024): "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty"
- Cai et al. (2024): "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads"
- Gu et al. (2026): "Verification-Aware Training for Speculative Decoding" (NAVER AI)
- Fu et al. (2024): "Lookahead Decoding: Speculative Decoding without Draft Model"

## Related Concepts
- `concepts/ai-engineering/llm-inference.md`
- `concepts/ai-engineering/llm-serving.md`
- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/model-quantization.md`