---
title: "CASTLE: Training Natural Language Search Before the First Real Query"
description: "Airbnb solves the cold-start problem for natural language search by jointly generating synthetic queries and relevance labels from de-identified booking data. CASTLE achieves 9.2× better distributional alignment (KL divergence 1.01 vs. 9.33 baseline) and 91–93% human label agreement."
tags: [source, airbnb, natural-language-search, cold-start, synthetic-data, information-retrieval, en]
locale: en
source_url: "https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query"
blog: airbnb
published: "2026-10-13"
---

# CASTLE: Training Natural Language Search Before the First Real Query

**Source**: Wei et al., Airbnb Engineering, 2026-10-13

**Lead**: Airbnb introduces CASTLE (Contrastive And Seed-guided Training for natural Language sEarch), a framework that jointly generates synthetic training queries and relevance labels from de-identified booking sessions—solving the cold-start problem for natural language search without any real user traffic.

## The Cold-Start Problem

Natural language search lets guests express intent freely ("romantic cabin near skiing," "pet-friendly beach house that sleeps eight") rather than navigating filters. But training the model requires both queries and relevance labels mapping queries to listings. With no prior traffic, both must be synthesized from scratch.

Prior approaches (InPars, Promptagator) generate queries from documents then add labels via separate LLM judgments—introducing a second error source and producing query distributions far from real users (KL divergence 9.33–26.2).

## CASTLE's Solution: Contrastive Listing Pairs from Booking Sessions

When a guest books a listing after viewing alternatives, that event encodes preference: the booked listing was chosen over viewed-but-not-booked alternatives. CASTLE uses these **(positive, negative) listing pairs** as structured input for query generation.

Key insight: Because the LLM is instructed to generate a query satisfied by the positive but not the negative listing, **the relevance label is correct by construction**—no post-hoc judgment needed. The positive/negative distinction comes from actual user behavior, not the LLM, avoiding circularity.

**Query generation variants** (combined for diversity):
- **Template-based**: Structural diversity across common patterns
- **Few-shot**: ~500 seed queries from user research as linguistic exemplars
- **Attribute-grounded**: Focus on distinguishing attributes (fireplace, ski proximity)
- **Explicit variety mechanism**: Prevents "query collapse" to short repetitive phrases

## Results

| Metric | CASTLE | Best Baseline (Promptagator) |
|--------|--------|------------------------------|
| KL divergence (overall) | **1.01** | 9.33 |
| KL divergence (attribute-type) | **0.08** | 0.09 (survey seeds) |
| Query length σ | 2.48 | 0.99 |
| Human label agreement | **91–93%** | — |

CASTLE's 1.01 KL divergence is a **9.2× improvement** over Promptagator. The attribute-type KL (0.08) even beats hand-curated survey seeds (0.09), meaning generated queries capture real guest intent diversity more faithfully than the seeds themselves.

**Beyond cold-start**: CASTLE's synthetic data continues providing value once real traffic arrives by naturally oversampling long-tail intents (rare property types, amenity combinations) that appear infrequently in organic traffic but matter when they do.

## CASTLE-R for Production

CASTLE-R extends the framework for settings where some real traffic has accumulated, using a Virtual Judge (LLM evaluator) for listings without booking history and incorporating real query seeds.

## Relevance to Software Engineers

For teams building **cold-start search/recommendation systems**: CASTLE demonstrates that **behavioral grounding + LLM generation** are complementary, not competing. Contrastive pairs from user behavior provide distributional alignment and labels by construction; LLM prompting provides linguistic diversity. Together they close the synthetic-real gap neither achieves alone.

Full paper: [arXiv:2605.21812](https://arxiv.org/abs/2605.21812) (CIKM 2026, DOI: 10.1145/3799682.3841071)

## References

- Original article: [https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query](https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query)
- Jeronymo et al. (2023) InPars-v2: LLMs as Efficient Dataset Generators for IR. arXiv:2301.01820.
- Dai et al. (2023) Promptagator: Few-shot Dense Retrieval From 8 Examples. ICLR.