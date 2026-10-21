---
title: "Databricks에서 SQL로 open-Jev 실행하기"
description: "오픈 가중치 Jev 결정 모델을 서버리스 GPU에 서빙하고 ai_query로 거버넌스 데이터에 SQL에서 직접 호출한다."
tags: [source, databricks, model-serving, sql, llm, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/running-open-jev-sql-databricks"
blog: databricks
published_date: 2026-09-24
---

# Databricks에서 SQL로 open-Jev 실행하기

## 개요

Jev 계열 "System One" 결정 모델은 정해진 선택지에서 빠르고 잘 보정된 결정을 내놓아 대규모 적용에 싸지만, 거대한 거버넌스 데이터에 닿아야 진가를 낸다. 이 글은 오픈 가중치 결정 모델(SemIf-OpenJev)을 Databricks에 서빙하고 SQL 콘솔이나 Lakeflow 잡에서 직접 호출하는 법을 호텔 리뷰 분류 예제로 보여준다.

## 노트북에서 엔드포인트까지

가져오기 가능한 노트북이 전체 과정을 자동화한다. 모델 선택, 서버리스 GPU 선택, 전체 실행 세 단계면 가중치를 내려받아 Express Deployments로 등록하고 GPU Model Serving 엔드포인트를 만든다. GPU 인프라 관리 없이 관리형 분류기 엔드포인트가 생겨 앱이나 SQL에서 호출할 수 있다.

## ai_query로 SQL에서 모델 호출하기

`ai_query`는 chat-completions 형태가 아닌 임의의 커스텀 모델 API를 지원하므로, SemIf의 구조화 요청 형식을 SQL에서 바로 보낼 수 있다. 선택된 분류와 선택지별 확률이 구조화 컬럼으로 돌아와 Databricks에 이미 저장된 테이블을 프로덕션 규모로 스코어링할 수 있다. AI Runtime으로 파인튜닝·커스터마이징하면 기업별 결정 기준에 맞출 수도 있다.

## References

- 원문: [Running open-Jev in SQL on Databricks](https://www.databricks.com/blog/running-open-jev-sql-databricks)
