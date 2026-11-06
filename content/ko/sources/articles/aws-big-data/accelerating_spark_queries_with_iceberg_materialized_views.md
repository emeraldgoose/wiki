---
title: "Iceberg 머티리얼라이즈드 뷰로 Spark 쿼리 가속"
description: "Iceberg 머티리얼라이즈드 뷰와 자동 쿼리 재작성으로 기존 SQL을 바꾸지 않고 Spark 쿼리를 가속하는 방법을 설명한다."
tags: [source, article, aws-big-data, spark, iceberg, materialized-views, query-optimization, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/"
blog: "AWS Big Data"
published: "2026-09-10"
---

# Iceberg 머티리얼라이즈드 뷰로 Spark 쿼리 가속

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/) · **게시일**: 2026-09-10

## 개요

Apache Spark 기반 분석 작업에서는 다중 조인, 대규모 집계, 윈도우 함수 때문에 쿼리 실행 시간이 늘어나지만, 원본 SQL을 수정할 수 없는 경우가 많다. 대시보드, 패키지형 애플리케이션, 레거시 보고서가 그 사례다. AWS는 Amazon EMR 7.12.0 이상과 AWS Glue 5.1 이상에서 Apache Iceberg 머티리얼라이즈드 뷰를 사용해 기존 SQL을 그대로 유지하면서 쿼리를 가속하는 기능을 제공한다. 핵심은 머티리얼라이즈드 뷰가 미리 계산 결과를 저장하고, 자동 쿼리 재작성이 들어오는 쿼리 계획을 이 뷰의 메타데이터와 비교해 필요한 부분을 뷰 읽기로 대체하는 것이다.

자동 재작성은 구조적 매칭과 정확 매칭 두 전략을 사용한다. 구조적 매칭은 단일 SELECT-FROM-WHERE-GROUP-BY 형태의 머티리얼라이즈드 뷰를 대상으로 집계 수준 조정과 조건 추출을 수행하고, 정확 매칭은 윈도우 함수나 외부 조인이 포함된 뷰를 정규화된 형태로 비교한다. 뷰가 stale인 경우 재작성자는 이를 건너뛰어 오래된 결과가 반환되지 않게 하며, 조건에 맞는 뷰가 없으면 원본 쿼리가 그대로 실행되어 정확성이 유지된다. 또한 전체 쿼리를 모두 커버하지 않아도 머티리얼라이즈드 뷰가 쿼리 계획의 일부만 가속하고 나머지는 원래 계획으로 유지될 수 있다.

## 핵심 내용

- 기존 SQL 수정 없이 Iceberg 머티리얼라이즈드 뷰로 Spark 쿼리 실행 시간을 줄일 수 있다.
- 데이터 소스는 Iceberg 또는 Parquet 형식이어야 하며 AWS Glue Data Catalog에 등록되어 있어야 한다.
- `spark.sql.optimizer.answerQueriesWithMVs.enabled=true` 설정으로 자동 재작성을 활성화한다.
- 자동 새로고침은 일정에 따라 MV를 갱신하고, 스냅샷 ID와 Parquet 파일 ETag를 검사해 변경 시만 새로고침한다.
- Structural rewrite는 집계, 조인, 필터 중심 계획을 가속하고 exact-match rewrite는 보다 복잡한 패턴을 가속한다.
- 뷰가 오래되면 stale로 판단해 건너뛰며 원본 쿼리가 실행된다.
- MV 설계에 따라 가속 범위, 스토리지 비용, 여러 쿼리에서의 재사용성 사이의 절충이 필요하다.

## 상세

스토리지와 갱신 방식에서 다른 접근법과 차이가 명확하다. 일반 뷰는 매번 재실행하고, 사용자 ETL 파이프라인이나 수동 재작성은 절차와 새로고침을 직접 관리해야 한다. 머티리얼라이즈드 뷰와 자동 재작성은 AWS Glue Data Catalog에 의해 자동으로 새로고침되므로 쿼리 변경이 필요 없는 경우가 있다. 세 가지 MV 설계는 한 쿼리를 점진적으로 더 큰 부분까지 커버하여 단일 테이블 사전 집계와 완전한 쿼리 뷰의 속도, 스토리지, 재사용성 균형을 비교하게 한다. 계산 결과는 일반 S3 버킷 또는 S3 Tables에 Apache Iceberg 테이블로 저장되고 Athena, EMR, AWS Glue, Redshift, 외부 Iceberg 엔진에서 읽을 수 있다.

## 참고

- Source: [Accelerating Spark queries with Iceberg materialized views](https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/)