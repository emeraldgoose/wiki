---
title: "GenPage: Towards End-to-End Generative Homepage Construction at Netflix"
description: Single autoregressive transformer generating rows, entities, and layout together with pretraining plus WBC/RL post-training
tags: [source, article, netflix, recommendation, generative-models, reinforcement-learning, ai-engineering]
locale: en
source_url: "https://netflixtechblog.com/genpage-towards-end-to-end-generative-homepage-construction-at-netflix-77146fba8a08"
blog: netflix
published: 2026-06-29
---

# GenPage: Towards End-to-End Generative Homepage Construction at Netflix

Authors: Lequn Wang, Jiangwei Pan, Linas Baltrunas. The Netflix homepage is a structured 2-D layout (rows × entities: movies, shows, games, live) traditionally built by a multi-stage pipeline (candidate generation + ranking at row and entity levels). Inspired by the LLM prompt-response paradigm, GenPage trains one generative model answering: "given user + request, what homepage maximizes satisfaction?" — autoregressively emitting rows, entities, and layout together, unlike flat-list generative recommenders (TIGER, HSTU, OneRec).

## Background: why generative

Goals: end-to-end modeling (one transformer replaces the multi-stage stack — fewer models, no cross-stage objective misalignment, less feature engineering); whole-page RL optimization (diversity, row stopping-power interactions like Continue Watching satisfying intent but cutting browsing); clearer data/compute/capacity scaling; extensibility to new content types, layouts, UI components, per-entity artwork. Production constraints: real-time latency, entity cold start in an evolving catalog, model freshness, business-rule enforcement.

## Methodology

**Domain-specific tokenization.** Context (engagement history, profile, request context) = prompt; page (rows + entities in layout order) = response; feedback derives supervision via the internal reward system. Custom tokens beat text tokenizers: "watched OITNB 50 min 30 days ago" = 4 tokens (Entity_ID, Action_Type, Time_Bucket, Duration_Bucket) vs 16 with GPT-5 — cheaper inference plus direct product-concept control for rule enforcement. Entities/rows are single tokens with daily vocabulary refresh; OOV handled by semantic-embedding fusion and fallbacks. Long sources (impression history) use handcrafted summaries — acknowledged prompt-engineering debt. Pagination appends prior rows + real-time engagements for in-session responsiveness.

**Reward system.** Internal system (tuned by A/B tests to long-term satisfaction) assigns scalar rewards per impressed entity (binge > 10-min watch; abandonment negative); page reward = sum over entities.

**Architecture.** Standard decoder-only transformer; input/output weights untied since pretraining (softmax next-token) and WBC post-training (per-token sigmoids) demand different logits.

**Training recipe (LLM-style).** Pretrain from scratch with next-token prediction on positively-received production impressions — teaches the "homepage language" but only imitates production (plus model-degeneration risk on self-generated pages). Post-train two ways: weighted binary classification (token-level value prediction with per-token credit assignment by construction — simpler, matches production ranker objectives) and RL (harder, but the path to true page-level optimization, test-time reasoning, multi-token entities). Cold start, freshness (daily incremental updates: latest day + sampled past, avoiding catastrophic forgetting), and business rules handled around this core.

## Results

- Online A/B vs mature multi-stage production recommender: statistically significant gains on the core launch-decision engagement metric with −20% end-to-end serving latency.
- Offline: prompt enrichment beats model-capacity scaling in the current regime (120M→900M params follows power-law loss decreases, but context wins per dollar); RL post-training increased homepage diversity with no explicit diversity objective.

## Limitations / open questions

- Long context still needs handcrafted summarization; end-to-end compression is future work.
- LLM-style capabilities (language, multimodality, reasoning) not yet incorporated; hybrid domain+text tokenization proposed.
- Pretraining on production impressions bakes in production-system biases; degeneration under self-training loops unaddressed.

## Relevance to SW engineers

- Recast structured-output problems as prompt→response generation when outputs serialize to token sequences — whole-output optimization (RL) captures cross-element interactions stage-wise objectives miss.
- Domain tokenizers buy order-of-magnitude sequence compression plus output control; map tokens 1:1 to product concepts.
- Before scaling parameters, enrich the prompt — context quality currently beats capacity per dollar.
- Plan freshness from day one: daily vocab refresh, incremental updates with replay, OOV fallbacks.

## Related concepts

- `concepts/ai-engineering/rag.md` (context engineering, prompt design)
- `concepts/machine-learning/reinforcement-learning.md` (page-level RL, reward modeling)
- `concepts/machine-learning/attention.md` (decoder-only transformers)
