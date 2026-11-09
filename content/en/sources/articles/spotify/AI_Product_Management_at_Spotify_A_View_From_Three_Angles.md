---
title: "AI Product Management at Spotify: A View From Three Angles"
description: "Three Spotify product managers describe how the AI PM role diverges across the research, foundation-model and user-experience layers of the same stack."
tags: [source, spotify, ai-engineering, product-management, en]
locale: en
source_url: "https://engineering.atspotify.com/2026/11/ai-product-management-at-spotify-a-view-from-three-angles/"
blog: spotify
published_date: 2026-11-10
---

# AI Product Management at Spotify: A View From Three Angles

**Source**: [AI Product Management at Spotify: A View From Three Angles](https://engineering.atspotify.com/2026/11/ai-product-management-at-spotify-a-view-from-three-angles/) · **Published**: 2026-11-09

## Overview

Most writing about product management and AI treats "the AI PM" as a single job, but what the role looks like depends on what you are building. Three principal product managers at Spotify — Henok in Tech Research, Divita on a recommendation foundation model, and Humberto on the session experience users actually touch — work on the same stack in the same part of the organization and still have very different day-to-day work and definitions of success. An idea from research can become a reusable model capability that unlocks a new experience, so the layers are connected; getting it to ship takes all three.

The authors argue the shared vocabulary hides the differences. Everyone says quality, evals and shipping, but the meaning shifts with the problem space each PM owns. Impact shifts too: a change in what the organization believes or where it invests is a major research win; for a model PM the payoff is a model improvement that lifts recommendations across multiple experiences; for an experience PM it is whether users love the product and come back. The closing argument is that product management remains the same craft — define the problem, know your customer, measure what matters, build conviction through evidence — and the AI stack adds a layer of specialization with more flavors than people realize.

## Key points

- Research layer (Henok): the product is technical leverage. Better models let product teams do work that once required deep research involvement, so research moves toward shared methods, system design and emerging capabilities where the right approach is still unclear — for example how to evaluate open-ended model behavior or how to represent users and content for several products at once.
- The prototype-to-product gap is the research question: evaluation, latency, cost, data and integration all become part of it, because a more complex model can look great in a demo without changing the production tasks that matter.
- A promising architecture is not a roadmap. Once evidence grows, the harder product question is what the organization should do with it, which touches infrastructure, evaluation, interfaces and several teams' plans; the way through is a concrete problem, a useful test, and agreed evidence for the next step, while the methods developed along the way already improve existing systems.
- Model layer (Divita): a foundation model for recommendations has internal teams as customers. Behaviour is learned through training rather than specified in code, so the two real levers are what you teach the model and how you check what it learned — data and evals — and offline evals must be connected to what listeners actually experience.
- "Good is not enough if nobody ships with it": success means finding a team whose current system hit a ceiling on a metric they care about, agreeing what the capability must deliver, defining the integration contract, and testing the riskiest assumptions before asking the partner team to commit. The team's best result this year came from agreeing on how success would be measured before agreeing on the architecture.
- Experience layer (Humberto): input is open-ended instead of constrained, which reshapes supposedly fixed constraints — latency that is unacceptable for keyword search is tolerable in a conversational interaction — and questions like how the system behaves when it is not confident, or how it recovers, belong to the product rather than the model.
- Evaluation is treated as a continuous product, not a pre-launch phase: datasets from real usage, feedback loops, LLM-based judges and custom evaluators tuned to the supported interactions, with a general-purpose eval as a starting point rather than the finish line; because users talk to the system in real time, frustration is simultaneously feedback on the experience, the model and possibly the training data.

## Details

The research role is described as providing product and strategic context without prescribing answers, connecting work to decisions early and being explicit about what the evidence does and does not show, since research impact can take months to appear in another team's roadmap and the decision window may close if that starts only when the research is complete. Henok notes the pace of AI also demands understanding the technology more deeply than in many previous PM roles, staying close to one or two projects at a time to judge the choices and obstacles involved.

On the model side, Divita frames the platform work in classic product terms: product-market fit means knowing which problems teams can solve with the model, the value proposition explains what it offers for a particular experience, and business impact comes through what teams ship with it. Because a single evaluation cannot answer every question, the team tracks how the model develops across training cycles and how those changes translate across experiences, which is how it distinguishes a promising result from a pattern it can plan around — and how it makes the case for a model whose benefits build as more teams adopt it.

For the experience layer, Humberto stresses that the experience team is closest to the user and therefore has the clearest view of which model gaps and unanswered research questions matter now, turning dependency on the other layers into a shared prioritization signal rather than a bottleneck. His summary of the job: the most direct line to the user and the most tangible ownership of the outcome, but built on systems you influence rather than control, for users whose expectations are being reshaped in real time by every other AI product they touch.

## References

- Original article: [AI Product Management at Spotify: A View From Three Angles](https://engineering.atspotify.com/2026/11/ai-product-management-at-spotify-a-view-from-three-angles/)
