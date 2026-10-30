---
title: "From weeks to a day: how we made LLM evaluation fast enough to iterate on"
description: "Airbnb's LLM evaluation infrastructure compresses iteration cycles from weeks to a day."
tags: [source, airbnb, evaluation, llm, en]
locale: en
source_url: "https://airbnb.tech/ai-ml/from-weeks-to-a-day-how-we-made-llm-evaluation-fast-enough-to-iterate-on"
blog: airbnb
published_date: 2026-07-27
---

# From weeks to a day: how we made LLM evaluation fast enough to iterate on

**Source**: [airbnb blog](https://airbnb.tech/ai-ml/from-weeks-to-a-day-how-we-made-llm-evaluation-fast-enough-to-iterate-on) · **Published**: 2026-07-27

## Overview

Shipping a production LLM system means iterating fast on improvements to something that is, by construction, non-deterministic. Models drift, judges disagree with themselves, references regenerate as different strings, and bugs may persist until the next release because retraining takes weeks. At Airbnb, most of this friction came from infrastructure challenges, not model quality, and fixes came from classical software engineering techniques. Reliable LLM infrastructure is built by addressing four layers: three engineering enhancements plus an integration layer tying them together. The seams are where the friction concentrates.

## Key points

- Iteration speed is limited by infrastructure, not only model quality.
- Deterministic evaluation foundations make judges and references reproducible.
- Layered engineering enhancements handle evaluation, serving, and integration concerns.
- The integration layer is easy to overlook but essential end to end.
- Named, measured layers keep LLM evaluation fast enough to iterate.

## Details

The article outlines a layered approach to LLM evaluation infrastructure, combining deterministic evaluation foundations with integrated validation so production iteration cycles shrink from weeks to about a day.

## References

- Original article: [https://airbnb.tech/ai-ml/from-weeks-to-a-day-how-we-made-llm-evaluation-fast-enough-to-iterate-on](https://airbnb.tech/ai-ml/from-weeks-to-a-day-how-we-made-llm-evaluation-fast-enough-to-iterate-on)
