---
title: SageMaker에서 Iceberg 구체화 뷰로 메달리온 아키텍처 구축하기
description: Bronze→Silver→Gold 메달리온 파이프라인을 3개 구체화 뷰 SQL로 선언 — DAG·CDC 없이 증분 리프레시와 중첩 뷰로 구현.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, medallion, materialized-views, sagemaker, s3-tables, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/building-medallion-architecture-with-iceberg-materialized-views-in-amazon-sagemaker/"
blog: aws
---

# SageMaker에서 Iceberg 구체화 뷰로 메달리온 아키텍처 구축하기

**발행**: 2026-09-02 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/building-medallion-architecture-with-iceberg-materialized-views-in-amazon-sagemaker/)

## 문제

전통적 메달리온(Bronze→Silver→Gold) 파이프라인은 사실상 세 개의 시스템이다: 계층별 ETL 잡, 이를 순서대로 실행하는 오케스트레이터(Airflow·Step Functions), 신규 행만 처리하기 위한 직접 작성 CDC(워터마크·스냅샷 비교·체인지 스트림). 각자 작성·테스트·배포·유지보수해야 하고, 하나가 깨지면 전체가 멈춘다.

## 선언적 대안

SageMaker의 Iceberg 구체화 뷰는 변환+오케스트레이션+증분 처리를 **계층당 하나의 SQL 정의**로 압축한다. 각 계층의 내용을 선언(`CREATE MATERIALIZED VIEW ... SCHEDULE REFRESH EVERY 1 DAY AS SELECT ...`)하면 관리형 Spark(AWS Glue)가 리프레시를 실행하고, Iceberg의 행 수준 변경 추적(position/equality delete)이 변경 행만 처리한다. 글의 전체 파이프라인은 SQL 3문장, 구축 2분 이내. 지원 엔진: Athena Spark, Glue 5.1+, EMR 7.12+.

## 동작 방식

- **Bronze**(`trips_bronze`, S3 Tables): 라이드셰어링 원시 트립을 그대로 적재(INSERT/append) — 감사·리플레이용 원본 보존.
- **Silver**(`mv_trips_silver`): null 필터링, 문자열→타임스탬프 캐스팅, 파생 컬럼(`revenue_per_mile`, `rating_category`). 정의만 있고 데이터는 리프레시 시점에 흐름.
- **Gold**(Silver 위 중첩 MV): `mv_city_daily_metrics`(도시×일자별 트립·드라이버·매출·팁), `mv_vehicle_performance`(차종×도시별), 일간 스케줄. Gold는 Silver로부터 증분 읽기.
- **전파 데모**: Bronze에 INSERT → Silver `REFRESH`(신규 3건만 처리) → Gold 리프레시(연쇄·증분). MERGE 기반 UPDATE도 동일하게 전파.
- **스토리지·저작**: S3 Tables + Glue Data Catalog, SageMaker Unified Studio 노트북(Athena/Glue Spark 런타임)에서 작성, Data Agent로 자연어→SQL 생성 가능.

## 한계 (원문 명시)

1. 최소 스케줄 단위 **1시간** — 그 이하 신선도 불가.
2. **연쇄 리프레시 자동 아님** — Silver 리프레시가 Gold를 깨우지 않음. 순차 호출 또는 별도 스케줄 필요.
3. **삭제는 `REFRESH ... FULL`** — 증분 리프레시는 삽입·수정만 감지, 행 삭제는 감지 못함.
4. SQL 부분집합만 지원(일부 윈도우 함수·UDF·복잡 표현식 불가).
5. 뷰 정의에 영향 주는 소스 스키마 변경 시 드롭 후 재생성.
6. **AWS 전용 확장** — 오픈소스 Iceberg 표준 아님, AWS 외부로 이식 불가.

## 요금

예약 자동 리프레시는 관리형 Spark 기준 약 $0.44/DPU-시간(초 단위, 최소 1분). 수동 리프레시는 호출 서비스(Athena/EMR/Glue) 요금. MV 데이터는 S3 Tables/S3 표준 스토리지 요금. 튜토리얼 300건 실행 비용은 0.5 DPU-시간 미만(약 $0.22).

## 세미나 시사점

- 핵심 전환은 **명령형 파이프라인에서 선언적 데이터로**: SQL만 유지하고 스케줄링·CDC·증분 연산은 플랫폼에 위임.
- 정직한 경계(시간 단위 하한, 수동 연쇄, 삭제 시 FULL, AWS 전용)가 이 패턴의 적용 범위(큐레이션 배치 마트)와 비적용 범위(1시간 이내 SLA·이식 가능한 오픈소스 스택)를 정확히 규정.

## 관련 개념

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/ai-engineering/feature-store.md`
