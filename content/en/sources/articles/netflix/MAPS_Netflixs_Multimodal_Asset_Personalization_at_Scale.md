---
title: "MAPS: Netflix's Multimodal Asset Personalization at Scale"
description: Multimodal embeddings (CLIP, MediaFM) for cold-start artwork and video preview personalization with a unified cross-canvas model
tags: [source, article, netflix, personalization, multimodal, embedding, recommendation]
locale: en
source_url: "https://netflixtechblog.com/maps-netflixs-multimodal-asset-personalization-at-scale-32f96320785e"
blog: netflix
published: 2026-08-28
---

# MAPS: Netflix's Multimodal Asset Personalization at Scale

Authors: Emma Yanyang Kong, Aditya Deshpande, Asad Abbasi, Bowei Yan, David Fagnan, Ashish Rastogi, Dhaval Patel, Ray Zhang.

Every visual cue on Netflix — title artwork, autoplaying video previews — is a personalization problem of its own: which image of *Squid Game* should *you* see? Legacy models answered well for mature titles but failed right after launch, treating each asset as an opaque ID with no interaction history. MAPS lets models "see and hear" assets via multimodal embeddings so personalization kicks in near launch.

## Background: the cold-start problem

Artwork personalization matches diverse per-title artwork sets to member taste from interaction histories. But a new title's assets have no history, so the system fell back to exploration plus popularity heuristics that ignore taste. Only after enough interactions accumulated could personalization take over — the classic cold-start gap.

## Methodology

**Content-aware asset representation (artwork).** Each artwork is encoded with CLIP (pretrained image-text model); the 768-dim CLIP image embedding is concatenated with the asset's learned ID embedding and passed through an MLP to form the asset representation. A brand-new artwork arrives with its CLIP vector, so member preferences over visual themes, talent, and color palettes — expressed in embedding space rather than tied to asset IDs — transfer immediately, even across titles (e.g. affinity for a comedian's artwork carries to their new title).

**Five models to one (cross-canvas transfer).** Artwork spans five canvases (billboard, vertical-box, horizontal-panel, short-panel, landscape-panel) with historically one model each, since ID-based models cannot relate cropped/resized renderings of one scene. CLIP embeddings are largely invariant to crop, resize, and aspect ratio, so near-identical renderings map to nearly the same vector: a single unified model pools signal across all canvases, with the largest gains on data-starved canvases.

**Reward-weighted training.** Pooling canvases raises a mixing problem: canvases differ wildly in impression volume, and raw-count training would let the highest-volume canvas dominate. Instead each example is weighted by the long-term reward score ρ of its interaction type (building on Netflix's long-term reward modeling), rebalancing the mixture with no hand-tuned per-canvas weights and optimizing for long-term member satisfaction.

**Unbiased offline evaluation (IPS).** Offline evaluation on production logs is biased toward the logging policy. Netflix uses inverse propensity scoring on a dedicated exploration-traffic slice served by a randomized policy with exactly-logged propensities — the biggest reason offline numbers track online outcomes. Candidates must beat the baseline on IPS ratio before earning A/B traffic.

**Query-aware artwork ranking.** For search, member intent is explicit in the query. Because CLIP shares one text-image space, the ranker blends the personalization score with cosine similarity between the query's CLIP text embedding and the asset's CLIP image embedding, mixed by weight α tuned via A/B testing — with no extra modeling effort.

**Video previews via MediaFM.** Video appeal comes from motion, pacing, dialogue, and soundtrack — invisible to ID models and only partly captured by SeqCLIP (mean of per-frame CLIP vectors). MediaFM, Netflix's in-house multimodal foundation model trained on 80M shots, fuses visual (SeqCLIP), audio (pretrained speech/audio embeddings), and text (caption encoder) signals per shot. Adoption required no new infrastructure: shot embeddings drop into the asset representation like CLIP vectors.

**Cheap embedding screening (linear probe).** End-to-end trials cost retraining plus weeks of A/B traffic, so candidates are gated by a proxy task: predict each title's debiased popularity winner (from exploration data, propensity-adjusted) from the embedding alone with a linear probe under binary cross-entropy. Probe accuracy ranked MediaFM > SeqCLIP, matching later offline IPS and online A/B orderings — so the probe now gates every new MediaFM version.

**Netflix Embedding Store.** All embeddings live in a shared store serving identical vectors at training and inference time (no skew) and decoupling foundation-model updates from personalization-model deployments: new embeddings are registered, backfilled, and validated independently, then consumed via configuration alone.

## Results

- Ablation vs the five-model production system: V1 (embeddings only) and V2 (unified only) each helped on sparse canvases but neither moved online core metrics alone; V3 (both) won a statistically significant online lift and runs in production. Effects compound: the V3 short-panel lift (5.691%) exceeds V1+V2 combined.
- Shipped ahead of Netflix's largest TV home-screen redesign in a decade (short-panel dominant overnight): a month-long holdback A/B showed significant gains on core discovery and streaming hours.
- Video: MediaFM > SeqCLIP > ID-only both offline (IPS) and in a five-week online A/B (significant streaming-metric lift, largest on TV). MediaFM is now the default video preview embedding.

## Limitations / open questions

- IPS depends on a dedicated randomized exploration slice — a permanent traffic cost.
- The linear probe only detects popularity-relevant signal, not personalized value; a high-probe embedding could still fail online.
- Unified cross-canvas pooling assumes embedding-space transfer is always benign; canvas-specific presentation effects may be washed out.

## Relevance to SW engineers

- Content embeddings convert cold-start from a blind spot into transfer learning: represent new items by what they *are*, not by ID.
- When pooling heterogeneous data sources, weight by long-term value rather than volume or hand-tuned weights.
- Gate expensive end-to-end experiments with a cheap proxy task whose ranking correlates with online outcomes.
- A shared embedding store with train/serve consistency and decoupled releases is the infrastructure that makes all of the above practical.

## Related concepts

- `concepts/ai-engineering/rag.md` (multimodal embeddings, retrieval representations)
- `concepts/machine-learning/embedding.md` (embedding-space transfer)
- `concepts/machine-learning/attention.md` (transformer-based ranking)
