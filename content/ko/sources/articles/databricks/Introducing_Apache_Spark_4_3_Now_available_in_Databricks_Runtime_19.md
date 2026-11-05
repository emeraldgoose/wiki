---
title: "Apache Spark® 4.3 소개 - Databricks Runtime 19에서 사용 가능"
description: "Spark 4.3은 Real-Time Mode에 상태 저장 처리를 도입해 P99 지연 시간 150ms 미만을 달성하고, Auto CDC, 작은 데이터 처리 가속, 풍부한 SQL 지원을 더한다."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19"
blog: databricks
published_date: 2026-11-06
---

# Apache Spark® 4.3 소개 - Databricks Runtime 19에서 사용 가능

**원문**: [databricks](https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19) · **게시일**: 2026-11-05

## 개요

Apache Spark 4.3은 Structured Streaming을 확장해 Real-Time Mode에서 상태 저장 처리를 지원한다. 스트리밍 집계, 중복 제거, 사용자 지정 상태 저장 처리를 통해 이벤트 간 컨텍스트를 기억해야 하는 응용 프로그램을 구축할 수 있으며, 보고된 벤치마크에서 대표적인 상태 저장 워크로드의 P99 종단 간 지연 시간이 150밀리초 미만이었다. 이를 통해 Real-Time Mode가 완전한 스트리밍 엔진으로 확장되고, 밀리초 수준 지연에 도달하기 위해 별도 엔진이 필요할 가능성이 줄어든다. 이 릴리스는 배치 분석, 변경 데이터 캡처, 작은 데이터셋 반복, 원격 실행, SQL 전반에서도 Spark를 강화한다.

릴리스의 주요 기능은 여러 가지다. SCD Type 2 Auto CDC는 Python, SQL, Spark Connect를 통해 기록의 변화 이력을 더 적은 사용자 지정 변경 처리 로직으로 추적한다. Project Feather는 작은 단일 파티션 질의 조각의 고정 실행 오버헤드를 줄이고, Arrow 네이티브 캐싱은 더 효율적인 데이터 재사용을 지원한다. Spark Connect는 관측성과 JDBC 및 Python 개선을 통해 원격 실행 개발과 운영을 더 쉽게 만든다. SQL 지원은 VARIANT 변환, JSON_TABLE, 시계열 조인, 나노초 타임스탬프 미리보기를 통해 중첩 및 시간 지향 데이터의 네이티브 처리를 확장한다. Spark 4.3은 또한 6개월마다 한 번에서 3개월마다 한 번으로 릴리스 주기를 단축하는 분기별 기능 릴리스 주기를 시작한다.

Real-Time Mode는 Structured Streaming의 기존 API와 내구성 및 복구를 위한 상태 저장소 및 체크포인팅 메커니즘 위에 구축된다. 상태 저장 처리를 지원하려면 스케줄링과 셔플 동작에 근본적인 변화가 필요했다. 네이티브 동시 스테이지 스케줄링과 파이프라인 셔플은 블로킹 구체화 단계를 기다리지 않고 생산자와 소비자 스테이지가 동시에 실행되도록 한다. 파이프라인 셔플 의존성은 이 실행 계약을 정의하며, 셔플 매니저가 실제 데이터 전송을 제공한다.

## 핵심 내용

- 상태 저장 실시간 응용 프로그램이 스트리밍 집계, 중복 제거, transformWithState를 낮은 지연 시간으로 사용할 수 있다.
- 벤치마크한 세 상태 저장 워크로드의 P99 지연 시간이 150ms 미만으로 보고되었지만, 이는 보편적 지연 보장은 아니다.
- SCD Type 2 Auto CDC는 Python, SQL, Spark Connect에서 더 적은 사용자 지정 로직으로 기록 이력을 추적한다.
- Project Feather는 적격한 작은 단일 파티션 조각의 스케줄링 및 셔플 오버헤드를 줄인다.
- Spark Connect 관측성과 JDBC 및 Python 사용성 개선으로 원격 개발과 운영이 쉬워진다.
- VARIANT 처리, JSON_TABLE, 시계열 조인, 나노초 타임스탬프가 네이티브 SQL 분석을 확장한다.
- 릴리스 주기가 6개월에서 분기별로 단축된다.

## 상세

보고된 P99 종단 간 지연 시간 값은 dropDuplicates 136ms, window aggregation 139ms, transformWithState 141ms이다. Spark는 일반 의존성을 블로킹 셔플 매니저로, 파이프라인 의존성을 스트리밍 셔플 매니저로 라우팅하며, 파이프라인 그룹의 스테이지는 충분한 태스크 슬롯이 있을 때만 함께 실행되고 함께 실패한다. Real-Time Mode 벤치마크와 실행 상세는 링크된 원문에서 가져왔으며, 정확한 벤치마크 구성, API, 미리보기, 플랫폼 가용성은 원문에서 확인해야 한다.

## 참고 자료

- 원문: [databricks](https://www.databricks.com/blog/introducing-apache-spark-43-now-available-databricks-runtime-19)
