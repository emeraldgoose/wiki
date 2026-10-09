---
title: How LinkedIn Built the Engineering Infrastructure to Ignite Professional Knowledge Sharing
description: "Collaborative Articles — LinkedIn's first generative-AI product infra: prompt tooling, expert matching, trust systems"
date: 2023-11-20
tags: [source, linkedin, generative-ai, prompt-engineering, infrastructure]
locale: en
source_url: "https://engineering.linkedin.com/blog/2023/how-linkedin-built-the-engineering-infrastructure-to-ignite-prof"
blog: linkedin
author: Shweta Patira
---

# How LinkedIn Built the Engineering Infrastructure to Ignite Professional Knowledge Sharing

Co-authors: Shweta Patira, Ankan Saha, Yilin Li, Manas Somaiya. This post covers **Collaborative Articles** — AI-seeded professional Q&A where experts add real-world advice — and the generative-AI infrastructure built from scratch to launch LinkedIn's first GAI product.

## Product shape

Instead of classic Q&A, LinkedIn generates articles across professional topics with AI-powered conversation starters, then invites experts to contribute ideas, stories, and advice. Three hard problems: (1) generating huge volumes of questions + starter articles, (2) finding and matching the right experts, (3) distributing articles to members who need them.

## Sprinting with "Progress over Perfection"

GAI tooling barely existed, so three workstreams ran in parallel: prompt engineering/tooling, the article viewing + contribution experience, and AI-driven expert identification/matching.

### Prompt workflow industrialization

Early iteration was spreadsheets-by-hand: hours of inference → sample outputs → editors scoring yesterday's prompts. The team built:

- a **versioned prompt templating system** (single- and multi-step prompts),
- **human + automated response evaluation** scoring content quality.

### Hack-track prototyping

A three-engineer team shipped daily member-experience variants as coded mockups ("tape — rip, replace, repeat"), keeping abstraction high so internal teams could play with changes and keep feedback loops tight.

### Connecting the dots

Topic generation at scale → editorial review → publishing queues → distribution: matching millions of experts to questions, then surfacing answers via search engines, Feed, InMails, and notifications.

## Expert identification: signals of mastery

Combining noisy signals into matchable expertise:

- **Explicit:** profile skills, endorsements, recent titles.
- **Implicit:** skills inferred from hiring patterns for job posts, self-evaluations in job applications.
- **Propensity:** likelihood of contributing original thought, from past sharing behavior.

Once contributions flowed, engagement/quality feedback fine-tuned the matching — raw signals into actionable routing.

## Trust: surfacing gems without stifling debate

Multi-expert threads need defenses that preserve healthy disagreement: trust classifiers filter unsafe/harmful/unprofessional content, member reporting enables fast reaction, and repeat offenders lose contribution access.

## Results (six months in)

- **1M+ expert contributions**; **+74% articles read in the last month**; Collaborative Articles among LinkedIn's fastest-growing traffic drivers.

## Takeaways for SW engineers

1. First GAI products need prompt-ops (versioning, eval) before model sophistication.
2. A dedicated hack-track de-risks UX exploration without blocking production paths.
3. Expert routing = explicit + implicit + propensity signals, closed-loop on engagement.
4. Trust systems must be tuned for debate, not just removal.

## References

- Source: https://engineering.linkedin.com/blog/2023/how-linkedin-built-the-engineering-infrastructure-to-ignite-prof
