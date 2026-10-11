---
title: "Amazon Athena로 데이터 레이크 전반의 dbt 실행을 표준화한 Moeve 사례"
description: "Athena, Step Functions, Fargate 기반의 중앙집중식 서버리스 dbt 런처로 신규 프로젝트 온보딩을 수일에서 15분으로 단축한 사례."
published: "2026-09-22"
source_url: "https://aws.amazon.com/blogs/big-data/how-moeve-standardized-dbt-runs-across-data-lakes-with-amazon-athena"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, athena, dbt, ko]
---

# Amazon Athena로 데이터 레이크 전반의 dbt 실행을 표준화한 Moeve 사례

## 개요

Moeve의 분석 팀들은 각자 다른 방식으로 dbt를 실행하고 있었다. 실행 로직이 프로젝트별 파이프라인에 박혀 있었고, 팀마다 컴퓨팅 엔진이 달랐으며, 비용 가시성도 없었다. 회사는 Amazon Athena 기반의 중앙집중식 서버리스 dbt 런처를 구축해 모든 프로젝트에 동일한 실행 계약을 적용했다. DynamoDB에서 파라미터를 읽어 실행하고, 완료 이벤트를 EventBridge로 발행하는 구조다. 신규 dbt 프로젝트 온보딩은 수일에서 약 15분으로 줄었다.

## Athena를 기본 엔진으로 선택한 이유

워크로드가 지속형이 아니라 간헐적 버스트형이라는 점이 결정적이었다. 각 dbt 프로젝트는 스케줄이나 데이터 도착 시 몇 분간 실행되고 멈추므로, 서버리스 과금과 잘 맞는다. 클러스터 운영이 필요 없고, 데이터를 소유한 계정에서 컴퓨팅이 실행되니 계정별 비용 귀속도 자연스럽다. dbt Athena 어댑터의 성숙도와 Iceberg 기반의 멱등 증분 병합 지원도 선택을 뒷받침했다.

비용 최적화의 핵심은 데이터 기반 병합 조건이다. 고정된 기간 필터 대신 유입 데이터셋의 파티션 값에서 타깃 필터를 도출해, 병합이 영향받는 파티션만 스캔하도록 했다. 소스 입력 역시 명시적 범위나 기본 윈도우로 제한한다.

## 중앙집중식 런처 아키텍처

Step Functions 상태 머신이 실행 요청을 받아 DynamoDB에서 프로젝트 파라미터(환경, IAM 역할, 엔진, 타임아웃, 재시도, 기본 처리 윈도우)를 읽고, 공용 dbt 이미지로 일회성 Fargate 컨테이너를 띄운다. 컨테이너는 대상 데이터 레이크 계정의 역할을 수임하므로 컴퓨팅은 데이터 곁에 머문다. 모델 단위 결과와 데이터 품질 테스트 결과는 Elementary 패키지로 기록되고, 구조화된 완료 이벤트가 중앙 EventBridge 버스로 발행된다.

파라미터를 파이프라인 코드가 아닌 DynamoDB에 둔 것은 의도적 설계다. 배포 없이 타임아웃과 재시도를 바꿀 수 있고, 신규 프로젝트 등록은 모델 병합과 설정 한 건으로 끝난다. DuckDB 기반 로컬 CI 검증으로 2분 안에 피드백을 받으며, 최종 검증은 대상 계정의 Athena에서 이뤄진다.

## 이벤트 기반 오케스트레이션 분리

런처는 다음에 무엇을 실행할지 결정하지 않는다. 하위 소비자들이 완료 이벤트를 구독하며, Moeve의 오케스트레이션 계층은 데이터셋 의존성을 그래프로 모델링해 입력이 준비된 프로젝트를 시작한다. 실행 계층과 오케스트레이션 계층은 독립적으로 진화했고, 오케스트레이션 재구축 때도 런처는 손대지 않았다. 표준화 덕분에 Step Functions 상태, Fargate 로그, dbt/Elementary 결과, 버스 이벤트라는 관측 체계도 공짜로 얻었다.

## 참고 자료

- [원문: How Moeve standardized dbt runs across data lakes with Amazon Athena](https://aws.amazon.com/blogs/big-data/how-moeve-standardized-dbt-runs-across-data-lakes-with-amazon-athena)
- [Top 10 performance tuning tips for Amazon Athena](https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/)
