---
title: "AWS에서 Apache Iceberg 테이블을 위한 올바른 스트리밍 수집 경로 선택하기"
description: "AWS의 다섯 가지 Iceberg 스트리밍 수집 경로(스트리밍 테이블, MSK Connect의 Iceberg 싱크 커넥터, Amazon Data Firehose, Managed Service for Apache Flink, EMR 위 Spark Structured Streaming)를 여덟 가지 기술 기준으로 비교하고, 신선도·CDC·컴팩션 소유권을 묻는 두 질문으로 좁히는 의사결정 프레임워크를 제시합니다."
tags: [source, aws-big-data, streaming, iceberg, data-engineering, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/choose-the-right-streaming-ingestion-path-for-apache-iceberg-tables-on-aws"
blog: aws-big-data
published_date: 2026-11-14
---

# AWS에서 Apache Iceberg 테이블을 위한 올바른 스트리밍 수집 경로 선택하기

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/choose-the-right-streaming-ingestion-path-for-apache-iceberg-tables-on-aws) · **게시일**: 2026-11-13

## 개요

실시간 데이터를 Apache Iceberg 테이블에 기록하는 수집 경로 선택은 저지연 데이터 레이크를 구축하는 핵심 단계입니다. 조직이 AI 에이전트, 운영 대시보드, 분석 워크로드에 실시간 데이터를 공급하려면 테이블 포맷을 하나로 공유하는 것만으로는 부족하고, 수집 지연을 실제로 줄이는 스트리밍 경로를 골라야 합니다. 저자들은 이 선택을 운영적 요구 사항과 기술적 요구 사항 사이의 절충으로 보며, 그 결정이 파이프라인 코드, IAM 모델, 운영 런북 속에 자리 잡기 때문에 테이블 자체보다 되돌리기가 훨씬 어렵다고 경고합니다.

글에서 비교하는 다섯 가지 경로는 다음과 같습니다. Amazon MSK와 Amazon Kinesis Data Streams에서 기본 제공되는 전송 기능인 스트리밍 테이블, Amazon MSK Connect의 Iceberg 싱크 커넥터, 서버리스 방식의 Amazon Data Firehose, 그리고 애플리케이션을 직접 작성하는 Amazon Managed Service for Apache Flink와 Amazon EMR 위의 Spark Structured Streaming입니다. 다섯 경로는 모두 여덟 가지 기술 기준, 즉 업서트 동작, 테이블 유지 관리, 스키마 진화, 메시지 직렬화, 소스·대상 지원, 확장성, 여러 테이블로의 팬아웃, 이동 중 변환을 두고 평가됩니다. 기술 기준에 앞서 네 가지 운영 질문이 후보를 가릅니다. 완전관리형을 원하는지, 설정과 코드 중 무엇을 선호하는지, 분 미만의 데이터 신선도가 필요한지, 이식 가능한 오픈소스 방식이 필요한지입니다.

이 글은 새 기능이 출시될 때마다 갱신하겠다고 밝힌 살아 있는 문서입니다. 마지막에는 의사결정 프레임워크가 제시됩니다. 쓰기 패턴이 추가 전용인지 아니면 행 단위 갱신과 삭제가 필요한지, 그리고 컴팩션 소유권이 서비스에 있는지 팀에 있는지라는 두 질문만으로 보통 후보가 한두 개로 좁혀집니다.

## 핵심 내용

- 스트리밍 테이블은 Amazon MSK Express 브로커와 Kinesis Data Streams On-Demand 모드의 기본 전송 기능으로, 자체 관리 파이프라인보다 전송 비용이 최대 60% 낮고, 적정 크기의 파일을 써서 후속 쿼리 비용을 추가로 최대 30%까지 줄입니다.
- 스트리밍 테이블은 AWS Glue Schema Registry에 등록된 스키마로 레코드를 검증하고, 최적화된 Parquet 파일로 인라인 컴팩션을 수행하며, 검증에 실패한 레코드는 Amazon S3의 데드레터 큐로 보냅니다. 추가 전용이며 사용자 엔진에는 읽기 전용입니다.
- MSK Connect의 Iceberg 싱크 커넥터는 토픽 파티션 수에 맞춰 태스크를 늘려 확장하고, 대상 테이블을 자동 생성하며, 하나의 토픽을 여러 Iceberg 테이블로 팬아웃할 수 있습니다. 다만 갱신이나 삭제를 지원하지 않는 추가 전용 쓰기이고 내장 컴팩션이 없습니다.
- Amazon Data Firehose는 소스 지원 폭이 가장 넓습니다(MSK, Kinesis Data Streams, Direct PUT). JQ 표현식으로 라우팅하며 코드 없이 삽입·갱신·삭제를 처리하고, AWS Lake Formation으로 테이블·컬럼 수준 접근 제어를 적용합니다. 입력은 JSON만, 출력은 항상 Parquet입니다.
- Firehose는 처리량과 파티션 수가 서로 절충 관계이고 작은 파일을 많이 만들어 외부 컴팩션 전략이 처음부터 필요하며, 갱신 시마다 삭제 파일과 데이터 파일로 Amazon S3 PUT 요금이 발생하고 Amazon MSK Serverless는 소스로 지원하지 않습니다.
- Managed Service for Apache Flink는 애플리케이션 작성·유지가 필요한 유일한 경로이지만, 이퀄리티 삭제를 포함한 완전한 CDC, 워터마크 기반의 이벤트 시간 의미론, Flink 체크포인트에 맞춘 정확히 한 번 커밋, Iceberg 1.10 이상 싱크에서의 내장 컴팩션을 제공합니다.
- Amazon EMR의 Spark Structured Streaming은 MERGE INTO 전체 지원과 rewrite_data_files, expire_snapshots, remove_orphan_files 등 Iceberg Spark 프로시저 전체를 제공합니다. MERGE 전에 중복을 제거해야 하며 이는 성능 최적화가 아니라 정확성 요건입니다.
- 분 미만 신선도를 지원하면서 컴팩션까지 관리해 주는 경로는 Flink와 EMR의 Spark 두 가지뿐입니다.
- Spark는 소스 파티션당 태스크 하나(Kinesis 샤드 하나 또는 MSK 토픽 파티션 하나당 하나)를 만들므로, 파티션이 적은 소스에서는 익스큐터를 더해도 처리량이 오르지 않습니다.
- Firehose에서 CreateDeliveryStream 호출에 AppendOnly 플래그를 true로 설정하면 추가 전용 워크로드의 처리량에 맞춰 자동 확장합니다.
- 결론은 짧습니다. 가장 낮은 운영 부담을 원하는 추가 전용 워크로드는 스트리밍 테이블부터, 갱신과 삭제가 있는 CDC는 Managed Service for Apache Flink를 향합니다.

## 세부 사항

### 여덟 가지 기술 기준과 5단계 참조 아키텍처

여덟 가지 기준은 선호보다 먼저 가능성을 가릅니다. 추가 전용 로깅·IoT 워크로드인지, 소스 상태를 그대로 반영하는 CDC인지가 업서트 동작을 결정하고, Amazon S3 Tables는 파일 컴팩션, 스냅샷 만료, 고아 파일 제거를 자동으로 수행하거나 싱크 파이프라인 안에서 직접 유지 관리할 수 있습니다. 스키마 진화, JSON·Avro·Protobuf 직렬화와 스키마 레지스트리 선택, 완전관리형 S3 Tables 대신 자체 S3 버킷의 Iceberg를 AWS Glue Data Catalog로 카탈로그하는 방식, 확장성, 팬아웃, 이동 중 변환이 이어집니다. 참조 아키텍처는 5단계 패턴입니다. 스트림 소스(SDK 애플리케이션, 로그 파일, IoT 이벤트, 데이터베이스 CDC), 스트림 스토리지(MSK 또는 Kinesis Data Streams, 혹은 Direct PUT으로 Firehose에 직접), 스트림 처리(다섯 옵션 중 하나), 스트림 싱크(S3 Tables 또는 범용 S3 버킷의 Iceberg 테이블), Amazon Athena를 통한 분석입니다.

### 스트리밍 테이블: 인라인 컴팩션을 갖춘 완전관리형 전송

토픽이나 스트림을 선택하고 등록된 스키마를 지정한 뒤 S3 테이블 버킷을 대상으로 정하면, 서비스가 설정된 신선도 구간까지 레코드를 버퍼링하고 검증·변환한 뒤 최적화된 Parquet 파일로 인라인 컴팩션하여 커밋합니다. 쓰기 조율과 정확히 한 번 전송 의미론이 내장되어 있어, 그렇지 않으면 실패한 커밋으로 나타나는 동시 쓰기 충돌이 사라집니다. MSK에서는 Express 브로커 백엔드에서 동작해 브로커의 읽기 용량을 소모하지 않고 가용 영역 간 전송 요금도 없으며, Kinesis에서는 읽기 한도와 향상된 팬아웃을 소비하지 않습니다. Iceberg가 필요 없다면 같은 전송으로 소스 형식 그대로 범용 S3 버킷에 쓸 수 있어 아카이브, 백업, ML 학습 데이터에 유용합니다. 단점은 추가 전용이자 읽기 전용이라는 점입니다. CDC를 적용할 수 없고 행 삭제는 레코드 만료 작업을 통해서만 가능합니다.

### 설정 기반 경로: MSK Connect와 Data Firehose

MSK Connect의 Iceberg 싱크 커넥터는 이미 Kafka Connect를 운영하는 팀에 잘 맞습니다. 표준 Kafka Connect 컨버터로 Avro, JSON, Protobuf를 처리하고 스키마 레지스트리를 지원하며, 스키마 변경을 대상 테이블로 전파하고 내용 기반 팬아웃도 됩니다. 제약도 뚜렷합니다. 단순 메시지 변환만 가능해 조인, 집계, 상태 기반 로직이 없고, Iceberg 브랜치에 쓸 수 없으며, Kafka 소스만 지원됩니다. 커넥터가 연속으로 커밋하면서 작은 파일이 많이 생기므로 공격적인 컴팩션 일정이 없으면 쿼리 성능이 점점 나빠집니다. Firehose는 소스 범위가 가장 넓은 서버리스 경로로, JQ 표현식으로 레코드를 라우팅하고 이동 중 변환을 위해 Lambda 함수를 호출할 수 있습니다. 컬럼 이름과 타입은 대상 테이블과 정확히 일치해야 하고, 초과 필드는 건너뛰며, 불일치 레코드는 S3 오류 버킷으로 갑니다. 스키마 진화는 컬럼 추가만 허용되고 이름 변경·삭제·타입 변경은 수동 개입이 필요하며, 스키마 레지스트리 강제가 없어 잘못된 데이터 유입 위험이 있습니다.

### 애플리케이션 코드 경로: Flink와 EMR의 Spark

Flink는 마이크로배치가 아니라 레코드를 하나씩 처리하므로, 이벤트 시간으로 키를 잡은 윈도우 집계는 이벤트 도착 순서와 무관하게 같은 결과를 냅니다. 체크포인트 간격이 커밋 빈도와 파일 크기를 결정하며, 후속 쿼리 성능에 가장 큰 영향을 주는 설정입니다. 내장 유지 관리가 있어도 컴팩션 주기 사이에는 작은 파일이 계속 쌓입니다. Flink 경험이 없는 팀은 상태, 워터마크, 백프레셔 학습을 계획해야 하고, Managed Service for Apache Flink Agent Skill이 관용적인 애플리케이션 코드를 생성해 이 과정을 줄여 줍니다. EMR의 Spark는 이미 Spark를 운영하고, MERGE 의미론이 필요하며, 분 단위 지연을 수용할 수 있는 팀에 적합합니다. 배치와 스트리밍이 같은 DataFrame API를 공유하므로 하나의 변환 코드로 야간 재처리 작업과 상시 파이프라인을 모두 처리합니다. 다만 소스 배치에 같은 키의 행이 여러 개면 MERGE INTO가 모호해집니다. Spark가 어떤 행을 적용할지 비결정적으로 고르거나 multiple matching rows 오류로 배치를 실패할 수 있으므로, 키별 이벤트 타임스탬프 순위 같은 방식으로 중복을 제거해야 합니다. 수십 초에서 수 분의 마이크로배치 지연, 비슷한 처리량에서 Flink 애플리케이션보다 높은 비용, 파이프라인 안에서 직접 운영하는 컴팩션까지가 남은 과제입니다.
