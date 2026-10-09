---
title: 데이터베이스 인덱싱
description: "세미나 수준 개념: B-트리 인덱스, 복합 키, 커버링 인덱스, 쓰기 트레이드오프, 쿼리 플래닝"
tags: [concept, computer-science, database, indexing, b-tree, query-optimization, ko]
published: 2026-09-06
locale: ko
---

# 데이터베이스 인덱싱

**데이터베이스 인덱스**는 테이블 전체 스캔 없이 행을 찾게 하는 보조 자료구조다 — 쓰기 오버헤드와 저장 공간을 읽기 속도와 맞바꾼다. 인덱스 설계(어떤 컬럼을, 어떤 순서로, 어떤 종류로)는 관계형 성능 작업에서 지렛대가 가장 큰 활동이다.

## 정의

- **인덱스**: 키 값 → 행 위치(힙 튜플 포인터, 또는 InnoDB 같은 인덱스-조직 테이블에서는 PK)를 매핑하는 구조(보통 B-트리 변형). 플래너가 조회·범위 스캔·정렬·그룹화에 활용할 수 있다.
- **선택도(selectivity)**: 조건을 만족하는 행의 비율. 선택도가 높은 조건(`id = 42`)은 혜택이 막대하고, 낮은 조건(`country = 'US'`가 60%)은 어차피 스캔하는 경우가 많다.
- **클러스터드 vs 넌클러스터드**: 클러스터드 인덱스는 물리적 행 순서를 정한다(테이블당 하나 — InnoDB의 PK). 넌클러스터드(세컨더리) 인덱스는 행을 가리키며 추가 홉(**북마크 룩업**)이 필요하다.
- **풀 테이블 스캔**: 모든 페이지를 읽는다. 올바른 폴백이며, 결과 비율이 크면 인덱스 탐색보다 진짜로 빠르다 — 본질적 악이 아니다.

## 왜 중요한가

- **상수 개선이 아니라 복잡도 변화**: 인덱스는 O(n) 스캔을 O(log n) 조회로 바꾼다. 1억 행 테이블에서 밀리초와 수 분의 차이다.
- **실전 장애의 지배적 원인**: 없거나 잘못된 인덱스는 하드웨어·설정·쿼리 스타일을 합친 것보다 많은 실제 DB 장애를 일으킨다.
- **쓰기/읽기 트레이드오프의 명시화**: 모든 인덱스는 INSERT/UPDATE/DELETE에 세금(트리 유지, WAL 기록, 복제)을 매긴다. 인덱싱은 예산 짜기이지 공짜 속도가 아니다.
- **플래너 가독성**: 플래너가 무엇을 쓰고 못 쓰는지(sargability, leftmost prefix, 암시적 캐스트)를 아는 것이 찍기와 엔지니어링을 가른다.

## 동작 원리

### B-트리 구조

```
            [20 | 50]
           /    |    \
   [5|10|15] [30|40] [60|70|80]
   (리프 페이지는 범위 스캔용 이중 연결, 각 리프가 행을 가리킴)
```

- 균형 트리이며 분기가 수백(8 KB 페이지, 작은 키)이라 수십억 행도 깊이 2–4다. 깊이 = 점 조회당 최악 페이지 읽기 횟수다.
- **범위 스캔**은 리프 연결 리스트를 순회하고, 인덱스 순서와 맞으면 **정렬**(`ORDER BY`)이 공짜로 오며, **접두어 압축**이 반복 키를 줄인다.
- 변형: B+트리(값은 리프에만 — DB가 실제로 쓰는 것), LSM-트리(쓰기 버퍼링 후 병합 압축 — Cassandra, RocksDB, Bigtable 계열 스토리지 엔진), 해시 인덱스(동등 비교 전용, 범위 불가), GiST/GIN(PostgreSQL의 전문 검색·배열·기하), 비트맵(낮은 카디널리티 분석용).

### 복합 인덱스와 Leftmost Prefix

```sql
CREATE INDEX idx_orders ON orders (customer_id, order_date);
-- 가능:  WHERE customer_id = ? AND order_date BETWEEN ? AND ?
-- 가능:  WHERE customer_id = ?
-- 불가:  WHERE order_date = ?   (선행 컬럼 부재)
```

- 컬럼 순서는 **동등 먼저, 범위 마지막**: 동등 컬럼은 순서 무관, 범위 컬럼은 인덱스 사용당 최대 하나. 보통 선택도 높은 순이 휴리스틱이지만 범위-컬럼-마지막 규칙이 우선한다.
- **커버링 인덱스**: 쿼리가 필요로 하는 모든 컬럼 포함 → 엔진이 인덱스만으로 답한다(**index-only scan**, `EXPLAIN`에 표시). 키를 넓히지 않고 커버리지를 넓히려고 `INCLUDE` 컬럼(PostgreSQL, SQL Server)을 쓴다.
- **부분 인덱스**(`WHERE active`): 쿼리들이 조건을 공유하면 더 작고 빠르고 유지가 싸다. **표현식 인덱스**(`lower(email)`)는 일반 컬럼 인덱스가 못 받는 함수 호출을 받는다.

### 플래너와 EXPLAIN

- 비용 기반 플래너는 테이블 통계(`ANALYZE`, auto-vacuum 통계)로 접근 경로(순차 스캔, 인덱스 스캔, 비트맵 힙 스캔, nested loop/hash/merge 조인)별 행 수 × 비용을 추정한다. 오래된 통계 → 잘못된 플랜이다.
- `EXPLAIN (ANALYZE, BUFFERS)` 읽기: 실제 vs 추정 행 수(10배 이상 어긋나면 오래된 통계나 상관 조건 의심), buffers hit vs read(캐시 적중도), index-only scan 성립 여부를 본다.
- **Sargability**: `WHERE created_at > now() - interval '7 days'`는 인덱스를 타지만, `WHERE date_trunc('day', created_at) = ...`이나 타입이 어긋난 `WHERE phone::text LIKE '%42'`는 대체로 못 탄다(함수/타입 장벽 — 표현식 인덱스나 조건 수정으로 해결).

### 쓰기 측 비용

- INSERT마다 모든 인덱스를 갱신한다(비순차 키는 랜덤 리프 쓰기 — UUIDv4 PK가 InnoDB 클러스터를 조각내는 반면 자동 증가 키는 깔끔히 append되는 이유).
- 인덱스드 컬럼의 UPDATE = 해당 인덱스에서 삭제 + 삽입. PostgreSQL의 HOT(heap-only tuple) 갱신은 인덱스드 컬럼이 안 바뀔 때만 인덱스 churn을 피한다.
- 인덱스 블로트(vacuum 사이 죽은 엔트리)와 단편화(페이지 분할)는 `VACUUM`/`REINDEX`(Postgres)나 온라인 `OPTIMIZE`(MySQL)로 관리한다.

## 흔한 함정

1. **"안전하게" 모든 컬럼에 인덱스**: 쓰기 처리량이 무너지고 복제가 밀리며(인덱스 변경마다 WAL 기록·재생) 플래너가 겹치는 선택지에 헷갈린다. 불안이 아니라 증거(`pg_stat_statements`, 슬로 로그)에서 인덱싱하라.
2. **잘못된 복합 순서**: 한 고객의 날짜 범위 조회에 `(order_date, customer_id)`는 `(customer_id, order_date)`보다 훨씬 많이 스캔한다. 동등 먼저, 범위 마지막.
3. **암시적 타입 캐스트의 인덱스 무력화**: `text` 컬럼에 `WHERE phone = 123`(또는 collation 불일치)은 스캔을 강제한다. 타입을 정확히 맞춘다.
4. **낮은 선택도 단일 컬럼 인덱스**: `gender`, `is_deleted` 인덱스는 단독으로 거의 안 쓰이면서 쓰기 세금은 꼬박 낸다. 부분 인덱스나 선택적 컬럼과 묶은 복합 인덱스를 쓴다.
5. **N+1을 인덱스로 "해결"**: 인덱스는 1000번 점 조회를 파국에서 준-빠름으로 바꿀 뿐, JOIN/배치 한 방이 여전히 100–1000배 낫다. 접근 패턴을 먼저 고친다.
6. **스키마 변경 후 EXPLAIN 미확인**: 통계·플래너 동작·데이터 분포는 drift한다. 인덱스드 컬럼을 건드리는 마이그레이션마다 상위 쿼리에 `EXPLAIN (ANALYZE, BUFFERS)`.
7. **대규모 클러스터드 PK로 UUIDv4**: 랜덤 삽입 위치 → 페이지 분할·단편화·캐시 비친화 쓰기(InnoDB). 자동 증가/순차 키, 불투명 ID가 필요하면 시간 순 UUIDv7을 쓴다.

## 관련 개념

- [[concepts/computer-science/database-transactions|데이터베이스 트랜잭션]] (락 vs MVCC, 격리와의 상호작용)
- [[concepts/computer-science/caching|캐싱]] (캐시로서의 버퍼 풀, 메모리를 놓고 경쟁하는 인덱스 페이지)

## 참고 문헌

- Garcia-Molina, Ullman, Widom — *Database Systems: The Complete Book* (13–14장: 인덱싱, 쿼리 처리)
- PostgreSQL docs — "Indexes" + "Using EXPLAIN" (플래너 권위 레퍼런스)
- MySQL docs — "Optimization and Indexes" (InnoDB 클러스터드 인덱스 동작)
- Use The Index, Luke (use-the-index-luke.com) — sargability·복합 설계 실전 가이드
