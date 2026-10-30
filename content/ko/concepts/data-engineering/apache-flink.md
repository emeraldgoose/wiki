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

## 상태 관리 (State Management)

### 상태란 무엇인가?

**상태(State)**는 오퍼레이터가 여러 이벤트에 걸쳐 기억하는 정보입니다. 대표적인 예:

- 패턴 탐지(CEP)를 위해 지금까지 본 이벤트 시퀀스
- 분/시/일 단위로 보류 중인 집계값
- 스트림으로 훈련 중인 모델의 현재 파라미터
- 과거 발생 이벤트에 대한 효율적 접근

Flink는 상태를 다음 목적을 위해 인식해야 합니다.

- **체크포인트**와 **세이브포인트**를 통한 **장애 내성(fault tolerance)**
- 상태를 병렬 인스턴스 간에 재분배함으로써 **애플리케이션 스케일링**

상태가 어디에 어떻게 저장되는지는 [상태 백엔드](#상태-백엔드-state-backends)를 참조하세요.

### 키 기반 상태 (Keyed State)

키 기반 상태는 **현재 입력 요소의 키에 범위가 한정된 내장 키/값 저장소**처럼 동작합니다.

- **`KeyedStream`에서만 사용 가능** (`keyBy` / `key_by` 이후)
- **현재 이벤트 키에 해당하는 값**에만 접근 가능
- 스트림과 상태가 키로 **정렬(alignment)**되어 있어, 갱신은 로컬 연산(트랜잭션 오버헤드 없음)
- 이 정렬 덕분에 Flink는 상태를 재분배하고 스트림 파티셔닝을 투명하게 조정할 수 있음

**키 그룹(Key Group)**은 키 기반 상태 재분배의 원자 단위입니다.

- 키 그룹 개수 = 설정된 **최대 병렬도(maximum parallelism)**
- 각 병렬 오퍼레이터 인스턴스는 하나 이상의 키 그룹을 소유
- 향후 스케일링을 고려해 최대 병렬도를 결정할 것

관리형 키 기반 상태 프리미티브 (`RichFunction.open()`에서 `RuntimeContext`로 생성, 요소 단위로 읽기/쓰기):

- `ValueState<T>` — 키당 단일 값; `update(T)`, `value()`
- `ListState<T>` — 키당 리스트; `add(T)` / `addAll(...)`, `update(List<T>)`로 전체 교체, `get()`으로 순회
- `ReducingState<T>` — `ReduceFunction`으로 유지되는 키당 단일 집계값
- `AggregatingState<IN, OUT>` — `AggregateFunction` 기반 키당 집계값
- `MapState<K, V>` — 키당 맵; `put`, `get`, `remove`, `contains`, `entries()`

참고:

- 상태 디스크립터(`ValueStateDescriptor` 등)는 타입 정보와 선택적 `StateTtlConfig`를 보관
- 체크포인팅이 활성화되면 키 기반 상태는 체크포인트의 일부로 자동 저장

### 오퍼레이터 상태 (Operator State)

오퍼레이터(비키) 상태는 키가 아닌 **단일 병렬 오퍼레이터 인스턴스에 범위가 한정**됩니다.

- `CheckpointedFunction`(또는 리스트 상태용 `ListCheckpointed`) 구현으로 접근
- 체크포인트 시 `snapshotState(...)`로 상태 기록, 초기화/복구 시 `initializeState(...)`
- 리스트 스타일 오퍼레이터 상태는 스케일 아웃 시 두 가지 재분배 방식 지원:
  - **균등 분할(Even-split)**: 전체 상태는 태스크별 리스트의 연결; 복구 시 새 태스크에 균등 분할(비어 있을 수 있음)
  - **유니온(Union)**: 모든 새 태스크가 전체 리스트 수신 — 카디널리티가 큰 상태에서는 피할 것(RPC 프레임 크기/OOM 위험)
- 주요 용도: 소스 오프셋, 버퍼링 싱크, 글로벌 카운터

### 브로드캐스트 상태 (Broadcast State)

브로드캐스트 상태는 **한 스트림이 모든 태스크에 브로드캐스트될 때 사용하는 맵 형식의 특수 오퍼레이터 상태**입니다.

- `MapStateDescriptor`로 선언
- `broadcast(descriptor)`로 브로드캐스트 입력, `connect(...)`로 비브로드캐스트 스트림과 연결
- **브로드캐스트 측에서 쓰기**, 다른 측은 **읽기 전용** 뷰
- 고려사항:
  - 태스크 간 통신 없음: 모든 태스크가 각 요소에 대해 동일하게 갱신해야 함
  - 이벤트가 태스크마다 다른 순서로 도착할 수 있으므로, 갱신 로직은 순서에 의존하지 않아야 함
  - 각 태스크가 자신의 복사본을 체크포인트(상태 크기가 병렬도 `p`에 비례)
  - RocksDB 백엔드 미지원 — 런타임에 메모리에 보관

### 상태 백엔드 (State Backends)

| 백엔드 | 저장소 | 용도 |
|---------|---------|------|
| **HashMapStateBackend** | JVM 힙 | 작은 상태, 저지연 |
| **EmbeddedRocksDBStateBackend** | 로컬 디스크 (RocksDB) | 큰 상태 (TB), 증분 체크포인트 |
| **ChangelogStateBackend** | 원격 브로커 (Kafka/Pulsar) | 상태 분리; 빠른 복구 |

참고:

- 백엔드 선택은 애플리케이션 로직과 독립 — 상태 디스크립터는 동일
- 체크포인트 *위치*(상태 저장소)는 별도 설정, 보통 분산 파일시스템/오브젝트 스토어
- RocksDB는 증분 체크포인트 지원; 힙 백엔드는 일반적으로 전체 상태 스냅샷
- 브로드캐스트/오퍼레이터 상태는 메모리 전용

### 상태 영속성, 체크포인트, 세이브포인트

- **체크포인트**: 입력 오프셋 + 오퍼레이터 상태의 일관된 스냅샷; 정확히 한 번 복구 가능
- 체크포인트 주기는 런타임 오버헤드와 복구 시간의 트레이드오프
- 체크포인팅은 **기본 비활성** — 실행 환경에서 활성화 필요
- 체크포인트 지점으로 재생(replay)해야 하므로, 되감기(rewind) 가능한 소스(Kafka 등) 필요
- **정렬 체크포인트(aligned)**는 배리어 정렬 사용; **비정렬 체크포인트(unaligned)**는 백프레셔 하에서 지연을 줄이지만 복구 시 중복 발생 가능
- **세이브포인트**: 사용자 트리거, 수동 관리 스냅샷(업그레이드, 마이그레이션, 스케일링, A/B 테스트); 자동 만료 없음
- 장애 발생 시 오퍼레이터는 최신 성공 체크포인트/세이브포인트에서 복구

### 상태 TTL (State TTL)

`StateTtlConfig`로 상태 디스크립터에 수명을 부여해 무한 상태 증가 방지:

- 키 기반 상태(`Value`/`List`/`Map`/`Reducing`/`Aggregating`)에 적용
- 만료된 항목은 접근 시 지연 정리, 백엔드에 따라 컴팩션/체크포인트 중 적극 정리
- 갱신 방식(생성/쓰기 시 vs 읽기/쓰기 시), 만료됐지만 미정리 항목의 가시성, 정리 전략 설정 가능

### 쿼리 가능한 상태 (Queryable State)

일부 키/오퍼레이터 상태를 쿼리 가능한 상태 서버를 통해 외부 클라이언트에 노출해 임시 조회·디버깅에 사용. API는 발전 중이며 버전 간 변경 가능 — 운영 가시성은 지표·명시적 내보내기 권장.

### 운영 모범 사례

- 자연스러운 키가 있으면 **오퍼레이터 상태보다 키 기반 상태** 선호
- 큰 상태는 **RocksDB**, 작고 저지연 상태는 **힙**
- **최대 병렬도**는 미래 스케일링을 고려해 설정(키 그룹 수 고정)
- 장애 내성을 위해 **체크포인트 활성화**, 주기는 상태 크기와 소스 재생 비용에 맞게 조정
- **TTL**로 상태 크기 한정; 상태 크기와 체크포인트 지속시간 모니터링
- TTL·정리 없는 무한 키별 컬렉션 지양

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