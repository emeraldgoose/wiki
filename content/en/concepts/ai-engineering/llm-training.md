---
title: LLM Training & Fine-Tuning
description: End-to-end workflow for pre-training, continued pre-training, supervised fine-tuning, and preference alignment of large language models
tags: [concept, ai-engineering, llm-training, fine-tuning, pre-training, rlhf]
locale: en
---

# LLM Training & Fine-Tuning

**LLM Training** encompasses the full lifecycle from raw text to aligned model: pre-training on massive corpora, continued pre-training on domain data, supervised fine-tuning (SFT) on instruction data, and preference alignment (RLHF/DPO) for human values.

## Training Stages

### 1. Pre-Training (Foundation)
**Objective**: Next-token prediction on massive diverse corpus (trillions of tokens)
- **Data**: Common Crawl, Wikipedia, code (GitHub), books, academic papers
- **Architecture**: Decoder-only Transformer (GPT, LLaMA, etc.)
- **Scaling Laws**: Compute-optimal allocation (Chinchilla: tokens ≈ 20× params)
- **Parallelism**: 3D/4D parallelism (DP + TP + PP + CP/EP)
- **Checkpointing**: Distributed checkpoint (ShardedTensor); async save

### 2. Continued Pre-Training (Domain Adaptation)
**Objective**: Adapt foundation model to domain-specific distribution
- **Data**: Domain corpus (code, legal, medical, finance, multilingual)
- **Ratio**: 1–10% of pre-training compute typically sufficient
- **Techniques**: 
  - **Rehearsal**: Mix % of original pre-training data to prevent catastrophic forgetting
  - **Learning rate**: Lower (1e-5 → 1e-6); warmup + cosine decay
  - **Tokenizer extension**: Add domain-specific tokens if needed

### 3. Supervised Fine-Tuning (SFT / Instruction Tuning)
**Objective**: Teach model to follow instructions and use tools
- **Data**: High-quality instruction-response pairs (50K–1M samples)
  - Human-annotated (Alpaca, Dolly, OpenAssistant)
  - Synthetic (Self-Instruct, Evol-Instruct, Magpie)
  - Distilled from stronger models
- **Format**: Chat templates (ChatML, Llama-3, Gemma, etc.)
- **Loss**: Next-token prediction on response only (mask prompt)
- **Hyperparameters**: LR 1e-5–2e-5; 1–3 epochs; packing for efficiency

### 4. Preference Alignment (RLHF / RLAIF / DPO)
**Objective**: Align with human preferences (helpful, harmless, honest)

#### RLHF (Reinforcement Learning from Human Feedback)
1. **Reward Model (RM)**: Bradley-Terry model on pairwise comparisons
2. **PPO**: Policy optimization with KL penalty vs SFT reference
3. **Challenges**: Reward hacking, training instability, high compute

#### DPO (Direct Preference Optimization) — Rafailov et al., 2023
- **No RM, no PPO**: Direct loss on preference pairs
- **Loss**: `log σ(β log π(y_w|x)/π_ref(y_w|x) - β log π(y_l|x)/π_ref(y_l|x))`
- **Simpler, stable, offline**: Preferred for most practical deployments

#### Variants
- **IPO**: Identity preference optimization (no reference model)
- **KTO**: Kahneman-Tversky optimization (binary feedback only)
- **SPIN**: Self-play fine-tuning (no human data)
- **SimPO**: Simpler DPO with length normalization

## Key Techniques

### Data Quality & Curation
- **Deduplication**: Exact + fuzzy (MinHash LSH) at document/paragraph level
- **Filtering**: Quality classifiers (fastText, GPT-based), toxicity, PII
- **Mixing**: Domain proportions tuned via scaling law experiments
- **Curriculum**: Easy → hard; domain-specific phases

### Memory & Compute Optimization
| Technique | Memory Savings | Use Case |
|-----------|---------------|----------|
| **ZeRO-3** | Full sharding (params/grads/opts) | Large models (>13B) |
| **FSDP** | PyTorch native sharding | Standard in PyTorch 2.0+ |
| **Activation Checkpointing** | Recompute vs store | All large models |
| **FlashAttention** | IO-aware attention kernel | 2× speedup, less HBM |
| **Sequence Parallelism** | Split sequence across GPUs | Long context (>32K) |
| **Context Parallelism** | Ring attention for ultra-long | 1M+ context |
| **BF16/FP8** | Reduced precision | H100+ (FP8); A100 (BF16) |

### Distributed Training
- **Data Parallelism (DP)**: Replicate model; split batch
- **Tensor Parallelism (TP)**: Split layers (attention heads, MLP)
- **Pipeline Parallelism (PP)**: Split layers across GPUs (micro-batches)
- **Expert Parallelism (EP)**: For MoE; route tokens to experts
- **3D/4D Parallelism**: Combine DP+TP+PP(+EP/CP) for 100B+ models

### Continued Pre-Training Strategies
- **Knowledge Distillation** (see `concepts/machine-learning/knowledge-distillation.md`): Teacher → student
- **Mid-Training Distillation**: Forward KL during continued pre-training (Meta, 2026)
- **Switch Distillation**: Entropy-based routing between KD and CE

## Evaluation During Training

### Perplexity & Loss Curves
- Train/val loss convergence; watch for divergence
- Domain-specific eval sets for continued pre-training

### Downstream Benchmarks
| Category | Benchmarks |
|----------|------------|
| **Knowledge** | MMLU, GPQA, TriviaQA |
| **Reasoning** | GSM8K, MATH, BBH, ARC |
| **Code** | HumanEval, MBPP, LiveCodeBench |
| **Long Context** | Needle-in-Haystack, RULER, LongBench |
| **Alignment** | MT-Bench, AlpacaEval, Arena-Hard |
| **Safety** | TruthfulQA, ToxiGen, WildGuard |

### LLM-as-a-Judge
- Use strong model (GPT-4, Claude) to evaluate outputs
- Structured rubrics > single-score
- Calibrate against human annotations

## Practical Recipes

### 7B Model SFT (Single Node, 8×A100)
```bash
torchrun --nproc_per_node=8 train.py \
  --model meta-llama/Llama-3-8B \
  --data data/sft.jsonl \
  --lr 2e-5 --epochs 3 --batch_size 4 \
  --gradient_accumulation 4 \
  --bf16 --flash_attn --fsdp full_shard
```

### 70B Model DPO (Multi-Node, 32×H100)
```bash
torchrun --nnodes=4 --nproc_per_node=8 train_dpo.py \
  --model meta-llama/Llama-3-70B \
  --data data/preferences.jsonl \
  --beta 0.1 --lr 5e-7 --epochs 1 \
  --bf16 --fsdp full_shard --tp 4 --pp 2
```

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Catastrophic Forgetting** | Pre-training knowledge lost | Rehearsal mix; lower LR; LoRA |
| **Reward Hacking** | High reward, nonsense output | KL penalty; RM ensemble; DPO |
| **Length Bias** | Verbose outputs preferred | Length normalization (SimPO); reward shaping |
| **Training Instability** | Loss spikes, NaN | Gradient clipping; LR warmup; BF16 |
| **Data Contamination** | Benchmark leakage | Dedupe vs benchmarks; holdout sets |

## Key References
- Kaplan et al. (2020): "Scaling Laws for Neural Language Models"
- Hoffmann et al. (2022): "Training Compute-Optimal Large Language Models" (Chinchilla)
- Touvron et al. (2023): "LLaMA 2: Open Foundation and Fine-Tuned Chat Models"
- Rafailov et al. (2023): "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
- He et al. (2026): "Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall" (Meta)
- Zhao et al. (2024): "SPIN: Self-Play Fine-Tuning Converts Weak Language Models to Strong Ones"

## Related Concepts
- `concepts/machine-learning/knowledge-distillation.md`
- `concepts/ai-engineering/rlhf.md`
- `concepts/ai-engineering/llm-serving.md`
- `concepts/ai-engineering/model-quantization.md`
- `concepts/machine-learning/transformer.md`