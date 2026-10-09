---
title: Apache Spark
description: en/concepts/data-engineering/apache-spark.md 한국어 번역 요약
tags: [concept, data-engineering, spark, ko]
locale: ko
---

# Apache Spark

**원문 출처**: 전체 문서 + 소스 아티클 (AWS 레이크하우스, Netflix Kueue 비교, Databricks 엔지니어링, Uber Hudi)

## 무엇인가

대규모 데이터를 위한 통합 배치 + 스트림 처리 엔진. 내결함성 RDD/DataFrame/Dataset API를 갖춘 메모리 기반 클러스터 컴퓨팅이다.

## 아키텍처 (상세)

### 핵심 구성 요소

- **드라이버(Driver)**: 사용자 코드를 논리 플랜 → 물리 플랜(DAG) → 태스크로 변환
- **클러스터 매니저**: YARN, Kubernetes, Standalone, Mesos — 리소스 할당
- **워커(익제큐터)**: 태스크 실행, 메모리/디스크에 데이터 캐시, 하트비트 보고
- **블록 매니저**: 캐시된 블록 관리 (메모리 + 디스크), 셔플 처리

### 실행 모델

```
User Code → Logical Plan (Catalyst) → Physical Plan (DAG) → Stages (shuffle boundaries) → Tasks
```

**지연 평가(Lazy Evaluation)**: 트랜스포메이션은 계보(lineage) 그래프를 만들고, 액션이 실행을 트리거한다.

### RDD 계보와 내결함성

- 각 RDD는 부모 RDD와 변환 함수를 추적
- 파티션 유실 → 계보에서 재계산 (결정적)
- 긴 계보는 체크포인팅으로 그래프 절단

### DAG 스케줄러

- **내로우 트랜스포메이션** (map, filter): 스테이지 내에서 파이프라이닝
- **와이드 트랜스포메이션** (셔플: groupBy, join, repartition): 스테이지 경계 생성
- **태스크 스케줄링**: 지역성 인식 (PROCESS_LOCAL → NODE_LOCAL → RACK_LOCAL → ANY)

## API

| API | 타입 안전성 | 최적화 | 사용 사례 |
|-----|-------------|--------------|----------|
| RDD | 낮음 (Java/Scala) | 수동 | 저수준 제어, 커스텀 로직 |
| DataFrame | 없음 (비타입) | Catalyst 옵티마이저 | SQL 유사, 정형 데이터 |
| Dataset | 높음 (타입) | Catalyst + 인코더 | 타입 안전, 복잡한 로직 |

**구조화 API** (DataFrame/Dataset): Catalyst 옵티마이저 (논리 → 물리), Tungsten (오프힙 메모리, 코드 생성).

## 스트리밍: Structured Streaming

- 스트림을 **무한 테이블**로 취급 (이벤트 타임 + 워터마크)
- 체크포인팅 + 멱등 싱크로 **정확히 한 번** 보장
- **이벤트 타임 처리**: 윈도우 집계, 늦은 데이터 처리
- **상태 저장 연산**: `mapGroupsWithState`, `flatMapGroupsWithState`

## 대규모 성능 사례 (소스 기반)

### AWS 레이크하우스 (Razor Group)

- 무거운 ETL용 EC2 위 Spark (Graviton + Spot)
- Bronze/Silver/Gold Iceberg 테이블
- Iceberg 메타데이터로 컬럼 프루닝 + 파티션 프루닝

### Netflix Kueue 비교

- Netflix는 배치를 Kueue (K8s 작업 큐잉)로 이전
- Kueue 워크로드로서의 Spark 작업
- 멀티테넌트용 선점/공정 공유

### Databricks 모니터링

- 50억 시계열, 하루 10조 샘플
- Pantheon (Thanos 포크)으로 메트릭 수집
- Hydra: 고카디널리티 트러블슈팅용 레이크하우스 (Delta)

### Uber Hudi + Spark

- 메타데이터 테이블의 Hudi 컬럼 통계 → 푸터 읽기 없이 파일 프루닝
- 프레디킷 컬럼 정렬 → 더 촘촘한 min/max → 프루닝 개선
- 익스포트 워크로드에서 디스크 24.8% 절감

## 핵심 최적화 (세미나 체크리스트)

### 셔플 최적화

```python
# 1. Reduce shuffle volume
df.filter(...).groupBy(...)  # filter BEFORE groupBy
spark.sql.adaptive.enabled = True  # AQE: coalesce partitions, skew join

# 2. Broadcast joins for small tables
df.join(broadcast(small_df), ...)

# 3. Shuffle partitions
spark.sql.shuffle.partitions = 200  # tune to data size (128-256MB/partition)

# 4. Shuffle service (external shuffle service for dynamic allocation)
```

### 메모리 관리

```python
# Off-heap (Tungsten)
spark.memory.offHeap.enabled = true
spark.memory.offHeap.size = 2g

# Storage vs Execution fraction
spark.memory.fraction = 0.6  # default
spark.storage.memoryFraction = 0.5  # within fraction
```

### 직렬화

```python
spark.serializer = org.apache.spark.serializer.KryoSerializer
spark.kryo.registrator = com.my.CustomKryoRegistrator
```

### 파일 포맷

- **Parquet**: 컬럼형, 프레디킷 푸시다운, 딕셔너리 인코딩
- **ORC**: 유사, Hive용 프레디킷 푸시다운이 더 우수
- **Delta/Iceberg**: ACID, 타임 트래블, 스키마 진화

## Spark 사용 시점 (대안과 비교)

| 시나리오 | Spark | Flink | Trino/Presto |
|----------|-------|-------|--------------|
| 대규모 ETL | ✅ | | |
| 스트림 처리 (정확히 한 번) | ✅ | ✅ | |
| 애드혹 SQL | | | ✅ |
| ML 파이프라인 | ✅ (MLlib) | | |
| 저지연 서빙 | | ✅ | |

## 관련 소스

- `sources/articles/aws-bigdata.md` (EC2 위 Spark 레이크하우스)
- `sources/articles/netflix-techblog.md` (Kueue 배치 오케스트레이션)
- `sources/articles/databricks-engineering.md` (모니터링, Delta Lake)
- `sources/articles/uber-engineering.md` (Hudi 컬럼 통계 + Spark)

## 관련 가이드

- `guides/data-engineering/spark/optimize-shuffle.md`
- `guides/data-engineering/spark/optimize-join.md`
