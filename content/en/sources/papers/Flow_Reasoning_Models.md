---
title: "Flow Reasoning Models: Turning Flows Into Efficient Recurrent Reasoners"
description: "Flow Reasoning Models turn discrete flow language models into recurrent reasoners via self-conditioning, stabilized by Fixed-Point Forcing; 99.5 percent Sudoku-Extreme at 44x fewer FLOPs"
tags: [source, paper, arxiv, flow-models, reasoning, diffusion, test-time-scaling]
locale: en
arxiv_id: 2606.29150
published: 2026-08-28
---

# Flow Reasoning Models: Turning Flows Into Efficient Recurrent Reasoners

**arXiv**: [2606.29150](https://arxiv.org/abs/2606.29150) (v2 read; v3 retitled, content equivalent) | **HuggingFace**: [papers/2606.29150](https://huggingface.co/papers/2606.29150) | **Published**: 2026-08-28 (v1: 2026-06-28) | **Authors**: Alec Helbling*, Andrey Bryutkin* (co-first), Mauro Martino, Duen Horng (Polo) Chau, Nima Dehmamy, Hendrik Strobelt — MIT-IBM Computing Research Lab, IBM Research, Georgia Tech, MIT | **License**: CC BY 4.0

## Lead summary

Structured reasoning (Sudoku, Zebra puzzles, mazes) requires making and revising many interdependent decisions until they are globally consistent. Autoregressive models commit tokens in a fixed order and cannot revise; masked diffusion models predict tokens in parallel but cannot condition same-step updates on each other. Flow Reasoning Models (FRMs) take a third path: start from a discrete flow language model that denoises all tokens jointly, then add a **recurrent refinement axis** by self-conditioning the denoiser on its own past predictions. The key technical contribution, **Fixed-Point Forcing (FPF)**, fixes the exposure bias that otherwise makes recurrence converge to confidently wrong answers: it trains each update on carries produced by the model's own rollout dynamics while keeping the standard flow-matching objective untouched (no backpropagation through time). Result: 99.5% on Sudoku-Extreme, 100.0% on Zebra, 99.9% on Maze-Unique — matching the next-best method's peak with **44x fewer inference FLOPs** — and convergence itself becomes a near-perfect predictor of correctness (AUROC 1.00).

## Abstract (full scope)

The paper frames structured reasoning as conditional generation: given a problem specification $c$ (Sudoku clues, maze layout), generate a discrete solution $y$. A naive discrete flow (their FLM baseline) solves only ~13% of Sudoku-Extreme puzzles. FRMs feed each clean prediction back as the state to refine, creating an interpretable recurrent state that decodes directly into the current candidate solution, with training-efficient recurrence (no BPTT, canonical flow-matching loss retained). Self-conditioning alone lifts Sudoku-Extreme from ~13% to ~33%, but most problems remain unsolved. A dynamical-systems reading explains why: recurrence is learned fixed-point iteration, and conventional self-conditioning converges to **spurious fixed points** — confident, self-consistent, wrong. FPF trains on rollout-derived conditioning states so the model learns to correct states its own dynamics produce. Under FPF, correct solutions become stable attractors, incorrect states stay transient, and convergence predicts correctness.

## Background

- **Autoregressive models** commit tokens left-to-right with teacher forcing; an early bad token cannot be revised once its global consequences surface. The paper's plain causal-decoder baseline exists only to contextualize this.
- **Masked diffusion language models** (MDLM, Sahoo et al. 2024; ReMDM; Adaptive MDLM) denoise in parallel with flexible order, but same-step token updates are conditionally independent given the current state — aggressive parallel updates risk inconsistency, so hard problems need many conservative steps plus extras like remasking.
- **Discrete flow models** (Flow Language Models / FLMs, Flow Map LMs, Embedded Language Flows) model all tokens and interdependencies simultaneously via Gaussian-to-one-hot probability paths. Strong at unconditional generation, but nearly unexplored for structured reasoning — the paper's own FLM baseline gets 13.9% on Sudoku-Extreme, 67.9% on Zebra.
- **Recurrent reasoners** (HRM, TRM, FPRM, Equilibrium Reasoners/EqR) scale test-time compute through weight-tied recurrence and attractor dynamics. FRMs share the attractor intuition but keep a standard non-causal [Transformer](../../concepts/machine-learning/transformer.md)-based DiT backbone and the standard flow objective — a deliberate path toward scaling to larger models and less specialized domains rather than a bespoke architecture.
- **Self-conditioning** (Analog Bits, Chen et al. 2023) previously improved unconditional generation; **scheduled sampling** (Bengio et al. 2015) and **Self Forcing** (Huang et al. 2025, video diffusion) are the classic references for the exposure-bias problem FPF addresses.

## Methodology

### Discrete flows for conditional reasoning

Only the solution $y = (y_1, \dots, y_L)$ over vocabulary $\mathcal{V}$ is noised; the problem $c$ is fixed conditioning. The solution is encoded as a one-hot endpoint $x_1 \in \{0,1\}^{L \times |\mathcal{V}|}$, decoded by positionwise argmax. Flow matching connects noise $\varepsilon \sim \mathcal{N}(0,I)$ to the endpoint via the linear interpolant:

$$x_t = (1-t)\varepsilon + t x_1, \qquad t \in [0,1] \tag{1}$$

The denoiser $D_\theta^t(x_t \mid c)$ uses the categorical clean-prediction parameterization: it predicts the clean-token distribution per position, which both decodes into a candidate solution and defines the probability-flow velocity:

$$v_\theta^t(x_t \mid c) = (D_\theta^t(x_t \mid c) - x_t)/(1-t) \tag{2}$$

trained with tokenwise cross-entropy:

$$\mathcal{L}_{\mathrm{CE}}(\theta) = \mathbb{E}_{t,c,y,\varepsilon}\left[-\sum_{i=1}^{L}\log D_\theta^t(x_t \mid c)_{i,y_i}\right] \tag{3}$$

This vanilla model is the paper's FLM baseline — and the thing FRMs extend along a new recurrent axis.

### Self-conditioning as recurrence

The denoiser gains a carry input, $D_\theta^t(x_t \mid c, s)$, holding a previous clean-solution prediction ($s = \emptyset$ is the null carry). Training uses two passes: a null-carry pass produces the detached carry $\tilde{s} = \mathrm{stopgrad}[D_\theta^t(x_t \mid c, \emptyset)]$, and the supervised pass conditions on $\tilde{s}$ or null. Path and loss are unchanged; no gradients flow through the carry. At inference, holding $(x_t, t)$ fixed, recurrent refinement iterates:

$$s_t^{(0)} = \emptyset, \qquad s_t^{(k+1)} = D_\theta^t(x_t \mid c, s_t^{(k)}) \tag{4}$$

Reasoning depth $k$ is thus a discrete axis separate from flow time $t$; a sampler alternates advancing $x_t$ with extra recurrent updates. Every update directly estimates the same clean solution, so training needs no BPTT.

### Fixed-point view and exposure bias

Fixing $(x_t, c, t)$, Eq. (4) is fixed-point iteration over candidate solutions. Desired behavior: the gold solution $y^\star$ is attracting,

$$s_t^{(k)} \longrightarrow s_t^\star, \quad D_\theta^t(x_t \mid c, s_t^\star) = s_t^\star, \quad \mathrm{decode}(s_t^\star) = y^\star \tag{5}$$

while invalid states stay transient. Conventional training breaks this: the carry comes from a one-pass prediction on the ground-truth-derived interpolant, but inference carries come from the model's own closed loop —

$$p_{\mathrm{train}}(s \mid x_t, c, t) \neq p_{\mathrm{infer}}^{(k)}(s \mid \hat{x}_t, c, t) \tag{6}$$

with mismatch growing in depth. Two coupled effects: the denoiser misreads its own overconfident errors as evidence (amplifying them into spurious fixed points), and it never sees the subtle low-residual errors near convergence, so it never learns the final corrections. Empirically: solve rate plateaus while gold-target cross-entropy *rises* with depth.

### Fixed-Point Forcing (FPF)

FPF replaces the one-pass carry with a detached carry from the model's own multi-step inference dynamics: sample supervision time $t$ and rollout start $t_{\mathrm{start}} \sim \mathcal{U}(0,t)$, run the inference-time self-conditioned integrator from $t_{\mathrm{start}}$ to $t$, detach its final prediction $s_{\mathrm{FPF}}$, and supervise $D_\theta^t(x_t \mid c, \mathrm{stopgrad}(s_{\mathrm{FPF}}))$. Crucially, the loss-bearing input stays on the canonical interpolant $x_t = (1-t)\varepsilon + ty$ with target $y$ — FPF changes only the *carry distribution*, never the supervised state or objective. Deeper rollouts additionally expose the model to near-convergence residual errors, teaching local corrections around fixed points. Training is two-stage: Stage A trains self-conditioning from scratch; Stage B restarts optimizer/EMA from Stage-A weights and applies FPF. All runs use a non-causal DiT, AdamW, constant LR, EMA 0.9999 (per-dataset sizes: 7M/25M/8M params for Sudoku/Zebra/Maze).

## Results

Peak exact-solve rates (Table 1): **Sudoku-Extreme 99.5% (7M params), Zebra 100.0% (25M), Maze-Unique 99.9% (8M)** — top of every column against flow baselines (best: Adaptive MDLM 19.1%/98.3%/100.0%) and specialized recurrent reasoners (best: EqR 98.7% Sudoku-Extreme). On Sudoku-Extreme, FRM matches EqR's 98.7% peak with **44x fewer inference FLOPs** (operator-level profiled, batch-one forward pass x realized NFE), and leads the full accuracy–compute frontier on all three tasks.

Training-recipe ablation, three-seed means (Table 2):

| Variant | Sudoku-Extreme | Zebra | Maze-Unique |
|---|---|---|---|
| Base flow | 13.1 ± 0.7% | 62.3 ± 29.1% | 77.6 ± 16.7% |
| + Self-conditioning | 32.6 ± 3.7% | 36.9 ± 18.0% | 96.2 ± 3.0% |
| + Fixed-Point Forcing | **99.2 ± 0.3%** | **99.9 ± 0.2%** | **98.0 ± 1.8%** |

Note Zebra's seed variance collapses under FPF (29.1 → 0.2). On the easier Sudoku-Shah variant, self-conditioning alone suffices (30% → 99%) — FPF matters for hard constraint problems.

Dynamics diagnostics: under conventional self-conditioning the adjacent-state residual (token-averaged symmetric KL) predicts correctness at chance (AUROC 0.50); under FPF it reaches **AUROC 1.00** — convergence becomes an observable signature of correct reasoning (not a formal certificate). FPF keeps converting extra evaluations into corrected solutions with depth; the baseline saturates.

## Limitations and open questions

- Convergence-as-correctness is an empirical signature, explicitly not a correctness certificate.
- Solved-puzzle mean NFE is an oracle diagnostic (needs ground truth to know when to stop), so it is not deployable early stopping for every method; FLOPs are a lower bound ignoring memory traffic and overhead.
- Some Zebra baselines (MDLM/Adaptive MDLM published peaks) could not be reproduced in the authors' pipeline and enter tables only as daggered reference values.
- Demonstrated at 7–25M params on synthetic puzzles; scaling to larger models and less structured tasks is stated future work.
- Combined self-conditioning + preference-style objectives can be unstable in training (noted via the v1 FLOWDPO line, dropped in this version).

## Relevance to software engineers

- **Pattern**: any iterative-refinement sampler (diffusion/flow decoders, self-refine LLM loops) suffers the same train–inference distribution gap on its own intermediate states. FPF's fix is cheap and portable: train the refinement channel on rollout-generated states while keeping the supervised objective on clean data — no BPTT, minimal code change (one carry-construction swap).
- **Test-time scaling signal**: a calibrated convergence residual (adjacent-step symmetric KL ≈ 0 ⟺ likely correct) gives a label-free halting/confidence readout for agentic loops — e.g., stop iterating or escalate to a bigger model when the residual stays high.
- **Efficiency lesson**: 44x FLOP parity came from better dynamics, not a bigger model (7M params). For constraint-heavy generation (scheduling, config synthesis, query planning), small recurrent-refinement models can beat large one-shot ones.
- **Evaluation hygiene worth copying**: accuracy–compute frontiers from measured operating points only (no extrapolation), FLOP counting via profiler x realized evaluations, and pinning exact dataset revisions.

## References

- Paper: https://arxiv.org/abs/2606.29150 — HTML: https://arxiv.org/html/2606.29150v2
- Flow map language models (Lee et al. 2026, 2602.16813); Analog Bits (Chen et al. 2023, 2208.04202); Equilibrium Reasoners (Huang et al. 2026, 2605.21488); HRM (Wang et al. 2025a); TRM (Jolicoeur-Martineau 2025); Solve the loop (Fein-Ashley & Rashidinejad 2026, 2605.12466); Self Forcing (Huang et al. 2025); scheduled sampling (Bengio et al. 2015).
- Internal: [Transformer](../../concepts/machine-learning/transformer.md) (FRM backbone family: non-causal DiT).
