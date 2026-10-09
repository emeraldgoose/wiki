---
title: "Data Modeling for Analytics"
description: "스타 및 눈꽃 스키마, 정규화와 비정규화, 천천히 변하는 치수, analytical data modeling patterns"
tags: [concept, data-engineering, data-modeling, analytics]
locale: ko
published: 2026-09-07
---

# Data Modeling for Analytics (분석을 위한 데이터 모델링)

## 정의
분석 워크로드에 최적화된 데이터 모델을 설계하는 과정입니다. OLTP 워크로드와는 다른 요구사항(조회 성능, 집계 효율성)을 반영한 스키마 설계가 핵심입니다.

## 왜 중요한가
- **조회 성능**: 적절한 스키마 선택으로 쿼리 속도 2~10배 개선
- **유지보수**: schema 변화에 유연하게 대처 가능한 모델
- **비용 최적화**: 불필요한 데이터 저장 최소화

## 스타 스키마 (Star Schema)
- **센터 테이블(Fact)**: 거래, 이벤트, 로그 등 중심 사실 테이블
- **주변 차원 테이블(Dimension)**: 날짜, 고객, 제품, 위치 등
- **장점**: 간단한 조인 구조, 직관적인 쿼리 작성
- **단점**: 데이터 중복, 차원 테이블 증가는 관리의 증가

## 눈꽃 스키마 (Snowflake Schema)
- 차원 테이블이 정규화되어 계층 구조를 이룸
- **장점**: 저장 공간 절감 (일반적으로 20~30% 절감)
- **단점**: 복잡한 조인, 쿼리 성능 약간 저하

## 정규화 vs 비정규화
| 구분 | 정규화 (3NF) | 비정규화 (스타/눈꽃) |
|---|---|---|
| 저장 공간 | 효율적 | 중복으로 증가 |
| 조회 성능 | 복잡한 조인 필요 | 직접적 접근 가능 |
| 유지보수 | 스키마 변화에 강함 | 변경 시 여러 테이블 업데이트 필요 |
| 적합한 워크로드 | OLTP | OLAP/분석 |

## 천천히 변하는 치수 (Slowly Changing Dimensions, SCD)
- **SCD Type 1**: 덮어쓰기 (예: 고객 주소 변경, 이전 정보 소실)
- **SCD Type 2**: 이력 유지 (예: 주소변경 record 신규 행 추가, effective_date 관리)
- **SCD Type 3**: 부분 이력 (예: 현재 주소 열 추가, 이전 값 보관)
- **활용**: 고객 주소 이력, 직원 부서 변경 이력

## 참조
- "The Data Warehouse Toolkit" — Ralph Kimball
- dbt Labs documentation: models 구조 및 best practices
- "Data Model Resource Library" — 다양한 패턴 모음
