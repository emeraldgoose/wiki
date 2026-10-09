---
title: Concurrency vs Parallelism
description: "Seminar-level concept: concurrent vs parallel execution, threads, async, races, deadlocks, and models"
tags: [concept, computer-science, concurrency, parallelism, threads, async]
locale: en
published: 2026-09-06
---

# Concurrency vs Parallelism

> Concurrency is dealing with many things at once (overlapping lifetimes, interleaved execution); parallelism is doing many things at once (simultaneous execution on multiple cores). Every correct concurrent program must tame shared state — races, deadlocks, and visibility.

## Definition

- **Concurrency**: a program manages multiple tasks with overlapping lifetimes. Execution may interleave on a single core (time-slicing, event loops) — tasks *appear* to run together.
- **Parallelism**: multiple tasks literally execute simultaneously, requiring multiple cores (threads on separate CPUs, SIMD lanes, GPU cores, distributed nodes).

Classic formulation (Rob Pike): *"Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once."* Concurrency is a program-structuring property; parallelism is a hardware-execution property. A concurrent program (e.g. Go goroutines, async tasks) may run on one core with zero parallelism — and parallel execution is often introduced *inside* a concurrent design.

## Why It Matters

- **Performance**: I/O-bound servers handle 10k connections via concurrency (async/event loops); CPU-bound work (rendering, training, simulation) needs real parallelism to use 32 cores.
- **Correctness is hard**: data races, deadlocks, and starvation are nondeterministic — they pass tests and fail in production at 3 AM.
- **System design**: every backend decision — thread-per-request vs. event loop, locks vs. lock-free, shared memory vs. message passing — is a concurrency-model decision.
- **Hardware trends**: single-core scaling ended (~2005); all future speedups come from parallelism (multicore, GPUs, clusters).

## How It Works

### Concurrency Models

| Model | Unit | How it runs | Examples | Best for |
|-------|------|-------------|----------|----------|
| Threads + shared memory | OS/kernel thread | Preemptive scheduling, shared heap | Java threads, pthreads | CPU-bound parallel work; legacy code |
| Event loop / async | Task/coroutine | Single-threaded, non-blocking I/O | Node.js, Python asyncio, nginx | Many idle I/O connections |
| Actor / message passing | Actor | No shared state, async messages | Erlang, Akka, Go channels (CSP) | Distributed, fault-tolerant systems |
| SIMD / data parallel | Lane | One instruction, many data | NumPy, GPUs, AVX | Numerical loops, ML inference |
| Distributed | Process/node | Network messages | MapReduce, Spark, microservices | Internet-scale data |

### Threads vs. Async (Worked Contrast)

Thread-per-request (blocking I/O, dedicated stack ~MBs per thread):

```python
# threads: simple code, but 10k threads = GBs of stacks + context-switch cost
with ThreadPoolExecutor(max_workers=100) as pool:
    pool.map(fetch_url, urls)
```

Async event loop (one thread, tasks yield at I/O):

```python
# asyncio: 10k connections on one thread; code must never block
async with aiohttp.ClientSession() as s:
    await asyncio.gather(*[fetch(s, u) for u in urls])
```

Rule of thumb: **I/O-bound → async/concurrency** (wait without wasting threads); **CPU-bound → threads/processes/parallelism** (GIL-bound languages like CPython need multiprocessing for CPU parallelism).

### The Three Hazards

**1. Data race.** Two threads access shared state with at least one write and no synchronization:

```python
counter = 0
def inc():
    global counter
    for _ in range(100_000):
        counter += 1   # read-modify-write: two threads interleave → lost updates
```

Fix: locks/mutexes, atomics, or confinement (one owner + message passing).

**2. Deadlock.** Four conditions (Coffman): mutual exclusion, hold-and-wait, no preemption, circular wait. Classic: thread A holds lock 1 wants lock 2; thread B holds 2 wants 1. Fixes: global lock ordering, lock timeouts / `try_lock`, or lock-free/message-passing designs.

**3. Visibility / memory model.** Even without races on paper, CPU caches and compiler reordering mean a write on one core may not be *visible* to another without memory barriers (`volatile`, atomics with ordering, channel operations). Never reason "it worked on x86" — the language memory model (Java JMM, C++11 atomics, Go memory model) is the contract.

### Synchronization Toolkit

| Tool | Cost | Use when |
|------|------|----------|
| Mutex / lock | Blocks; contention serializes | Short critical sections on shared state |
| Read-write lock | Concurrent reads | Read-heavy workloads |
| Semaphore | Counter-based permits | Bounded resources (connection pools) |
| Condition variable / channel | Wait/signal | Producer–consumer handoff |
| Atomic / CAS | Lock-free fast path | Counters, lock-free structures |
| Immutable data + message passing | Copying overhead | Eliminating shared state entirely |

**Amdahl's Law** bounds the win: if fraction `p` of work is parallelizable over `n` cores, speedup ≤ 1 / ((1−p) + p/n). A program 90% parallelizable on 32 cores still caps at ~7.6× — the serial 10% dominates. Optimize the serial part or parallelize more.

## Common Pitfalls

- **Confusing the terms in design reviews.** "We made it concurrent" (async I/O) does not speed up CPU-bound code; "we made it parallel" (32 threads) does not help 10k idle connections. Match the tool to I/O-bound vs. CPU-bound.
- **Locking too much (serializing everything).** One giant global lock makes 32 threads run sequentially — correct but pointless. Keep critical sections minimal; prefer per-shard locks or lock-free reads.
- **Locking too little (racy "it works on my machine").** Races are timing-dependent; stress tests and sanitizers (ThreadSanitizer, `-race` detectors) catch what unit tests miss.
- **Deadlock via inconsistent lock order.** Any two locks acquired in different orders in different places can deadlock. Enforce a global ordering, or use a single lock per subsystem.
- **Blocking the event loop.** One synchronous 200 ms call in async code stalls *all* 10k connections. Offload blocking work to a thread pool.
- **Ignoring the GIL (CPython).** Threads do not parallelize CPU-bound Python; use multiprocessing, native extensions that release the GIL (NumPy), or another runtime.
- **Premature distribution.** Distributed parallelism adds network partitions and exactly-once headaches — exhaust single-machine parallelism (cores, SIMD, GPU) first.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] — Amdahl's law and speedup analysis
- [[concepts/computer-science/hash-tables|Hash Tables]] — concurrent maps and sharding shared state
- [[concepts/computer-science/graphs|Graphs]] — wait-for graphs for deadlock detection; DAG scheduling of parallel tasks

## References

- Pike — "Concurrency Is Not Parallelism" (talk, 2012).
- Amdahl — "Validity of the Single Processor Approach" (1967).
- Goetz et al. — *Java Concurrency in Practice* (the practical reference).
- Herlihy & Shavit — *The Art of Multiprocessor Programming* (lock-free theory).
