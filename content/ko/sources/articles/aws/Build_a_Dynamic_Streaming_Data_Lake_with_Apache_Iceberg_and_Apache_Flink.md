---
title: Iceberg와 Flink로 동적 스트리밍 데이터 레이크 구축하기
description: Flink 관리형 서비스 위 Iceberg Dynamic Sink의 레코드 단위 테이블 라우팅과 자동 스키마 진화 — 파이프라인 재시작 없이 신규 이벤트 타입·컬럼 대응.
date: 2026-09-02
tags: [aws, data-engineering, lakehouse, apache-iceberg, apache-flink, streaming, schema-evolution, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-a-dynamic-streaming-data-lake-with-apache-iceberg-and-apache-flink/"
blog: aws
---

# Iceberg와 Flink로 동적 스트리밍 데이터 레이크 구축하기

**발행**: 2026-09-02 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-dynamic-streaming-data-lake-with-apache-iceberg-and-apache-flink/)

## 문제

상류 스키마 변경은 스트리밍 레이크 파이프라인에 나쁜 선택을 강요한다: 잡 재시작(수집 중단·인플라이트 데이터 위험) 또는 수동 마이그레이션(공수·불일치 위험) 중 하나. 예: `order_events`를 Iceberg에 쓰던 Flink 잡이 수요일에 프로듀서가 `loyalty_tier` 필드와 신규 `interaction_events` 타입을 추가했음을 알게 되는 상황.

## 해법: Flink 관리형 서비스 위 Iceberg Dynamic Sink

Flink 2.3 + Iceberg 1.11.0에서 **Dynamic Iceberg Sink**는 대상 테이블을 **레코드 단위**로 결정하고 스트림 중간에 스키마를 진화시킨다 — 재시작 없음:

- **라우팅**: `DynamicRecordGenerator`가 각 입력을 테이블 ID·브랜치·Iceberg 스키마·파티션 스펙·분배 모드·행 페이로드를 담은 `DynamicRecord`로 변환. 하나의 Flink 잡이 `order_events`·`interaction_events`·`user_events`·미래 타입을 각각 별도 Iceberg 테이블로 라우팅. 없는 테이블은 첫 목격 시 생성.
- **스키마 진화**: 쓰기 전 레코드 스키마와 테이블 스키마를 비교, 신규 필드는 다음 데이터 파일과 함께 optional 컬럼으로 추가. 기존 파일 유효 유지(신규 컬럼은 null 반환). 컬럼 추가·타입 확장(int→long, float→double)·required→optional 완화·컬럼 삭제 지원 — **컬럼명 변경은 미지원**.
- **`immediateTableUpdate`**: `true`면 라이터 서브태스크가 생성·변경을 인라인 적용(최저 지연, 카탈로그 호출 증가). `false`면 스키마 변경 레코드를 테이블명 키로 업데이트 오퍼레이터에 우회시켜 같은 테이블 변경을 직렬화. 정상 상태에서는 어느 쪽도 추가 셔플 없음.
- **정확히 한 번**: Flink 체크포인팅 + Iceberg 2단계 커밋으로 중복·손실 없는 종단 일관성.

## 스키마 소스 2종 (하류 동일)

1. **JSON 추론**(`SchemaAgnosticRoutingGenerator`): 레코드마다 Iceberg 스키마를 보수적 규칙으로 추론(정수→long, 실수→double, ISO-8601 문자열→timestamp, 중첩 객체→struct). 편리하지만 손실 있고 계약 없음 — 프로듀서가 필드 의미를 몰래 바꿔도 막을 수 없음.
2. **Glue Schema Registry(Avro)**: 프로듀서가 Avro 스키마를 등록, Kinesis 레코드가 스키마 버전 ID를 담고 있으며, 컨슈머가 등록된 정확한 스키마로 디코딩. 정밀 타입(long은 long, timestamp-micros 보존), 등록 시점 호환성 정책 강제, 단일 진실 원천. 새 버전 등록 시 잡 재시작 없이 Iceberg 테이블 진화.

## 파티셔닝

파티셔닝은 싱크가 아니라 **제너레이터**가 결정: 전역 `partition.candidates` 목록(예: `event_time,region,product`)에서 해당 테이블에 실제 존재하는 필드로만 스펙 도출. 후보 모두 없으면 비파티션 테이블(`$partitions`/카탈로그 스펙으로 모니터링 — `event_time` 대신 `create_timestamp`를 내는 프로듀서는 조용히 비파티션 테이블을 양산). 스펙 진화는 메타데이터 전용, 기존 파일은 압축 시까지 원래 스펙 유지.

## 토폴로지와 격리 트레이드오프

이벤트 타입이 섞인 단일 Kinesis 스트림이 설명은 간단하지만, 분리된 스트림도 동일하게 동작: 소스들을 하나의 DataStream으로 union 후 제너레이터가 레코드별 라우팅. union은 셔플 비용 없음(싱크가 내부 테이블별 라이터 키로 항상 재배분). 진짜 대가는 **격리**: 모든 테이블이 하나의 라이터 풀·커밋 집계기·커미터를 공유하므로 핫 스트림의 백프레셔가 전 테이블에 전파되고 라이터 병렬도도 잡 단위. 중소 규모 다수 이벤트는 하나로 묶고, 대용량 스트림은 별도 애플리케이션으로 분리.

## 배포(CDK)와 검증

`cdk-infrastructure`: `npm install`→`cdk bootstrap`→`cdk deploy -c appType=dynamic|dynamic-avro -c tableFormatVersion=2`(`-c catalogType=s3tables`로 S3 Tables 카탈로그 선택, 포맷 v2는 광범위 엔진 호환, v3는 EMR 7.12+/Glue ETL 같은 v3 인식 엔진용). 앱 시작 후 데이터 제너레이터로 v1 페이로드 전송 → `userAgent`·`scrollDepth`가 든 v2 전송 — 체크포인트 주기 내 새 테이블 등장, 신규 필드는 optional 컬럼으로, Athena에서 쿼리. 전체 코드: [aws-samples GitHub 저장소](https://github.com/aws-samples/sample-streaming-data-lake-with-apache-iceberg-and-apache-flink).

## 세미나 시사점

- 레코드별 목적지 + 함께 전달되는 스키마는 싱크를 정적 종점에서 **스키마 계약을 가진 라우터**로 바꾼다 — 재시작이 사라지는 구조적 이유.
- JSON 대 레지스트리 선택은 성능이 아니라 거버넌스 결정: 탐색은 추론, 무음 타입 드리프트가 용납 안 되는 프로덕션은 레지스트리 기반 Avro.
- 단일 싱크 union은 셔플은 공짜지만 격리로 대가를 치른다 — 블라스트 레이디어스를 의도적으로 설계할 것.

## 관련 개념

- `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/apache-flink.md`
