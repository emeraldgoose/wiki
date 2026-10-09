---
title: Encoding Your Domain Expert
description: Spotify's context layer behind its AI data assistant — the cluster model where domain experts curate datasets, vetted question-SQL pairs, and docs so an LLM agent answers reliably at warehouse scale
tags: [source, rss, spotify, data-assistant, context-engineering, rag, text-to-sql, llm-agents]
locale: en
source_url: "https://engineering.atspotify.com/2026/6/encoding-your-domain-expert-the-context-layer-behind-spotifys-data-assistant"
blog: spotify
published_date: 2026-06-10
---

# Encoding Your Domain Expert: The Context Layer Behind Spotify's Data Assistant

Authors: Pavlina Mitsou (Senior Engineer), Jonathan Warburton (Senior Engineer). Source: Spotify Engineering, Jun 10, 2026.

**Lead**: Dashboards didn't scale and Slack-ing a data expert didn't scale either. Spotify's answer is an AI data assistant whose reliability comes not from the model but from a curated **context layer**: domain experts encode what they know into owned "clusters" — datasets, vetted question–SQL pairs, and business docs — and a ReAct agent answers from that context with its query and sources attached. In production since August 2025: 2,100+ users, 13,000+ conversations, 60,000+ messages across 177 clusters.

## Background: the old pattern broke

The classic flow — look for a dashboard, find none, message the domain expert on Slack, wait — collapsed under scale: thousands of fast-moving teams, 70,000+ datasets, petabytes of data, 1.4 trillion data points a day. No individual knows the whole warehouse, and dumping schemas into an LLM fails twice over: even million-token context windows cannot fit a warehouse, and schemas don't carry meaning — an INT64 column says nothing about legacy test values vs. real data, and nothing defines "active user".

## The cluster model: ownership scales context

Spotify's unit of curation is the **cluster** — a data domain tied to an initiative, an organization, or an ad-hoc interest. Any insights team can build a cluster around its topics, and each cluster is owned by named domain experts. The core principle: the people who best understand a domain are the best ones to curate the context the model sees. Experts spend less time answering one-off questions and more time shaping the knowledge layer that answers thousands.

Each cluster's context layer has three curated components:

1. **Datasets** — relevant warehouse tables with full schemas plus profiling: column cardinality, samples of common values, partition structure.
2. **Pairs** — vetted question-and-SQL examples, written or approved by experts, that teach both query structure and the patterns the team wants followed (few-shot learning fuel).
3. **Docs** — business documentation: definitions, caveats, metric semantics ("completely bananas" edge cases included).

## The agent: ReAct with receipts

When a question arrives, the agent selects the appropriate context, writes SQL, runs it against the warehouse, and returns the answer **alongside the query and its sources**. It follows a ReAct loop — reasoning and acting in steps, adjusting based on each tool call's result. Answers surface where people work: a Slack bot, an MCP server for IDEs and AI tools, and a web UI for exploration. Crucially, when no knowledge base covers the topic, the agent says so — that transparency is what makes its answers trustworthy.

## Results and reach

- Live since August 2025; 2,100+ Spotifiers, 13,000+ conversations, 60,000+ messages, 177 clusters spanning advertising, podcasts, music, audiobooks, finance, creator tools, and more.
- Over a quarter of users had never written SQL — genuine democratization, not just acceleration.

## Limitations / open questions

- Quality follows curation: unowned or stale clusters decay into confident-sounding wrong answers; ownership hygiene is the ongoing cost.
- Coverage gaps are handled by disclosure, not answers — good for trust, but leaves long-tail questions unserved until someone curates them.
- Question–SQL pairs can over-anchor the agent to taught patterns on novel questions.

## Relevance to SW engineers

- For text-to-SQL at warehouse scale, invest in the **context layer** (profiling, vetted pairs, definitions) before model upgrades — retrieval over owned, curated context beats bigger windows over raw schemas.
- Ship answers with receipts (query + sources) and explicit coverage disclosure; it converts skeptical domain users.
- Expose the agent on existing surfaces (chat, MCP, IDE) rather than demanding a new destination.
- Related: `concepts/ai-engineering/rag.md`, `concepts/ai-engineering/agent.md`.

## References

- Source article: https://engineering.atspotify.com/2026/6/encoding-your-domain-expert-the-context-layer-behind-spotifys-data-assistant
