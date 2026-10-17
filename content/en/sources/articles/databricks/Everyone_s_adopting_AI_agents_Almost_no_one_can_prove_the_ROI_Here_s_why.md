---
title: "Everyone's adopting AI agents. Almost no one can prove the ROI. Here's why"
description: Promoted on 2026-10-17
tags: [source, article, en]
locale: en
source_url: "https://www.databricks.com/blog/everyones-adopting-ai-agents-almost-no-one-can-prove-roi-heres-why"
blog: databricks
published: 2026-10-17
---

# Everyone's adopting AI agents. Almost no one can prove the ROI. Here's why

**Source**: Databricks Blog, 2026-10-13

**Lead**: Amber Roberts, Staff Technical Marketing Manager at Databricks, has spent years observing how AI actually gets used inside organizations—not just how it's pitched. In this conversation, she explains why "faster" is the wrong way to think about agentic AI, why so many companies struggle to show ROI on AI investments, and what must be true for an AI agent to be useful at work instead of just impressive in a demo.

## Why Speed Is the Wrong Way to Measure AI Productivity

Most conversations about AI productivity still focus on speed: doing the same tasks faster. Roberts argues this is the wrong lens for agentic AI. Traditional productivity meant how much work one person could do alone. In an agentic world, productivity means how much a person can accomplish with a team of AI assistants working alongside them—without sacrificing quality.

The shift is from individual throughput to *collaborative capacity*. An agent that completes a task in half the time but requires constant human correction is less valuable than one that takes the same time but operates autonomously with high reliability. The metric should be: how much high-quality work can a human + agent team produce together?

## The AI ROI Gap: Why Adoption Is Outpacing Proof

The "ROI gap" exists because the people buying AI and the people using it are often different, and most organizations are still in a trial-and-error phase figuring out which use cases actually work. Leadership approves budgets based on vendor demos and industry hype; practitioners discover that integrating agents into real workflows requires data plumbing, governance, and domain-specific context that demos gloss over.

Roberts notes that organizations typically go through three phases:
1. **Experimentation**: Broad, shallow trials across many use cases.
2. **Consolidation**: Doubling down on 2–3 use cases showing measurable signal.
3. **Operationalization**: Building the data, governance, and evaluation infrastructure to run those use cases reliably at scale.

Most companies are stuck between phases 1 and 2. The gap closes only when phase 3 investments are made.

## Redefining Productivity for an Agentic World

Productivity in an agentic world has three dimensions:
- **Throughput**: How much work gets done (traditional metric).
- **Autonomy**: How little human intervention is required per unit of work.
- **Quality**: How reliable and correct the output is without human review.

An agent that scores high on throughput but low on autonomy and quality creates "productivity theater"—impressive demos that don't translate to production value. The winning agents balance all three.

## Why Business Context Beats Raw Task Speed

The agents that create real value are the ones with business context: your data, your history, your constraints. Without it, an agent can only give generic advice, not decisions your company can act on. Roberts emphasizes that context isn't just "more data"—it's the *right* data connected to the agent's reasoning loop:
- Institutional knowledge (past decisions, tribal knowledge, post-mortems).
- Current state (live metrics, active incidents, in-flight projects).
- Constraints (compliance, budget, organizational politics).

An agent with context can say "don't do X because last quarter it caused Y"; an agent without context says "X is a best practice."

## The Agentic AI Playbook for the Enterprise

Roberts outlines a practical playbook:
1. **Start with a problem, not a capability**: Identify a specific, painful, measurable business problem. Then ask if an agent can help.
2. **Invest in context infrastructure first**: Unified data layer, lineage, governance—before buying agent frameworks.
3. **Build evaluation before deployment**: Define what "good" looks like for each use case. Automate evaluation so you can iterate.
4. **Design for human-in-the-loop, not human-out-of-the-loop**: The goal is amplification, not replacement. Plan for handoff, override, and audit trails.
5. **Measure what matters**: Track autonomy rate (percentage of tasks completed without human intervention), quality gates passed, and business outcome deltas—not just latency or token count.

## Where High-Value, Repeatable Use Cases Are Showing Up

Based on Databricks customer patterns, the highest-ROI agent use cases cluster in:
- **Code generation + review**: Agents that write, test, and explain code changes within the team's repo and standards.
- **Data analysis + reporting**: Agents that answer ad-hoc business questions by writing and executing SQL against governed data.
- **Incident response**: Agents that correlate logs, metrics, and recent changes to propose root causes and runbooks.
- **Knowledge synthesis**: Agents that answer "how do we do X here?" by searching docs, code, and past tickets.

These share a pattern: they operate on *structured, governed, proprietary data* with *clear correctness criteria*.

## Measuring Success: Old Metrics Still Matter, But They're Not Enough

Traditional metrics (latency, cost per token, throughput) are necessary but insufficient. Roberts recommends adding:
- **Autonomy rate**: % of end-to-end tasks completed without human intervention.
- **Quality gate pass rate**: % of agent outputs passing automated + human review.
- **Time-to-trust**: How long until a team trusts the agent enough to stop checking every output.
- **Business outcome delta**: The actual KPI movement (revenue, cost reduction, risk mitigation) attributable to the agent.

## The Most Common Mistake: Scaling Before It's Ready

The number one failure mode: scaling an agent to 100 users before it works reliably for 5. This burns trust, creates technical debt, and makes the ROI gap wider. The fix: ruthless evaluation gating. No scale until autonomy rate >80% and quality gate pass rate >95% on a representative eval set.

## What a Day's Work Looks Like Five Years from Now

Roberts paints a picture: you start the day by reviewing 3–5 agent-completed deliverables (code PRs, analysis reports, incident summaries), provide lightweight feedback on 1–2, and spend the rest of your time on strategy, architecture, and the 10% of problems agents *can't* handle yet. The agent team handles the "how"; you handle the "what" and "why."

## References

- Original article: [https://www.databricks.com/blog/everyones-adopting-ai-agents-almost-no-one-can-prove-roi-heres-why](https://www.databricks.com/blog/everyones-adopting-ai-agents-almost-no-one-can-prove-roi-heres-why)