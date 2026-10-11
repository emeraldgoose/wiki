---
title: "How I built agent-based security reviews on Databricks"
description: "Seven bounded review agents on Unity Catalog, Lakeflow Jobs, and Databricks Apps that automate routine security work while escalating novel cases to humans."
tags: [source, databricks, unity-catalog, ai-agents, security, en]
locale: en
source_url: "https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks"
blog: databricks
published_date: 2026-09-24
---

# How I built agent-based security reviews on Databricks

**Source**: [Databricks Blog](https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks) · **Published**: 2026-09-24

## Overview

Routine integrations and genuinely novel architectures waited in the same security queue for scarce expert reviewers. The author built an agent layer on Databricks that automates predictable work — intake, risk tiering, requirements drafting, follow-ups — while routing novel, high-risk, or ambiguous cases to people. The first version took under two hours because Unity Catalog, hosted foundation models, Lakeflow Jobs, and Databricks Apps already shared one governance model.

## Seven focused agents, each with one job

Rather than one broad reviewer, the system uses bounded agents — intake, risk assessment, requirements, specialized reviews (e.g. browser-extension threat modeling, vendor assessment), validation, workflow, and learning — as scheduled notebook jobs behind a conversational Databricks Apps front door. Intake turns plain-language descriptions into structured requests with a consultation mode; risk assessment defaults upward on incomplete pictures; eligible low/medium-risk cases complete on the automated path once criteria and evidence check out, while everything else arrives at a human with summary, evidence, and open questions attached.

## Trust through evidence and measurement

Trust comes from the system around the model: grounding in real standards, mandatory evidence (design docs, classification levels, control references), conservative escalation instead of optimistic assumptions, and a learning agent that refines prompts from reviewer edits. An executive dashboard on the same Unity Catalog tables tracks volume, risk mix, automation rate, and cycle time from operational records — routine requests that waited days now complete in minutes, freeing experts for novel designs.

## References

- [How I built agent-based security reviews on Databricks](https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks)
