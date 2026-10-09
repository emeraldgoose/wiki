---
title: Database Indexing
description: "Seminar-level concept: B-tree indexes, composite keys, covering indexes, write trade-offs, query planning"
tags: [concept, computer-science, database, indexing, b-tree, query-optimization]
published: 2026-09-06
locale: en
---

# Database Indexing

> [한국어 버전](/ko/concepts/computer-science/database-indexing)

A **database index** is an auxiliary data structure that lets the engine locate rows without scanning the whole table — trading write overhead and storage for read speed. Index design (which columns, in which order, of which type) is the highest-leverage activity in relational performance work.

## Definition

- **Index**: a structure (usually a B-tree variant) mapping key values → row locations (heap tuple pointers, or primary keys in index-organized tables like InnoDB). The query planner may use it for lookup, range scans, ordering, and grouping.
- **Selectivity**: fraction of rows a predicate matches. Highly selective predicates (`id = 42`) benefit enormously; low-selectivity ones (`country = 'US'` matching 60%) often scan anyway.
- **Clustered vs non-clustered**: a clustered index dictates physical row order (one per table — the primary key in InnoDB); non-clustered (secondary) indexes point at rows and need an extra hop (**bookmark lookup**).
- **Full table scan**: reading every page. Correct fallback, and genuinely faster than index navigation for large result fractions — not inherently evil.

## Why It Matters

- **Complexity change, not constant-factor**: an index turns O(n) scans into O(log n) lookups. On a 100M-row table that is the difference between milliseconds and minutes.
- **The dominant production bottleneck**: missing or wrong indexes cause more real-world DB incidents than hardware, configuration, or query style combined.
- **Write/read trade-off made explicit**: every index taxes INSERT/UPDATE/DELETE (maintain each tree, write-ahead log it, replicate it). Indexing is budgeting, not free speed.
- **Planner legibility**: understanding what the planner can and cannot use (sargability, leftmost prefix, implicit casts) is what separates guessing from engineering.

## How It Works

### B-Tree Structure

```
            [20 | 50]
           /    |    \
   [5|10|15] [30|40] [60|70|80]
   (leaf pages → doubly linked for range scans; each leaf points at rows)
```

- Balanced tree, fan-out in the hundreds (8 KB pages, small keys) → depth 2–4 even for billions of rows. Depth = worst-case page reads per point lookup.
- **Range scans** walk the leaf linked list; **ordering** (`ORDER BY`) can come free if it matches index order; **prefix compression** shrinks repetitive keys.
- Variants: B+tree (values in leaves only — what databases actually use), LSM-tree (buffered writes, merge-compacted — Cassandra, RocksDB, Bigtable storage engines), hash indexes (equality only, no ranges), GiST/GIN (full-text, arrays, geometry in PostgreSQL), bitmap (low-cardinality analytics).

### Composite Indexes and Leftmost Prefix

```sql
CREATE INDEX idx_orders ON orders (customer_id, order_date);
-- serves:  WHERE customer_id = ? AND order_date BETWEEN ? AND ?
-- serves:  WHERE customer_id = ?
-- does NOT serve:  WHERE order_date = ?   (leftmost column missing)
```

- Column order follows **equality-first, range-last**: equality columns in any order, then at most one range column per index usage. High-selectivity-first is the usual heuristic, but the range-column-last rule dominates.
- **Covering index**: includes every column the query needs → the engine answers from the index alone (**index-only scan**, visible in `EXPLAIN`). Often created with `INCLUDE` columns (PostgreSQL, SQL Server) to widen coverage without widening the key.
- **Partial index** (`WHERE active`): smaller, faster, cheaper to maintain when queries share a predicate. **Expression index** (`lower(email)`) serves function calls the plain column index cannot.

### The Planner and EXPLAIN

- The cost-based planner estimates rows × cost per access path (seq scan, index scan, bitmap heap scan, nested loop / hash / merge join) using table statistics (`ANALYZE`, auto-vacuum stats). Stale statistics → wrong plans.
- Read `EXPLAIN (ANALYZE, BUFFERS)`: check actual vs estimated rows (misestimates >10× flag stale stats or correlated predicates), buffers hit vs read (cache effectiveness), and whether an index-only scan materialized.
- **Sargability**: `WHERE created_at > now() - interval '7 days'` uses an index; `WHERE date_trunc('day', created_at) = ...` or `WHERE phone::text LIKE '%42'` on mismatched types generally does not (function/type barrier — fix with expression indexes or corrected predicates).

### Write-Side Costs

- Each INSERT updates every index (random leaf page writes for non-sequential keys — the reason UUIDv4 primary keys fragment InnoDB clusters while auto-increment appends neatly).
- Each UPDATE of an indexed column = delete + insert in that index. HOT (heap-only tuple) updates in PostgreSQL avoid index churn only when no indexed column changes.
- Index bloat (dead entries between vacuums) and fragmentation (page splits) are maintained with `VACUUM`/`REINDEX` (Postgres) or online `OPTIMIZE` (MySQL).

## Common Pitfalls

1. **Indexing every column "to be safe"**: write throughput collapses, replication lags (every index change is WAL-logged and replayed), and the planner gets confused by overlapping options. Index from evidence (`pg_stat_statements`, slow logs), not anxiety.
2. **Wrong composite order**: `(order_date, customer_id)` for a query filtering one customer over a date range scans far more than `(customer_id, order_date)`. Equality first, range last.
3. **Implicit type casts killing index use**: `WHERE phone = 123` against a `text` column (or mismatched collations) forces a scan. Match types exactly.
4. **Low-selectivity single-column indexes**: an index on `gender` or `is_deleted` is nearly never used alone — and still taxes writes. Use partial indexes or composite indexes where the flag rides along with a selective column.
5. **N+1 queries "fixed" with indexes**: an index makes 1000 point lookups fast-ish instead of catastrophic, but one JOIN/batched fetch is still 100–1000× better. Fix the access pattern first.
6. **Never checking EXPLAIN after schema changes**: statistics, planner behavior, and data distribution drift. `EXPLAIN (ANALYZE, BUFFERS)` on the top queries after every migration touching indexed columns.
7. **UUIDv4 as clustered PK at scale**: random insertion points → page splits, fragmentation, and cache-hostile writes in InnoDB. Prefer auto-increment/sequential keys, or UUIDv7 (time-ordered) if opaque IDs are required.

## Related Concepts

- [[concepts/computer-science/database-transactions|Database Transactions]] (locking vs MVCC, how indexes interact with isolation)
- [[concepts/computer-science/caching|Caching]] (buffer pool as cache; index pages compete for memory)

## References

- Garcia-Molina, Ullman, Widom — *Database Systems: The Complete Book* (ch. 13–14: indexing, query processing)
- PostgreSQL docs — "Indexes" + "Using EXPLAIN" (authoritative planner reference)
- MySQL docs — "Optimization and Indexes" (InnoDB clustered index behavior)
- Use The Index, Luke (use-the-index-luke.com) — practitioner field guide to sargability and composite design
