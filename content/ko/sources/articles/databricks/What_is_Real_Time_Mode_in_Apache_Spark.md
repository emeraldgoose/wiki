---
title: "Apache Spark의 Real-Time Mode란 무엇인가?"
description: "Real-Time Mode는 각 레코드를 도착 즉시 처리하는 Spark Structured Streaming 트리거(밀리초 단위 종단 지연) — 같은 엔진·API에서 사기 탐지, 개인화, 실시간 AI 기능을 제공하며 별도의 스트림 전용 엔진이 필요 없다."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/what-is-real-time-mode"
blog: databricks
published_date: "2026-11-19"
---

# Apache Spark의 Real-Time Mode란 무엇인가?

**출처**: [databricks](https://www.databricks.com/blog/what-is-real-time-mode) · **게시일**: 2026-11-13

## 개요

Real-Time Mode는 다음 마이크로 배치를 기다리지 않고 레코드가 도착하는 즉시 처리하는 Apache Spark Structured Streaming 트리거다. Spark 스트리밍을 수 초 지연에서 밀리초 단위 종단 지연으로 끌어내리며, 배치·마이크로 배치와 동일한 엔진과 API 위에서 동작한다. Real-Time Mode 이전에는 초 미만 응답이 필요한 팀이 별도의 스트림 전용 엔진을 추가하는 경우가 많았는데, Real-Time Mode는 대부분의 워크로드에서 그 요구를 없앤다. 기존 쿼리의 트리거만 바꾸면 Spark가 연속적으로 실행한다.

## 핵심 내용

- Real-Time Mode 활성화는 트리거 한 줄 변경이다. 소스, 변환 로직, 체크포인트는 그대로이므로 재작성이 필요 없다.
- 사기 탐지, 개인화, 실시간 AI 기능 — 이전에는 Apache Flink급 엔진이 필요했던 워크로드에 사용한다.
- DraftKings는 라이브 스포츠 베팅의 사기 탐지에 `transformWithState`와 함께 Real-Time Mode를 사용한다.
- MakeMyTrip은 44ms P50 지연시간으로 개인화된 호텔 결과를 제공한다.
- 같은 파이프라인이 모델 학습·온라인 추론용 피처를 계산하고 AI 에이전트에 최신 이벤트를 계속 공급한다.

## 세부 내용

Real-Time Mode는 Spark의 마이크로 배치 모델(초 단위 지연)과 인터랙티브·AI 지향 유스케이스의 초 미만 요구 사이의 간극을 겨냥한다. Spark Structured Streaming 안에서 동작하므로 기존 지식·코드·운영을 그대로 이어 쓸 수 있다: 동일한 DataFrame/Dataset API, 동일한 체크포인팅 모델, 동일한 운영 도구. `transformWithState`를 통한 상태ful 처리를 지원하며, 이것이 DraftKings식 라이브 이벤트 사기 점수를 가능하게 한다.

원문의 FAQ는 어떤 Spark 버전이 Real-Time Mode를 지원하는지, 서버리스나 Free Edition에서 실행되는지, 상태ful 연산 지원 여부, Apache Flink 및 과거의 continuous processing 실험 모드와의 관계 같은 운영 질문을 다룬다. 또한 온라인 추론과 에이전트 컨텍스트를 위한 밀리초 단위 피처 신선도를 강조하는 Databricks의 "agentic AI playbook" 포지셔닝 속에 Real-Time Mode를 위치시킨다.

## 참고 자료

- 원문: [What is Real-Time Mode in Apache Spark?](https://www.databricks.com/blog/what-is-real-time-mode)
