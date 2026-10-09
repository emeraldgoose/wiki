---
title: Database Transactions
description: "Seminar-level concept: ACID, isolation levels, MVCC, locking, deadlocks, write-ahead logging"
tags: [concept, computer-science, database, transactions, acid, mvcc, isolation]
published: 2026-09-06
locale: en
---

# Database Transactions

> [한국어 버전](/ko/concepts/computer-science/database-transactions)

A **transaction** bundles multiple reads and writes into a single atomic unit: either all effects commit or none do, with well-defined visibility rules for concurrent transactions. ACID, isolation levels, and write-ahead logging are the machinery that makes shared mutable state trustworthy.

## Definition

- **Transaction**: a sequence of operations satisfying **ACID** — Atomicity (all-or-nothing), Consistency (invariants hold before and after), Isolation (concurrent transactions don't observe each other's partial work), Durability (committed work survives crashes).
- **Isolation level**: how much concurrent interference a transaction tolerates. Weaker = faster, stronger = fewer anomalies. SQL standard levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable.
- **MVCC** (Multi-Version Concurrency Control): readers see versioned snapshots instead of blocking on writers (PostgreSQL, InnoDB, CockroachDB). The alternative is lock-based concurrency (classic 2PL).
- **WAL** (Write-Ahead Log): every change is logged durably before being applied — the basis of crash recovery and replication.

## Why It Matters

- **Correctness under concurrency**: bank transfers, inventory decrements, and seat reservations are all read-modify-write races without transactions. The isolation level decides which races are prevented and at what cost.
- **Recovery story**: durability via WAL + checkpoints is what lets a database promise "committed means committed" across power loss. Backup and point-in-time recovery are WAL replay.
- **Distributed systems bottleneck**: single-node transactions are solved; distributed transactions (2PC, saga compensation) trade latency, availability, and complexity — the hard part of microservice data design.
- **Performance tuning surface**: lock contention, serialization failures, and vacuum/bloat from old snapshots are top production issues, all rooted in transaction behavior.

## How It Works

### ACID, Concretely

```
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;   -- both visible together, or (on ROLLBACK / crash) neither
```

- **Atomicity**: commit makes all writes visible at once; abort discards all. Implemented by holding uncommitted versions/tentative writes and dropping them on rollback.
- **Consistency**: constraints (FK, CHECK, UNIQUE) are checked at statement or commit time (deferrable constraints). The DB guarantees no committed transaction violates them.
- **Isolation**: see levels below — the dial between anomalies and throughput.
- **Durability**: commit returns only after the WAL record reaches durable storage (`synchronous_commit`, `innodb_flush_log_at_trx_commit`, `fsync`). Relaxing this (async commit) buys throughput with a documented crash-loss window.

### Isolation Levels and Anomalies

| Level | Dirty read | Non-repeatable read | Phantom | Lost update* |
|---|---|---|---|---|
| Read Uncommitted | possible | possible | possible | possible |
| Read Committed | prevented | possible | possible | possible |
| Repeatable Read | prevented | prevented | possible† | prevented† |
| Serializable | prevented | prevented | prevented | prevented |

\* Lost update prevention assumes the level's snapshot/claim mechanism covers the write-write case (Postgres RR aborts; MySQL RR locks).
† PostgreSQL's Repeatable Read prevents phantoms for the snapshot (no new rows visible) but true serializability needs `SERIALIZABLE` (SSI — serializable snapshot isolation, aborts on dangerous patterns).

- **Dirty read**: reading uncommitted data that may roll back. Prevented everywhere except Read Uncommitted (rarely used; mainly for non-blocking rough analytics).
- **Non-repeatable read**: two reads in one transaction return different values (a concurrent commit landed between). Read Committed (Postgres/MySQL default) allows it.
- **Phantom**: a re-executed range query returns new rows. Matters for aggregates and constraint-like checks ("no overlapping bookings").
- **Write skew** (the classic beyond-phantoms case): two doctors both see "≥1 on call", each takes the other off — both commits valid under RR, invariant broken. Needs Serializable or explicit locking (`SELECT ... FOR UPDATE`).
- **Practical rule**: default to Read Committed + targeted `SELECT ... FOR UPDATE` on contested rows; escalate specific transactions to Serializable and code retry-on-serialization-failure loops.

### MVCC in a Nutshell (PostgreSQL Flavor)

- Each row version carries `xmin` (creating txn) / `xmax` (deleting/locking txn). A statement sees versions committed before its snapshot.
- Writers never block readers; readers never block writers. Writers block writers on the same row (second updater waits, then re-evaluates or errors on conflict).
- Old versions accumulate until no snapshot needs them → `VACUUM` reclaims (hence bloat when long transactions pin `xmin`). Index entries point at versions; HOT updates avoid new index entries when indexed columns are untouched.
- InnoDB differs in mechanics (undo-log-built snapshots, clustered index) but honors the same contract shape.

### Locking, Deadlocks, 2PC

- **Row locks** (`FOR UPDATE`), **predicate/gap locks** (InnoDB gap/next-key locks prevent phantoms under RR at the cost of wider blocking), **table/ advisory locks** (explicit coordination: `pg_advisory_lock` for rate limiting, leader election, idempotent jobs).
- **Deadlock**: T1 holds A waits B, T2 holds B waits A → the engine detects the cycle (deadlock_timeout / innodb_deadlock_detect) and aborts a victim with a retryable error. Prevention: consistent lock order, shortest transactions, lowest sufficient isolation.
- **Distributed commit (2PC)**: prepare on all participants, then commit/abort. Correct but blocking — coordinator failure stalls participants holding locks. Modern alternatives: **sagas** (compensating actions per step, eventual consistency) and single-writer/transactional-outbox patterns that avoid 2PC across services.

### WAL, Checkpoints, Recovery

```
client COMMIT → WAL flushed (durable) → return ACK → (later) dirty pages checkpointed
crash → replay WAL from last checkpoint → committed work restored, partial work discarded
```

- Checkpoints bound recovery time; WAL archiving + base backups give point-in-time recovery; logical/physical replication streams WAL records to standbys.

## Common Pitfalls

1. **Assuming Repeatable Read = Serializable**: write skew passes under RR in every major engine. Auditing-style invariants ("count never negative", "no double booking") need Serializable or explicit locks.
2. **No retry loop on serialization/deadlock errors**: Postgres `40001`, MySQL `1213/1205` are *expected* control flow under contention. Every transactional path needs bounded retry with backoff — code that treats them as fatal will flake in production.
3. **Long-running transactions**: an idle-in-transaction session pins snapshots (bloat, vacuum stall) and holds locks. Set `idle_in_transaction_session_timeout`, commit promptly, never wait on user input inside a transaction.
4. **SELECT-then-UPDATE without locking**: check-then-act races (balance check → debit) under Read Committed double-spend. Lock the row first (`FOR UPDATE`) or make the update conditional (`UPDATE ... WHERE balance >= 100` + check row count).
5. **2PC across microservices**: coordinator failure modes, latency coupling, and lock-holding across network calls. Prefer transactional outbox + consumer idempotency, or sagas with compensations.
6. **Async commit without understanding the window**: `synchronous_commit = off` / `innodb_flush_log_at_trx_commit = 2` can lose ~1 s of "committed" work on crash. Fine for analytics ingestion, unacceptable for payments — choose per workload, explicitly.
7. **Ignoring lock monitoring**: `pg_locks` + `pg_stat_activity`, `performance_schema` / `SHOW ENGINE INNODB STATUS` exist precisely for contention diagnosis. Alert on lock waits, not just slow queries.

## Related Concepts

- [[concepts/computer-science/database-indexing|Database Indexing]] (gap locks on index ranges, index-only snapshots)
- [[concepts/computer-science/processes-and-threads|Processes and Threads]] (deadlock theory, lock ordering — same Coffman conditions)

## References

- Garcia-Molina, Ullman, Widom — *Database Systems: The Complete Book* (ch. 17–19: transactions, concurrency, recovery)
- Bernstein, Hadzilacos, Goodman — *Concurrency Control and Recovery in Database Systems* (free PDF; the formal reference)
- PostgreSQL docs — "Transaction Isolation", "MVCC", "WAL"; MySQL docs — "InnoDB Locking and Transaction Model"
- Gray & Reuter — *Transaction Processing* (2PC, TP monitors, classic practice)
