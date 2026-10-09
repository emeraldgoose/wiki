---
title: Engineering the Next Generation of LinkedIn's Feed
description: LinkedIn's LLM-powered Feed rebuild — unified dual-encoder retrieval and transformer-based Generative Recommender ranking
date: 2026-03-12
tags: [source, linkedin, feed, ranking, llm, recommender-systems, retrieval]
locale: en
source_url: "https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed"
blog: linkedin
author: Hristo Danchev
---

# Engineering the Next Generation of LinkedIn's Feed

LinkedIn's Feed serves more than 1.3 billion professionals. This post describes a full rebuild of the Feed recommendation stack: a unified LLM-based retrieval pipeline plus a transformer-based Generative Recommender (GR) for ranking, served on GPUs at millisecond latency.

## Why rebuild: limits of the old architecture

- **Heterogeneous retrieval.** Content arrived from many parallel sources — chronological network index, geographic trending, collaborative filtering, industry trending, embedding-based retrieval — each with its own infrastructure, index, and tuning. High maintenance cost and no holistic optimization.
- **Independent impression scoring.** The ranker scored each candidate post in isolation, ignoring what the member had just read and the trajectory of their interests.

## Unified retrieval through fine-tuned LLMs

A single dual-encoder pipeline replaces the multi-source architecture. One shared LLM encodes both member and post prompts into a shared embedding space; relevance is cosine similarity, retrieved via k-NN over a GPU-accelerated index (sub-50 ms retrieval latency over millions of posts).

### From structured data to effective prompts

A "prompt library" of templates converts structured features into LLM-readable text:

- **Posts:** format, author headline, company, industry, engagement counts, post text.
- **Members:** profile, skills, work history, education, plus the chronologically ordered engagement history.

**Numerical features needed special handling.** Raw counts ("views:12345") tokenize as arbitrary text — correlation between popularity and embedding similarity was near zero (−0.004). The fix was **percentile bucketing** (`71`, i.e. 71st percentile of views): stable single-token representations that restored the popularity signal — 30× better correlation and +15% recall@10.

### Training dual encoders at scale

- **Loss:** InfoNCE with easy negatives (random unseen posts) and hard negatives (shown but not engaged).
- **Hard negatives matter:** +2 hard negatives per member → +3.6% recall@10 over easy-only baseline (+2.0% from the first, +1.6% from the second).
- **History filtering:** keeping only positively-engaged posts (dropping impressed-but-skipped) cut per-sequence memory 37%, allowed 40% more sequences per batch, and sped training iterations 2.6× at equal or better quality.
- **Compute:** trained on 8 H100 GPUs.

### Online serving: freshness at scale

Three continuous nearline pipelines — prompt generation, embedding inference, index updates — keep embeddings fresh: new posts embedded in near-real time, engaging posts refreshed dynamically.

## Ranking: the Generative Recommender

Ranking treats the member's interaction history (>1,000 past interactions) as a sequence — a "professional story" — modeled with a causal-attention transformer over interleaved post representations and action embeddings (dwells, likes, comments, shares).

- **Sequential > pointwise.** Trajectory modeling especially helps sparse users: more signal per interaction than isolated scoring.
- **Late fusion.** Transformer output is concatenated with per-timestep context (device, profile embeddings, affinity scores) before prediction, keeping the transformer compact.
- **MMoE head.** A Multi-gate Mixture-of-Experts head predicts multiple engagement tasks, with passive tasks (click, skip, long dwell) and active tasks (like, comment, share) getting specialized gating over shared sequential representations.
- **Serving.** Disaggregated CPU feature processing / GPU inference, shared-context batching (history encoded once, all candidates scored in parallel), and a custom Flash-Attention variant (GRMIS/SRMIS) delivering ~2× speedup over PyTorch SDPA.
- **Impact.** The companion Feed SR rollout reported **+2.10% time spent** in A/B tests vs. the prior DCNv2 model.

## Takeaways for SW engineers

1. Percentile-bucket numerical features before feeding them to LLM prompts.
2. Hard negatives (shown-not-engaged) are worth far more than extra easy negatives.
3. Filter training histories to positive engagements — cheaper and no worse.
4. Late-fuse context features instead of bloating transformer input width.
5. Custom attention kernels (GRMIS/SRMIS style) buy ~2× serving headroom for multi-item scoring.

## Related concepts

- `concepts/machine-learning/transformer.md` (GR ranking architecture)
- `concepts/ai-engineering/rag.md` (retrieval over embedding index)

## References

- Source: https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed
- Companion paper: "An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" (Feb 2026)
