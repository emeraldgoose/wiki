---
title: Apache Kafka
description: en/concepts/data-engineering/apache-kafka.md 한국어 번역 요약
tags: [concept, data-engineering, kafka, ko]
locale: ko
---

# Apache Kafka

**원문 출처**: 소스 아티클 (Uber Kafka 최적화, Netflix 스트림 처리, Twitter Sparrow 전환, LinkedIn FishDB)

## 무엇인가

분산 이벤트 스트리밍 플랫폼: 발행/구독(pub/sub), 저장, 처리를 담당한다. 로그 구조(log-structured), 파티션 분할, 복제된 커밋 로그(replicated commit log) 방식이다.

## 아키텍처

### 핵심 구성 요소

- **토픽(Topic)**: 카테고리/피드 이름. 파티션으로 나뉘며 순서가 보장됨
- **파티션(Partition)**: 레코드의 순서 있는 불변 시퀀스 (오프셋으로 식별)
- **브로커(Broker)**: 파티션을 저장하는 서버. 리더/팔로워 복제 구조
- **컨슈머 그룹(Consumer Group)**: 병렬 컨슈머 집합. 그룹 내에서 각 파티션 → 하나의 컨슈머에 할당

### 복제

- **ISR (In-Sync Replicas)**: 리더를 따라잡은 동기화된 팔로워 집합
- **acks=all**: ISR 전체의 확인 응답을 기다림 (내구성 보장)
- **min.insync.replicas**: 쓰기 허용에 필요한 최소 ISR 수

### 프로듀서

- **배칭(Batching)**: `linger.ms`, `batch.size`
- **압축(Compression)**: `snappy`, `lz4`, `zstd` (처리량/압축률 균형은 lz4가 최상)
- **멱등성(Idempotence)**: `enable.idempotence=true` + `acks=all` → 파티션당 정확히 한 번(exactly-once) 전달
- **트랜잭션(Transactions)**: 다중 파티션에 대한 원자적 쓰기

### 컨슈머

- **폴 루프(Poll loop)**: `poll(Duration)` → 레코드 수신 → 처리 → 오프셋 커밋
- **오프셋 관리**: 자동 커밋 (유실/중복 위험) vs 수동 커밋 (트랜잭션과 함께 exactly-once 달성)
- **리밸런싱(Rebalancing)**: 협력적 스티키 할당자(cooperative sticky assignor)로 중단 최소화

## 스트림 처리 (Kafka Streams / ksqlDB)

- **토폴로지(Topology)**: 소스(Source) → 변환(Transform) → 싱크(Sink)
- **상태 저장 연산**: 집계, 조인, 윈도잉 (텀블링, 호핑, 세션)
- **상태 저장소(State stores)**: RocksDB 기반 + 변경로그 토픽(changelog topic)으로 장애 복원
- **정확히 한 번 처리**: `processing.guarantee=exactly_once_v2`

## 대규모 성능 사례 (소스 기반)

### Uber (비용 효율적 익스포트)

- Hudi 컬럼 통계 + 정렬로 프레디킷 프루닝(predicate pruning)
- Hudi 테이블의 인제스천 계층으로 Kafka 사용

### Netflix (실시간 분산 그래프)

- eBPF 플로우 로그 → Kafka → 토폴로지 계층
- 초당 수백만 레코드. 불변 자료구조 → GC 압박
- ASG 변경 시 해시 기반 파티션 재분배

### Twitter (Sparrow: 배치 → 스트리밍)

- Sparrow 프로젝트: 배치 이벤트 방식 → 스트리밍 아키텍처
- 검색, 분석용 실시간 파이프라인

### LinkedIn (FishDB 검색)

- 실시간 업데이트를 Kafka로 뒷받침하는 피드 검색 엔진

## 핵심 최적화 (세미나 체크리스트)

### 처리량

```properties
# Producer
linger.ms=5
batch.size=65536
compression.type=lz4
buffer.memory=67108864

# Broker
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
```

### 지연시간

```properties
# Consumer
fetch.min.bytes=1
fetch.max.wait.ms=500
max.poll.records=500
```

### 스토리지

```properties
# Log retention
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Compaction for keyed topics
cleanup.policy=compact
min.cleanable.dirty.ratio=0.5
```

## Kafka 사용 시점 (대안과 비교)

| 시나리오 | Kafka | Pulsar | RabbitMQ | Kinesis |
|----------|-------|--------|----------|---------|
| 고처리량 이벤트 로그 | ✅ | ✅ | | |
| 멀티테넌트, 지리적 복제 | | ✅ | | |
| 복잡한 라우팅, 저지연 | | | ✅ | |
| AWS 관리형, 서버리스 | | | | ✅ |
| 정확히 한 번, 상태 저장 처리 | ✅ | ✅ | | |

## 관련 소스

- `sources/articles/uber-engineering.md` (Hudi 인제스천용 Kafka)
- `sources/articles/netflix-techblog.md` (실시간 그래프, eBPF → Kafka)
- `sources/articles/twitter-engineering.md` (Sparrow 배치→스트림)
- `sources/articles/linkedin-engineering.md` (FishDB 검색)

## 관련 가이드

- `guides/data-engineering/kafka/partitioning.md`
