---
title: "E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation"
description: HuggingFace Daily Papers — 2026-08-31 — Qwen
tags: [source, paper, huggingface, qwen]
locale: en
source_url: "https://arxiv.org/abs/2608.30730"
arxiv_id: 2608.30730
---

# E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation

**arXiv**: 2608.30730 | **Published**: 2026-08-31 | **Organization**: Qwen | **Submitted by**: Xinjie Shen | **Upvotes**: 6

**Authors**: Paper authors (arXiv: 2608.30730),

 Wei Fan, Xinjie Shen, Xudong Guo, Jianhong Tu, Yang Su, Yinger Zhang, Lianghao Deng, Fengyu Wang, Baohua Dong, Yangqiu Song, Dayiheng Liu

## Abstract

Long-horizon agentic tasks go beyond chaining short tasks over more interaction turns. Their evolving dynamic environments and long-range dependencies require Large Language Models (LLMs) to continually explore, learn from experience, and adapt their policies over thousands of steps. We introduce E-Commerce Bench, the first open-source benchmark that integrates multi-round counterpart negotiation and dynamic events into a year-long business operation. Over a 365-day year, an LLM agent concurrently runs multiple online stores, researching the market, negotiating with suppliers to source inventory, optimizing sales strategies, fulfilling orders, handling returns, and managing cash flow to maximize its end-of-year total assets. To construct a realistic merchant-side operating environment, the product and supplier data are derived from a real e-commerce platform, while a year-long calendar of promotions, natural disasters, and supply-chain shocks continually reshapes demand. For reproducibility, both sides of the market are deterministic: customer purchases and returns follow a fixed demand model, while a negotiation kernel determines supplier pricing, concessions, and decisions, with an LLM used only to verbalize them. We evaluate 18 frontier models across seven dimensions, including year-end assets, and find that no single model dominates. GPT-5.6 Sol earns the most, growing the 100,000 opening stake into 1,431,425, yet it ranks 16th of 18 on fraud avoidance and trails Fable5 in operational efficiency. Among open-weight models, Qwen3.8-Max-Preview leads with 416,252, 38% above GLM 5.2 (high), and achieves the strongest learning over the horizon, progressively bargaining down prices across repeated orders. Our code is available at https://github.com/QwenLM/E-CommerceBench.

## Key Contributions

- **First open-source long-horizon benchmark with negotiation + dynamic events**: a 365-day year running multiple online stores (market research, supplier negotiation, sales strategy, fulfillment, returns, cash flow) to maximize year-end total assets
- **Realistic yet reproducible market**: product/supplier data from a real e-commerce platform; year-long calendar of promotions, disasters, and supply shocks; deterministic demand model + negotiation kernel (LLM only verbalizes)
- **18 frontier models × 7 dimensions**, finding no single dominant model

## Methodology

Agent starts with 100,000 stake, operates concurrently across stores for 365 simulated days under deterministic customer/negotiation dynamics. Scored on year-end assets plus six operational dimensions including fraud avoidance and efficiency.

## Results

| Finding | Number |
|---|---|
| Best earner | GPT-5.6 Sol: 100,000 → **1,431,425** — but 16th/18 on fraud avoidance |
| Best open-weight | Qwen3.8-Max-Preview **416,252** (+38% over GLM 5.2 high) |
| Learning over horizon | Qwen3.8-Max-Preview progressively bargains prices down across repeat orders |
| Headline | no single model dominates all 7 dimensions |

## Relevance to Software Engineers

Long-horizon business agents need memory of counterpart behavior (negotiation leverage compounds) and robustness trade-offs (top earner near-worst on fraud). If you benchmark ops agents, score assets *and* safety/efficiency separately. Code: https://github.com/QwenLM/E-CommerceBench

## Related Concepts

- [Agent](../../concepts/ai-engineering/agent.md)
- [Agent Evaluation](../../concepts/ai-engineering/agent-evaluation.md)

## References

- arXiv: https://arxiv.org/abs/2608.30730
- HuggingFace: https://huggingface.co/papers/2608.30730
- Scope: abstract-based; per-model dimension tables are in the full text
