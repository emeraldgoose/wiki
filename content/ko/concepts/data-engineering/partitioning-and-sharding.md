---
title: "Partitioning and Sharding"
description: "파티션 프루닝, 버킷팅 전략, 편중 처리, Spark/Iceberg/BigQuery의 파티셔닝 전략, 예시와 함정"
tags: [concept, data-engineering, partitioning, sharding, scalability]
locale: ko
published: 2026-09-07
---

# Partitioning and Sharding (파티셔닝과 샤딩)

## 정의
대규모 데이터 셋에서 쿼리 성능과 스토리지 효율성을 개선하기 위해 데이터를 물리적으로 또는 논리적으로 나누는 기술입니다.

## 왜 중요한가
- **조회 성능**: 파티션 프루닝(Partition Pruning)으로 스캔 데이터 양 90% 이상 절감
- **스토리지 비용**: hot data만 고성능 스토리지에, cold data는 저렴한 스토리지에
- **병렬 처리**: 여러 노드에 workload 분산하여 처리량 증가

## 파티셔닝 (Partitioning)
데이터를 논리적 단위로 나누어 같은 파일에 저장하는 기술입니다.

### 주요 전략
- **Range Partitioning**: 값의 범위 기반 (예: `order_date >= '2024-01-01' AND order_date < '2024-04-01'`)
  - 장점: 시간 시리즈 데이터에 최적, 프루닝 용이
  - 단점: 범위 바깥 데이터는 새로운 파티션 필요
- **List Partitioning**: 특정 값의 목록 기반 (예: `region IN ('US', 'EU', 'APAC')`)
  - 장점: 균등한 데이터 분산, 명확한 카테고리
  - 단점: 새로운 카테고리 추가 시 스키마 변경 필요
- **Hash Partitioning**: 해시 함수 기반 (예: `hash(user_id) % 10`)
  - 장점: 균등 분산, 핫스팟 방지
  - 단점: 특정 키에 대한 쿼리는 특정 파티션만 사용 불가

### Apache Iceberg 예시
```sql
-- 파티션이 있는 테이블 생성
CREATE TABLE sales (
  order_id BIGINT,
  order_date DATE,
  customer_id BIGINT,
  amount DECIMAL(10,2)
)
PARTITION BY (order_date);

-- 파티션 프루닝으로 빠른 조회
SELECT * FROM sales
WHERE order_date = '2024-09-01'; -- 불필요한 파티션 스캔 생략
```

### Apache Hive / Spark 예시
```sql
-- Hive 파티션된 테이블 쿼리
SELECT * FROM sales
PARTITION (date '2024-09-01')
WHERE amount > 1000;
```

## 샤딩 (Sharding)
데이터를 여러 노드 또는 서버에 분산 저장하는 기술입니다.

### 샤딩 전략
- **키 기반 샤딩**: 해시나 범위 키를 기반으로 샤드 결정
  - 장점: predictable한 데이터 분배
  - 단점: 샤드 키 선택에 따라 핫스팟 발생 가능
- **지리적 샤딩**: 사용자 위치 기반 샤드 배분
  - 장점: 지연 시간 최소화, 지역 comply
  - 단점: cross-shard 쿼리는 비용이 비쌈
- **소프트 샤딩**: 리디렉션 테이블을 통한 유연한 샤드 매핑
  - 장점: 샤드 재구성 시 minimal downtime
  - 단점: 추가 조회 overhead

### 예시: 키 기반 샤딩 (6 샤드)
```python
def get_shard(user_id: int, num_shards: int = 6) -> int:
    return hash(user_id) % num_shards

# 사용 예시
shard = get_shard(12345)  # -> 3 (4번째 샤드에 저장)
```

## 파티션 프루닝 (Partition Pruning)
쿼리 optimizer가 불필요한 파티션을 자동으로 건너뛰는 기술입니다.

### 조건
- 파티션 컬럼에 등치 비교(`=`) 또는 범위 비교(`BETWEEN`, `>`, `<`)가 있어야 함
- 통계가 수집되어 있어야 optimizer가 효과적으로 판단 가능

### 효과
- **Snowflake/BigQuery**: 자동 파티션 프루닝, 스캔 바이트 수 자동 감소
- **Spark/Iceberg**: `WHERE` 절에 파티션 컬럼이 포함되면 미스캔 방지
- **예상 효과**: 10TB 데이터 셋에서 월간 보고서 쿼리 시 1TB 이하로 스캔 감소 (90% 이상 절감)

## 흔한 함정
- **잘못된 파티션 컬럼 선택**: 쿼리 패턴과 무관한 컬럼으로 파티션 Then poor pruning
- **너무 많은 파티션**: 메타데이터 오버헤드로 인해 오히려 성능 저하
- **데이터 불균형( skew)**: 특정 파티션에 데이터가 몰려 성능 불균형
- **점진적 파티션 추가 누락**: 새 데이터 범위에 대해 ALTER TABLE로 파티션 추가 잊어버림

## 예방 가이드라인
1. **쿼리 패턴 분석**: 가장 빈번한 필터 조건을 기준으로 파티션 컬럼 결정
2. **적정 파티션 수**: 100~1000개 범위 권장 (데이터 양에 따라 다름)
3. **정기적 통계 수집**: `ANALYZE TABLE` 또는 자동 통계 수집 설정
4. **스케우 모니터링**: 파티션별 데이터 분산도 점검 및 재균형
5. **점진적 추가**: `ALTER TABLE ... ADD PARTITION`으로 새 데이터 범위 점진적 추가

## 참조
- "Designing Data-Intensive Applications" — Martin Kleppmann, Chapter 11
- Apache Iceberg 공식 문서: partitioning and partition evolution
- "Seven Databases in Seven Weeks" — Eric Redmond and Jim Wilson
- Cloud provider 가이드: BigQuery partitioning, DynamoDB partitioning
