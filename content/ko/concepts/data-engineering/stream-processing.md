---
title: 스트림 처리 (Stream Processing)
description: en/concepts/data-engineering/stream-processing.md 한국어 번역 요약
tags: [concept, data-engineering, stream-processing, ko]
locale: ko
---

# 스트림 처리 (Stream Processing)

**원문 출처**: Netflix 실시간 그래프, Twitter Sparrow, Uber 익스포트 워크로드, Databricks 모니터링, LinkedIn FishDB

## 무엇인가

무한(unbounded) 데이터 스트림에 대한 연속 계산. 이벤트 기반, 저지연, 상태 저장(stateful) 처리이다.

## 핵심 개념

### 이벤트 타임 vs 처리 타임

| 측면 | 이벤트 타임 | 처리 타임 |
|--------|------------|-----------------|
| 정의 | 이벤트 발생 시점 | 이벤트 처리 시점 |
| 정확성 | 늦은/순서 뒤바뀐 데이터 처리 | 단순, 비결정적 |
| 워터마크 | 필요 | 불필요 |

**워터마크(Watermarks)**: 단조 증가하는 타임스탬프 임계값. "T 이전의 모든 이벤트가 도착했다"는 의미. 늦은 이벤트 → 사이드 출력 또는 폐기.

### 윈도잉

| 타입 | 정의 | 사용 사례 |
|------|------------|----------|
| 텀블링(Tumbling) | 고정 크기, 비중첩 | 시간당 카운트 |
| 호핑(Hopping) | 고정 크기, 중첩 | 1분마다 5분 집계 |
| 세션(Session) | 활동 간격 기준 | 사용자 세션 |
| 글로벌(Global) | 전체 요소 | 단일 집계 |

### 상태 저장 처리

- **키드 상태(Keyed state)**: 키별 상태 (map, list, aggregating)
- **오퍼레이터 상태(Operator state)**: 오퍼레이터별 상태 (Kafka 컨슈머 오프셋)
- **체크포인팅(Checkpointing)**: 영속 스토리지에 주기적 스냅샷 (정확히 한 번 보장)

### 이벤트 타임 조인

- **인터벌 조인**: `left.ts BETWEEN right.ts - X AND right.ts + Y`
- **시간 테이블 조인**: 버전 관리 테이블과 조인 (이벤트 타임 기준 조회)

## 프레임워크 비교

| 기능 | Flink | Spark Structured Streaming | Kafka Streams |
|---------|-------|---------------------------|---------------|
| 이벤트 타임 | ✅ 네이티브 | ✅ 네이티브 | ✅ 네이티브 |
| 정확히 한 번 | ✅ | ✅ | ✅ (v2) |
| 지연시간 | ~ms | ~100ms | ~ms |
| 상태 백엔드 | RocksDB/메모리 | RocksDB/메모리 | RocksDB |
| SQL 지원 | Flink SQL | Spark SQL | ksqlDB |
| 배포 | K8s/YARN | K8s/YARN | 임베디드 |

## 소스별 패턴

### Netflix (실시간 분산 그래프)

- eBPF → Kafka → 다층 토폴로지 (네트워크, IPC, 트레이싱)
- 불변 자료구조 → 초당 수백만 레코드에서 GC 압박
- ASG 스케일 시 해시 기반 파티션 재분배
- 실시간 업데이트: 1시간 묵은 배치 대비 수십 분 단위

### Twitter (Sparrow: 배치 → 스트리밍)

- 배치 이벤트 방식에서 스트리밍 파이프라인으로 전환
- 실시간 검색, 분석, 데이터 품질

### Uber (익스포트 워크로드)

- 파일 프루닝용 Hudi 컬럼 통계 (푸터 읽기 회피)
- 더 촘촘한 min/max를 위한 프레디킷 컬럼 정렬
- 스트리밍 친화적: 증분 업데이트

### Databricks (Hydra)

- 고카디널리티 메트릭 → Delta Lake
- Grafana용 PromQL-to-SQL 변환
- 심층 분석용 직접 SQL 접근

## 세미나 수준 설계 체크리스트

1. **이벤트 타임 의미 정의** (소스 타임스탬프, 워터마크 전략)
2. **윈도잉 선택** (비즈니스 로직에 따라 텀블링/호핑/세션)
3. **상태 설계** (키드 vs 오퍼레이터, 정리를 위한 TTL)
4. **체크포인팅 간격** (복구 시간 vs 오버헤드 트레이드오프)
5. **늦은 이벤트 처리** (사이드 출력, 허용 지연)
5. **정확히 한 번 싱크** (멱등 쓰기, 트랜잭션 싱크)
6. **모니터링**: 랙(lag), 지연시간, 처리량, 백프레셔

## 관련 소스

- `sources/articles/netflix-techblog.md` (실시간 그래프)
- `sources/articles/twitter-engineering.md` (Sparrow 배치→스트림)
- `sources/articles/uber-engineering.md` (Hudi 스트리밍 친화)
- `sources/articles/databricks-engineering.md` (Hydra 고카디널리티)
- `sources/articles/linkedin-engineering.md` (FishDB 검색)

## 관련 가이드

- `guides/data-engineering/spark/optimize-shuffle.md`
- `guides/data-engineering/kafka/partitioning.md`
