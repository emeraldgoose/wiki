---
title: "De-identifying text at scale: How Airbnb protects personal data in AI training"
description: "Airbnb de-identifies PII in messages, reviews, and support chats before ML training by extending Microsoft's Presidio library in-process, with GLiNER recognizers, phrase-context matching, consistent per-run fake values, and a per-entity, per-language benchmark."
tags: [source, airbnb, privacy, machine-learning, nlp, en]
locale: en
source_url: "https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training"
blog: airbnb
published_date: 2026-11-28
---

# De-identifying text at scale: How Airbnb protects personal data in AI training

**Source**: [Airbnb Engineering & Data Science](https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training) · **Published**: 2026-11-18

## Overview

Airbnb trains machine learning models on transaction information — messages, reviews, and support chats — that contains personally identifiable information (PII) such as names, home and current location, and payment details. Before any of that text reaches a model, Airbnb removes PII and replaces it with realistic simulated data, both to minimize the number of copies of personal data and to prevent leakage into and through the models. Privacy decisions start as policy set by Airbnb's Privacy Architecture team with Legal, Policy, and Engineering, and Engineering then implements those decisions as code.

The team built the system on Presidio, the open-source PII library originally developed by Microsoft and now community-governed, because it met their requirements: on-premises hosting, general-purpose and highly modular components (pluggable recognizers, NLP engines, operators), multilingual support, separation of detection from obfuscation within one framework, support for redaction/masking/realistic replacement, and consistent fake values within a run. Managed cloud services were rejected because they are not on-premises, and standalone NER models because they only solve part of the problem.

Presidio ships as a Python package that each consumer imports in-process, so raw personal data is de-identified inside the calling process with no separate service holding it and no central bottleneck. At Airbnb, models train through a shared ML workflow orchestrator, so the library ships as a reusable pipeline step: a team supplies only its data schema marking which columns carry personal data, while Airbnb owns the recognizers, operators, language handling, and runtime. The resulting dataset is tagged as de-identified, the tag follows the data into the model registry where it gates deployment to production, and each run records the library version and configuration so registered models can be traced back to their datasets.

## Key points

- Two-stage pipeline: the Presidio Analyzer finds spans that look like personal data and labels each with an entity type and confidence score; the Anonymizer resolves overlapping spans and applies an operator (redact, mask, or realistic replacement) to each surviving span.
- Three recognizer kinds: pattern-based (regex + context words), NER-based (model-driven), and list/context-based. Overlapping claims (e.g. a LISTING_ID inside an EMAIL_ADDRESS) are left unresolved by the Analyzer and settled in a configurable step in the Anonymizer.
- Airbnb-specific entity types such as LISTING_ID and AIRBNB_GIFT_CARD are PatternRecognizers, since no general-purpose model knows them; context words decide between shape-identical digit runs (gift card vs. Luhn-valid credit card vs. listing ID).
- Phrase-context layer: stock context matching is single-token, so "gift card" never fired and "card" fired next to credit cards. Airbnb added an ordered contiguous multi-word phrase match before a candidate, scored above single-word hits, so the more specific phrase wins the span.
- NER backend: spaCy (Presidio's default) is fast and cheap but its generic NER tags any place as a location and never resolved full street addresses on their benchmark. Airbnb replaced spaCy for PERSON and LOCATION with GLiNER, a zero-shot NER model that takes an entity description at inference time (e.g. ask specifically for a street address); precision improved for both. GLiNER2 is wired into the harness as a candidate and is adopted per recognizer only when the benchmark shows a gain.
- Language detection is a prerequisite: recognizers and models are language-specific, and short spans like names carry few cues, so language is detected on the whole record or taken from locale metadata; if neither is confident, a more conservative configuration is used rather than risking the wrong language model.
- Anonymizer: most entity types use faker-generated realistic values instead of `<PERSON>`-style placeholders, because placeholder tokens are themselves a learnable pattern. Custom fakers keep structural non-personal data (a listing's own URL) intact, pin card faking to a locale with full coverage, parse phone-number structure to keep real country/area codes while faking the rest, and draw fakes from reserved/never-issued identifier ranges so they cannot collide with real values.
- Consistency vs. unlinkability: within a run the same real value must map to the same fake (internal coherence), but across runs the same input must produce different fakes (so fakes are not a fingerprint linking outputs). Each fake is seeded from the real value plus a per-run secret; no real-to-fake mapping is stored.
- Structured columns: identifiers are hashed with a caller-supplied salt; coordinates are truncated to a Privacy-set precision; 64-bit internal IDs go through format-preserving encryption so de-identified tables pass the same schema checks.
- Evaluation holds every design decision to measurement on three dimensions — recall (a miss is a leak), precision (over-redaction trains noise), and throughput — with recall weighted first. Metrics are reported per entity type and per language with labeled-instance counts plus a span-claim confusion table, because aggregate scores hide exactly the failure that matters. The benchmark scores the overlap-resolved spans the library actually emits, not raw Analyzer candidates, and the NER backend is a harness parameter so spaCy/GLiNER/GLiNER2 are scored side by side on the same golden sets. A new language ships only when a labeled dataset in that language exists, gaps are folded back into the benchmark, and no previously working language or entity type regresses before release.

## Details

Deployment is in-process by design: each pipeline step calls the library directly, which keeps the data flow simple and removes a central bottleneck, at the cost of distribution — the library only protects data if every pipeline calls it on the current version with a compliant configuration, which is why it is packaged as a shared orchestrator step with Airbnb-owned defaults. Detection thresholds and entity scope are configurable per recognizer and per consumer: a pipeline feeding raw text into training wants a low threshold and accepts false positives, while reviewed data can trade recall for fewer redactions. Operator choice is likewise configurable per model and use case — faker-based replacement for training text, masking for human review — and the same engine covers structured columns via salted hashing, coordinate truncation, and format-preserving encryption of internal IDs.

The benchmark is the arbiter of "good enough": not a number hit once, but a bar every new version must clear again, run against the deployed version side by side before release, with no regression in any language or entity type that previously worked. Future work includes more languages, LLM-based recognizers, and extending de-identification beyond text to other media.

## References

- Original article: [De-identifying text at scale: How Airbnb protects personal data in AI training](https://airbnb.tech/infrastructure/de-identifying-text-at-scale-how-airbnb-protects-personal-data-in-ai-training) (Airbnb Engineering & Data Science, 2026-11-18)
- Presidio: [microsoft/presidio](https://github.com/microsoft/presidio)
