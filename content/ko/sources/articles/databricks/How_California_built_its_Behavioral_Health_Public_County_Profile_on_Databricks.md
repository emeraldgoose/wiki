---
title: "캘리포니아는 Databricks로 행동건강 공개 카운티 프로파일을 어떻게 만들었나"
description: "58개 카운티의 행동건강 데이터를 하나의 공개 대시보드로 묶어 BHSA 투명성과 감독을 실현한 캘리포니아 DHCS 사례."
tags: [source, databricks, lakehouse, public-sector, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-california-built-its-behavioral-health-public-county-profile-databricks"
blog: databricks
published_date: 2026-10-09
---

# 캘리포니아는 Databricks로 행동건강 공개 카운티 프로파일을 어떻게 만들었나

**출처**: [Databricks Blog](https://www.databricks.com/blog/how-california-built-its-behavioral-health-public-county-profile-databricks) · **발행**: 2026-10-09

## 개요

캘리포니아 보건의료서비스부(DHCS)는 58개 카운티의 행동건강 데이터를 모은 사상初の 공개 대시보드 Behavioral Health Public County Profile을 출시했다. FedRAMP 인증 환경의 Databricks 위에 구축된 이 대시보드는 주민발의안 1호에 따른 행동건강서비스법(BHSA)의 책임 엔진으로, 누구나 카운티별 자금·서비스·성과를 비교할 수 있다.

## 분산 사일로에서 하나의 프로파일로

카운티 지출 계획, 인구통계, 노숙인 서비스, 성과 지표는 서로 다른 시스템·주기에 흩어져 있었다. 프로파일은 이를 통합해 카운티 비교, 서비스 사각지대 파악, 주거 관련 서비스 추적, 카운티별 3개년 BHSA 통합계획 열람, 투자-성과 연계 지표 모니터링을 가능케 했다. 법정 보고가 민주적 감독 수단으로 바뀐 셈이다.

## 투명성 뒤의 플랫폼

수십 개 카운티 소스는 Spark Declarative Pipelines와 Lakeflow Connect로 하나의 거버넌스 플랫폼에 수집되고, Semantic View가 지표를 한 번만 정의해 카운티 간 비교를 동일 기준으로 맞추며, 서버리스 컴퓨트가 인프라 관리를 없애고, 종단 계보와 FedRAMP 보안이 공개 수치마다 추적 가능성과 보호를 보장한다. 교훈은 투명성을 정적 정기 보고서가 아닌 살아있는 데이터 제품으로 다루라는 것이다.

## References

- [How California built its Behavioral Health Public County Profile on Databricks](https://www.databricks.com/blog/how-california-built-its-behavioral-health-public-county-profile-databricks)
