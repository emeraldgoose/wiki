---
title: Hash Tables
description: "Seminar-level concept: hash functions, collision resolution, load factor, amortized O(1) operations"
tags: [concept, computer-science, data-structures, hash-table, dictionary]
locale: en
published: 2026-09-06
---

# Hash Tables

[한국어 버전](/ko/concepts/computer-science/hash-tables.md)

> A hash table stores key–value pairs and finds any key in O(1) average time by converting the key into an array index with a hash function, resolving the inevitable collisions by chaining or open addressing.

## Definition

A **hash table** (hash map, dictionary) is a data structure mapping keys to values. A **hash function** `h(key)` converts each key into an index into a backing array of `m` slots. Because there are more possible keys than slots, **collisions** (two keys mapping to the same slot) are unavoidable, so every hash table pairs its hash function with a **collision-resolution strategy**.

## Why It Matters

- **The default lookup structure**: Python `dict`, Java `HashMap`, Go `map`, and Redis hashes power caches, indexes, memoization, symbol tables, and deduplication.
- **Amortized O(1)**: average-case constant-time insert, lookup, and delete make it the answer whenever order does not matter.
- **Foundation for bigger systems**: consistent hashing (distributed caches, Dynamo-style stores), hash joins in databases, and content-addressed storage (Git objects) all generalize this one idea.
- **Interview staple**: Two Sum, grouping anagrams, and LRU-cache design all reduce to "use a hash table."

## How It Works

### Operations and Complexity

| Operation | Average | Worst | Notes |
|-----------|---------|-------|-------|
| Insert | O(1) | O(n) | Resize occasionally costs O(n), amortized O(1) |
| Lookup | O(1) | O(n) | All keys collide → degrades to a list scan |
| Delete | O(1) | O(n) | Open addressing needs tombstones (below) |

### A Good Hash Function

1. **Deterministic**: same key → same hash, every time.
2. **Uniform**: spreads keys evenly across slots (minimizes collisions).
3. **Fast**: it runs on every operation, so it must be cheap.
4. **Avalanche**: flipping one input bit changes ~half the output bits (e.g. MurmurHash, xxHash, SHA-family for security contexts).

Note: **cryptographic** hashes (SHA-256) resist adversarial collisions but are slower; **non-cryptographic** hashes (MurmurHash, FxHash) are the default for in-memory tables.

### Collision Resolution

**1. Separate chaining.** Each slot holds a linked list (or small tree) of entries:

```
slot 3: → (anna, 1) → (zack, 2)
slot 4: → (bob, 3)
```

Simple, never "fills up," degrades gracefully. Java's `HashMap` upgrades long chains to red-black trees (O(log n) worst case per lookup).

**2. Open addressing.** All entries live in the array itself; on collision, probe for the next free slot:

- *Linear probing*: check `h, h+1, h+2, …` — great cache locality but suffers **primary clustering**.
- *Quadratic probing*: steps grow as 1, 4, 9, … — reduces clustering.
- *Double hashing*: step size from a second hash — best spread, slightly more compute.

Open addressing needs **tombstones** on delete: a removed slot is marked "deleted" rather than emptied, so probes for later keys still pass through it.

### Load Factor and Resizing

**Load factor** α = n / m (entries / slots). Chaining works up to α ≈ 1–8; open addressing degrades past α ≈ 0.7. When α crosses a threshold (commonly 0.75), the table **resizes**: allocate a ~2× array and rehash every entry — an O(n) operation that happens rarely enough to keep all operations O(1) **amortized**.

```python
table = {}
for i in range(1_000_000):
    table[f"user:{i}"] = i   # occasional resizes; each op still ~O(1) amortized
```

## Common Pitfalls

- **Unhashable or mutable keys.** Using a mutable list as a key (or mutating an object after inserting it) corrupts lookups — keys must be immutable while in the table.
- **Bad hash functions.** Hashing every string to its length turns the table into O(n) linked lists. Always use a well-distributed hash; for custom objects, implement both hash and equality consistently (equal objects must hash equally).
- **Hash-flooding DoS.** Attackers crafting colliding keys can force O(n) behavior per op. Defenses: randomized seeds (Python's `PYTHONHASHSEED` / SipHash) — and never assume adversarial input hashes uniformly.
- **Assuming ordering.** Classic hash tables are unordered; iterating yields arbitrary order. Need order? Use an order-preserving variant (`OrderedDict`, `IndexMap`, B-tree map) — at a cost.
- **Ignoring worst case in latency-sensitive paths.** Real-time or high-percentile-latency systems must account for resize pauses and collision worst cases, not just the average.
- **Open-addressing delete without tombstones.** Emptying a slot on delete silently breaks lookup of keys that probed past it.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] — amortized O(1) and the average-vs-worst-case distinction
- [[concepts/computer-science/trees|Trees]] — balanced trees as the ordered-map alternative
- [[concepts/computer-science/dynamic-programming|Dynamic Programming]] — memoization tables are usually hash tables

## References

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 11: Hash Tables.
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 3.4–3.5: Hash Tables.
- De Candia et al. — "Dynamo: Amazon's Highly Available Key-value Store" (consistent hashing application).
