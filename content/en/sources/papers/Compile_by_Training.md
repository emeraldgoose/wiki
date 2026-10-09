---
title: "Compile by Training: Turning Natural-Language Specifications into Local Neural Functions"
description: "HuggingFace Daily Papers — 2026-09-03 — compile NL specs into local LoRA neural functions"
tags: [source, paper, huggingface]
locale: en
arxiv_id: 2609.04199
---

# Compile by Training: Turning Natural-Language Specifications into Local Neural Functions

**arXiv**: [2609.04199](https://arxiv.org/abs/2609.04199) | **HuggingFace**: [papers/2609.04199](https://huggingface.co/papers/2609.04199) | **Published**: 2026-09-03 | **Submitted by**: Yuntian Deng (University of Waterloo) | **Venue**: EMNLP 2026 System Demonstrations

**Authors**: Yuntian Deng, Pengyu Nie, Stuart Shieber

## Abstract

Many recurring text functions are easy to describe but difficult to implement with rules, while calling a large remote model for every input introduces repeated cost, latency, and provider dependency. This paper presents *compile by training*: turn a natural-language specification into a reusable neural function. At compile time, teacher models generate task-specific examples that train a small adapter for a compact interpreter. The resulting function runs without the teachers and can be stored, versioned, and composed like ordinary software. On FuzzyBench-Hard — a subset on which the Program-as-Weights (PAW) fast compiler produced no exact matches — compile by training reaches **83.6% semantic accuracy (LLM Exact Match)**, at a compile-time cost of roughly a minute versus seconds for the fast compiler. The authors deploy the compiler as a public interactive service (demo at programasweights.com) and demonstrate compiled functions in a multi-site website helper, a language-controlled 3D avatar, and a bidirectional English–Claudish translator.

## Background: Problem Setup (WHY)

The motivating example is an email-triage function: map "Signature needed by EOD" to `immediate`, but a newsletter to `wait`. The behavior is easy to describe and valuable across thousands of messages, yet tedious to encode as rules. A general-purpose remote LLM handles it, but every invocation pays network latency, provider cost, and external-service dependence.

The paper positions a large class of recurring text functions in this gap: **too fuzzy for conventional code, but too narrow and frequent to justify a large-model call per invocation**. The proposed reframing: adaptation becomes a *software build step* — use large models once, at compile time, to build a smaller reusable neural function; LLMs act as tool builders rather than run-time dependencies.

This work builds directly on Program-as-Weights (PAW, Zhang et al., 2026), in which a neural program specializes a shared local interpreter. PAW introduced an amortized compiler that predicts such a program in a single forward pass — fast (seconds), but spending the same fixed computation on every function. Compile by training retains the same program format and run-time interface, uses the amortized prediction as a starting point, and then invests additional computation in teacher synthesis plus specification-specific optimization. The paper asks three practical questions: (1) does the extra compile-time investment beat one-shot weight prediction, (2) can a minute-scale build stay usable in an interactive service, and (3) can independently compiled neural functions serve as components in larger applications?

## Methodology (HOW)

### System interface

Formally, the system exposes `p_s = Compile(s)`, `ŷ = Run(p_s, x)`, where `s` is a natural-language specification, `p_s` the compiled program, `x` a new input, and `ŷ` the output. A shared frozen LM is the interpreter; each compiled program supplies the adapter and prompt specializing it for one function. User workflow: **Specify** (describe a text-to-text function in NL) → **Compile** (submit a build job, monitor queue/training progress) → **Run** (open or download the completed program, invoke on new inputs through the SDK). The downloaded `.paw` artifact packages the specification plus the components needed to specialize the shared interpreter; it can be stored, versioned, cached, and reused. Compilation is hosted (specification goes to the PAW service and teacher APIs), but local SDK execution sends no future inputs to PAW or the teachers.

### Stage 1 — From specification to supervision

A specification alone has too few labeled examples to train on, so one or more teacher models synthesize a task-specific dataset `D_s = {(x_i, y_i)}, i=1..n ~ T(s)`. Teacher requests use a structured JSON format so generated examples enter the training pipeline automatically; the compiler validates each response and rejects malformed/incomplete batches. The public service combines a lower-cost teacher (most examples) with a larger teacher (complementary supervision). Example: for a spec extracting arXiv IDs from `/pdf/` links while ignoring `/abs/` links, a teacher-generated pair is `Input: "Check these papers: https://arxiv.org/pdf/2607.02512.pdf and https://arxiv.org/abs/2507.08800." → Output: ["2607.02512"]`.

### Stage 2 — Specialization and packaging

Training a full model per specification would be prohibitively expensive. Instead, all programs share a **frozen quantized Qwen3-0.6B interpreter**, and each function is a lightweight **LoRA adapter (rank 64, alpha 16)** plus a run-time scaffold — a compiler-generated prompt template encoding the free-form specification as structured task instructions/examples with a placeholder for the run-time input. The amortized PAW compiler provides initial adapter parameters θ_s^(0) and scaffold r_s (seconds), refined by minimizing `L(θ_s) = Σ_{(x,y) ∈ D_s} −log p_{θ_s}(y | r_s(x))` on a **100-step cosine schedule**. After optimization, adapter + scaffold + spec + interpreter metadata are packaged into program `p_s`.

### Interactive minute-scale compilation

Three engineering choices make tens-of-seconds builds interactive: (1) **Overlapping synthesis and training** — teacher requests, model loading, and training start concurrently; training begins once the first batch's examples arrive and blocks only if it catches up with synthesis, with incoming examples assigned to the earliest open batch slots. This shortens the critical path because teacher synthesis is slower and more variable than a training step. (2) **Coordinating jobs and reusing work** — API holds persistent job records, a shared queue dispatches to GPU workers, workers reuse cached teacher outputs before requesting new examples, and completed programs go to a shared artifact store linked to the job record. (3) **Interaction design** — compilation is a background build: users keep browsing while the UI reports queue position and training progress; jobs persist across navigation/reloads.

## Results

**Metric/benchmark.** Exact match is too strict (e.g., JSON differing only in whitespace/key order), so the paper reports **LLM Exact Match (LEM)**: fraction of predictions an LLM judge deems semantically correct given spec, input, reference, and prediction. The selected GPT-5.5 judge reaches 0.977 accuracy, Cohen's κ = 0.946 against 128 author labels. Benchmark is **FuzzyBench-Hard**: the subset of FuzzyBench specs where the PAW fast compiler produced zero exact matches (its LEM is still nonzero since some predictions are semantically right).

**Training vs. fast compiler.** Compile by training improves mean LEM by **+0.612 absolute, from 0.224 to 0.836**, at **50.9 s vs. 3.5 s** compile time.

**Supervision ablations (Table 1).** With 3600 unique pairs repeated into a 6400-example training set, a **2:1 mix of GPT-5.4-mini and GPT-5.5 raises mean LEM from 0.746 to 0.851** vs. mini alone. Data scaling: 1440 unique pairs → 0.821; 2400 → 0.836; 3600 → 0.836; 7200 → 0.866 (plateau between 2400–3600, further gain at 7200).

**Latency.** Cold compile of a representative spec at May-2026 launch: **50.9 s on B300, 68.2 s on H200, 99.2 s on RTX**; teacher synthesis dominates, so synthesis/training overlap directly shortens the critical path. Load test with 4 concurrent jobs: all completed, mean queue wait **1.01 s**, even worker utilization.

**Deployed applications.** (1) *paw-helper* website assistant: generic pipeline executor + site-specific content pack of **30 compiled programs (28 in live routing**, 2 for eval/back-compat), one backend serving four sites (author's homepage, Waterloo CS486 course site, NeuralOS, PAW site); router sends each page-aware question through a small subtree mixing compiled classifiers/answerers/selectors/validators with deterministic links and BM25 retrieval (e.g., CS486 "What changed about Assignment 1?" merges course-page and Piazza answers). (2) *Avatar Director*: NL command → small action DSL (sequences, durations, repetition, compatible parallel motions), browser-validated and rendered to animate a 3D character ("jump twice, then dance"); **43/44** hand-authored validation instructions produced the expected action structure. (3) *English↔Claudish translator*: one spec + one adapter per direction on the shared 0.6B interpreter; **100,747 successful web-demo requests between Aug 22 and Sep 2, 2026**.

## Limitations / Open Questions

- **Synthetic supervision inherits teacher errors.** The paper states applications needing guaranteed correctness should validate outputs or retain deterministic control paths — the division of labor in paw-helper (fuzzy decisions to compiled functions, exact ops to ordinary code) is the recommended pattern.
- **Evaluation is correctness + latency, not UX.** Application evidence focuses on composition and structured execution; systematic user studies are explicitly future work.
- **Cost/accuracy frontier is still rough.** +0.612 LEM costs ~15× compile latency; the 2400→3600 data plateau vs. the 7200 gain leaves the sample-efficiency curve open, as does when the fast compiler alone suffices.
- **Narrow interpreter scope.** All results use a single frozen 0.6B interpreter and text-to-text (or text-to-DSL) functions; generalization to other modalities, larger interpreters, or long-horizon agentic tasks is untested.

## Relevance to Software Engineers

- **New build artifact: the `.paw` program.** Treat a fuzzy text function like a compiled binary — version it, cache it, roll it back, and serve it from an artifact store. The Compile/Run split means secrets and vendor calls stay at build time; run time is local and offline-capable.
- **The "compile fuzzy specs" pattern is directly reusable.** Spec → teacher-synthesized JSON pairs (validated/rejected in pipeline) → LoRA (r=64, α=16, warm-started from an amortized predictor, 100-step cosine) on a frozen small model → packaged adapter + prompt scaffold. Concrete starting recipe: ~2400 unique pairs (the observed knee of the scaling curve), 2:1 cheap/strong teacher mix (+0.105 LEM in their sweep), streaming synthesis into training to hide teacher latency.
- **Compose, don't monolith.** paw-helper's proven topology: small compiled classifiers/routers/validators around deterministic retrieval, caching, and branch control — fuzzy models decide, ordinary code executes. Copy this for support bots, triage queues, and site assistants.
- **Latency budgeting numbers.** ~50 s cold compile on a B300-class GPU, ~1 s queue under 4-way concurrency, 3.5 s fast-compiler fallback — good enough for background builds with progress UI, not for blocking requests. Ship the fast compiler as default and offer fine-tuned compile as the "release build."
- **Where not to use it.** Anything needing correctness guarantees (billing, access control, medical/legal) must keep a deterministic validator or human approval after the neural function — teacher-distilled adapters can be wrong 14–17% of the time even after tuning.

## Related Concepts

- `concepts/ai-engineering/llm-training.md`
- `concepts/ai-engineering/agent.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.04199
- HuggingFace: https://huggingface.co/papers/2609.04199
- Demo: https://programasweights.com (playground, avatar, Claudish translator)
- paw-helper: https://github.com/programasweights/paw-helper
- Claudish translator code: https://github.com/programasweights/claudish
