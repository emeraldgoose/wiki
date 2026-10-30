---
title: "데이터를 이동하지 않고 투자 인사이트 얻기: Lakehouse Federation"
description: "Lakehouse Federation은 온프레미스 포트폴리오 데이터를 그 자리에서 조회하고 FactSet 마켓플레이스 데이터와 조인해, 데이터 이동이나 복사 없이 대시보드와 Genie를 가능하게 합니다."
tags: [source, databricks, data-engineering, federation, lakehouse, finance, ko]
locale: ko
source_url: "https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation"
blog: databricks
published_date: "2026-10-27"
---

# 데이터를 이동하지 않고 투자 인사이트 얻기: Lakehouse Federation

**원문**: [databricks](https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation) · **게시일**: 2026-10-27

## 개요

오늘날 기업 환경에서 데이터는 한 곳에 있지 않습니다. 금융 기관, 자산 운용사, 개별 투자자 모두 공통 과제에 직면합니다. 포트폴리오 보유 종목, 매매 포지션, 고객 정보 같은 민감한 데이터는 주로 온프레미스 방화벽 뒤, 클라우드, 또는 양쪽에 함께 저장되며, 분석에 필요한 시장 데이터, 애널리스트 추정치, 재무 기본 데이터 같은 제3자 데이터는 점점 더 클라우드에 있습니다. 전통적 접근은 불편한 선택을 강요합니다. 민감한 데이터를 클라우드로 복사하거나, 취약한 ETL 파이프라인을 구축하거나, 통합을 포기하는 것입니다.

Databricks Lakehouse Federation은 온프레미스 소스를 페더레이션하고 제3자 클라우드 데이터를 구독해, 복사나 중간 객체 저장 없이 단일 SQL 쿼리로 두 카탈로그를 조인할 수 있게 합니다.

## 핵심 내용

- Lakehouse Federation은 SQL Server, PostgreSQL, MySQL, Snowflake 같은 외부 데이터베이스에 페더레이션 연결을 만들고 Databricks에서 표준 SQL로 직접 조회합니다. 데이터는 전혀 이동하지 않습니다.
- FactSet 같은 마켓플레이스 데이터 셰어가 Unity Catalog의 페더레이션 카탈로그 옆에 놓이고, 단일 SQL 쿼리가 일반 테이블처럼 조인합니다.
- 구체적 부유관리 사례는 온프레미스 SQL Server의 보유 종목을 마켓플레이스의 FactSet 추정치, 기본, 심볼로지 데이터와 조인합니다.
- 대시보드는 각 위젯에 조인 쿼리를 그대로 삽입하며, 저장된 뷰나 테이블이 없고 매 새로고침 때 소스를 재페더레이션합니다.
- Genie는 자연어를 동일 쿼리로 번역해 포트폴리오 매니저, 재무 고문, 개별 투자자 모두에게 데이터 접근을 민주화합니다.
- 이 패턴은 넓게 적용됩니다. 의료는 HIPAA 보호 환자 기록과 약물 상호작용 DB를, 제조는 온프레미스 IoT 텔레메트리와 클라우드 공급망 데이터를, 리테일은 매장 POS와 제3자 인구통계를 조인할 수 있습니다.

## 상세

워크스루는 온프레미스 데이터베이스에 매핑되는 외부 카탈로그를 만들어 외부 테이블이 네이티브 Unity Catalog 객체처럼 보이게 합니다. 데이터는 SQL Server를 떠나지 않으며, 모든 쿼리는 실시간으로 소스에서 실행됩니다. FactSet 데이터는 마켓플레이스에서 구독되어 추정치, 재무, 심볼로지 같은 스키마를 가진 셰어드 카탈로그로 제공됩니다.

두 소스가 모두 접근 가능해지면, 에셋 매니저는 페더레이션된 보유 종목과 FactSet 테이블을 아우르는 단일 쿼리를 실행해 포트폴리오 건강, 위험 분포, 투자 추천, 상위 성과, 전체 보유 테이블, Genie 자연어 답변을 산출합니다. 작성할 파이프라인, 스케줄할 구체화 뷰, 유지할 골드 레이어가 없습니다.

컴퓨트를 데이터로 가져오는 방식으로 Lakehouse Federation은 민감한 1자 데이터를 보호하면서 제3자 데이터와의 풍부한 분석을 가능하게 하여, 하이브리드 데이터 분석의 경제성을 바꿉니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/unlocking-investment-insights-without-migrating-your-data-lakehouse-federation
