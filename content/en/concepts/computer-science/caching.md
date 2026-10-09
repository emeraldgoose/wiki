---
title: Caching
description: "Seminar-level concept: cache hierarchies, eviction policies, TTL, invalidation, stampede protection, CDN and app caches"
tags: [concept, computer-science, caching, redis, cdn, performance, eviction]
published: 2026-09-06
locale: en
---

# Caching

> [한국어 버전](/ko/concepts/computer-science/caching)

A **cache** is a faster, smaller store in front of a slower source of truth, serving repeated requests without recomputation or refetch. Caching is the single most cost-effective performance technique — and invalidation, in Phil Karlton's famous formulation, one of the two hard problems.

## Definition

- **Cache**: a lookup structure keyed by request identity, holding previously computed/fetched values with an eviction and/or expiration policy. Hits avoid the backing store; misses pay full cost plus fill cost.
- **Hit ratio**: hits / total lookups. The deciding metric — a 95% hit ratio means the backing store sees 1/20th of traffic. Measure per cache tier, not globally.
- **TTL (time-to-live)**: how long an entry is considered fresh. The blunt instrument that bounds staleness: shorter TTL = fresher data, lower hit ratio.
- **Invalidation**: proactively removing/refreshing entries when the source changes — precise but requires knowing every affected key.

## Why It Matters

- **Latency and cost collapse**: memory serves in ~100 ns, SSD in ~100 µs, cross-region fetch in ~100 ms — six orders of magnitude. Each cache tier crossed off is a different latency universe.
- **Protecting the source of truth**: databases and origins survive traffic spikes because caches absorb the repeated 99%. Capacity planning usually means cache planning.
- **The consistency trade**: every cache introduces a window where readers see stale data. Choosing TTLs and invalidation is choosing which staleness each feature tolerates.
- **Layered reality**: CPU L1/L2/L3 → page cache → application cache (Redis/Memcached) → CDN edge → browser cache. A request may traverse five caches; reasoning must be per-layer.

## How It Works

### The Hierarchy

```
registers → L1 (~1ns) → L2 (~4ns) → L3 (~15ns) → RAM (~100ns)
  → SSD (~100µs) → same-AZ network (~0.5ms) → cross-region (~100ms) → origin compute?
```

- Each level is ~10–1000× slower and ~10–100× larger than the last. Design rule: keep the hot set in the fastest tier that fits it, and size tiers from measured working sets, not guesses.
- **Page cache** (OS): file and mmap reads served from free RAM — often the biggest "cache" on a box, and the reason databases preach "fit the working set in memory."
- **Application cache** (Redis, Memcached): explicit key-value store for query results, sessions, rendered fragments, rate-limit counters. Network hop (~0.5 ms) but shared across app instances.
- **CDN edge**: geographically distributed reverse proxies (CloudFront, Cloudflare, Fastly) serving static and cacheable dynamic content near users; also offloads TLS and absorbs DDoS.
- **Browser cache**: `Cache-Control`/`ETag` driven; eliminates the request entirely on hit (the cheapest request is the one never made).

### Eviction Policies

| Policy | Rule | Strengths / weaknesses |
|---|---|---|
| LRU | Evict least recently used | Great for recency workloads; scans pollute it |
| LFU / TinyLFU | Evict least frequently used | Resists scans; needs aging to adapt to shifts |
| FIFO | Evict oldest inserted | Simple; ignores usefulness entirely |
| Random | Evict uniformly at random | Surprisingly competitive, trivially cheap |
| TTL-only | Expire by time, evict expired | Predictable staleness; ignores value/size |
| ARC / LRU-K / S3-FIFO | Adaptive/ghost-history hybrids | Near-optimal across mixed workloads (Redis, Caffeine) |

- Real systems: Redis offers `allkeys-lru/lfu/random`, `volatile-*` (TTL'd keys only); Caffeine (Java) uses Window-TinyLFU; modern research favors **S3-FIFO** (SOSP'23) — FIFO queues plus ghost history, beating LRU with less bookkeeping.
- **Scan resistance** matters: a nightly batch sweeping 10M cold keys must not evict the 100k hot ones. Segmented designs (probation/protected segments) exist for exactly this.

### Patterns: Aside, Through, Write-Behind

```
Cache-aside (lazy):      app → cache? miss → DB → fill cache → return
Read-through:            app → cache → (miss: cache loads DB itself)
Write-through:           app → cache → DB synchronously (consistent, slower writes)
Write-behind (back):     app → cache → ACK → DB async (fast, loss window)
```

- **Cache-aside** is the default: only requested data is cached (no cold-fill waste), but the app owns invalidation logic.
- **Write-through** keeps cache and DB consistent at write cost — right for small, critical datasets. **Write-behind** absorbs write bursts (metrics, counters) but can lose acknowledged writes on crash; size the window deliberately.
- **Refresh-ahead**: background refresh of hot keys before TTL expiry smooths latency (Guava/Caffeine `refreshAfterWrite`) at the cost of occasional redundant loads.

### Stampede Protection

- **Thundering herd**: hot key expires → 1000 concurrent misses → 1000 identical DB queries → DB dies, then all 1000 fill the same value.
- Cures: **request coalescing** (singleflight — one in-flight load per key, waiters share the result; in Go's `singleflight`, Redis with `SET NX` lock + wait, or Caffeine's built-in coalescing), **probabilistic early refresh** (XFetch-style: refresh before expiry with probability rising near TTL end), **stale-while-revalidate** (`Cache-Control: stale-while-revalidate=N` — serve stale instantly, refresh in background).
- Negative caching (cache misses/404s briefly) stops repeated expensive lookups for absent keys; pair with bloom filters for large keyspaces.

## Common Pitfalls

1. **No TTL ("cache forever")**: every entry becomes permanent stale-data risk and unbounded memory growth. Every key gets a TTL; "forever" is a TTL you chose explicitly with an invalidation story.
2. **Caching without measuring hit ratio**: a 40%-hit cache adds a network hop to 60% of requests while barely shielding the DB. Instrument hits/misses/evictions per key-prefix before tuning size or policy.
3. **Key design collisions**: `user:{id}` vs `user:{id}:profile` vs locale/currency variants under one key serves wrong content to wrong users. Namespace keys (`v1:profile:{locale}:{id}`) and include every varying dimension.
4. **Cold-start collapse after deploys/restarts**: flushing the cache on deploy sends full traffic to the DB. Warm gradually (rolling restarts, persistent Redis, pre-warming scripts) or keep cache infrastructure independent of app deploys.
5. **Stale reads breaking money-adjacent flows**: caching balances, inventory counts, or auth decisions with minute-long TTLs creates oversell/overdraft windows. Cache presentation data aggressively; verify transactional facts at decision time.
6. **Unbounded key cardinality**: per-user-per-query-string keys grow memory forever and tank hit ratio. Normalize keys (strip tracking params, bucket time windows) and set maxmemory policies (`noeviction` in production Redis is a memory bomb — prefer `allkeys-lru` with alerts).
7. **Dog-piling the CDN origin**: edge TTLs too short or `Vary: *` semantics force every edge request to origin. Tier the cache (edge → shield/parent → origin) and fix `Vary`/`Cache-Control` at the origin.

## Related Concepts

- [[concepts/computer-science/virtual-memory|Virtual Memory]] (page cache, TLB as hardware cache)
- [[concepts/computer-science/http|HTTP]] (Cache-Control, ETag, CDN semantics)
- [[concepts/computer-science/database-indexing|Database Indexing]] (buffer pool vs application cache layering)

## References

- Nygard — *Release It!* (stability patterns: timeouts, circuit breakers, bulkheads around caches)
- Redis docs — "Eviction policies", "Latency"; Memcached docs — LRU/crawler behavior
- heterogenous classics: LRU-K (O'Neil et al. 1993), ARC (Megidson & Modha 2003), TinyLFU (Eini & Mansour 2017), S3-FIFO (SOSP'23)
- Google SRE Workbook — "Handling Overload" (thundering herd, load shedding, backpressure)
- Cloudflare / Fastly learning centers — CDN caching semantics in practice
