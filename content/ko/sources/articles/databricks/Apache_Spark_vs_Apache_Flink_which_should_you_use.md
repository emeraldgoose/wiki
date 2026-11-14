---
title: "Apache Spark vs Apache Flink: 무엇을 선택해야 할까?"
description: "Databricks는 과거 플링크 도입의 명분이던 지연 시간 격차를 Spark Real-Time Mode가 메웠다고 진단한다. 공개 벤치마크에서 스파크는 상태 없는 처리, 상태 기반 집계, 스트림-정적 조인에서 플링크와 동급이거나 더 낮은 p99 지연을 기록했고, 결과는 플링크 대비 최대 92% 빠른 것으로 요약됐다. 글은 두 엔진을 기능별로 비교하고 플링크가 여전히 적합한 좁은 사례들을 짚어 준다."
tags: [source, databricks, apache-spark, apache-flink, streaming, ko]
locale: ko
source_url: "https://www.databricks.com/blog/spark-vs-flink"
blog: databricks
published_date: 2026-11-14
---

# Apache Spark vs Apache Flink: 무엇을 선택해야 할까?

**원문**: [Databricks 블로그](https://www.databricks.com/blog/spark-vs-flink)

## 개요

지난 몇 년간 스파크 옆에 아파치 플링크를 추가하는 가장 큰 이유는 지연 시간이었다. 플링크는 스트림 우선 엔진인 반면 스파크는 초 단위 마이크로배치로 스트리밍했기 때문이다. Databricks의 답은 Real-Time Mode다. 기존 Structured Streaming 쿼리에 트리거를 지정해 밀리초 수준의 엔드투엔드 지연을 내는 방식으로, 이 격차가 사라지자 질문은 "어느 엔진이 가장자리에서 더 빠른가"에서 "몇 개의 엔진을 만들고, 운영하고, 거버넌스할 것인가"로 바뀌었다고 글은 주장한다.

스파크는 통합 엔진이다. 배치 ETL, SQL 분석, 머신러닝, 스트리밍을 한 엔진에서 처리하며 같은 DataFrame과 SQL 코드가 예약 배치 작업, 마이크로배치 스트림, Real-Time Mode 스트림 사이를 그대로 오간다. 플링크는 전문가용이다. 처음부터 스트리밍을 위해 설계되어 배치를 유한한 스트림으로 다루며 키 기반 상태와 복합 이벤트 처리에 강하다. Databricks는 플링크의 적합 범위를 좁은 사례로 한정하고, 공개 벤치마크와 이름을 밝힌 프로덕션 고객 사례로 엔진 통합 논리를 뒷받침한다.

글은 증거의 한계도 솔직하게 밝힌다. 벤치마크는 Databricks가 실행했고, 스파크는 Databricks 위에서, 플링크는 AWS Managed Service for Apache Flink 1.18에서 구동됐으며, 스파크의 최악 실행과 플링크의 최선 실행을 비교했다. 결과는 워크로드에 따라 달라지므로, 결정 전에 각 팀이 자체 파이프라인으로 먼저 검증하라는 조언으로 끝맺는다.

## 핵심 내용

- Databricks의 공개 벤치마크에서 Spark Real-Time Mode는 상태 없는 작업에서는 플링크와 동급, 상태 기반 집계와 스트림-정적 조인에서는 더 낮은 p99 지연을 보였다.
- 벤치마크 코드는 공개됐고, 고객 워크로드에서 파생한 피처 연산 작업으로 초당 1만 레코드를 30분 동안 흘리며 Kafka 입력-출력 지연을 측정했다.
- p99 결과: 상태 없는 변환은 양쪽 모두 3ms, 상태 기반 집계는 14ms(스파크) 대 45ms(플링크), 스트림-정적 조인은 9ms 대 95ms였다.
- Databricks는 결과를 플링크 대비 최대 92% 빠르다고 요약하면서도, 스파크 최악 실행과 플링크 최선 실행을 비교했다는 단서를 달았다.
- MakeMyTrip은 두 번째 엔진을 피하기 위해 플링크 대신 Spark Real-Time Mode를 선택했고, P50은 44ms로, P99는 1분 이상에서 약 500ms로 줄었다. Coinbase와 DraftKings도 프로덕션에서 Real-Time Mode를 운영한다.
- Real-Time Mode는 기존 Structured Streaming 쿼리의 트리거일 뿐이라 같은 코드가 재작성 없이 지연 등급을 이동하며, update 출력 모드와 Kafka 또는 행 단위 foreach 싱크가 필요하다.
- 상태 연산자는 오픈소스 Apache Spark 4.3에 도착했고 Databricks에서는 일반 공급 단계로, 클래식 컴퓨트나 Lakeflow Spark Declarative Pipelines에서 구동된다.
- 플링크가 남는 영역은 네 가지다. 로컬 디스크보다 훨씬 큰 키 기반 상태(Flink 2.x의 분리형 상태 ForSt), 내장 CEP 라이브러리나 SQL MATCH_RECOGNIZE를 쓰는 복합 이벤트 처리, 저지연 경로의 이벤트 타임 타이머, 그리고 이미 운영 중인 플링크 플랫폼.
- Real-Time Mode의 transformWithState는 아직 이벤트 타임 타이머를 지원하지 않는다. 글이 짚는 유일한 기술적 격차다.
- 엔진 하나는 코드베이스 하나, 팀 하나, 거버넌스 모델 하나를 뜻한다. 스트리밍 테이블과 배치 테이블이 Unity Catalog에서 계보와 접근 제어를 공유하고, 같은 파이프라인이 학습용과 온라인 추론용 ML 피처를 함께 만든다(DraftKings 사례).
- 마이그레이션은 옮겨 적기에 가깝다. 대부분의 Flink SQL과 DataStream 로직은 Structured Streaming의 Spark SQL과 DataFrame으로 옮겨지며, 상태 없는 작업과 집계부터 시작해 상태 로직을 transformWithState로 옮기면 된다.

## 세부 사항

### 통합 엔진 대 스트림 우선 전문 엔진

스파크는 배치 엔진으로 시작해 스트림을 계속 자라나는 테이블로 다루는 Structured Streaming을 얹었다. 플링크는 반대로 스트리밍을 먼저 설계하고 배치를 유한한 스트림으로 취급한다. 둘 다 아파치 소프트웨어 재단 프로젝트로 정확히 한 번 처리, 상태 연산자, SQL API를 갖추고 있지만, 차이는 범위다. 언어 지원도 갈린다. 스파크는 Python, SQL, Scala, Java에 Spark Connect를 통한 Go, Rust, Swift 클라이언트까지 지원하고, 플링크는 Java, SQL, PyFlink를 제공한다. 머신러닝에서 스파크는 MLlib, 피처 파이프라인, SQL 벡터 검색, LLM 데이터 준비를 갖춘 반면 플링크는 네이티브 ML이 제한적이라 보통 다른 시스템과 짝을 이룬다. 레이크하우스 연동도 스파크가 Delta Lake와 Apache Iceberg 읽기·쓰기를 네이티브로 지원하는 것과 달리 플링크는 커넥터 방식이다.

### 지연 시간 벤치마크 해부

벤치마크는 고객 파생 피처 연산 워크로드를 초당 1만 레코드로 30분 동안 흘리며 Kafka 입력-출력 지연을 측정했다. Spark Real-Time Mode는 상태 없는 변환에서 3ms로 플링크와 나란히 갔지만, 상태가 개입되는 순간 격차가 벌어졌다. 상태 기반 집계에서 14ms 대 45ms, 스트림-정적 조인에서 9ms 대 95ms였고, Databricks는 이를 묶어 플링크 대비 최대 92% 빠르다고 발표했다. 단서도 분명하다. 스파크는 Databricks에서, 플링크는 AWS의 매니지드 서비스 1.18 버전에서 구동됐고, 비교는 스파크 최악 실행 대 플링크 최선 실행이다. 이 수치들은 해당 워크로드 패턴에 대한 근거로 읽어야 하며 보편적 판정이 아니다. 프로덕션 수치도 같은 방향을 가리킨다. MakeMyTrip은 두 번째 엔진 구상을 접은 뒤 P50을 44ms로, P99를 1분 이상에서 약 500ms로 낮췄다.

### 플링크를 고르는 조건과 엔진 통합의 이유

플링크는 네 조건이 대부분 겹칠 때 빛난다. 로컬 디스크를 넘는 초대형 키 상태(Flink 2.x 분리형 상태), Flink CEP나 SQL MATCH_RECOGNIZE로 이벤트 시퀀스 패턴을 찾는 복합 이벤트 처리, 저지연 경로가 이벤트 타임 타이머에 크게 의존하는 경우, 그리고 배치·SQL·ML을 먹이지 않는 독립 스트림을 지닌 기존 플링크 플랫폼. 반대로 스트림이 분석, ML 피처, 레이크하우스 테이블까지 연결된다면 스파크 하나로 로직·운영·거버넌스의 복제를 피할 수 있다. 두 번째 엔진은 코드베이스 하나, 기술 스택 하나, 거버넌스 규칙 하나를 더한다. 배치는 스파크, 스트리밍은 플링크로 나눈 팀은 같은 비즈니스 로직을 두 번 쓰고 두 버전 사이의 어긋남을 디버깅하곤 한다. 파이프라인을 손으로 엮는 대신 선언할 수도 있다. Spark Declarative Pipelines는 스트리밍 테이블의 의존성 관리와 증분 새로 고침을 맡는다. 아파치 스파크 원 창시자들이 세운 Databricks는 Real-Time Mode를 일반 공급으로 운영하며, 오픈소스 스파크용 코드는 Databricks에서 수정 없이 돌아간다.
