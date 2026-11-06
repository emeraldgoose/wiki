---
title: "Feature Views를 활용한 실시간 사기 탐지"
description: "Feature Views가 학습과 서빙에서 feature 정의를 통합해 실시간 사기 탐지의 skew를 줄인다."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/real-time-fraud-detection-feature-views"
blog: databricks
published_date: "2026-11-07"
---

# Feature Views를 활용한 실시간 사기 탐지

**원문**: [Databricks Blog](https://www.databricks.com/blog/real-time-fraud-detection-feature-views) · **게시일**: 2026-11-05

## 개요

실시간 사기 탐지는 짧은 판단 시간 안에 고객의 최근 활동, 일반적인 지출 패턴, 현재 거래 세부 정보를 결합해야 한다. Databricks Feature Store의 Feature Views는 feature를 한 번 정의해 point-in-time training data와 managed serving pipeline 양쪽에서 사용하게 해 training-serving skew와 data leakage 위험을 줄인다.

글은 streaming payment 시나리오를 데모로 사용한다. features는 5분 transaction count, 10분 total, 30일 평균과 표준편차, 그리고 live payment와 고객 baseline 비교를 위한 request-time 계산을 포함한다. historical, streaming, on-demand 기능은 모두 Unity Catalog 아래의 동일한 feature 정의에서 동작한다.

feature 로직을 학습과 서빙에서 일관되게 유지함으로써 model은 학습 때와 일치하는 입력을 받고, streaming 및 on-demand 계산이 customer context를 최신 상태로 유지한다. 별도 preprocessing pipeline 없이 사기 탐지의 적시성을 개선한다.

## 핵심 내용

- 실시간 fraud model은 최근 활동, 지출 baseline, transaction context가 필요하다.
- training-serving skew는 학습과 production에서 feature 계산이 다를 때 발생한다.
- point-in-time correct features는 data leakage를 방지한다.
- Feature Views는 training과 serving을 위한 하나의 feature 정의를 제공한다.
- Rolling window와 Sawtooth window가 단기와 장기 baseline을 유지한다.
- on-demand features는 live transaction을 stored customer baseline과 비교한다.

## 상세

walkthrough는 Kafka에서의 ingestion, training용 managed offline storage, Unity Catalog governance, request-time Model Serving를 설명한다. 실시간 transaction monitoring과 visualization을 위해 Databricks Apps도 사용한다.

## 참고 자료

- 원문: [Databricks Blog](https://www.databricks.com/blog/real-time-fraud-detection-feature-views)
