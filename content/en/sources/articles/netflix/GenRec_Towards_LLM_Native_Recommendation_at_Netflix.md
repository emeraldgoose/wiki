---
title: "GenRec: Towards LLM-Native Recommendation at Netflix"
description: Two-phase LLM-backed full-catalog ranker with context engineering, reward-weighted losses, and prefill-only serving
tags: [source, article, netflix, llm, recommendation, genai, ai-engineering]
locale: en
source_url: "https://netflixtechblog.com/genrec-towards-llm-native-recommendation-at-netflix-f20be6f643e3"
blog: netflix
published: 2026-07-30
---

# GenRec: Towards LLM-Native Recommendation at Netflix

Authors: Ying Li, Arjun Rao, Shradha Sehgal. Production recommenders rely on thousands of hand-crafted features plus bespoke sequence/interaction/multi-task architectures — costly to extend to new content types (movies, series, games, live, podcasts) and surfaces. LLMs offer world knowledge and language understanding, but off-the-shelf models over-recommend popular items, hallucinate out-of-catalog titles, and ignore business constraints. GenRec post-trains an internal foundation LLM into a production ranker that matches or beats a mature system with far fewer labels and signals.

## Background: problem setting

Full-catalog (or top-K) ranking: map request (user u, context τ, time t, history H) to ranking π over catalog C, optimizing expected *long-term* member utility (satisfaction/retention), not short-term engagement.

## Methodology

**Two-phase training.** Phase 1: adapt an open-source LLM on proprietary Netflix corpora (content understanding, member behavior/preferences, language) — infrequently refreshed, shared backbone for many apps. Phase 2: post-train into a ranker with ranking-specific data/objectives — frequently refreshed to track new content and tastes, optimized under serving-cost constraints.

**Conversations as training data.** Hundreds of billions of events (views, plays, durations, thumbs, add-to-list, abandons) become single/multi-turn "conversations": user message = verbalized context, profile, history, item metadata, task; assistant message = actual engagement. Phase 2 learns assistant-given-user dependence, jointly supporting LM and ranking objectives; at inference only the verbalized context is fed in — no assistant decoding.

**Context engineering (the new feature budget).** Naive verbalization blows the token budget, so within a fixed budget: retain high-signal engagements in full (long plays, thumbs-up), omit low-signal (short plays, hovers), summarize/compress repetitive behavior (binge-watching), elaborate selectively on cold-start items (new releases). Prioritize recent high-signal history; structure prompts for shared prefixes (prefix caching). Cost-quality study: tokens cut to ~one-third with negligible MRR loss.

**Multi-objective loss.** (1) Catalog-aware ranking: cross-entropy over catalog/candidate set toward high-value positives (long plays, strong feedback, denoised thresholds). (2) Language modeling over verbalized I/O to preserve understanding and enable explanations. (3) Reward-weighted alignment: per-example scalar weights from long-term satisfaction proxies (return behavior, exploration, sustained engagement) and behavior rebalancing (content types, launch stages) — simpler and cheaper than full RL, with GRPO-style RL left to future work.

**Architecture and serving.** Decoder-only Transformer with pooled hidden state h; catalog-aware scoring head ϕ(h, eᵢ) over learned item embeddings (dot product/small MLP, sampled softmax at scale) constrains output to in-catalog items. Served on Netflix's internal LLM stack with vLLM: smaller/distilled models, aggressive context compaction, and **prefill-only inference** — one forward pass scores the candidate set with no autoregressive decoding.

## Results

- Offline: ~+1.6% MRR over a mature production ranker with ~40× fewer Phase-2 labels; quality keeps improving with more data/signals.
- Online: large A/B (~10% traffic, ~4 weeks, low-data/low-signal config) — statistically significant gains on short- and long-term metrics.
- Ablations: Phase-1 base beats off-the-shelf LLM by ~10–20%; Phase-2 adds ~35–50% (growing to ~80% as Phase-1 goes stale over 2 weeks); GenRec matches/exceeds baseline with 10–40× fewer Phase-2 labels; larger backbones (1B→10B) win under fixed budgets.

## Limitations / open questions

- Phase-1 staleness decays fast (2-week horizon) — refresh cadence is load-bearing.
- Reward weighting inherits reward-model blind spots; RL methods (GRPO) unexplored at scale.
- Results shown on batch-compute surfaces; real-time/high-QPS generalization unproven here.

## Relevance to SW engineers

- The "prompt becomes the feature vector": effort shifts from feature engineering to deciding what signals to include, how far back, and how to compress within budget.
- Shared foundation backbones replace per-task custom architectures; differentiation moves to verbalization, post-training objectives, and inference optimization.
- LLM-backed RecSys inherits scaling laws — invest via data/model scaling curves — and LLM infra (GPU, vLLM/Triton, batching, caching).

## Related concepts

- `concepts/ai-engineering/rag.md` (verbalization, context engineering)
- `concepts/machine-learning/attention.md` (transformer rankers)
- `concepts/data-engineering/stream-processing.md` (interaction log processing)
