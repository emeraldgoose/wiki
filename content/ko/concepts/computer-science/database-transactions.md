---
title: 데이터베이스 트랜잭션
description: "세미나 수준 개념: ACID, 격리 수준, MVCC, 락, 교착상태, write-ahead 로깅"
tags: [concept, computer-science, database, transactions, acid, mvcc, isolation, ko]
published: 2026-09-06
locale: ko
---

# 데이터베이스 트랜잭션

**트랜잭션**은 여러 읽기와 쓰기를 하나의 원자적 단위로 묶는다. 전부 커밋되거나 전부 안 되며, 동시 트랜잭션 간의 가시성 규칙이 명확하다. ACID, 격리 수준, write-ahead 로깅은 공유 가변 상태를 신뢰할 수 있게 만드는 기계 장치다.

## 정의

- **트랜잭션**: **ACID**를 만족하는 연산 시퀀스 — 원자성(전부 아니면 전무), 일관성(전후에 불변식 유지), 격리성(동시 트랜잭션이 서로의 중간 작업을 보지 않음), 지속성(커밋된 작업은 크래시 후에도 생존).
- **격리 수준**: 트랜잭션이 감내하는 동시 간섭의 정도. 약할수록 빠르고 강할수록 이상 현상이 적다. SQL 표준 수준: Read Uncommitted, Read Committed, Repeatable Read, Serializable.
- **MVCC**(다중 버전 동시성 제어): 쓰기를 기다리며 막히는 대신 버전화된 스냅샷을 읽는다(PostgreSQL, InnoDB, CockroachDB). 대안은 락 기반 동시성(고전 2PL).
- **WAL**(Write-Ahead Log): 모든 변경을 적용 전에 durable하게 먼저 기록한다 — 크래시 복구와 복제의 기반이다.

## 왜 중요한가

- **동시성 하의 정확성**: 계좌 이체, 재고 차감, 좌석 예약은 트랜잭션 없이 전부 read-modify-write 레이스다. 격리 수준이 어떤 레이스를 막고 어떤 비용을 치를지 정한다.
- **복구 스토리**: WAL + 체크포인트를 통한 지속성이 "커밋은 커밋이다"를 정전 너머로 약속한다. 백업과 시점 복구는 WAL 재생이다.
- **분산 시스템의 병목**: 단일 노드 트랜잭션은 해결됐고, 분산 트랜잭션(2PC, saga 보상)이 지연·가용성·복잡성을 맞바꾼다 — 마이크로서비스 데이터 설계의 어려운 부분이다.
- **성능 튜닝 표면**: 락 경합, 직렬화 실패, 오래된 스냅샷의 vacuum/블로트는 대표적 실전 이슈이며 모두 트랜잭션 동작에 뿌리를 둔다.

## 동작 원리

### ACID, 구체적으로

```
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;   -- 둘 다 함께 보이거나 (ROLLBACK/크래시 시) 둘 다 없음
```

- **원자성**: 커밋하면 모든 쓰기가 한 번에 보이고, 중단하면 전부 버린다. 미커밋 버전/잠정 쓰기를 쥐고 있다가 롤백 시 폐기하는 식으로 구현한다.
- **일관성**: 제약(FK, CHECK, UNIQUE)을 문장 또는 커밋 시점에 검사(지연 가능 제약). 커밋된 트랜잭션이 이를 어기지 않음을 DB가 보장한다.
- **격리성**: 아래 수준들 — 이상 현상과 처리량의 다이얼이다.
- **지속성**: WAL 레코드가 durable 저장소에 닿은 뒤에야 커밋을 반환한다(`synchronous_commit`, `innodb_flush_log_at_trx_commit`, `fsync`). 완화하면(async commit) 문서화된 크래시-손실 구간을 대가로 처리량을 산다.

### 격리 수준과 이상 현상

| 수준 | Dirty read | Non-repeatable read | Phantom | Lost update* |
|---|---|---|---|---|
| Read Uncommitted | 가능 | 가능 | 가능 | 가능 |
| Read Committed | 방지 | 가능 | 가능 | 가능 |
| Repeatable Read | 방지 | 방지 | 가능† | 방지† |
| Serializable | 방지 | 방지 | 방지 | 방지 |

\* lost update 방지는 해당 수준의 스냅샷/선점 메커니즘이 쓰기-쓰기 경합을 커버한다는 가정이다(Postgres RR은 abort, MySQL RR은 락).
† PostgreSQL의 Repeatable Read는 스냅샷에 새 행이 안 보여 팬텀처럼 보이지만, 진짜 직렬성은 `SERIALIZABLE`(SSI — 직렬 가능 스냅샷 격리, 위험 패턴에서 abort)이 필요하다.

- **Dirty read**: 롤백될 수 있는 미커밋 데이터 읽기. Read Uncommitted(대충 보는 분석용으로 가끔)에서만 허용된다.
- **Non-repeatable read**: 한 트랜잭션의 두 읽기가 다른 값을 반환(사이에 동시 커밋 착지). Read Committed(Postgres/MySQL 기본값)는 허용한다.
- **Phantom**: 범위 쿼리 재실행에 새 행이 등장. 집계와 제약성 검사("겹치는 예약 없음")에 중요하다.
- **Write skew**(팬텀 너머의 고전): 당직 의사 둘이 "≥1명"을 보고 서로를 빼버린다 — RR에서 둘 다 커밋되고 불변식이 깨진다. Serializable이나 명시적 락(`SELECT ... FOR UPDATE`)이 필요하다.
- **실전 규칙**: 기본 Read Committed + 경합 행에 `SELECT ... FOR UPDATE`, 특정 트랜잭션만 Serializable로 올리고 직렬화-실패 재시도 루프를 짠다.

### MVCC 한눈에 (PostgreSQL식)

- 각 행 버전이 `xmin`(생성 txn)/`xmax`(삭제/잠금 txn)를 달고 있다. 문장은 스냅샷 이전에 커밋된 버전만 본다.
- 쓰기가 읽기를 막지 않고 읽기가 쓰기를 막지 않는다. 같은 행의 쓰기끼리는 막는다(두 번째 갱신자는 대기 후 재평가 또는 충돌 에러).
- 어떤 스냅샷도 안 쓰는 구 버전이 쌓이면 `VACUUM`이 회수한다(그래서 긴 트랜잭션이 `xmin`을 붙잡으면 블로트). 인덱스 엔트리는 버전을 가리키고, HOT 갱신은 인덱스드 컬럼이 안 바뀌면 새 인덱스 엔트리를 피한다.
- InnoDB는 mechanics가 다르지만(undo 로그로 스냅샷 구성, 클러스터드 인덱스) 계약의 모양은 같다.

### 락, 교착상태, 2PC

- **행 락**(`FOR UPDATE`), **조건/갭 락**(InnoDB gap/next-key 락은 RR에서 팬텀을 막는 대신 더 넓게 막는다), **테이블/어드바이저리 락**(명시적 조율: `pg_advisory_lock`으로 rate limiting, 리더 선출, 멱등 잡).
- **교착상태**: T1이 A를 쥐고 B를 기다리고 T2가 B를 쥐고 A를 기다림 → 엔진이 사이클을 감지(deadlock_timeout/innodb_deadlock_detect)하고 희생자를 abort(재시도 가능한 에러). 예방: 일관된 락 순서, 최단 트랜잭션, 최소 충분 격리.
- **분산 커밋(2PC)**: 모든 참가자에 prepare 후 commit/abort. 정확하지만 블로킹 — 코디네이터 장애가 락을 쥔 참가자를 멈춘다. 현대 대안: **saga**(단계별 보상 액션, 최종 일관성)와 2PC를 피하는 single-writer/transactional-outbox 패턴.

### WAL, 체크포인트, 복구

```
클라이언트 COMMIT → WAL 플러시 (durable) → ACK 반환 → (나중에) 더티 페이지 체크포인트
크래시 → 마지막 체크포인트부터 WAL 재생 → 커밋분 복원, 미완분 폐기
```

- 체크포인트가 복구 시간을 묶어두고, WAL 아카이빙 + 베이스 백업이 시점 복구를, WAL 레코드 스트리밍이 스탠바이 복제를 만든다.

## 흔한 함정

1. **Repeatable Read = Serializable 착각**: write skew는 모든 주요 엔진의 RR을 통과한다. 감사성 불변식("잔고는 음수 불가", "중복 예약 금지")은 Serializable이나 명시적 락이 필요하다.
2. **직렬화/교착 에러 재시도 루프 부재**: Postgres `40001`, MySQL `1213/1205`는 경합 하의 *예상된* 제어 흐름이다. 모든 트랜잭션 경로에 유한 재시도 + 백오프가 필요 — 치명 에러 취급 코드는 실전에서 flake한다.
3. **긴 트랜잭션**: idle-in-transaction 세션이 스냅샷을 붙잡고(블로트, vacuum 정체) 락을 쥔다. `idle_in_transaction_session_timeout` 설정, 신속 커밋, 트랜잭션 안에서 사용자 입력 대기는 절대 금지.
4. **락 없는 SELECT-후-UPDATE**: Read Committed에서 검사-후-행동 레이스(잔액 확인 → 출금)는 이중 지출한다. 행을 먼저 잠그거나(`FOR UPDATE`) 조건부 갱신(`UPDATE ... WHERE balance >= 100` + 영향 행 수 확인)으로 만든다.
5. **마이크로서비스 간 2PC**: 코디네이터 장애 모드, 지연 결합, 네트워크 호출 너머 락 점유. transactional outbox + 컨슈머 멱등, 또는 보상을 곁들인 saga를 선호한다.
6. **손실 구간을 모르는 비동기 커밋**: `synchronous_commit = off`/`innodb_flush_log_at_trx_commit = 2`는 크래시 시 약 1초의 "커밋분"을 잃을 수 있다. 분석 수집엔 괜찮고 결제엔 불가 — 워크로드별로 명시적 선택.
7. **락 모니터링 무시**: `pg_locks` + `pg_stat_activity`, `performance_schema`/`SHOW ENGINE INNODB STATUS`가 경합 진단용으로 존재한다. 슬로 쿼리가 아니라 락 대기에 알람을 건다.

## 관련 개념

- [[concepts/computer-science/database-indexing|데이터베이스 인덱싱]] (인덱스 범위의 갭 락, 인덱스-온리 스냅샷)
- [[concepts/computer-science/processes-and-threads|프로세스와 스레드]] (교착상태 이론, 락 순서 — 같은 Coffman 조건)

## 참고 문헌

- Garcia-Molina, Ullman, Widom — *Database Systems: The Complete Book* (17–19장: 트랜잭션, 동시성, 복구)
- Bernstein, Hadzilacos, Goodman — *Concurrency Control and Recovery in Database Systems* (무료 PDF, 형식적 레퍼런스)
- PostgreSQL docs — "Transaction Isolation", "MVCC", "WAL"; MySQL docs — "InnoDB Locking and Transaction Model"
- Gray & Reuter — *Transaction Processing* (2PC, TP 모니터, 고전 실무)
