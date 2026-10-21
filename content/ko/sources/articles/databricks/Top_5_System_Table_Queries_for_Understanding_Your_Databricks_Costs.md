---
title: "Databricks 비용 파악을 위한 시스템 테이블 쿼리 5선"
description: "제품·웨어하우스·팀별 지출 분석부터 이상 탐지와 다음 달 예측까지, 시스템 테이블 SQL 쿼리 다섯 개로 비용을 파악한다."
tags: [source, databricks, cost-optimization, system-tables, sql, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/top-5-system-table-queries-understanding-your-databricks-costs"
blog: databricks
published_date: 2026-09-22
---

# Databricks 비용 파악을 위한 시스템 테이블 쿼리 5선

## 개요

`system.billing.usage`를 `system.billing.list_prices`와 조인하면 계정 전체 지출을 거의 실시간으로 볼 수 있다. 오늘의 비용 설명에서 다음 달 예측까지 이어지는 다섯 스타터 쿼리를 AI/BI 대시보드 데이터셋으로 고정해 시각화·Genie 문답과 함께 쓰면 가장 효과적이다.

## 돈이 어디로 가는지: 제품·웨어하우스·팀

쿼리 1은 일별 지출을 제품별로 나눈다(사용량 팩트와 정가 차원의 조인, 할인 반영 테이블로 교체 가능). 쿼리 2는 웨어하우스별 일일 비용 추이를 본다. 소비량이 사용량의 대리 지표이므로 리사이징·auto-stop 튜닝 후보를 찾고, 웨어하우스 이벤트와 모니터링 페이지로 교차 확인한다. 쿼리 3은 강제 커스텀 태그(팀·프로젝트)별 지출을 묶어, 미태그 레코드로 태그 강제 누락 지점을 드러낸다.

## 급증 포착과 전망

쿼리 4는 14일 이동 평균 기준으로 일일 지출을 판정한다(1 표준편차 초과는 상승, 2 초과는 이상). 대시보드 패널이나 폭주 잡·웨어하우스용 자동 알림으로 쓴다. 쿼리 5는 SQL AI 함수 `ai_forecast`로 최근 사용량을 30일 전망으로 외삽한다. 수동 시계열 모델링 없이 다음 달 청구서를 가늠할 수 있으나, 완전히 새로운 계획 워크로드는 히스토리에 없으므로 별도 반영해야 한다.

## References

- 원문: [Top 5 System Table Queries for Understanding Your Databricks Costs](https://www.databricks.com/blog/top-5-system-table-queries-understanding-your-databricks-costs)
