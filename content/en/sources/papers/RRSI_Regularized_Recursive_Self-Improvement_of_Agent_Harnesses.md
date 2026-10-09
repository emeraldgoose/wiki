---
title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
description: "RRSI regularizes recursive harness self-improvement on both proposal and selection sides, keeping evolve gains while transferring up to 4.7 points out of distribution on 30 percent fewer policy tokens."
published: "2026-09-21"
arxiv_id: "2609.24972"
hf_url: "https://huggingface.co/papers/2609.24972"
authors: "Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhang, Yoonho Lee, Chengsong Huang, Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao, Burak Gokturk, Tomas Pfister, Chen-Yu Lee"
organization: "Google Cloud AI Research"
tags: [source, paper, huggingface, agents, agent-harness, self-improvement, regularization]
locale: "en"
---

# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses



**arXiv**: [2609.24972](https://arxiv.org/abs/2609.24972) | **HuggingFace**: [papers/2609.24972](https://huggingface.co/papers/2609.24972) | **Published**: 2026-09-21 | **Organization**: Google Cloud AI Research | **Submitted by**: Peng Xia | **Upvotes**: 168

**Authors**: Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhang, Yoonho Lee (Stanford), Chengsong Huang (WashU), Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao (UNC-Chapel Hill), Burak Gokturk, Tomas Pfister, Chen-Yu Lee

**Code**: [github.com/google-research/rrsi](https://github.com/google-research/rrsi) · **Project**: [regularized-rsi.com](https://regularized-rsi.com/)

## Abstract

An LLM agent's capability is largely magnified by its harness, namely the prompts, control flow, tooling, memory, and context management surrounding the frozen backbone model. Recent methods increasingly automate this process by iteratively proposing and selecting component-wise edits of an agent harness, practically establishing a form of recursive self-improvement (RSI) at the agent-system level. However, such recursive evolution may overfit by memorizing the training tasks, showing large in-distribution gains that shrink or even vanish on out-of-distribution benchmarks. We introduce Regularized Recursive Self-Improvement of Agent Harnesses (RRSI), which incorporates the principles of regularizations into harness self-improvement by constraining the evolution candidate proposal and selection. The proposer operates with a temporally annealed budget, limiting how many edits a candidate can bundle, and it encourages unexplored trajectories based on evolution history. The selector is equipped with a critic and a pruner: the critic screens benchmark-specific proposals, while the pruner removes changes that are too small, too expensive, or no longer useful. Together these constraints favor reusable agent mechanisms over benchmark-specific ones or even noises. Across eight benchmarks spanning coding, agentic workspace and engineering design tasks, RRSI gains up to 14.1 points on the split it evolves against and up to 4.7 points on the five out-of-distribution benchmarks, while producing a harness that runs on 30% fewer policy tokens than the unregularized evolution.

## Background and Problem Setup

A modern agent is a system, not a model: a frozen backbone wrapped in a harness of system/task prompts, control flow (plan, act, reflect, stop), tool interfaces and descriptions, memory and skill files, and context management. Recent product gains came more from harness engineering than new weights — but manually, progress is bounded by how many trajectories an engineer can read. Automating the loop (Meta-Harness, AHE, TTHE, HarnessX and others) creates practical RSI: the current system's feedback improves the harness that shapes its next behavior.

The failure mode RRSI attacks is adaptive overfitting. Each round reuses the same finite evolve set to propose and select edits, so evolve-set scores can climb via three coupled behaviors: benchmark-specific fitting (encoding task names, entities, judge-pleasing phrasing), noise chasing (stochastic winners promoted to permanent state), and complexity accumulation (edits that add tokens/steps without adding mechanism). Prior methods show exactly this: large evolve gains that shrink or vanish out of distribution, with some finishing below the starting harness H0.

RRSI's stance: keep the harness fully editable (prompts, control flow, tools, memory, subagents — anything), but regularize the search trajectory through that space, on both the proposal side (how much adaptive capacity one round may spend, and where) and the selection side (which measured improvements may become permanent).

## Methodology

Formally the agent is A = (policy, H) with score S(H; D) and policy-token cost C(H; D) averaged over tasks and sampled trajectories. Each round t executes Ht on the evolve set, summarizes feedback Ft, proposes candidates Ht+1 from P(·|Ht, Ft), evaluates on the same evolve set, and keeps the argmax. RRSI constrains P and the acceptance rule with classical-regularization analogues (L0-style update sparsity, Ridge-style cost shrinkage, Lasso-style structural pruning).

**Proposal side.**

- *L0-style annealed update sparsity.* One candidate may bundle at most bt independently attributable edits, with bt following a cosine anneal from bmax down to bmin over T rounds. Early rounds can combine coordinated changes to discover mechanisms; late rounds become sparse and attributable, so any measured change maps to an identifiable mechanism.
- *Evidence-aware credit assignment.* Every evaluated candidate logs its component, hypothesis, diff, score/cost deltas, and accept/reject. The proposer conditions on this full history: rejected mechanisms stay negative evidence, successful ones keep explicit credit — so the search stops re-spending capacity on falsified hypotheses (adaptive-data-analysis discipline).
- *Structured exploration.* When progress over the last w rounds stays inside the empirical noise band δ, part of the budget is reserved for components never yet exercised (e.g. stop rewriting prompts, go touch control flow or memory). Diversity/entropy regularization for edit families.

**Selection side (all non-compensatory — a candidate must pass every gate).**

- *Leakage screening.* Before any evaluation, a critic LLM reads each diff and rejects task names, entity names, task-specific values/answers, benchmark-specific logic, and inert machinery. Generic prompt/tool improvements pass. Screening pre-evaluation matters: a leaking candidate never gets the inflated score that would attract later rounds.
- *Stability-aware acceptance.* A pre-evolution noise band δ is estimated by repeatedly evaluating the unchanged base harness. The best evolve score so far S* sets a floor: candidates must satisfy S_hat(H') >= S* − δ, blocking downhill walks through individually-noise-sized regressions.
- *Ridge-style complexity-aware acceptance.* For gains above the noise band (ΔS > δ), additional inference cost must be justified: ΔC <= β0 + β1·ΔS, where ΔC is relative policy-token change. β0/β1 are fixed on the evolve set. Within-noise candidates follow a stricter rule (appendix). Aggregate footprint shrinks without forcing any single component out.
- *Lasso-style structural pruning.* Components exercised over a fixed window without strictly positive measured gain are reported as deletion targets. Mechanisms must keep earning their place; score-only evolution otherwise never removes anything.

Setup for the reported runs: frozen policy Claude Opus 4.8 in all domains (plus a Gemini 3.5 Flash replication); proposer, failure-feedback analyst, and leakage critic all Claude Opus 4.8; base harnesses Terminus-2 (coding), ReAct over MCP tool gateway with dynamic toolbelt and ReSum-style context management (workspace/design).

## Results

Eight benchmarks in three domains; each harness evolves on one suite and runs unchanged everywhere else. No held-out split regresses.

- **Overall transfer.** Evolve-split gains: +6.0 on Terminal-Bench 2.1, +4.9 on EngDesign, +1.1 on Harvey LAB. What survives elsewhere: SWE-bench Verified +1.8 (never scored during evolution), Harvey LAB in-distribution held-out +2.3, the three OOD agentic benchmarks +3.5 to +4.7 (7.2–13.1% relative), Frontier-Eng +4.3 Medal points (+24.3% relative).
- **Head-to-head on agentic workspace** (same H0, evolve set, candidate budget; H0 = 89.4 evolve / 86.9 ID held-out / 36.0 JobBench / 48.8 GDPval / 34.2 APEX): every prior method wins evolve but collapses OOD — Meta-Harness +0.9 OOD-average, HarnessX flat at base, AHE and TTHE below H0 (TTHE −1.7). RRSI posts the *smallest* evolve gain (90.5) and the only OOD average clearing H0 by more than a point (43.6 vs 39.7): JobBench 40.7, GDPval 52.3, APEX-Agents 37.9.
- **Ablations** (OOD avg over JobBench/GDPval/APEX): full RRSI 90.5 evolve / 43.6 OOD / 2.42M tokens per trial; w/o proposal regularizers 90.7 / 41.9 / 2.69M; w/o acceptance regularizers 91.5 / 41.0 / 3.59M; unregularized 92.8 / 40.3 / 3.80M. Removing either side raises evolve score and lowers transfer — the trade the regularizers are designed to make.
- **Policy robustness.** Independent coding evolutions: Gemini 3.5 Flash 64.6→78.7 on Terminal-Bench (+14.1, the paper's headline evolve number) with +2.2 transfer to SWE-bench Verified (76.8→79.0); Claude Opus 4.8 74.2→80.2 (+6.0) with +1.8 transfer (82.0→83.8). A harness evolved with Gemini 3.5 Flash still helps unseen Gemini 3.1 Flash Lite (11.2→14.6, +30.4% relative) — mechanisms, not policy-specific fits.
- **Efficiency.** RRSI is the lightest evolved harness: 2.42M policy tokens/trial vs 3.59–3.82M for priors (AHE +58% tokens for −4.4 OOD points), 26.3 steps/trial vs 27.3–34.6. Unevolved H0 is still cheapest (1.56M, 21.2 steps) — evolution buys part of its gain with test-time compute; the budget decides how much. Headline: 30% fewer policy tokens than unregularized evolution.
- **Not judge hacking.** Harvey LAB/JobBench/GDPval use judge grading, but EngDesign/Frontier-Eng grade via deterministic simulators/testbenches — gains survive there unchanged.

## Limitations and Open Questions

- Backbone weights stay frozen; nothing here covers weight-updating RSI or co-evolution of model and harness.
- RRSI still needs a finite evolve set plus several hyperparameters (budgets, windows, β0/β1, noise band); effectiveness depends on feedback quality and search budget.
- Transfer is shown across 8 benchmarks, 3 domains, and 2–3 policy families, but substantially different architectures, tool ecosystems, and much longer self-improvement horizons remain unvalidated.

## Relevance to Software Engineers

- If you auto-tune agents against a fixed eval set, copy the gates: leakage critic before scoring, noise-band floor before accepting, cost-justified acceptance (ΔC <= β0 + β1·ΔS), and pruning of components that stop earning their place. Each maps to a real overfitting behavior (benchmark fitting, noise chasing, complexity creep).
- Anneal edit-bundle size over the run: broad exploration early, sparse attributable edits late. The ablation shows proposal steering alone is worth +1.7 OOD points at nearly identical evolve score.
- Measure transfer, not evolve score: the best evolve harness in the paper (92.8) is the worst transfer harness (40.3 OOD). Ship the harness with the best held-out/cross-benchmark numbers per token, which here is also the cheapest evolved harness.

## Related Concepts

- [Agent](../../concepts/ai-engineering/agent.md)
- [Agent Evaluation](../../concepts/ai-engineering/agent-evaluation.md)
- [LLM Training](../../concepts/ai-engineering/llm-training.md)

## References

- arXiv: https://arxiv.org/abs/2609.24972
- HuggingFace: https://huggingface.co/papers/2609.24972
- Code: https://github.com/google-research/rrsi
- Project: https://regularized-rsi.com/
