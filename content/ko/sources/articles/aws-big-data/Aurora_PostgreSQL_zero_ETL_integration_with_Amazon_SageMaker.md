---
title: "Amazon SageMaker와 Aurora PostgreSQL 제로 ETL 통합"
description: "Aurora PostgreSQL 데이터를 커스텀 ETL 없이 Iceberg 테이블로 SageMaker AI에 수 초 내 복제합니다." (한국어 번역)
tags: [source, aws-big-data, aurora, zero-etl, sagemaker, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/aurora-postgresql-zero-etl-integration-with-amazon-sagemaker"
blog: aws-big-data
published_date: 2026-09-29
---

# Amazon SageMaker와 Aurora PostgreSQL 제로 ETL 통합

## 개요

Aurora PostgreSQL과 SageMaker의 제로 ETL 통합으로 운영 데이터를 커스텀 파이프라인 없이 수 초 내 분석에 활용할 수 있습니다. 변경분이 Glue 관리 카탈로그에 Apache Iceberg 테이블로 자동 복제되어, Athena·Redshift·Spark·BI·ML 도구가 SageMaker AI에서 다른 레이크하우스 데이터와 함께 조회합니다. 파이프라인 지연·운영 부담·데이터 사일로가 사라집니다.

## 동작 방식

핵심은 변경 데이터 캡처(CDC)입니다. Aurora의 향상된 논리 복제가 WAL에서 모든 삽입·수정·삭제를 스트리밍하고 DDL 전파까지 자동 처리합니다. 흐름은 다음과 같습니다: 애플리케이션이 Aurora에 기록 → 제로 ETL이 변경 캡처 → Glue 관리 카탈로그에 수 초 내 복제 → Athena·Redshift로 조회하고 SageMaker AI에서 Iceberg 테이블로 직접 모델 학습. Glue Data Catalog와 Lake Formation 거버넌스 위에 열린 표준으로 구축되어, 데이터 한 벌로 SQL·Spark·BI·AI/ML을 모두 수용합니다.

## 통합 설정

- **소스 DB:** 논리·향상 논리 복제를 켠 클러스터 파라미터 그룹을 만들고 지원되는 Aurora PostgreSQL 버전의 클러스터에 적용한 뒤 재부팅합니다.
- **대상 카탈로그:** Redshift 관리 스토리지 기반 Glue 관리 카탈로그를 만들고, Glue·Redshift가 맡을 수 있는 IAM 역할을 만들며, Lake Formation 데이터레이크 관리자와 Redshift 서비스 연결 역할의 읽기 권한을 구성한 뒤, 카탈로그를 통합 대상으로 등록하고 소스 클러스터 ARN에서의 인바운드 통합을 허용하는 리소스 정책을 추가합니다.
- **시드와 생성:** 기준 데이터를 먼저 적재(히스토리 기반)한 뒤 데이터 필터와 함께 `create-integration`을 호출합니다. 상태가 `creating`에서 `active`로 바뀌면 `describe-integrations`로 모니터링합니다.
- **검증:** Lake Formation 테이블 권한을 부여하고 Redshift Data API로 조회합니다. 새 행을 삽입 후 재조회하면 수 초 내 실시간 복제가 확인됩니다.

## 정리와 다음 단계

통합을 먼저 삭제하면 복제가 멈추고(기존 데이터는 양쪽에 유지), 이어서 Glue 카탈로그, 실습용 Aurora 클러스터·파라미터 그룹을 삭제합니다. 지원 데이터 타입·스키마 변경 처리·필터링 제한을 숙지해야 합니다. RDS for MySQL·DynamoDB 등 지원 소스를 늘려 중앙 집중식 실시간 플랫폼으로 확장하고, Redshift ML·대규모 SQL 분석·연합 쿼리와 결합하는 것이 자연스러운 다음 단계입니다.

## References

- 원문: [Aurora PostgreSQL zero-ETL integration with Amazon SageMaker](https://aws.amazon.com/blogs/big-data/aurora-postgresql-zero-etl-integration-with-amazon-sagemaker)
