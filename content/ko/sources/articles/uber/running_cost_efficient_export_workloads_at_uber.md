---
title: Uber에서 비용 효율적인 익스포트 워크로드 운영하기
description: Apache Hudi 컬럼 통계와 테이블 정렬로 풀테이블 익스포트 스캔을 선택적 저접촉 조회로 전환한 Uber GCS 레이크하우스 사례
tags: [source, uber, data-engineering, hudi, lakehouse, gcs, cost-optimization, ko]
locale: ko
source_url: "https://www.uber.com/us/en/blog/running-cost-efficient-export/"
blog: uber
published_date: 2026-08-12
---

# Uber에서 비용 효율적인 익스포트 워크로드 운영하기

**저자**: Pankaj Mohapatra, Arun Mahadeva Iyer, Balajee Nagasubramaniam
**출처**: [Uber Blog](https://www.uber.com/us/en/blog/running-cost-efficient-export/)
**날짜**: 2026-08-12

## 문제

익스포트 워크로드(DSAR, 컴플라이언스, 프라이버시)는 방대한 히스토리 데이터에서 소량 결과만 조회한다. 날짜 파티션된 Hudi 테이블에 대한 포인트/좁은 조건 쿼리를 주 수회 반복 실행하는데, 파라미터만 바뀌고 탐색 범위는 전체 히스토리다. GCS 기반 레이크하우스에서 반복 풀테이블 스캔은 데이터를 hot 상태로 유지해 GCS 자동 클래스 티어링을 무력화한다 (목표 ~60% Standard / 15% Nearline / 10% Coldline / 15% Archive가 100% Standard로 붕괴). 스토리지·검색·Class B 메타데이터 연산·GCS 이그레스·지연시간 비용이 모두 증가한다.

## 해결: Hudi 컬럼 통계 + 테이블 정렬

- **컬럼 통계**: Hudi 메타데이터 테이블이 파일별 컬럼 min/max/null/count를 보관. 데이터 스캔 전에 메타데이터 조회만으로 파일 프루닝 — Parquet 푸터를 열 필요가 없다 (푸터 읽기 자체가 파일을 hot으로 만든다).
- **테이블 정렬**: 조건 컬럼(예: 사용자 ID) 기준 클러스터링으로 파일별 min/max 범위를 타이트하게 만들어 프루닝 선택도를 높인다. 컬럼 통계가 메커니즘이고, 정렬이 효과를 증폭시킨다.

## 결과

실제 파티션 벤치마크:

- 디스크 사용량 24.8% 감소 (정렬로 동일 값 클러스터링 → 압축 효율 향상)
- 조건 개수(소/중/다) 전반에서 효과적 파일 프루닝
- GCS 이그레스, Class B 연산, 쿼리 지연시간 감소
- 오래된 데이터가 cold 유지 → 자동 티어링 정상 동작

## 정렬 + 보조 인덱스가 아닌 이유

컬럼 통계는 파일 수 × 추적 컬럼에 비례해 확장되지만, 보조 인덱스는 값별 매핑을 유지해야 해 메타데이터·연산 부담이 크다. 미정렬 테이블에서는 보조 인덱스만으로 스캔 비용이 유의미하게 줄지 않고, 정렬된 테이블에서는 컬럼 통계가 더 단순하고 저장 효율적이다.

## Uber 너머의 적용

방대한 히스토리에서 소량을 선택 조회하는 패턴은 금융(감사 추적), 의료(환자 기록 요청), 법률 디스커버리 등에서 반복된다. Hudi Table Service(백필 정렬·인덱스 구축·증분 정렬의 중앙 엔진)가 핵심 enabler다.

## 세미나 시사점

- 클라우드 스토리지 비용은 저장 바이트가 아니라 *접근 패턴 × 파일 배치*가 결정한다.
- 프루닝 메타데이터를 테이블 레벨로 옮겨 cold 파일을 건드리지 않게 하라.
- 물리적 클러스터링(정렬)은 min/max 기반 프루닝의 효과를 배가시킨다.
- 가장 가벼우면서 충분히 프루닝되는 인덱스를 선택하고, 출력 크기가 아닌 스캔 면적으로 측정하라.

## 관련 개념

- `concepts/data-engineering/apache-hudi.md`
- `concepts/data-engineering/lakehouse.md`
