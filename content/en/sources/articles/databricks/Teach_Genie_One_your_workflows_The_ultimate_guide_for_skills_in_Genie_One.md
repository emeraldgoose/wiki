---
title: "Teach Genie One your workflows: The ultimate guide for skills in Genie One"
description: "Skills are durable, reusable workflow recipes in Genie One — plain-language, open Agent Skills format — that encode how your team works: steps, checks, format and sign-off, shareable across the organization via Unity Gateway."
tags: [source, databricks, en]
locale: en
source_url: "https://www.databricks.com/blog/teach-genie-one-your-workflows-ultimate-guide-skills-genie-one"
blog: databricks
published_date: "2026-11-19"
---

# Teach Genie One your workflows: The ultimate guide for skills in Genie One

**Source**: [databricks](https://www.databricks.com/blog/teach-genie-one-your-workflows-ultimate-guide-skills-genie-one) · **Published**: 2026-11-16

## Overview

Every team has "recipes" that govern how they work — how finance assembles the month-end pack, the checks sales operations runs before a forecast call, the format leadership expects for a retrospective. These live in people's heads, old emails and unfindable "here's how I do it" docs.

Genie One already understands your business through Genie Ontology — your business definitions and how teams use data. Skills add the missing layer: **how you like things done**. A skill is a workflow recipe Genie One can follow on demand, ensuring consistent format and output — e.g., prompt "Put together our trading report for last month" and get it the way your team would prepare it, with the same checks, structure and level of detail.

## Key points

- **Durable, reusable assets**: a skill is a written record of how your team works, in plain language, in the open Agent Skills format — yours to keep, review and build upon.
- **Two invocation paths**: users call skills directly, or Genie One decides a skill is relevant to the request; skill guidance stays scoped to that task.
- **Shareable via Unity Gateway**: publish a skill and any MCP-capable agent — including coding agents your teams already use — can consume the same recipe; share it across the organization so one person's best way of working becomes everyone's.
- **Easy to create**: build a skill directly in Genie One through one conversation by explaining your workflow in detail once.
- **When to reach for a skill**: you keep explaining the same thing; it's done regularly; it has steps; the format matters; there are rules you always apply; you keep making the same manual tweak.
- **Where skills sit**: business definitions belong in Genie Ontology (curated in Unity Catalog Semantics — metric views for structured metrics like "net sales", pages for concept definitions like "active customer", domains to organize by business area); workspace instructions hold org-wide conventions; memory holds personal facts; a skill holds the *method*. Genie Ontology says what things mean; a skill says a specific way to get it done.
- **Skills + Genie Agents**: a Genie Agent is the domain expert (metric definitions, tables, joins, business rules for one scoped domain like sales or finance); a skill is the recipe for a specific task (e.g., a "weekly forecast risk memo" skill tells Genie One to compare this week's pipeline with last week's, flag slipped deals, and produce a one-page memo).

## Details

**Map the workflow before you build.** Skill quality comes from how well you describe the work. Walk the task end to end and answer:

1. Under what conditions should it be used — what would someone say or ask that means this skill applies?
2. What tools and data does it use — which data, Genie Agents, documents or connected tools (Gmail, Google Drive) are involved?
3. What order do things happen in — which steps depend on others (e.g., confirm which month is complete before pulling its numbers)?
4. Where does it need to dig deeper — which steps repeat until a question is answered (break an unusual result down until it fits in one sentence)?
5. What gets checked every time — checks cover more than numbers; they can be conditions the result must meet (e.g., the document always contains a table with the four expected columns).
6. What should the result look like — summary, email, ticket; sections, length, tone, destination.
7. Where do you want a say — finished result straight away, or pause for review / upfront questions?

Then hand it to Genie One: describe the workflow in your own words and ask it to interview you before it writes anything. Because Genie One draws on Genie Ontology, its questions focus on how you work, not what your data means.

**Example — monthly trading brief.** A commercial finance team writes a leadership trading brief every month: pull last month's numbers, check each channel against rules, dig into anything unusual, look for team emails explaining it, write a short brief. Described in a couple of sentences, that was enough for Genie One to draft the skill — the team then refined checks, format and sign-off until the output matched their standard.

## References

- Original article: [Teach Genie One your workflows: The ultimate guide for skills in Genie One](https://www.databricks.com/blog/teach-genie-one-your-workflows-ultimate-guide-skills-genie-one)
