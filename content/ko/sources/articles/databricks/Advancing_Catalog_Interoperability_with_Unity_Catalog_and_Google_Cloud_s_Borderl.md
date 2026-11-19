---
title: "Unity Catalog와 Google Cloud Borderless Lakehouse의 카탈로그 상호운용성 진전"
description: "Databricks와 Google Cloud가 Unity Catalog와 Google Cloud borderless Lakehouse 간 양방향 카탈로그 페더레이션(Iceberg 테이블, GA)을 열었고, 거버넌스 메타데이터(domain, status, PII 태그)가 카탈로그 간 테이블과 함께 이동하도록 Iceberg catalog labels 제안을 주도했다."
tags: [source, article, databricks, unity-catalog, iceberg, google-cloud, ko]
locale: ko
source_url: "https://www.databricks.com/blog/advancing-catalog-interoperability-unity-catalog-and-google-clouds-borderless-lakehouse"
blog: databricks
published_date: 2026-11-19
---

# Unity Catalog와 Google Cloud Borderless Lakehouse의 카탈로그 상호운용성 진전

**Source**: [Databricks Blog](https://www.databricks.com/blog/advancing-catalog-interoperability-unity-catalog-and-google-clouds-borderless-lakehouse)
**게시일**: 2026-11-18

## 개요

Databricks와 Google Cloud가 카탈로그 상호운용성의 이정표를 발표했다. 이제 고객은 Unity Catalog와 Google Cloud borderless Lakehouse 양쪽에서 단일 사본의 데이터에 접근할 수 있다. 이는 개방형 테이블 포맷(Delta Lake, Iceberg)과 제로카피 접근을 위한 카탈로그 페더레이션으로 이어진 파트너십의 오픈 레이크하우스 작업을, 양방향 상호운용성과 개방형 카탈로그 메타데이터로 확장한 것이다.

## 주요 내용

- 인바운드(Google Cloud → Databricks): Google Cloud로의 Lakehouse Federation이 일반 제공(GA)으로 전환되었다. Google Cloud Lakehouse 런타임 카탈로그가 관리하는 Iceberg 테이블을 Unity Catalog에 마운트해 Databricks(서버리스 Databricks SQL/Lakehouse 포함)로 쿼리하거나, 코드나 SQL 없이 자연어로 답하는 Genie로 분석할 수 있다.
- 아웃바운드(Databricks → Google Cloud): Databricks의 데이터를 Google Cloud Lakehouse로 가져올 수 있어, BigQuery 같은 엔진이 Unity Catalog 관리 테이블을 데이터 복사 없이 읽을 수 있다.
- 다음 프런티어 — 카탈로그 메타데이터: Databricks와 Google Cloud는 Iceberg 커뮤니티에서 catalog labels 제안을 주도해 반영시켰다. 카탈로그가 키-값 쌍(라벨)으로 메타데이터를 공유하도록 하는 제안이다. `domain=finance`, `status=certified`로 태그된 테이블이나 `pii=ssn`으로 태그된 컬럼은 카탈로그 간 페더레이션되어도 태그를 유지한다.
- 에이전트 시대의 거버넌스에 공유 라벨이 중요하다. 카탈로그 메타데이터로 민감 데이터를 마스킹 대상으로 표시하고, 에이전트가 자산을 검색할 때 맥락을 제공할 수 있다. 양사는 비즈니스·접근 의미론이 시스템마다 재정의되지 않고 데이터와 함께 이동하도록 오픈 거버넌스를 진전시키겠다고 약속했다.
- 시작하기: Unity Catalog와 Google Cloud borderless Lakehouse 간 Catalog Federation 문서, 또는 Google의 Unity Catalog 페더레이션 문서를 참고하거나, Databricks 계정 팀에 문의하면 된다.

## 상세

- 레이크하우스 아키텍처는 오픈 테이블 포맷에서 제로카피 크로스플랫폼 접근을 위한 카탈로그 페더레이션으로 진화해 왔으며, 이번 발표는 그 진전의 최신 이정표다.
- 상호운용성은 양방향이다: Lakehouse Federation(GA)을 통한 Google Cloud → Databricks, 그리고 BigQuery가 Unity Catalog 테이블을 읽는 Databricks → Google Cloud.
- Catalog labels는 메타데이터 이동성의 메커니즘이다. 거버넌스와 비즈니스 의미론(PII 태그, 인증 상태, 도메인)이 카탈로그 간 이동하는 테이블·컬럼에 계속 붙어 있다.
