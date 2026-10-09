---
title: Spark 셔플 최적화 — 가이드 (번역)
description: en/guides/data-engineering/spark/optimize-shuffle.md 한국어 번역 요약
tags: [guide, data-engineering, spark, shuffle, ko]
locale: ko
---

# Spark 셔플 최적화 — 실행 가이드

## 핵심 설정
```bash
spark.sql.adaptive.enabled=true
spark.sql.adaptive.coalescePartitions.enabled=true
spark.sql.adaptive.skewJoin.enabled=true
spark.shuffle.manager=sort
spark.shuffle.service.enabled=true
spark.dynamicAllocation.enabled=true
```

## 파티션 전략
- **목표**: 128-256MB/파티션, 코어 2-3× 태스크
- `spark.sql.shuffle.partitions` 동적 조정 (AQE가 자동 처리)
- `spark.sql.adaptive.advisoryPartitionSizeInBytes=128MB`

## 메모리/직렬화
- `spark.serializer=KryoSerializer`
- `spark.kryoserializer.buffer.max=512m`
- `spark.memory.offHeap.enabled=true`
- `spark.memory.offHeap.size=2g`

## 스큐 처리
- AQE 자동 스큐 조인 처리 (`spark.sql.adaptive.skewJoin.enabled=true`)
- 수동: `skewJoinHint` + 솔팅된 파티션 재분배
- 솔팅된 테이블: `bucketBy` + `sortBy` (버킷 조인 → 셔플 제거)

## 컬럼 프루닝 + 압축
- `spark.sql.parquet.columnarReaderBatchSize=4096`
- `spark.sql.parquet.enableVectorizedReader=true`
- `spark.shuffle.compress=true`, `spark.shuffle.spill.compress=true`
- 압축 코덱: `lz4` (속도) 또는 `zstd` (압축률)

## 모니터링
- Spark UI: Shuffle Read/Write, Spill (Memory/Disk), Skew 태스크
- `spark.sql.adaptive.logLevel=DEBUG`로 AQE 로그 확인
