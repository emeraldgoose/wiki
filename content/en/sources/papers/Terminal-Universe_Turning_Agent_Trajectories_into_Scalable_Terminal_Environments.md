---
title: "Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments"
description: "HuggingFace Daily Papers — 2026-09-03 — reconstruct executable terminal environments from agent trajectories"
tags: [source, paper, huggingface]
locale: en
arxiv_id: 2609.04148
published: 2026-09-03
---

# Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments



**arXiv**: [2609.04148](https://arxiv.org/abs/2609.04148) | **HuggingFace**: [papers/2609.04148](https://huggingface.co/papers/2609.04148) | **Published**: 2026-09-03 | **Submitted by**: taesiri | **Paper of the day #2 (2026-09-04)**

**Authors**: Jie Wu, Zhenru Zhang, Beichen Zhang, Xuwu Wang, Yuhui Su, Mouxiang Chen, Peng Wang, Zhihai Wang, Que Shen, Hao Zhou, An Yang, Fei Huang, Yujiu Yang, Dayiheng Liu (Qwen Team, Alibaba Group; Tsinghua University)

## Abstract

As terminal-based code agents become prevalent, agent trajectories have accumulated at scale while realistic, executable environments remain scarce — yet environments are what agent post-training actually requires: each environment can be re-queried into many verifiable tasks and provides execution feedback, whereas a trajectory is a single frozen demonstration. Terminal-Universe inverts the usual mapping: instead of rolling out trajectories from environments, it reconstructs environments from trajectories, observing that the tool-execution history (reads, writes, edits) recorded in a trajectory exposes the structure and contents of the environment it ran in. The framework replays recorded file operations to restore each file to its pre-agent state (a partial workspace), then a completion agent supplies missing files and dependencies. On each recovered workspace it reconstructs the original intent task and synthesizes entirely new ones, scaled along two axes — breadth (cross-workspace queries spanning multiple codebases via mined dependency relations) and depth (single-turn queries extended into multi-round sessions via a user agent). Applied to public terminal agent trajectories, the pipeline yields **37.3k task-sufficient environments**; supervised fine-tuning of Qwen3.5-27B on the resulting corpus improves **Terminal-Bench 2.1 by 11.9 points** and **EvoCode-Bench v2 MT@4 by 13.8 points**.

## Background: Problem Setup (WHY)

A trajectory and an environment are not equally useful for post-training. A trajectory is a fixed record: its quality is bounded by the policy model that produced it, and there is no way to check whether the codebase changes it made are actually correct. An environment has none of these limits — the same task can be re-solved by a stronger model, the result verified with tests, and harder tasks posed on the same workspace. Expert benchmarks like Terminal-Bench show the gold standard (custom container + instruction + executable verifier per task), but that reliability comes from manual effort, which caps how many tasks can be built — while post-training needs far more environments than manual curation can supply.

Existing work scales executable environments three ways, and the paper positions against all three (Table 1): (1) **Repository-based methods** (SWE-Gym, R2E-Gym) roll a repo back via git to before a historical fix — realistic but bounded by available histories. (2) **Perturbation methods** (SWE-smith, CLI-Gym) inject bugs into passing repos — a few repos yield many tasks, but every task is a repair task. (3) **Task-conditioned synthesis** (Endless Terminal, TMax, CLI-Universe, SkillSynth) generates task and environment together from taxonomies or seeds — controllable, but untethered to real projects, so workspaces come out small and tidy rather than real. Reported scales: 3.2k–37.5k tasks, but none with both multi-round and cross-workspace synthesis. Terminal-Universe (37.3k envs, 32.0k tasks, verifier ✓, multi-round ✓, cross-workspace ✓) is the only entry covering all three.

## Methodology (HOW)

### Core inversion: trajectory–environment duality

A trajectory and an environment are two views of the same episode. Prior work maps environment → trajectory (rollout); Terminal-Universe inverts it (reconstruct + reuse). Tool calls already reveal the workspace: `Read` shows file contents, `Write`/`Edit` show how it changed. Recovery is inherently lossy (untouched files, implicit system deps, network resources leave no trace), so reconstruction runs in three stages.

### Stage 1 — Deterministic replay

Replay processes the trajectory's read, write, and edit operations chronologically to recover, per accessed path, the earliest and latest file contents visible in the trajectory. The reconstructed initial workspace collects each pre-existing file at its **earliest observed version, before the agent's first change**; agent-created files are excluded and the agent's edits recorded separately for later verification. Because the trajectory exposes only touched paths (and content may be truncated), the result is a **partial workspace**.

### Stage 2 — Agentic completion

A completion agent takes the partial workspace plus the recovered task, then creates missing files, completes partial files, and restores needed dependencies — **without implementing the solution**. This stage runs on all replayed workspaces.

### Stage 3 — Environment filtering

A completed workspace is useful only if it exposes enough project context for its task. An agentic judge with read-only shell/file tools labels each workspace sufficient or insufficient (source, config, data, structure) conditioned on the recovered task; only sufficient ones proceed. Every workspace runs in a standardized **Ubuntu 24.04 container with network access** — cheaper and simpler than repo-specific images, at a modest resolve-rate cost (per Zeng et al., 2026).

### Re-querying: four mechanisms

- **Intent Recovery.** Consolidate source user request(s) into a self-contained task: single-round trajectories use the sole substantive request directly; multi-round ones take the first substantive request as the topic and fold in later requests only when they clarify/constrain/extend it. Agent actions and file evidence aid interpretation, but only user-stated requirements are kept.
- **Single-WS synthesis.** An offline generator inspects each workspace and synthesizes **five candidate tasks** under groundedness, structural-diversity, and verifiability constraints; one valid candidate per environment goes to rollout and verification.
- **Cross-WS synthesis (breadth).** An agent profiles each workspace's domain and capabilities; candidate pairs come from **TF-IDF nearest-neighbor retrieval**, and an LLM judge identifies **directional dependency edges** where a target workspace lacks a capability present in a reference workspace. Exactly one task per pair: a writable target plus a read-only reference mounted at a separate path. The query states only target behaviors and the reference mount path — never reference internals — so the solver must navigate and adapt the reference implementation itself (e.g., porting a feature across projects).
- **Multi-Round sessions (depth).** After the initial response, a user agent continues the session with two mechanisms: (1) a **requirement tracker** (active/satisfied/updated) that adds, modifies, or replaces constraints each round; (2) **round-level verification** — the updated spec is committed, an automated verifier authors acceptance tests *before* the coding agent acts, and the solver is strictly isolated from test scripts and tracebacks. The user agent translates structured failures into natural user-visible complaints; intermediate failures stay in history as supervision for error diagnosis and recovery.

### Verification

Every new task ships with an agent-authored verifier written inside the container, and **only trajectories whose tests all pass are kept** — execution feedback, not imitation quality, is the selection gate.

## Results

- **Scale.** 37.3k task-sufficient environments and 32.0k tasks from public terminal agent trajectories. New queries are generated over these environments and solved with **Qwen3.7-Max as teacher** to produce training rollouts.
- **Post-training gains.** SFT of **Qwen3.5-27B** on the corpus: **+11.9 points single-round on Terminal-Bench 2.1** and **+13.8 points multi-round on EvoCode-Bench v2 (MT@4)** over the same base model.
- **Ablations.** Each component contributes; most notably, **re-solving tasks in reconstructed environments far outperforms imitating the raw trajectories** — the environment, not the demonstration, is the valuable artifact. Trajectory complexity correlates with rollout complexity (multi-file edits, long tool chains expose more workspace state → more diverse, harder tasks), and replaying multiple sessions on the same workspace merges their exposed state into reconstructions more complex than any single trajectory yields — i.e., the framework scales naturally as stronger agents produce richer trajectories.

## Limitations / Open Questions

- **Generic containers.** Standard Ubuntu 24.04 images instead of repo-specific environments (SWE-Factory, RepoLaunch style) — edge cases needing specialized system deps or complex builds lose fidelity.
- **Distribution bounded by sources.** Domain, language, and toolchain coverage of reconstructed workspaces cannot exceed what the collected trajectories cover.
- **Single teacher.** One teacher (Qwen3.7-Max) generates tasks, solutions, and verifiers — its capability gaps bound coverage and its solution errors may escape its own tests. Multiple teachers plus an independent verifier model are future work.

## Relevance to Software Engineers

- **Mine your agent logs, not just your repos.** If you run terminal coding agents at any scale, their trajectories are latent environments. The replay recipe (chronological file-op replay → earliest-version workspace → agentic completion without solution leak → sufficiency filter) is directly reusable for building internal post-training corpora.
- **Verify, don't imitate.** The headline ablation says SFT on raw trajectories is weak; verifier-gated re-solved rollouts are strong. Gate training data on executable tests, not on teacher prestige.
- **Cross-repo tasks are the realism gap.** Single-repo benchmarks under-test the dominant real workflow (read reference implementation → port/adapt). The target-writable + reference-read-only mount pattern is a cheap template for harder evals.
- **Multi-round harness pattern.** Requirement tracker + pre-action acceptance tests + solver/test isolation + failure-to-complaint translation is a concrete design for believable interactive evals and training sessions.
- **Where not to use it.** Don't treat reconstructed workspaces as faithful repo replicas for build-sensitive work — generic images and lossy replay mean system-level edge cases may not reproduce.

## Related Concepts

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## References

- arXiv: https://arxiv.org/abs/2609.04148
- HuggingFace: https://huggingface.co/papers/2609.04148
- Related: SETA (https://huggingface.co/papers/2607.10891), Endless Terminal / TMax / CLI-Gym / CLI-Universe / SkillSynth (see paper Table 1)
