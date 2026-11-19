---
title: "Databricks Feature Views로 실시간 차선책(next-best-offer) 추천기 만들기"
description: "Databricks Solution Accelerator가 Feature Views 기반의 엔드투엔드 리테일 뱅킹 차선책 추천기를 소개한다: 배치·스트리밍 피처를 한 번만 선언하고, point-in-time 정확 학습과 밀리초 서빙(~34 ms p95)을 구현한다."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views"
blog: databricks
published_date: "2026-11-19"
---

# Databricks Feature Views로 실시간 차선책(next-best-offer) 추천기 만들기

**출처**: [databricks](https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views) · **게시일**: 2026-11-16

## 개요

실시간 개인화는 고객이 지금 무엇을 원하는지 이해하는 데서 출발한다. 리테일 뱅킹 고객이 계좌를 확인하고, 신용카드를 살펴보고, 대출 계산기를 여는 각각의 행동은 현재 의도를 드러내며, 관련성 높은 제안은 고객이 아직 세션에 머물러 있을 때 도달해야 한다. 어려운 점은 그 의도를 모델이 쓸 수 있게 만드는 것이다. 원시 클릭스트림 데이터는 두 가지 목적을 위해 시간 창 피처로 집계되어야 한다 — 특정 시점에 존재했던 과거 값으로 학습하는 것과 밀리초 지연으로 예측을 서빙하는 것. 이 두 파이프라인을 따로 만들면 중복된 피처 정의가 생기고, 시간이 지나며 드리프트해 모델 정확도를 갉아먹는다.

Databricks Feature Views는 피처를 한 번만 정의해 학습과 서빙에서 함께 쓰게 함으로써 이 문제를 해결한다. 이 글은 금융 서비스용 실시간 차선책(NBO) 추천기를 Databricks 위에 엔드투엔드로 구축하는 오픈소스 Solution Accelerator를 따라가며, 실행 가능한 노트북을 함께 제공한다.

## 핵심 내용

- **한 번 만들고 어디서나 서빙**: Feature Views는 배치·스트리밍 피처를 통합해 학습과 서빙이 선언적 정의를 공유하게 하므로 train/serve 스큐를 제거한다.
- **배치 피처**는 point-in-time 정확 학습을 위한 오프라인 Delta 테이블과 저지연 서빙을 위한 온라인 스토어에 구체화된다.
- **스트리밍 피처**는 온라인 스토어에 지속적으로 집계되며, 학습용 과거 값은 소스 이벤트에서 point-in-time으로 계산되고 오프라인 스토어에는 구체화되지 않는다.
- **Point-in-time 조인**: `create_training_set` API가 각 라벨 이벤트 시점에 존재했던 피처 값을 가져와 미래 데이터 누수를 방지한다.
- **같은 정의, 두 경로**: 추론 시 Model Serving 엔드포인트는 학습과 동일한 Feature View 선언을 사용해 `customer_id`로 온라인 스토어에서 배치 피처를 가져온다.
- **세션 내 의도**: SawtoothWindow는 긴 창의 스트리밍 피처(예: 30일 카테고리 카운트)를 이벤트가 도착할 때마다 전체 이력을 다시 계산하지 않고도 신선하게 유지한다.
- **벤치마크**: 최소 구성(작은 엔드포인트, 단일 노드 온라인 스토어, 튜닝 없음)에서 스트리밍 이벤트는 약 0.1초 만에 모델에 보이는 피처가 되었고, 학습·서빙 경로는 동일한 값을 산출했다.
- **~34 ms p95 지연**의 서빙(가속기의 대표 수치).

## 세부 내용

이 가속기는 리테일 뱅킹 NBO 추천기를 구현한다. 고객이 탐색하는 동안 시스템은 안정적인 고객 맥락(잔고, 지출, 가입 기간, 리스크 등급)과 세션 내 의도를 담은 최근 클릭스트림을 결합해 제안 카탈로그(신용카드 업그레이드, 예금 상품, 개인 대출)를 랭킹한다. 단일 LightGBM 랭커가 두 데이터를 모두 사용하며 Unity Catalog에 등록된다.

세 단계, 두 파트로 나뉜 실행 가능한 노트북으로 제공되며 카탈로그·스키마·온라인 스토어·피처 정의를 공유한다:

1. **배치·스트리밍 피처 정의** — 30일 평균 잔고는 `SlidingWindow`, 90일 지출은 `TumblingWindow`, 로열티 등급/리스크 등급/소득/가입 기간은 `ColumnSelection`, 최근 10분 카테고리 조회는 Kafka 스트림 위 `RollingWindow`, 30일 카테고리 관심은 `SawtoothWindow`, 지출 대 소득 비율은 `CustomUDF`로 선언한다. 스트리밍은 선언을 Kafka 토픽에 연결하면 Feature Views가 이벤트를 온라인 스토어에 지속적으로 집계하므로 별도의 수작업 스트리밍 잡이 필요 없다.
2. **Point-in-time 정확 피처로 학습** — Feature Engineering SDK의 point-in-time 조인이 각 피처를 과거 라벨 시점의 값으로 재구성하고, 그 결과가 Unity Catalog의 LightGBM 랭커로 들어간다.
3. **실시간 서빙** — 랭커는 라우트 최적화 Model Serving 엔드포인트에서 실행된다. 각 요청은 `{customer_id, 후보 제안들, 세션 맥락}`을 담고, 엔드포인트는 키로 온라인 스토어에서 피처를 가져와 40개 제안을 후보 좁히기 단계 없이 직접 채점한다. 두 번째 라우트 최적화 Feature Serving 엔드포인트는 피처 값을 노출해, 애플리케이션이 왜 그 제안이 선택됐는지 설명할 수 있게 한다.

벤치마크는 가장 중요한 두 가지를 측정한다: 클릭이 모델에 보이는 피처가 되기까지 얼마나 걸리는지, 그리고 학습과 서빙이 동일한 피처 값을 산출하는지. 둘 다 튜닝 없는 최소 구성에서 확인되었다.

## 참고 자료

- 원문: [Build a real-time next-best-offer recommender using Databricks Feature Views](https://www.databricks.com/blog/build-real-time-next-best-offer-recommender-using-databricks-feature-views)
