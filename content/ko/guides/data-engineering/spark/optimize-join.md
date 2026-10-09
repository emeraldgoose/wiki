---
title: Spark 조인 최적화 — 가이드 (번역)
description: en/guides/data-engineering/spark/optimize-join.md 한국어 번역 요약
tags: [guide, data-engineering, spark, join, ko]
locale: ko
---

# Spark 조인 최적화 — 실행 가이드

## 조인 유형 및 선택 기준

| 조인 유형 | 조건 | 설정 |
|----------|------|------|
| **Broadcast Hash Join** | 작은 테이블 < `spark.sql.autoBroadcastJoinThreshold` (기본 10MB) | 자동 |
| **Sort-Merge Join** | 기본값 (큰 테이블) | 정렬 필요 |
| **Shuffle Hash Join** | 작은 테이블이지만 브로드캐스트 임계값 초과 | `spark.sql.join.preferSortMergeJoin=false` |
| **Bucket Join** | 두 테이블 같은 버킷 수 + 정렬 키 | `bucketBy` + `sortBy` |

## 최적화 체크리스트

### 1. 브로드캐스트 조인 강제/확인
```python
# 강제
df.join(broadcast(small_df), "key")

# 임계값 조정
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "200m")

# 확인: Spark UI → SQL 탭 → "BroadcastHashJoin" 확인
```

### 2. 정렬-병합 조인 최적화
- 파티션 수: `spark.sql.adaptive.coalescePartitions.enabled=true`
- 스큐 처리: `spark.sql.adaptive.skewJoin.enabled=true`
- `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes=256m`
- `spark.sql.adaptive.skewJoin.skewedPartitionFactor=5`

### 3. 버킷 조인 (셔플 제거)
```python
# 테이블 생성 시
df.write.bucketBy(200, "key").sortBy("key").saveAsTable("tbl")

# 조인 시 자동으로 셔플 없이 조인
# 동일 버킷 수 + 동일 정렬 키 필수
```

### 4. 스큐 대응
- **Salted 키**: `concat(col("key"), lit("_"), (rand()*100).cast("int"))`
- **별도 처리**: 스큐 키만 분리 → 브로드캐스트 → 합치기
- AQE 자동 스큐 처리 신뢰 (Spark 3.2+)

### 5. 조인 순서 힌트
```python
# 힌트 (Spark가 자동 최적화하지만 명시 가능)
df.join(small_df.hint("broadcast"), "key")
df.join(large_df.hint("merge"), "key")
```

## 메모리 설정
```bash
spark.sql.join.sortMergeJoinOptimized.enabled=true
spark.memory.fraction=0.6
spark.memory.storageFraction=0.3
spark.executor.memoryOverhead=2g
```

## 모니터링
- Spark UI: Join 실행 계획, 셔플 읽기/쓰기, 스필
- `EXPLAIN`으로 물리 계획 확인: `*SortMergeJoin`, `*BroadcastHashJoin`
