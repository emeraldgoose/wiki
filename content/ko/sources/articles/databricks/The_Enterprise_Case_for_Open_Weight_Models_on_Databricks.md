---
title: "Databricks에서 Open-Weight Models의 Enterprise Case"
description: "비용, 통제, 거버넌스를 위해 open-weight와 frontier 모델을 함께 사용하는 근거."
tags: [source, article, databricks, open-weight-models, ko]
locale: ko
published_date: 2026-11-05
source_url: "https://www.databricks.com/blog/enterprise-case-open-weight-models-databricks"
blog: databricks
---

# Databricks에서 Open-Weight Models의 Enterprise Case

**원문**: [Databricks Blog](https://www.databricks.com/blog/enterprise-case-open-weight-models-databricks)

## 개요

Databricks field engineers는 enterprises가 단일 frontier provider 표준화 전략을 재평가하는 현장을 관찰한다. 주요 압박은 spend가 충분한 return을 만들지 못함, 2023 이후 model rankings의 반복적 변화, frontier guardrails의 legitimate work 차단, data retention policy 변화, model governance visibility, harness 성능 영향, open-weight model의 frontier catch-up 등이다. Databricks는 models와 harnesses가 governance를 약화하지 않고도 change할 수 있는 architecture를 권장한다. Unity Gateway는 open-weight와 frontier models를 unified API와 centralized governance controls로 제공하며, smart routing, fallback, budgets, audit trails 등을 지원한다.

## 핵심 내용

- AI budgets가 measured returns보다 빠르게 커진 경우가 있다.
- model rankings는 자주 바뀌므로 swap 가능성이 필요하다.
- frontier guardrails가 legitimate defensive analysis를 차단할 수 있다.
- data retention policy 변화는 compliance risk를 만들 수 있다.
- open-weight models가 now comparable intelligence/cost footing에 도달했다.
- Unity Gateway는 unified governance controls를 제공한다.

## 상세

Databricks는 average unique models per customer가 4.2에서 7.1로 증가했고 used models 중 약 40%가 open-weight라고 보고한다. smart routing은 routine tasks를 cheaper models로 shift하고 fallback chains는 rate limit/outage를 handle한다. GLM 5.2는 offered된 한 달 만에 open-weight tokens의 약 40%를 차지했다. 이 주장은 July 2026까지 customer data와 특정 period에 의존하며 broader cost/risk Tradeoffs도 고려해야 한다. migration 전에는 model-plus-harness performance와 governance controls를 평가해야 한다.

## 참고 자료

- 원문: [Databricks Blog](https://www.databricks.com/blog/enterprise-case-open-weight-models-databricks)
