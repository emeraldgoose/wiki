---
title: "한 번 구체화하고 어디서든 조회하기: Amazon Redshift의 Iceberg 구체화 뷰"
description: "Redshift에서 구체화 뷰 결과를 개방형 Iceberg 테이블로 저장해 한 번만 계산하고 Athena, Spark, SageMaker에서 읽는 기능과 증분 새로고침 소개." (한국어 번역)
published: "2026-10-05"
source_url: "https://aws.amazon.com/blogs/big-data/materialize-once-query-anywhere-introducing-iceberg-materialized-views-in-amazon-redshift"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, redshift, iceberg, ko, ko]
---

# 한 번 구체화하고 어디서든 조회하기: Amazon Redshift의 Iceberg 구체화 뷰

## 개요

Amazon Redshift에서 구체화 뷰 결과를 S3의 표준 Apache Iceberg 테이블로 저장할 수 있게 됐다(`CREATE MATERIALIZED VIEW ... USING ICEBERG`). 무거운 조인·집계는 Redshift(Serverless 또는 RG 인스턴스)에서 한 번만 계산하고, 결과는 Glue Data Catalog의 일반 Iceberg 테이블이 되어 Athena, EMR의 Spark, SageMaker, Glue가 복사 없이 직접 읽는다. 증분 새로고침으로 변경된 파티션만 다시 계산하고, Lake Formation으로 공유를 거버넌스할 수 있다.

## 언제 Iceberg 구체화 뷰를 쓸까

기존 RMS 구체화 뷰를 대체하는 것이 아니라 보완하는 용도다. Redshift에서만 읽고 대화형 대시보드에 최저 지연이 필요하면 RMS 뷰를 쓴다. 여러 엔진에서 미리 계산된 결과를 공유하거나, Iceberg를 상호운용성 표준으로 삼거나, 단일 엔진 파이프라인의 개방형 출력이 필요하면 Iceberg 구체화 뷰를 쓴다. 보통은 Iceberg 뷰로 개방형 공유를 기본값으로 두고, 가장 뜨거운 대시보드 위에 RMS 뷰를 올리는 조합이 쓰인다.

## 동작 방식

Redshift는 새로고침 간 Iceberg 스냅샷 ID를 추적해 적격 패턴(GROUP BY 포함 SUM/COUNT, 행 단위 델타, Iceberg 간 내부 조인)은 델타만 다시 계산한다. DISTINCT, 외부 조인, 윈도우 함수, 집합 연산, MIN/MAX/AVG 등은 전체 새로고침으로 처리된다. 뷰는 생성한 클러스터에 묶이지 않아 권한 있는 클러스터·워크그룹이 새로고침할 수 있고, 동시 새로고침은 Glue 카탈로그를 통해 조정된다. Serverless와 RG(Graviton) 인스턴스에서 지원되며 RA3·DC2는 제외된다.

## 설정 개요

IAM 정의자 역할(`redshift.amazonaws.com`과 `glue.amazonaws.com` 모두 신뢰), 범위를 좁힌 S3·Glue 인라인 정책과 PassRole, S3 버킷, 교차 엔진 읽기용 Glue 데이터베이스, 클러스터 역할 연결이 필요하다. 이후는 일반 SQL이다. 외부 스키마, Iceberg 베이스 테이블, `CREATE MATERIALIZED VIEW ... USING ICEBERG`를 만들고 Athena와 PyIceberg·Spark 리더로 검증한다. 필요하면 Lake Formation을 올려 테이블 단위 거버넌스를 추가한다.

## 참고 자료

- [원문: Materialize once, query anywhere](https://aws.amazon.com/blogs/big-data/materialize-once-query-anywhere-introducing-iceberg-materialized-views-in-amazon-redshift)
- [Materialized views stored as Apache Iceberg tables (Redshift 문서)](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-iceberg.html)
