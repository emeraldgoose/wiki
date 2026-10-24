---
title: "Predictive AI Functions로 인사이트와 예측 활용하기"
description: "SQL 분석가와 비즈니스 사용자가 예측·원인 분석·이상 탐지를 직접 실행할 수 있는 Predictive AI Functions 베타를 소개합니다."
tags: [source, databricks, data-engineering, forecasting, ko]
locale: ko
source_url: "https://www.databricks.com/blog/unlock-powerful-insights-and-forecasts-predictive-ai-functions"
blog: databricks
published_date: 2026-10-14
---

# Predictive AI Functions로 인사이트와 예측 활용하기

**원문**: [databricks](https://www.databricks.com/blog/unlock-powerful-insights-and-forecasts-predictive-ai-functions) · **게시일**: 2026-10-14

## 개요

데이터 팀은 늘 같은 질문을 받습니다. "다음 분기 매출은?", "이 지표는 왜 움직였나?", "최근 데이터가 평소 범위를 벗어났나?" 이런 고급 분석 질문에 답하려면 보통 데이터 과학 팀이 모델을 만들고 인프라를 관리해야 했습니다. 그 결과 비즈니스 사용자는 줄을 서서 기다리고, 많은 질문은 아예 나오지도 못했습니다.

베타로 공개된 Predictive AI Functions는 분석가와 비즈니스 사용자가 최신 ML 모델을 기반으로 한 내장 함수로 예측, 원인 분석, 이상 탐지를 직접 실행하게 해줍니다. SQL에서 바로 호출하거나 Genie에서 자연어로 질문하거나 대시보드에 넣을 수 있습니다.

## 핵심 내용

- 고급 ML 지식 없이 예측, 이상 탐지, 지표 원인 분석, 값을 수행합니다.
- Genie와 기존 워크플로에 쉽게 넣을 수 있고 모델을 직접 유지할 필요가 없습니다.
- `ai_forecast`, `ai_top_drivers`, `ai_detect_anomalies`, `ai_predict_value`, `ai_predict_class` 다섯 함수를 제공합니다.
- `ai_forecast`는 시계열을 미래로 투영합니다.
- `ai_top_drivers`는 지표 변화에 가장 크게 기여한 세그먼트를 찾습니다.
- `ai_detect_anomalies`는 시계열 데이터의 이상치 행을 표시합니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/unlock-powerful-insights-and-forecasts-predictive-ai-functions
