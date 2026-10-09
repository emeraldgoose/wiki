---
title: Delta Lake
description: en/concepts/data-engineering/delta-lake.md 한국어 번역 요약
tags: [concept, data-engineering, delta-lake, ko]
locale: ko
---

# Delta Lake

**원문 출처**: AWS 레이크하우스 (Iceberg 비교), Databricks 모니터링 (Hydra), Databricks Lakebase Postgres

## 무엇인가

데이터 레이크에 ACID 트랜잭션을 제공하는 오픈소스 스토리지 계층. Parquet + 트랜잭션 로그 기반이다.

## 아키텍처

### 트랜잭션 로그 (DeltaLog)

- 순서 있는 원자적 커밋 (JSON + 체크포인트 Parquet)
- **낙관적 동시성 제어**: 커밋 시점에 충돌이 없음을 검증
- **체크포인팅**: 10 커밋마다 (설정 가능) → 빠른 리플레이용 Parquet

### ACID 보장

- **원자성(Atomicity)**: 전부 아니면 전무(all-or-nothing) 커밋 (단일 파일 리네임)
- **일관성(Consistency)**: 스키마 강제, 제약 검증
- **격리성(Isolation)**: 충돌 감지로 직렬화 가능(Serializable, 기본값)
- **내구성(Durability)**: 커밋을 오브젝트 스토리지에 영속화

### 타임 트래블

```sql
SELECT * FROM table VERSION AS OF 123
SELECT * FROM table TIMESTAMP AS OF '2026-08-01'
```

- 임의의 과거 버전 조회 가능 (감사, 재현성, 롤백)

### 스키마 진화

- `mergeSchema` / `overwriteSchema` 옵션
- 컬럼 추가, 타입 변경 (확장), 순서 변경
- 쓰기 시 **스키마 강제** (불량 데이터 거부)

### DML 연산

| 연산 | 동작 방식 |
|-----------|-----------|
| MERGE | 업서트 (CDC, 점진적 차원) |
| UPDATE/DELETE | 영향받는 파일 재작성 (프레디킷 푸시다운) |
| INSERT | 새 파일 추가 |

## 최적화

### 파티셔닝 + Z-오더링

```sql
-- Partition by date, Z-order by user_id
OPTIMIZE table ZORDER BY (user_id)
```

- 관련 데이터를 함께 배치 → 프레디킷 푸시다운 개선

### 파일 컴팩션

```sql
OPTIMIZE table
-- or with conditions
OPTIMIZE table WHERE date > '2026-01-01'
```

- 작은 파일들을 결합 (기본 목표 128MB)

### Vacuum (보존 기간)

```sql
VACUUM table RETAIN 168 HOURS  -- default 7 days
```

- 트랜잭션 로그에 없는 파일 제거
- **주의**: 제거된 버전의 타임 트래블이 깨짐

## Delta vs Iceberg (AWS 소스 기반)

| 기능 | Delta Lake | Apache Iceberg |
|---------|------------|----------------|
| 트랜잭션 로그 | JSON + 체크포인트 | 매니페스트 목록 + 매니페스트 파일 |
| 파티션 진화 | 제한적 | 전체 지원 (파티션 분할/병합) |
| 히든 파티셔닝 | 미지원 | 지원 (변환 기준 파티션) |
| 생태계 | Databricks, Spark, Presto | Spark, Flink, Trino, Presto, Hive |
| 타임 트래블 | 버전 + 타임스탬프 | 스냅샷 ID + 타임스탬프 |

**핵심 통찰**: 둘 다 오브젝트 스토리지 위 ACID를 제공한다. Iceberg는 파티셔닝이 더 유연하고, Delta는 Databricks/Spark 통합이 더 타이트하다.

## 대규모 성능 사례 (소스 기반)

### AWS 레이크하우스 (Razor Group)

- Delta 대신 **Iceberg 선택** 이유: 파티션 진화, 히든 파티셔닝, 엔진 중립성
- Bronze/Silver/Gold 패턴이라면 Delta도 유사하게 동작

### Databricks Hydra

- 고카디널리티 메트릭 → 레이크하우스의 Delta 테이블
- Grafana용 PromQL-to-SQL 변환
- 배포 메타데이터와 조인하는 직접 SQL 접근

### Lakebase Postgres (LTAP)

- OLTP + OLAP용 오픈 컬럼형 단일 영속 복사본
- 통합 스토리지 포맷으로 Delta/Iceberg 사용

## 관련 소스

- `sources/articles/aws-bigdata.md` (Iceberg vs Delta 선택)
- `sources/articles/databricks-engineering.md` (Delta 위 Hydra, Lakebase LTAP)

## 관련 가이드

- `guides/data-engineering/spark/optimize-shuffle.md` (Delta 쓰기 최적화)
