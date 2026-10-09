---
title: "United Airlines가 Databricks 관리 데이터를 조회하기 위해 Redshift와 Glue Data Catalog 연합을 사용하는 방법"
description: "Databricks Unity Catalog에서 Glue 연합 카탈로그와 Lake Formation을 거쳐 Redshift Serverless로 이어지는 United Airlines 연합 체인: 리소스 링크 패턴과 측정된 비용 효과."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/how-united-airlines-uses-amazon-redshift-and-aws-glue-data-catalog-federation-to-query-databricks-managed-data/"
blog: "AWS Big Data"
locale: "ko"
tags: [aws, redshift, glue, lake-formation, databricks, unity-catalog, iceberg, federation, ko]
---

# United Airlines가 Databricks 관리 데이터를 조회하기 위해 Redshift와 Glue Data Catalog 연합을 사용하는 방법

[English version](../../../../en/sources/articles/aws/How_United_Airlines_Uses_Amazon_Redshift_and_Glue_Data_Catalog_Federation.md)

**저자**: Vaibhav Agrawal (AWS), Ankit Aggarwal와 Raja Kalluri (United Airlines) · **발행**: 2026-09-15 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-united-airlines-uses-amazon-redshift-and-aws-glue-data-catalog-federation-to-query-databricks-managed-data/)

## 문제

United Airlines는 S3 위 메달리온 (bronze→silver→gold) 아키텍처로 페타바이트를 큐레이션하며, 사용자 인터랙션 gold 레이어만 해도 수십 테라바이트의 near-실시간 스트림 데이터다. 테이블은 Databricks Unity Catalog에 카탈로그되어 있어 ~100명의 분석가가 일하는 Amazon Redshift Serverless에서는 보이지 않는다. 연합 없이는 Redshift Managed Storage로 데이터를 복제하고 동기화 파이프라인을 돌리는 수밖에 없었다 — 비싸고 드리프트에 취약하다.

## 해법 개요

Glue Data Catalog 연합이 메타데이터 계층에서 플랫폼을 잇는 4계층 체인:

1. **Unity Catalog**가 Iceberg REST API로 테이블 노출 (Delta 테이블은 Iceberg 호환용 UniForm 사용).
2. **Glue 연합 카탈로그** (`databricks-federated-catalog`)가 Unity Catalog에 연결 — 데이터 이동 없이 AWS에서 메타데이터 가시화.
3. **리소스 링크 데이터베이스** (기본 Glue 카탈로그의 `databricks_federated_db_link`)가 연합 데이터베이스를 가리킴 — Redshift가 `CREATE EXTERNAL SCHEMA`를 기본 카탈로그 대상으로만 해석하므로 필수.
4. **Redshift Serverless 외부 스키마**가 리소스 링크 참조. 쿼리 시 Redshift가 링크를 타고, Glue Federation이 Unity REST API를 호출하고, Lake Formation이 범위가 한정된 S3 자격 증명을 발급하고, Redshift가 S3의 Iceberg 파일을 직접 읽는다.

6단계 쿼리 흐름: 분석가 SQL → 외부 스키마 해석 → 연합 카탈로그 REST 호출 → 네임스페이스 IAM 역할의 `lakeformation:GetDataAccess` 호출 → 정책 평가·자격 증명 발급 → 직접 S3 읽기. Graviton 기반 Serverless 엔진 (연계 글 기준 레이크 쿼리 최대 2배 빠름)은 바로 이 Iceberg-직접 패턴용이다. 롤아웃은 단계적: 30개 테이블 프로덕션, 70개 전개 중, 수백 개 계획.

## 구현

**사전 요구사항**: Unity Catalog + 카탈로그/스키마/테이블이 있는 Databricks 워크스페이스 (UniForm on), Glue/Lake Formation/Redshift Serverless/IAM 권한이 있는 AWS 계정, 프로비저닝된 Serverless 워크그룹+네임스페이스, Lake Formation 관리자, AWS CLI. 1단계 (Unity 측 설정)는 연합으로 Unity Catalog 접근하는 companion 글을 따른다.

1. **Lake Formation**: 데이터 레이크 관리자 추가, `databricks-federated-catalog` 등록 확인.
2. **리소스 링크** (핵심 — 복사가 아닌 포인터):
   ```bash
   aws glue create-database --database-input '{"Name": "databricks_federated_db_link", "TargetDatabase": {"CatalogId": "<account-id>:databricks-federated-catalog", "DatabaseName": "databricks_federated_db"}}'
   ```
3. **네임스페이스 IAM 역할**: Glue 메타데이터 읽기 (`GetDatabase(s)`, `GetTable(s)`, `GetPartitions`, `GetCatalog(s)`) + `lakeformation:GetDataAccess` 연결. 프로덕션에서는 `Resource`를 좁힌다. Namespace → Security and encryption → Manage IAM roles에서 연결.
4. **Lake Formation 승인** (Grant-on-Target 패턴): 네임스페이스 역할에 리소스 링크 데이터베이스 `DESCRIBE` + 연합 카탈로그의 *대상* 테이블에 `SELECT, DESCRIBE` (링크에만 SELECT를 주는 것이 흔한 실패 원인).
5. **외부 스키마** (슈퍼유저로 접속, 예: Query Editor v2):
   ```sql
   CREATE EXTERNAL SCHEMA databricks_schema FROM DATA CATALOG
   DATABASE 'databricks_federated_db_link' IAM_ROLE '<arn>' REGION '<region>';
   ```
   관례: 연합 스키마는 `{domain}_iceberg` 명명, 분석가 뷰는 `WITH NO SCHEMA BINDING`으로 매 실행 신선한 스키마 해석.
6. **검증**: `SELECT * FROM SVV_EXTERNAL_TABLES WHERE schemaname='databricks_schema';` 후 `SELECT * FROM databricks_schema.<table> LIMIT 10;`. SAML 사용자는 IdP JDBC 플러그인으로 `ssl=true` 연결.

## 결과와 비즈니스 임팩트

| 영역 | 이전 | 이후 | 임팩트 |
|---|---|---|---|
| 데이터 접근 | Delta와 Redshift 사일로 | 실시간 연합 접근 | 신규 파이프라인 없이 ~100명 분석가 차단 해제 |
| DR | 3시간마다 Redshift 스냅샷 (RPO 3시간+) | S3 리전 간 복제, near-연속 RPO. DR 워크그룹도 동일 S3 데이터에 연합 | 복원력 향상, 스냅샷/복사 비용 감소 |
| 아키텍처 | 이중 처리 + 수동 카탈로그 동기화, 드리프트 취약 | 처리는 Databricks로 통합, Redshift는 쿼리 엔진 | 단일 진실 원천, 동기화 파이프라인 제로 |
| 인프라 비용 | 전용 Redshift ETL 클러스터 + RMS + 스냅샷 | 쿼리 엔진으로서의 Redshift만 | 중복 ETL 비용 약 $30K/월 제거 |

보안: 양쪽에 매핑된 Azure AD 그룹 기반 통합 ID (Redshift SAML + Unity 스키마), Lake Formation 세밀 제어, 최소 권한 네임스페이스 역할, 쿼리당 단기 발급 자격 증명, 전 구간 TLS. 요구사항: Delta 테이블 UniForm on, 연합 성능은 쓰기 시점 레이아웃을 그대로 반영하므로 잘 파티셔닝되고 주기적으로 컴팩션된 소스 필요.

## 세미나 시사점

- 리소스 링크 간접 참조가 핵심 트릭이다: Redshift는 기본 카탈로그만 볼 수 있으므로 링크가 연합 카탈로그로 가는 주소 지정 경로다.
- Grant-on-Target (연합 테이블 SELECT, 링크 DESCRIBE)이 외워둘 권한 형태다.
- 연합은 Redshift Serverless를 개방형 스토리지 위의 상태 없는 쿼리 엔진으로 재정의한다 — $30K/월 수치는 그 재정의 거부의 비용이다.

## 관련 개념

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/delta-lake.md`, `concepts/data-engineering/trino.md`

## 참고 자료

- [카탈로그 연합으로 Databricks Unity Catalog 데이터 접근하기](https://aws.amazon.com/blogs/big-data/access-databricks-unity-catalog-data-using-catalog-federation-in-the-aws-glue-data-catalog/)
- [Redshift 위 Apache Iceberg로 데이터 레이크 쿼리 2배 빠르게](https://aws.amazon.com/blogs/big-data/achieve-2x-faster-data-lake-query-performance-with-apache-iceberg-on-amazon-redshift/)
- [카탈로그 연합 서비스 제한](https://docs.aws.amazon.com/lake-formation/latest/dg/catalog-federation.html#catalog-federation-limitations)
