---
title: "임상 데이터와 대화하기: OpenSharing과 Genie One으로 AWS HealthLake 잠금 해제"
description: "Databricks App으로 실행되는 커스텀 OpenSharing 서버가 AWS HealthLake의 FHIR Iceberg 테이블을 실시간으로 읽게 해준다 — 내보내기 파이프라인·복제 없이 Unity Catalog 거버넌스와 Genie One 자연어 탐색을 제공."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/talk-your-clinical-data-unlocking-aws-healthlake-opensharing-and-genie-one"
blog: databricks
published_date: "2026-11-19"
---

# 임상 데이터와 대화하기: OpenSharing과 Genie One으로 AWS HealthLake 잠금 해제

**출처**: [databricks](https://www.databricks.com/blog/talk-your-clinical-data-unlocking-aws-healthlake-opensharing-and-genie-one) · **게시일**: 2026-11-16

## 개요

많은 헬스케어·라이프사이언스 조직이 임상 데이터 표준으로 AWS HealthLake를 채택하지만, 그 데이터를 분석과 AI를 위해 다른 플랫폼으로 확장하는 일은 전통적으로 내보내기 파이프라인, 데이터 복제, 별도 관리되는 거버넌스를 요구했다. 이 때문에 HealthLake가 관리하는 FHIR 데이터의 도구 간 상호운용성은 제한적이었다.

Databricks는 OpenSharing(Linux Foundation AI & Data 프로젝트)을 활용한 HealthLake–Databricks 통합을 처음으로 제시한다. 사용자는 HealthLake 데이터를 Databricks에서 실시간으로 질의할 수 있고 — 복제 없이 Databricks의 거버넌스·분석·AI 역량을 임상 데이터셋에 적용할 수 있으며 — Genie One으로 같은 데이터를 자연어로 탐색할 수 있다.

## 핵심 내용

- **FHIR와 HealthLake**: FHIR는 건강 정보 교환의 데이터 표준이며, HealthLake는 FHIR 데이터를 HealthLake 소유 S3 버킷의 Apache Iceberg 테이블로 저장하는 관리형 서비스다. 고객 IAM 역할은 그 버킷을 직접 읽을 수 없다.
- **공백**: HealthLake가 직접 Iceberg 접근용으로 발급하는 임시 Lake Formation 자격증명을 Unity Catalog는 요청할 수 없어, 외부 접근에는 과거 내보내기 파이프라인이 필요했다.
- **해법**: 커스텀 OpenSharing 서버가 Databricks App(관리형 서버리스)으로 실행된다. 각 테이블 요청마다 Lake Formation 자격증명을 쓰고, 테이블의 현재 Iceberg 스냅샷을 확인하고, 데이터 파일을 사전 서명(pre-sign)해 표준 OpenSharing 응답으로 반환한다 — Databricks 컴퓨트가 S3에서 파일을 직접 읽으므로 데이터는 서버를 거치지 않는다.
- **저장되는 자격증명 없음**: AWS 계정의 IAM 역할이 OIDC 페더레이션으로 앱의 Databricks 아이덴티티를 신뢰한다; Databricks에는 AWS 자격증명이 저장되지 않는다.
- **Unity Catalog 마운트**: Databricks는 이 공유를 다른 공유처럼 마운트한다 — 거버넌스된 분석, 노트북, 대시보드, AI, 그리고 Genie One 탐색.
- **공유된 거버넌스 책임**: HealthLake 데이터를 Databricks로 읽어온 후에는 PHI를 포함해 Databricks 안에서의 거버넌스는 사용자의 책임이다. 실제 환자 데이터를 쓰기 전에 AWS와 Databricks의 공동 책임 모델과 컴플라이언스 요구사항을 검토해야 한다.
- **거버넌스 기능**: 공유 카탈로그에 대한 권한 부여, 세분화 접근 제어(FGAC), 속성 기반(ABAC)·역할 기반(RBAC) 제어, 감사 가능한 접근·사용 이력.
- **Genie One**: 공유 카탈로그 위의 큐레이션된 Genie Agent — 임상 팀이 핵심 테이블, 평이한 설명, A1C 같은 개념을 정의하면 사용자는 "평균 A1C는 월별로 어떻게 추세가 바뀌나?" 같은 질문을 하고 테이블·차트가 포함된 SQL 기반 요약 답변을 Unity Catalog 권한이 적용된 상태로 받는다.

## 세부 내용

HealthLake는 분석 테이블을 HealthLake 서비스 소유 S3 버킷의 Apache Iceberg 테이블로 저장하며, 고객 IAM 역할은 직접 읽을 수 없다 — 직접 접근의 유일한 경로는 Lake Formation이 생성하는 임시 자격증명인데, Unity Catalog는 이를 스스로 요청할 수 없다. 이 통합은 정확히 그 공백을 메운다.

**아키텍처**: OpenSharing 서버(Databricks App)가 테이블 요청을 받아 Lake Formation 자격증명을 얻고, 현재 Iceberg 스냅샷을 확인하고, 데이터 파일을 사전 서명해 표준 OpenSharing 응답으로 반환한다. 이후 Databricks 컴퓨트가 S3에서 파일을 직접 읽는다 — 데이터는 서버를 통과하지 않는다. 아이덴티티는 OIDC 페더레이션으로 흐른다: 고객 AWS 계정의 IAM 역할이 앱의 Databricks 아이덴티티를 신뢰하므로 Databricks에 AWS 자격증명이 저장되지 않는다. 결과물은 Unity Catalog에 일반 공유처럼 마운트되어 grants, FGAC/ABAC/RBAC, 리니지, 감사 등 전체 거버넌스 표면이 적용된다.

**그 위의 자연어**: 공유 카탈로그가 마운트되면 조직은 임상 도메인에 범위가 지정된 Genie Agent를 만들 수 있다 — 핵심 임상 테이블을 정의하고, 평이한 설명을 추가하고, A1C 같은 임상 개념의 해석을 가르친다. 임상의나 운영자는 평이한 언어로 추세 질문을 던질 수 있고, Genie One이 큐레이션된 에이전트를 찾아 SQL을 생성해 테이블과 차트가 포함된 요약 답변을 Unity Catalog 권한에 따라 돌려준다. 과거 SQL 기술이나 대시보드 요청이 필요했던 질문이 몇 초 만에 해결된다.

이 글은 공동 책임 경계를 명확히 한다: 데이터가 읽혀온 이후의 거버넌스(PHI 포함)는 Databricks 안에서 사용자의 책임이며, 실제 환자 데이터 사용 전 컴플라이언스 검토가 필요하다.

## 참고 자료

- 원문: [Talk to your clinical data: unlocking AWS HealthLake with OpenSharing and Genie One](https://www.databricks.com/blog/talk-your-clinical-data-unlocking-aws-healthlake-opensharing-and-genie-one)
