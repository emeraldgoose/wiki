---
title: "클라우드 데이터 웨어하우스 비용에 예산과 알림 설정하기"
description: "Databricks SQL 웨어하우스 비용 거버넌스: 태그 귀속, 계층형 예산, 페이싱 알림, 대시보드, 최적화의 5단계 사전 관리법."
tags: [source, databricks, cost-optimization, sql-warehouses, finops, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/set-budgets-and-alerts-cloud-data-warehouse-costs"
blog: databricks
published_date: 2026-10-07
---

# 클라우드 데이터 웨어하우스 비용에 예산과 알림 설정하기

## 개요

월말 고지서에서 SQL 웨어하우스 폭탄을 발견하는 사후 정산 대신 사전 비용 관리가 필요하다. 프레임워크는 귀속·예산·알림·대시보드·최적화 5개 축이며, 출발점은 서버리스 웨어하우스 기본 채택이다. 버스티한 BI 워크로드의 유휴 과금을 없애주기 때문이다.

## 귀속: 웨어하우스와 쿼리에 태그 달기

모든 웨어하우스를 생성 시점에 태깅(팀·코스트센터·용도)하면 `system.billing.usage`가 DBU를 소유자와 연결한다. 네이티브 태그 강제 정책이 없으므로 Terraform·번들·API로 프로비저닝에 강제한다. 공유 웨어하우스 안에서는 쿼리 태그가 개별 문장에 업무 맥락(대시보드·dbt 모델)을 붙여 `system.query.history`에서 실제 지출 주체를 드러낸다. Governance Hub의 Cost 페이지에서 계정 차원 태깅 커버리지를 빠르게 확인할 수 있다.

## 제때 울리는 예산과 알림

Account Console(Usage > Budgets)에 계층형 예산을 만든다. 팀별 예산으로 책임을, 계정 전체 예산으로 안전망을, 워크스페이스·태그로 범위를 잡는다. 예산은 차단이 아닌 모니터링이므로 `system.billing.usage` 위의 SQL Alert를 곁들인다. 가장 값진 것은 월말 지출을 예측해 위반 며칠 전에 울리는 페이싱 알림이며, 일일 지출 임계값과 파이프라인 과금으로 숨어드는 구체화 뷰 리프레시 비용 점검도 함께 둔다.

## 대시보드, 모니터링, 실질 절감

기본 제공 사용량 대시보드를 가져오고 두 쿼리를 추가한다. 팀별 웨어하우스 비용과 미귀속 사용량(귀속 공백을 0으로 수렴)이다. 가시성 자체가 행동을 바꾸며, 한 은행의 셀프서비스 비용 플랫폼이 이를 입증했다. 그 다음이 청구서 절감이다. 관리형 테이블의 예측 최적화, auto-stop·statement timeout 조이기, 적정 기본 웨어하우스 지정, scale-up/scale-out의 의도적 선택, 쿼리 자체 수정이 그것이다. 비용 문제는 대개 비싼 쿼리 문제이며, 귀속 계층이 바로 그 쿼리를 가리킨다.

## References

- 원문: [Set Budgets and Alerts for Cloud Data Warehouse Costs](https://www.databricks.com/blog/set-budgets-and-alerts-cloud-data-warehouse-costs)
