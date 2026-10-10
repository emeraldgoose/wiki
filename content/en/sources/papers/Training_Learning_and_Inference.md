---
title: "Training, Learning and Inference: Unified Dynamics"
description: "Training, learning and inference: unified dynamics of neural systems"
tags: [paper, source, huggingface, ai-engineering, neural-dynamics, transformer, resnet, diffusion]
locale: en
---

# Training, Learning and Inference: Unified Dynamics

**arXiv**: 2608.20965 | **Authors**: (single author) | **Key Framework**: Generation-Fact Graph (GFG)

## Full-Body Seminar Summary

### Core Contribution
Unified dynamical systems view of **training, learning, and inference** across neural architectures. Demonstrates neural networks are **stateful dynamical systems** — not static function approximators.

### Generation-Fact Graph (GFG)
**Atomic generation fact**: `f = (u, τ, ω, z; ρ)` — origin, realized transformation, concrete occurrence, generated result, relation role.
Compiled into **GFG**: AI-native, compilable scientific fact substrate preserving generation histories. Enables recursive scientific process: analysis → intervention → replay → validation → new facts.

### Unified Training-Learning Dynamics (nanoGPT)
**Training**: Evolution of a **parameter-optimizer system** with state and memory.
- Each training action enters receiving state
- Produces finite-amplitude nonlinear functional response
- Conditioned by state and **target-specific update geometry**

**Learning**: Persistent reorganization of distributed functional support by these responses.
- Capability formation, maintenance, decline, recovery observable via target-specific states vs readout boundaries

**Three primary coordinates**:
1. Target-boundary state
2. Target-specific update geometry
3. Parameter-Adam receiving state

→ **Second-order predictor** (before post-update outputs read): 91.43% accuracy, 91.49% macro recall on held-out runs (4 transitions)

### Inference as Frozen Projection
Inference = **frozen projection of training-learning dynamics**.
- Component gating & rollback show causal recruitment
- Non-additive combination of query-conditioned support formed during training
- Organizational conditions realized by **Attention**

### Cross-Architecture Validation
Same core relation structure preserved across:
- Transformer/Adam (nanoGPT)
- ResNet/SGD momentum (CIFAR-100)
- Diffusion U-Net/AdamW (CIFAR-10)

**Core structure**: Realized updates → receiving-state-dependent nonlinear responses → learning persistently reorganizes distributed functional support → frozen inference recruits training-formed support → feedback alters subsequent formation states.

### Key Insight
Neural networks are **stateful dynamical systems**. Training, learning, inference are not separate phases but a unified dynamical process with receiving-state conditioning, persistent support reorganization, and frozen inference projection. All protocols, experiments, checkers, evidence publicly available.

### Related Concepts
- `concepts/machine-learning/attention.md` (attention as organizational condition)
- `concepts/machine-learning/transformer.md` (training dynamics)
- `guides/ai-engineering/build-agent.md` (inference-time behavior)
