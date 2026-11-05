---
title: "Zerobus Ingest와 Debezium으로 Unity Catalog에 push 기반 CDC 구현"
description: "Debezium으로 데이터베이스 변경을 캡처하고 Zerobus Ingest를 통해 Kafka 클러스터 없이 Unity Catalog Delta 테이블에 적재하는 방법."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium"
blog: databricks
published_date: 2026-11-06
---

# Zerobus Ingest와 Debezium으로 Unity Catalog에 push 기반 CDC 구현

**원문**: [databricks](https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium) · **게시일**: 2026-11-05

## 개요

운영 데이터베이스의 변경 사항을 분석용 레이크하우스에 전달해야 하는 경우가 많지만, 소스 데이터베이스가 외부 서비스의 인바운드 연결을 차단하는 개인 기업 네트워크나 제한된 서브넷에 위치하는 경우가 흔하다. 팀은 폴링 없이 삽입, 갱신, 삭제를 정확히 캡처하고, 하류에서 재생할 수 있는 순서 신호, 소스 데이터베이스에 대한 최소 부하, 잠긴 환경에서의 아웃바운드 연결, 전송 수단으로만 쓰는 Kafka 클러스터 미운영, 그리고 레이크하우스에서 질의 가능한 형태의 적재라는 여섯 가지 요구를 동시에 충족해야 한다.

Debezium은 캡처 측을 담당하는 개방형 로그 기반 변경 데이터 캡처 플랫폼이다. 테이블을 폴링하지 않고 PostgreSQL의 쓰기 선행 로그 같은 트랜잭션 로그를 추적해 구조화된 변경 이벤트를 발행한다. Zerobus Ingest는 목적지 측을 담당하는 서버리스 push 기반 수집 서비스로, 메시지 브로커 없이 레코드를 Unity Catalog Delta 테이블에 직접 쓴다. Debezium Server Zerobus 싱크는 둘을 연결해 변경 이벤트를 Databricks에 직접 적재한다. 이 싱크는 NVIDIA와 Databricks의 엔지니어들이 공동으로 만들어 Debezium 개방형 프로젝트에 기여했으며, Debezium Server 3.7에 포함되었다.

Debezium에는 두 가지 운영 모델이 있다. Kafka가 정식 이벤트 버스인 환경의 Kafka Connect 플러그인과, 일반 컴퓨트에서 실행되며 Zerobus Ingest 같은 Kafka가 아닌 목적지로 직접 push하는 독립형 Debezium Server이다. Zerobus Ingest는 추가 전용이므로 변경 스트림이 Delta 테이블에 적재된 뒤 하류 단계에서는 키별 최신 버전을 얻기 위한 병합으로 Type-1 디멘전 테이블을 구축한다. 싱크는 두 가지 테이블 계약을 지원하며, envelope 모드에서는 멱등성 키와 소스 오프셋 진행 전 내구성 있는 확인을 포함한 전체 Debezium 변경 이벤트를 적재한다.

## 핵심 내용

- Debezium은 트랜잭션 로그를 읽어 삽입, 갱신, 삭제를 캡처하고 소스 순서를 보존하며 소스 부하를 최소화한다.
- Zerobus Ingest는 push 기반이자 서버리스로, 브로커 없이 레코드를 Unity Catalog Delta 테이블에 직접 쓴다.
- Debezium Server Zerobus 싱크는 캡처와 레이크하우스 사이의 중간 Kafka 홉을 제거한다.
- 싱크는 NVIDIA와 Databricks의 공동 개발로 탄생했고 Debezium Server 3.7에 포함된다.
- 캡처가 데이터베이스 옆에서 실행되고 이벤트를 아웃바운드로 push하므로 개인 네트워크에서도 운영 가능하다.
- Zerobus는 추가 전용이므로 적재된 변경 스트림을 병합해 현재 상태 테이블을 하류에서 구축한다.

## 상세

이 글은 변경 이벤트를 Kafka에서 레이크하우스로 옮기기 위한 추가 복제 작업이 필요한 전통적 메시지 버스 아키텍처와 Zerobus 아키텍처를 대조한다. 여섯 가지 요구는 삭제 포함 전체 연산 캡처, 순서 보존, 폴링 오버헤드 회피, 개인 네트워크 지원, 순수 전송용 Kafka 회피, 레이크하우스 준비 데이터 적재이다. 각 Debezium 이벤트는 이전·이후 행 상태, 연산 코드, 소스 메타데이터, 타임스탬프를 담는다. Envelope 모드는 순서와 멱등성 보호 장치를 포함한 전체 이벤트를 적재한다. 정확한 커넥터 구성, 두 테이블 계약, 로컬 PostgreSQL 실습 안내는 링크된 원문과 커뮤니티 동반 how-to 블로그에 있다.

## 참고 자료

- 원문: [databricks](https://www.databricks.com/blog/push-based-cdc-unity-catalog-zerobus-ingest-and-debezium)
