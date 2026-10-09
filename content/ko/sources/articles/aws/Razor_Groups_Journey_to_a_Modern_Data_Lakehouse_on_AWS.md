---
title: Razor Group의 AWS 현대 데이터 레이크하우스 여정
description: Razor Group이 상시 가동 Redshift 클러스터에서 S3 Tables 기반 개방형 Iceberg 레이크하우스로 5단계 이전 — P95 65% 단축, 인프라 비용 63% 절감.
date: 2026-08-28
tags: [aws, data-engineering, lakehouse, apache-iceberg, redshift, spark, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/razor-groups-journey-to-a-modern-data-lakehouse-on-aws/"
blog: aws
---

# Razor Group의 AWS 현대 데이터 레이크하우스 여정

**저자**: Yaswanth Kothainti 외 · **발행**: 2026-08-28 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/razor-groups-journey-to-a-modern-data-lakehouse-on-aws/)

## 배경과 문제

이커머스 애그리게이터 Razor Group의 "Razor Operating System"은 Selling Partner API, Shopify, NetSuite, Walmart, Target 등의 신호를 Lambda와 MSK로 수집해 S3·DynamoDB에 적재하고 Redshift에서 모델링했다. 급성장 과정에서 세 가지 구조적 한계가 드러났다.

- **워크로드 경합**: ETL·변환·분석용 SQL 모델 1,000개 이상이 같은 Redshift 클러스터 자원을 놓고 경쟁.
- **상시 과금**: 사용률과 무관하게 프로비저닝 클러스터가 24시간 과금.
- **단일 엔진 종속**: 무거운 ETL부터 임시 탐색, BI 대시보드까지 모든 워크로드를 하나의 엔진에 맞춰야 함.

## 해법: 개방형 레이크하우스

데이터를 S3 Tables의 Apache Iceberg 포맷으로 한 번만 저장하고, 워크로드마다 최적 엔진을 선택하는 구조로 전환했다.

- **개방형 테이블 포맷**: Iceberg의 ACID 트랜잭션, 타임 트래블, 스키마·파티션 진화. 중복 없이 모든 호환 엔진에서 접근.
- **워크로드별 탄력적 확장**: 피크 때 켜고 유휴 때 0으로 — 공유 인프라 과다 프로비저닝 불필요.
- **관리형 스토리지**: 압축·스냅샷 만료·고아 파일 정리를 S3 Tables가 자동 처리.

## 아키텍처

| 계층 | 선택 |
|---|---|
| 수집 | AWS Lambda(이벤트 기반) + Amazon MSK |
| 저장 | Bronze / Silver / Gold Iceberg 테이블 (S3 Tables) |
| 거버넌스 | Glue Data Catalog(통합 메타데이터) + Lake Formation(컬럼·로우 수준 보안) |
| 컴퓨트(ETL) | EC2 위 Spark Connect (Graviton 리더 온디맨드 + Spot 워커로 약 70% 절감), 내부 NLB 경유 |
| 컴퓨트(탐색) | Athena (서버리스 SQL) |
| 컴퓨트(BI) | Redshift Serverless (자동 확장/일시정지) |
| 오케스트레이션 | Airflow — 9,300개 이상 파이프라인, 의존성 추적·SLA 모니터링 |
| 관측성 | 워크로드별 비용 귀속, 파이프라인 상태, 데이터 품질 검사 |

참고: 설계 당시에는 Redshift가 Iceberg 쓰기를 지원하지 않아 자체 관리 Spark가 유일한 수집 경로였다. 이후 Redshift가 Iceberg UPDATE/DELETE/MERGE 및 CREATE/INSERT를 지원하면서 제약이 해소됐다.

## 5단계 점진적 마이그레이션 (빅뱅 없음)

1. **기반 구축** — S3 Tables, Glue, Lake Formation 정책, Spark Connect 클러스터 배포.
2. **Bronze 수집 이전** — Airflow가 관리하는 Lambda 함수로 원시 데이터를 Iceberg에 직접 기록. 스케줄 기반에서 이벤트 기반으로 전환해 신선도 개선.
3. **변환 파이프라인 이전** — 가장 어려웠던 단계. 40개 이상 스키마의 의존성 체인을 따라 Redshift SQL 모델 1,000개 이상을 Spark로 점진 이전.
4. **서빙 통합** — 최종 사용자는 Redshift Serverless로 Gold 테이블 조회, 탐색·ML은 Spark Connect로 동일 테이블 읽기.
5. **전환 및 검증** — 구·신 스택 병렬 운영 후 출력 비교, 이후 구 스택 폐기.

## 결과

| 지표 | 이전 | 이후 |
|---|---|---|
| P95 쿼리 시간 | 180초 | 63초 (**65% 단축**) |
| 인프라 비용 | 상시 클러스터 + 관리형 스토리지 | EC2 + Lambda + Glue + Athena + Redshift Serverless + S3 Tables (**63% 절감**) |
| 동시 처리 용량 | 클러스터 크기에 제한 | 엔진별 독립 탄력 확장 |
| 엔진 유연성 | 단일 엔진 | 하나의 개방형 복사본 위에 Spark / Athena / Redshift |

## 시사점

- **한 번 저장, 여러 컴퓨트**: 개방형 포맷이 저장과 엔진을 분리하므로 워크로드마다 가장 저렴한 엔진을 선택할 수 있다.
- **관측성에는 비용 귀속이 포함되어야 한다** — 워크로드별 비용 가시성 없이는 최적화가 추측에 그친다. Razor Group은 Iceberg 스냅샷 유지보수가 주당 35시간 이상의 컴퓨트를 소모한다는 사실을 관측성으로 발견하고 자동화로 해결했다.
- **점진 이전이 빅뱅보다 낫다**: 각 단계가 독립적 가치(신선도→모델→서빙)를 제공하면서 전환 리스크를 낮췄다.

## 관련 개념

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/lakehouse.md`, `concepts/data-engineering/stream-processing.md`
