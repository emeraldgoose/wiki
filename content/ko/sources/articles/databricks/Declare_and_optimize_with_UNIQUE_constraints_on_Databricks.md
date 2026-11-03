---
title: "Databricks에서 UNIQUE 제약으로 선언하고 최적화하기"
description: "Databricks UNIQUE 제약으로 여러 고유성 보장을 선언하고 최적화에 활용할 수 있다."
tags: [source, databricks, data-engineering, sql, ko]
locale: ko
source_url: "https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks"
blog: databricks
published_date: 2026-11-04
---

# Databricks에서 UNIQUE 제약으로 선언하고 최적화하기

**원문**: [databricks](https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks) · **게시일**: 2026-11-03

## 개요

데이터 팀은 파이프라인에서 고유성 보장을 자주 유지하지만, 테이블 스키마에 이를 모두 표현할 유연한 방법이 없으면 사용자와 도구가 그 보장을 발견할 수 없고 쿼리 최적화기가 이를 안전하게 활용할 수 없다. 업무 엔터티는 고유한 것으로 알려진 값이나 값 조합을 하나보다 많이 가질 수 있다. Databricks는 이미 PRIMARY KEY와 FOREIGN KEY 제약을 지원하지만, 테이블에는 하나의 기본 키만 있을 수 있고 그 컬럼은 null이 아니어야 한다. UNIQUE 제약은 여러 번 nullable하거나 복합적인 고유성 보장을 허용함으로써 이 모델을 확장한다.

팀은 기본적으로 NORELY로 이런 보장을 선언하고, 이를 검증한 뒤 RELY를 사용해 최적화기가 중복 조인과 DISTINCT 집계를 제거하도록 할 수 있다. 10TB TPC-DS 벤치마크에서 RELY를 사용한 UNIQUE는 셔플의 99.99% 이상을 제거하고 쿼리를 최대 12배 빠르게 만들었다. UNIQUE 제약은 외래 키에서도 참조할 수 있다.

## 핵심 내용

- UNIQUE 제약은 여러 nullable 또는 복합 고유성 보장을 지원한다.
- PRIMARY KEY는 테이블당 하나의 null 불가 식별자로 제한된다.
- 제약은 매 쓰기마다 검증 비용을 치르지 않고 NORELY로 선언할 수 있다.
- 검증된 제약은 RELY를 사용해 최적화기 단순화를 활성화할 수 있다.
- 외래 키는 UNIQUE 제약을 참조할 수 있다.
- 벤치마크는 RELY 사용 시 큰 셔플 감소와 더 빠른 쿼리를 보여준다.

## 상세

이 글은 파이프라인의 고유성 보장을 스키마 메타데이터에 넣는 방법을 설명한다. 이를 기본 키와 분리해 선언하면 더 풍부한 데이터 모델을 지원하면서 검증도 명시적으로 유지된다. 데이터가 검증된 뒤에는 RELY로 최적화기가 이를 안전하게 사용해 중복 조인과 DISTINCT 연산을 피할 수 있다. 이렇게 하면 정확성 관리와 쿼리 최적화를 분리하고, 각 제약이 신뢰 가능해지는 시점을 팀이 제어할 수 있다.

## 참고 자료

- 아티클: [Databricks의 UNIQUE 제약 선언과 최적화](https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks)
