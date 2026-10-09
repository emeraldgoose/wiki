---
title: Running a Software Factory Efficiently at Uber Scale
description: Uber's cost equation and optimization levers for AI agent coding at scale — model selection, token efficiency, and managed-agent economics
tags: [source, uber, ai-engineering, agent, cost-optimization, software-factory]
locale: en
source_url: "https://www.uber.com/us/en/blog/efficient-software-factory/"
blog: uber
published_date: 2026-08-27
---

# Running a Software Factory Efficiently at Uber Scale

**Author**: Uday Kiran Medisetty (Distinguished Engineer)
**Source**: [Uber Blog](https://www.uber.com/us/en/blog/efficient-software-factory/)
**Date**: Aug 27, 2026

## Context

Over 70% of PRs at Uber are attributed to AI agents, with 3,600+ agent skills and 30K+ agent executions per day. From February to July 2026, weekly active users grew 7x and agent requests 9.4x, while total AI spend stabilized through optimization. Cost per 1K model requests fell ~34% from peak; cost per session fell 52% from its June peak.

## The Cost Equation

```
Total Spend = Users × Sessions/User × Turns/Session × Requests/Turn × Tokens/Request × Price/Token
```

Each term is independently measurable and optimizable — the article decomposes spend along these six drivers.

## Four Layers of Agent Usage

AI usage is organized into four layers, from most specialized to most general. Higher layers give Uber more control over cost, quality, and model selection:

1. Specialized managed agents (e.g. uReview code review)
2. Task-scoped coding agents
3. General-purpose coding assistants
4. Open-ended agent sessions

## Metrics by Layer

| Layer | Metrics | Answers |
|-------|---------|---------|
| Portfolio | Total cost, distinct users, per-tool cost | Where money goes |
| Unit Economics | Cost/user, req/user, cost/1K req, tokens/req, cost/1M tokens, cost/session | Tool getting cheaper? |
| Model Economics | Cost per model, cost/1K req, cost/1M tokens | Model releases changing bill? |
| Driver Decomposition | Adoption, engagement, input/output workload | Why number moved? |
| Managed Agent Outcomes | Cost/merged PR, cost/review, cost/alert, quality (revert rate, F1, MTTR) | Cheaper per value unit? |

## Optimization Levers

- **Price/Token**: Pareto-optimal model selection (benchmark-driven), model defaults
- **Tokens/Request**: 400K context cap, Medium reasoning, Prompt Caching, Tool search / CLI-resolved MCP, Code-mode batching, Gateway-routed SaaS MCPs
- **Requests/Turn**: Graph-grounded context, Continuous Skill Optimization
- **Visibility & Education**: Live cost counter in status line, spend tiers, session analysis dashboard

## Benchmark-Driven Model Selection (4 steps)

1. Define workload benchmark (real PRs with known bugs, graded easy/medium/hard)
2. Score: precision, recall, F1, cost/PR, latency, timeouts, noise
3. Pareto frontier: cost vs quality
4. Deploy Pareto-optimal config — and keep moving, as the frontier shifts every few weeks

**uReview example**: switching models improved F1 while dramatically reducing cost/PR. The Pareto-frontier visualization guides selection.

## Seminar Takeaways

- Decompose AI spend multiplicatively so each term maps to a concrete lever; portfolio-level totals alone cannot guide action.
- Benchmark on real work (graded by difficulty) and select on the cost–quality Pareto frontier rather than on headline model capability.
- Cap context and cache aggressively: tokens/request is the most controllable term at scale.
- Outcome metrics (cost per merged PR, revert rate, MTTR) matter more than raw token spend for managed agents.

## Related Concepts

- `concepts/ai-engineering/agent.md` (software factory agentic workflows)
- `concepts/ai-engineering/model-selection.md` (Pareto-optimal routing)
