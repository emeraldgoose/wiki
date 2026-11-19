---
title: "브랜치, 싱크, 서브: Lakebase Hackathon이 Lakebase 빌드에 대해 가르쳐준 것"
description: "Databricks Lakebase Hackathon은 브랜칭(트랙 1)과 싱크/서브(트랙 2)로 나뉘었다. Lyft의 Jevons Search는 쓰기 시 복사 브랜치로 지원 백로그 11건 중 10건을 해결했고, CIBC의 Branchflight는 5초 이내에 PR 프리뷰 환경을 만들었으며, Data Axle의 PriceWise는 최소 4ms의 가격 응답을 제공했다."
tags: [source, article, databricks, lakebase, postgres, hackathon, ko]
locale: ko
source_url: "https://www.databricks.com/blog/branch-sync-serve-what-our-lakebase-hackathon-taught-us-about-building-lakebase"
blog: databricks
published_date: 2026-11-19
---

# 브랜치, 싱크, 서브: Lakebase Hackathon이 Lakebase 빌드에 대해 가르쳐준 것

**Source**: [Databricks Blog](https://www.databricks.com/blog/branch-sync-serve-what-our-lakebase-hackathon-taught-us-about-building-lakebase)
**게시일**: 2026-11-18

## 개요

Databricks는 그 어느 때보다 넓은 고객층을 대상으로 Lakebase Hackathon을 열었다. Lakebase는 스토리지와 컴퓨팅이 분리된 완전 관리형 Postgres로, Unity Catalog 거버넌스 하에 레이크하우스 데이터 옆에 자리한다. 일반 Postgres로는 쉽지 않은 세 가지를 가능하게 한다. 브랜치(Git 브랜치처럼 동작하는 쓰기 시 복사 DB 브랜치 — 즉시 생성, 프로덕션 영향 없음), 싱크(synced tables가 Unity Catalog 테이블을 읽기 전용으로 Postgres에 지속 복사 — 리버스 ETL — 하고 Lakehouse Sync가 CDC로 Postgres를 Delta에 복제), 서브(애플리케이션 상태 보관, pgvector/PostGIS/pg_trgm 검색, Online Feature Store의 온라인 스토어). 트랙 1은 브랜칭과 앱 빌드, 트랙 2는 싱크와 서브를 다뤘다. 두 트랙 모두 Unity Catalog가 접근을 거버넌스한다.

## 주요 내용

- Lyft의 Jevons Search: 비즈니스 규칙이 DB 트리거 안에 있음을 모르고 환불·예약 취소를 수행하는 에이전트 문제. 지원 티켓 배치마다 프로덕션의 쓰기 시 복사 브랜치를 약 6초 만에 포크하고, 경량 gte-large 임베딩 분류기(MLflow 추적, Model Serving 서빙)가 티켓을 8개 정책 카테고리로 분류해 런타임에 LLM 토큰을 쓰지 않는다. 사전 계획만으로는 11개 백로그 중 2개만 정책 내 완전 해결됐지만 브랜치 테스트로는 10개를 해결했다. 같은 시간에 4배 많은 브랜치를 포크해도 통과율은 오르지 않았다 — 정밀한 의사결정과 실제 DB 피드백이 brute force를 이겼다.
- CIBC의 Branchflight: 모든 풀 리퀘스트에 프리뷰 환경을 제공 — PII 마스킹된 템플릿 브랜치에서 5초 이내에 제로카피 Lakebase 브랜치를 만들고 프리뷰 Databricks App을 배포한다. 환경은 미사용 시 0으로 스케일되고, 일정 시간 후 만료되며, 병합 전 스키마 diff 검사를 통과해야 한다. 플랫폼 상태·감사 로그·비용 지표도 Lakebase에 저장된다.
- Arbital Health의 7NF 벤치마크: 데이터를 고정하고 스키마만 바꾼다. 각 레이아웃이 별도의 Lakebase 브랜치로 실행되며, 모델은 정확한 행을 반환하는지만으로 채점된다 — 고객 DB에 최적의 스키마를 고르거나 text-to-SQL 모델을 개선하는 방법.
- 기타 브랜칭 프로젝트: OneTrust는 Lakebase 브랜치로 방화벽 규칙 변경을 검증(Go 앱, 전용 컴퓨트의 쓰기 시 복사 브랜치, 재귀적 도달성 쿼리; 공격 표면을 넓히는 시험은 즉시 폐기); 두 번째 CIBC 팀은 창작 작업에 Git 스타일 브랜칭/머지를 적용한 3D 시네마틱 워크스페이스 BranchCut을 구축; Reach Mobile은 근처 매장의 가격·거리·재고를 비교하는 StreetCart를 구축(프로덕션 스키마 변경 전 새 카테고리 속성 테스트에 브랜칭 활용); Markel은 별도의 Elasticsearch 복제본 대신 거버넌스된 골드 테이블을 Lakebase로 서빙한다.
- Data Axle의 PriceWise(트랙 2): 리스팅 18,000개 이상, 호스트들이 연간 잠재 객단가 수익의 약 64%를 놓친다고 추정. 하이브리드 검색(pgvector 임베딩 + BM25를 Reciprocal Rank Fusion으로 융합), 20마일 이내 리스팅의 PostGIS 비교를 포함한 4가지 수요 요인 기반 가격 제안, 내장된 Genie 에이전트로 구성. Genie 대화는 에이전트 메모리로 Lakebase에 저장되며, 가격 응답은 최소 4ms.
- 한 운송 회사 팀은 Unity Catalog의 항공편/공항/기상 경보 테이블을 Lakebase에 싱크해 Databricks App의 실시간 지도에 활용했고, 한 보험 회사 팀은 정책 발행 후 위험 점수화(검사관이 발견할 내용 예측)에 집중했다.
- Synced tables는 관리형 Spark Declarative Pipelines를 통해 큐레이션된 Unity Catalog 데이터를 Lakebase Postgres로 이동시키고, Lakebase Change Data Feed는 Postgres 변경을 Delta로 스트리밍한다. Online Feature Stores는 Lakebase 위에서 동작해 레이크하우스 피처를 실시간으로 모델에 서빙한다.

## 상세

- 해커톤은 이네이블먼트 세션으로 시작해 약 일주일간의 빌드로 이어지며, 가장 강력한 솔루션이 상을 받는다.
- Lakebase 브랜치는 쓰기 시 복사로 즉시 생성된다. 변경분에 대해서만 비용을 내고, 브랜치 생성은 프로덕션 성능에 영향을 주지 않는다.
- 모든 Lakebase 프로젝트는 프로덕션 브랜치로 시작하며, 자식 브랜치는 개발·테스트·실험에 쓰인다. 팀들은 Genie Code로 앱을 빌드하며 브랜치를 값싼 일회용 프로덕션 복사본처럼 다뤘다.
