---
title: Apache Flink
description: 이벤트 타임 시맨틱, 정확히 한 번 보장, 통합 배치/스트림 API를 가진 상태적 스트림 처리 엔진
tags: [concept, data-engineering, stream-processing, flink, real-time, ko]
locale: ko
---

# Apache Flink

**Apache Flink**은 언바운드 및 바운드 데이터 스트림에 대한 상태적 계산을 위해 설계된 분산 스트림 처리 엔진입니다. 이벤트 타임 처리, 정확히 한 번 보장, 배치와 스트리밍을 위한 통합 API를 제공합니다.

## 핵심 철학

### 스트리밍 우선, 배치는 특수한 경우
- **바운드 스트림** = 배치 처리 (유한 입력)
- **언바운드 스트림** = 실시간 처리 (무한 입력)
- 동일한 API, 오퍼레이터, 런타임으로 둘 다 처리

### 이벤트 타임 처리
- 이벤트가 **발생한 시점** 기준으로 처리, 처리된 시점이 아님
- 워터마크를 통해 늦게 도착/순서가 뒤바뀐 이벤트 처리
- 처리 지연과 무관하게 정확한 결과 보장

### 정확히 한 번 시맨틱
- **엔드투엔드 정확히 한 번**: 소스 → Flink → 싱크 (트랜잭셔널 싱크 사용)
- **체크포인팅**: 오퍼레이터 상태의 주기적 분산 스냅샷 (Chandy-Lamport)
- **세이브포인트**: 업그레이드, 마이그레이션, A/B 테스트용 수동 스냅샷

## 아키텍처

### 런타임 컴포넌트
```
JobManager (클러스터 코디네이터)
    ├── 리소스 매니저 (슬롯 할당)
    ├── 디스패처 (REST API, 작업 제출)
    └── JobMaster (작업별: 스케줄링, 페일오버, 체크포인트)

TaskManagers (워커 노드)
    ├── 태스크 슬롯 (리소스 단위)
    └── 오퍼레이터 (상태를 가진 서브태스크)
```

### 실행 모델
- **파이프라인 실행**: 오퍼레이터 간 데이터 연속적 흐름 (네트워크 셔플)
- **오퍼레이터 체이닝**: 호환되는 오퍼레이터를 단일 태스크로 융합 (직렬화/네트워크 감소)
- **비동기 I/O**: 외부 서비스 호출(DB, API) 논블로킹 처리

### 상태 백엔드
| 백엔드 | 저장소 | 용도 |
|---------|---------|------|
| **HashMap** | 힙 | 작은 상태, 저지연 |
| **EmbeddedRocksDB** | 로컬 디스크 (RocksDB) | 큰 상태 (TB), 증분 체크포인트 |
| **Changelog** | 원격 (Kafka/Pulsar) | 상태 분리; 빠른 복구 |

## 주요 API

### DataStream API (Java/Scala)
```java
// 워터마크가 있는 이벤트 타임 윈도우
DataStream<Event> stream = env.addSource(kafkaSource)
    .assignTimestampsAndWatermarks(WatermarkStrategy
        .<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
        .withTimestampAssigner((e, ts) -> e.getTimestamp()));

stream.keyBy(Event::getKey)
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .reduce((a, b) -> a.add(b))
    .addSink(icebergSink);
```

### Table API / SQL (통합 배치 + 스트림)
```sql
-- 윈도우 TVF를 사용한 스트리밍 집계
SELECT user_id, COUNT(*) AS cnt,
       window_start, window_end
FROM TABLE(
  TUMBLE(TABLE events, DESCRIPTOR(event_time), INTERVAL '5' MINUTE)
)
GROUP BY user_id, window_start, window_end;
```

### Python API (PyFlink)
Java/Scala API와 완전한 패리티; ML 전처리 파이프라인에 인기

## 커넥터 (소스 & 싱크)

### 소스
- **Kafka** (정확히 한 번, 컨슈머 그룹, 파티션 발견)
- **Kinesis** (향상된 팬아웃, 체크포인팅)
- **Pulsar** (트랜잭션, 지리적 복제)
- **파일 시스템** (S3, HDFS, 로컬 — 연속적 파일 모니터링)
- **JDBC/CDC** (Debezium으로 MySQL/Postgres/Oracle → Flink)

### 싱크
- **Kafka** (트랜잭셔널, 정확히 한 번)
- **Iceberg** (다이나믹 싱크, 스키마 진화, 브랜칭)
- **JDBC** (업서트, 배치 쓰기)
- **파일 시스템** (롤링 파일, 파티셔닝, 컴팩션)
- **OpenSearch/Elasticsearch** (벌크 인덱싱)

## 고급 기능

### 복합 이벤트 처리 (CEP)
- 이벤트 스트림에서 패턴 탐지 (예: "5분 내 A 후 B 다음 C")
- NFA 기반 패턴 매칭; 루프, 대안, 시간 제약 지원

### Stateful Functions (클라우드 네이티브)
- **임베디드 모드**: 함수를 Flink 오퍼레이터로
- **원격 모드**: 함수를 독립적 서비스로 (gRPC/HTTP)
- 서버리스 스타일 이벤트 드리븐 아키텍처 가능

### 스트리밍 SQL
- **다이나믹 테이블**: 스트림을 추가 전용 테이블로; 체인지로그 스트림을 업데이트 테이블로
- **시간적 조인**: 버전된 테이블 조인 (이벤트 타임 기준 룩업)
- **윈도우 TVF**: TUMBLE, HOP, CUMULATE, SESSION
- **CDC 수집**: `CREATE TABLE ... WITH ('connector' = 'mysql-cdc')`

## 운영 고려사항

### 고가용성
- **JobManager HA**: ZooKeeper/Kubernetes 리더 선출
- **TaskManager 장애**: 건강한 TM으로 자동 재스케줄링
- **상태 복구**: 최신 체크포인트/세이브포인트에서 (RocksDB 증분으로 초 단위)

### 스케일링
- **병렬도**: 오퍼레이터별 설정; 세이브포인트 + 재시작으로 변경
- **반응형 스케일링** (K8s): 백로그/지연 지표 기반 KEDA/HPA
- **예측형 스케일링**: ML 기반 부하 예측 (Netflix, Uber)

### 모니터링 & 디버깅
- **지표**: 지연시간, 처리량, 백프레셔, 체크포인트 지속시간, 상태 크기
- **웹 UI**: 작업 그래프, 타임라인, 플레임 그래프, 백프레셔 시각화
- **쿼리 가능한 상태**: 오퍼레이터 상태를 REST로 노출해 외부 룩업용

## Flink on Kubernetes

### 배포 모드
| 모드 | 설명 |
|------|------|
| **세션 클러스터** | 장시간 실행 클러스터; 여러 작업이 TM 공유 |
| **작업 클러스터** | 작업별 전용 클러스터; 리소스 격리 |
| **애플리케이션 클러스터** | 작업 + Flink 런타임 단일 컨테이너 (네이티브 K8s) |

### Kubernetes Operator
- **FlinkDeployment** CRD가 JobManager + TaskManager 파드 관리
- **세이브포인트/업그레이드**: 세이브포인트 통해 자동 롤링 업그레이드
- **자동 스케일링**: KEDA와 통합해 반응형 스케일링

### 관리형 서비스
- **Amazon Managed Service for Apache Flink** (KDA)
- **Google Dataflow** (Flink 러너)
- **Azure Stream Analytics** (Flink 호환)
- **Ververica Platform** (엔터프라이즈 Flink on K8s)

## Iceberg 통합 (스트리밍 레이크하우스)

### 다이나믹 싱크 (Flink 1.18+, Iceberg 1.5+)
```sql
CREATE TABLE events (
  event_id STRING,
  event_time TIMESTAMP(3),
  payload STRING,
  event_type STRING
) PARTITIONED BY (event_type)
WITH (
  'connector' = 'iceberg',
  'catalog-type' = 'rest',
  'catalog-uri' = 'https://polaris.example.com/api/catalog',
  'warehouse' = 's3://bucket/warehouse',
  'format-version' = '2'
);

-- 스키마 진화와 함께하는 스트리밍 삽입
INSERT INTO events SELECT ... FROM kafka_source;
```

### 기능
- **스키마 진화**: 파이프라인 재시작 없이 컬럼 추가, 타입 변경
- **자동 테이블 생성**: 새 이벤트 타입 → 새 파티션 테이블
- **정확히 한 번**: Iceberg 스펙으로 2단계 커밋
- **포맷 v2/v3**: v3는 로우 레벨 삭제 지원 (MERGE INTO)

## 주요 참고 자료
- [Flink Documentation](https://nightlies.apache.org/flink/flink-docs-master/)
- [Flink SQL Reference](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sql/overview/)
- [Flink on Kubernetes](https://nightlies.apache.org/flink/flink-docs-master/docs/deployment/resource-providers/kubernetes/)
- [Iceberg Flink Integration](https://iceberg.apache.org/docs/latest/flink/)
- [Ververica Blog](https://ververica.com/blog/) — Flink 엔지니어링 인사이트

## 관련 개념
- `concepts/data-engineering/stream-processing.md`
- `concepts/data-engineering/apache-iceberg.md`
- `concepts/data-engineering/apache-kafka.md`
- `concepts/infrastructure/kubernetes.md`