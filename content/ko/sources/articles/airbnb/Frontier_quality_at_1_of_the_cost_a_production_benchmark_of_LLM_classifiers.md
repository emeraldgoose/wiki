---
title: "Frontier quality at 1% of the cost: LLM 분류기 production benchmark"
description: "Airbnb fine-tuned classifier가 정책 screening에서 빠르고 저렴하게 frontier 품질을 달성한다."
tags: [source, article, airbnb, llm-classification, ko]
locale: ko
published_date: 2026-11-05
source_url: "https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers"
blog: airbnb
---

# Frontier quality at 1% of the cost: LLM 분류기 production benchmark

**원문**: [Airbnb Tech Blog](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers)

## 개요

Airbnb는 실제 production classification task에서 fine-tuned classifier 약 2B effective parameters를 frontier APIs와 비교 benchmark한다. 이 classifier는 약 1% cost로 100ms 미만에서 frontier 품질에 도달한다. classification task에는 risky user-generated content detection, support contact reason identification, review topic recognition 같은 고객 service application가 포함된다. 실제 평가 대상 task는 Airbnb pricing and payment transparency policy 위반 screening이며 high precision이 중요하다. policy 결정을 gate하는 속도 200ms 제약. 10,000 weighted examples held-out eval set. open-weight, proprietary, decision models와 Airbnb classifier 비교. concise 약 400-word prompt와 detailed 2,700-word prompt.

## 핵심 내용

- fine-tuned open-weight classifier가 훨씬 낮은 지연으로 frontier LLM accuracy에 도달할 수 있다.
- production task는 pricing/payment transparency violation screening이다.
- 약 2B effective parameters classifier F1은 0.563에서 fine-tuning 이후 0.902로 향상했다.
- domain-specific fine-tuning 후 median latency 약 35ms.
- proprietary generative models는 정확하지만 slow하고 inflexible.
- API model 비용은 volume에 따라 linear, self-hosted GPU는 fixed capacity까지 constant.

## 상세

Open-weight models는 vLLM으로 single NVIDIA RTX Pro 6000 GPU에 self-hosted; proprietary models는 vendor API. max F1 used because many proprietary models return verdict only; latency는 server-side. detailed prompt는 proprietary models에 1~3 points 추가와 fine-tuned classifier에 near match 제공하지만 latency/cost 증가. 빠른 deployable models에서는 prompt tuning이 quality gap을 close하지 못한다고. deployment는 traffic, latency budget, precision preference, hosting cost에 따라 선택해야 한다.

## 참고 자료

- 원문: [Airbnb Tech Blog](https://airbnb.tech/ai-ml/frontier-quality-at-1-of-the-cost-a-production-benchmark-of-llm-classifiers)
