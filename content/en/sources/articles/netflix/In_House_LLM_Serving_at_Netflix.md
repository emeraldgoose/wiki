---
title: "In-House LLM Serving at Netflix"
description: Self-hosted LLM stack on vLLM plus Triton — engine selection, model packaging, OpenAI-compatible API, versioned rollouts, constrained decoding
tags: [source, article, netflix, llm, model-serving, platform-engineering, ai-engineering]
locale: en
source_url: "https://netflixtechblog.com/in-house-llm-serving-at-netflix-a5a8e799ea2c"
blog: netflix
published: 2026-07-17
---

# In-House LLM Serving at Netflix

By the AI Platform Model Runtime and Inference teams. Unlike hosted-API consumers, Netflix runs the full LLM stack — deployment through inference — inside its existing production environment. The post covers the seriously-contested choices: engine selection, model packaging, API surface, deployment strategy, and output-constraint enforcement, including what production revealed that design didn't anticipate.

## Background: architecture

A unified JVM-based serving system fronts member-scale ML: routing/A-B logic, candidate generation, feature fetching, inference, post-processing, logging, with real-time and cached-batch paths. Small CPU models run in-process; large models delegate inference to the remote Model Scoring Service (MSS) — shared backend for XGBoost/TensorFlow/PyTorch/LLMs with NVIDIA Triton underneath (model loading, batching, GPU scheduling) plus a Java control plane (deployment, versioning, health, autoscaling, multi-region rollout).

## Methodology: four decisions in dependency order

**vLLM as paved-path engine.** Originally TensorRT-LLM (performant, Triton-integrated). By summer 2025 the workload mix (embeddings, prefill-only ranking/retrieval, autoregressive decoding, custom per-step constraint logic) plus closed open-source gaps triggered re-benchmarking: vLLM won on no-compile custom architectures, extensibility hooks for custom decoding, debuggability, and practitioner familiarity.

**Packaging: vLLM backend over Python backend.** Triton's Python backend freezes I/O tensor specs at packaging time, forcing coordinated packaging changes on every frontend upgrade; the vLLM backend reads a JSON config (weights + tokenizer) and generates specs dynamically — models and frontend evolve independently. Production caveats: Triton/vLLM version drift can break backend loading entirely (pin compatible versions; forbid author overrides), and custom pre/post-processing models still need the Python backend's full execute() control.

**Ecosystem-compatible HTTP frontend.** All models score via the same gRPC call (shared client libs, health checks, pipelines), but since the OpenAI-compatible API is the ecosystem default, it is exposed alongside gRPC via NVIDIA's Triton OpenAI frontend (embedded Triton server + TritonLLMEngine + FastAPI, KServe frontends retained for the Java control plane). Graduating hosted → fine-tuned self-hosted models becomes nearly seamless. One patched gap: response_format was silently dropped before vLLM (malformed JSON, no error) — fixed by git-subtreeing and translating it into guided-decoding parameters at request time.

**Deployment: Red-Black vs Versioned.** Red-Black (side-by-side, phased shift, atomic rollback) fails when a new version changes I/O schema: consumers can't update configs until the model is live, so old requests hit the new deployment mid-migration. Versioned deployments (independent deployment per modelId/modelVersion pair, consumer switches after readiness, cleanup after inactivity) close the gap at temporary extra GPU cost. Recommendation: embed variable configs (tensor shapes) in the model to stay version-agnostic on Red-Black; reserve Versioned for unavoidable breaking changes.

**Operational details.** Boot: materialize models on FSx at announcement (not S3/HF at startup) to bound cold starts; embedded vs standalone Triton per deployment; plugin install via entry_points; gate gRPC until ready. Observability: a lightweight HTTP proxy merges Triton's endpoint with vLLM's multiprocess .db metrics (Triton's bridge surfaces only 9 of 40+) into one /metrics.

**Constrained decoding at scale.** Business-logic constraints run inside the decode loop as per-request state machines emitting token-eligibility masks via vLLM's custom logits-processor interface. The V0 pure-Python per-request design was CPU/GIL-bound (latency growing linearly with batch size — invisible in single-request benchmarks). vLLM V1's batch-level processing plus a C++ multithreaded hot path made mask time flat vs batch size. Hardening: internal tracking for chunked-prefill partial prefills; state-machine reset on KV-cache preemption (token history shrinks non-monotonically).

## Results

A unified vLLM+Triton platform with a fast experimentation-to-production path; lessons concentrated in details (version pinning, silent API gaps, packaging trade-offs). Next: system-prompt compression, vLLM V1 async scheduling, GPU-fused vectorized logits processors, lower-precision variants.

## Limitations / open questions

- Version pinning between Triton and vLLM is operational toil on every upgrade.
- Constraint state machines must handle preemption/prefill edge cases manually — easy to get subtly wrong.
- Vectorized GPU logits processors and async scheduling are future work, not measured here.

## Relevance to SW engineers

- Don't make LLMs special snowflakes: reuse the same serving path, client libs, and deployment pipelines as every other model.
- Benchmark engines against *your* workload mix, not generic leaderboards; debuggability and handoff cost count.
- Decouple artifact evolution from frontend evolution (dynamic I/O specs) or pay coordinated-release tax forever.
- Load-test serving under realistic concurrency — serial-per-request bottlenecks hide in single-request benchmarks.

## Related concepts

- `concepts/ai-engineering/rag.md` (LLM inference infrastructure)
- `concepts/system-design/scalability.md` (rollout strategies, autoscaling)
