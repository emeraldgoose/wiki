---
title: Knowledge Distillation
description: Transfer knowledge from a large teacher model to a smaller student model via soft targets, intermediate representations, or behavior matching
tags: [concept, machine-learning, knowledge-distillation, model-compression, teacher-student]
locale: en
---

# Knowledge Distillation

**Knowledge Distillation (KD)** is a model compression technique where a large, high-capacity **teacher model** transfers its knowledge to a smaller, more efficient **student model**. The student learns to mimic the teacher's behavior — output distributions, intermediate representations, or reasoning patterns.

## Core Concept

```
Teacher (Large, Accurate, Slow)  →  Knowledge Transfer  →  Student (Small, Fast, Deployable)
```

- **Soft targets**: Teacher's full probability distribution (logits/softmax with temperature)
- **Hard targets**: Ground truth labels (standard cross-entropy)
- **Temperature (T)**: Softens distribution; higher T reveals more inter-class relationships

## Distillation Objectives

### 1. Logit-Based (Output) Distillation — Hinton et al., 2015
**Forward KL (Standard KD)**:
```
L_KD = T² × KL(softmax(z_teacher/T) || softmax(z_student/T))
L_CE = CrossEntropy(student_logits, labels)
L_total = α × L_KD + (1-α) × L_CE
```
- **Temperature T**: Typically 2–10; higher = softer, more information
- **Weight α**: Balances distillation vs ground truth (typically 0.5–0.9)

**Reverse KL**:
```
L_rev = KL(softmax(z_student/T) || softmax(z_teacher/T))
```
- Mode-seeking; student matches teacher's high-probability modes
- Less prone to over-smoothing but can miss low-probability knowledge

### 2. Feature-Based (Intermediate) Distillation
- **Hint training**: Match intermediate activations (attention, MLP outputs)
- **Attention transfer**: Match attention maps (KD for attention)
- **FitNets**: Train student's intermediate layer to predict teacher's (Romero et al., 2015)

### 3. Relation-Based Distillation
- **Instance relations**: Match pairwise similarities (Gram matrices)
- **Instance-feature relations**: Match sample-to-feature correlations

### 4. Data-Free Distillation
- Generate synthetic data from teacher (GAN, inversion, or sampling)
- No access to original training data required

## Advanced Variants

### Mid-Training Distillation (Meta, 2026)
- **Setting**: Distillation during **continued pre-training** (mid-training), not post-training
- **Finding**: Forward KD behaves differently at mid-training vs pre-training:
  - Pre-training: Improves both reasoning AND factual recall
  - Mid-training: Improves reasoning but **slows factual recall acquisition**
- **Cause**: Teacher confidence asymmetry (higher on procedural vs knowledge-intensive data) + student's evolving knowledge state
- **Solution**: **Switch Distillation** — route by teacher predictive entropy:
  - High teacher confidence (low entropy) → distill (KD)
  - Low teacher confidence (high entropy) → cross-entropy
- **Result**: 1.61–1.71× reasoning; 1.13–1.19× knowledge; preserves 96.7% factual recall

### Online / Self-Distillation
- **Born Again Networks**: Sequential distillation (student → new student)
- **Self-Distillation**: Model distills from its own earlier checkpoints / ensembles
- **No external teacher needed**

### Progressive Distillation
- Start with high temperature, gradually anneal to T=1
- Curriculum: easy (soft) → hard (sharp) targets

### Quantization-Aware Distillation
- Jointly optimize distillation + quantization (PTQ/QAT)
- Student trained with quantization noise; matches quantized teacher behavior

## Training Strategies

### Teacher Selection
| Factor | Recommendation |
|--------|----------------|
| **Capacity gap** | Teacher 2–10× larger than student |
| **Architecture match** | Same architecture family preferred (but cross-arch works) |
| **Quality** | Best available teacher; ensemble > single |

### Data Considerations
- **Original training data**: Best if available
- **Unlabeled data**: Teacher generates soft labels (semi-supervised)
- **Synthetic data**: Teacher generates both input + output (data-free)
- **Domain mismatch**: Fine-tune teacher on target domain first

### Loss Scheduling
- **Static α, T**: Simple; works well in practice
- **Dynamic α**: Increase KD weight as student improves
- **Dynamic T**: Anneal temperature (high → low)

## Applications for LLMs

### Model Compression
- LLaMA-70B → LLaMA-7B/13B (Alpaca, Vicuna style)
- GPT-4 → smaller open models (distillation via API)

### Specialized Distillation
- **Reasoning distillation**: Teacher's CoT → student (CoT distillation)
- **Tool-use distillation**: Teacher's tool calls → student
- **Multilingual distillation**: Teacher's high-resource → student's low-resource

### Efficient Deployment
- Distill to **edge-friendly** sizes (1B–3B) for mobile/on-device
- Combine with **quantization** (INT4/INT8) + **pruning**

## Evaluation

### Fidelity Metrics
- **Output KL**: KL(teacher || student) on held-out data
- **Agreement rate**: Top-1 token match percentage
- **Distribution similarity**: JS divergence, cosine similarity of logits

### Capability Retention
- **Downstream benchmarks**: MMLU, GSM8K, HumanEval, etc.
- **Relative performance**: Student / Teacher score ratio
- **Emergent abilities**: Does student retain CoT, tool use, etc.?

### Efficiency Gains
- **Latency**: Token/s improvement
- **Memory**: Parameter count, KV cache reduction
- **Throughput**: Batch inference speedup

## Key References
- Hinton et al. (2015): "Distilling the Knowledge in a Neural Network"
- Romero et al. (2015): "FitNets: Hints for Thin Deep Nets"
- He et al. (2026): "Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall" (Meta)
- Zhang et al. (2024): "Switch Distillation: Adaptive Routing for Knowledge Distillation"
- Agarwal et al. (2024): "Distilling Step-by-Step: Outperforming Larger Models with Less Training Data"

## Related Concepts
- `concepts/ai-engineering/llm-training.md`
- `concepts/ai-engineering/model-quantization.md`
- `concepts/ai-engineering/model-pruning.md`
- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/speculative-decoding.md` (draft model training)