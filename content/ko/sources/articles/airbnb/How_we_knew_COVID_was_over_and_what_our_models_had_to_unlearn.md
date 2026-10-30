---
title: "COVID가 끝났다는 걸 어떻게 알았고, 모델은 무엇을 잊어야 했나"
description: "Airbnb 예측 팀이 COVID 회복을 감지하고 모델의 팬데믹 가정을 풀어낸 과정."
tags: [source, airbnb, forecasting, machine-learning, ko]
locale: ko
source_url: "https://airbnb.tech/ai-ml/how-we-knew-covid-was-over-and-what-our-models-had-to-unlearn"
blog: airbnb
published_date: 2026-08-20
---

# COVID가 끝났다는 걸 어떻게 알았고, 모델은 무엇을 잊어야 했나

**원문**: [airbnb 블로그](https://airbnb.tech/ai-ml/how-we-knew-covid-was-over-and-what-our-models-had-to-unlearn) · **게시일**: 2026-08-20

## 개요

Airbnb의 Forecasting Data Science 팀은 수요, 예약, 점유율 등 회사 계획의 기반이 되는 다양한 예측을 생성한다. COVID-19로 인해 일반적인 가정이 깨졌기 때문에 팬데믹 행동으로 학습된 모델은 회복 신호가 나타나면 팬데믹 전 baseline으로 돌아가야 했다. 이 글은 팀이 COVID 종료를 어떻게 판단했고 모델이 무엇을 unlearn해야 했는지 설명한다.

## 핵심 내용

- 수요/예약/점유율 예측은 COVID가 무효화한 구조적 가정에 의존한다.
- 회복 감지에는 팬데믹 효과와 일반 seasonality/trend를 분리해야 했다.
- 모델은 COVID 기간 동안 배운 임시 행동을 버리고 안정 패턴을 다시 학습했다.
- 예측 인프라와 모니터링이 전환을 인식하는 데 필수적이었다.
- 충격기 학습만큼 팬데믹 이후 unlearning도 중요하다.

## 상세

예측 시스템은 거시적 레짐 변화를 추적하고 모델 가정을 적응해야 하며 그렇지 않으면 예측이 outdated pandemic behavior를 계속 인코딩한다.

## 참고 자료

- 원문: [https://airbnb.tech/ai-ml/how-we-knew-covid-was-over-and-what-our-models-had-to-unlearn](https://airbnb.tech/ai-ml/how-we-knew-covid-was-over-and-what-our-models-had-to-unlearn)
