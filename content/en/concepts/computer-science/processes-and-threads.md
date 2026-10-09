---
title: Processes and Threads
description: "Seminar-level concept: processes vs threads, PCB, scheduling, context switching, synchronization, concurrency pitfalls"
tags: [concept, computer-science, processes, threads, concurrency, scheduling]
published: 2026-09-06
locale: en
---

# Processes and Threads

A **process** is a running program with its own isolated address space; a **thread** is the smallest schedulable unit of execution inside a process, sharing the process's memory with its sibling threads. Everything about concurrency — performance, correctness bugs, and OS design — flows from this distinction.

## Definition

- **Process**: an instance of a program in execution. Owns a private virtual address space, file descriptors, security credentials, and one or more threads. The kernel tracks it in a **Process Control Block (PCB)**: PID, state (new/ready/running/waiting/terminated), program counter, registers, memory maps, open files, scheduling priority.
- **Thread**: a flow of control within a process — its own stack, registers, and program counter, but **shared** heap, code, and file descriptors with other threads in the same process.
- **Multiprocessing vs multithreading**: separate processes communicate via IPC (pipes, sockets, shared memory); threads communicate via shared memory directly, which is faster but requires explicit synchronization.

## Why It Matters

- **Isolation vs speed**: a crashing process does not take down its siblings; a crashing thread takes down the whole process. Choosing between them is the fundamental reliability/performance trade-off in server design (e.g., Chrome's multi-process tabs vs Nginx's threaded/evented workers).
- **Utilizing multicore hardware**: a single-threaded process uses one core. Threads (or processes) are how software converts additional cores into throughput.
- **Blocking I/O**: one thread can block on disk or network while others keep working — the basis of responsive servers and UIs.
- **Cost model**: process creation (`fork` + `exec`) is orders of magnitude heavier than thread creation; context switches between processes flush TLB entries, while thread switches within a process are cheaper.

## How It Works

### Process Lifecycle and State

```
new → ready ⇄ running → waiting → terminated
              (scheduler dispatch)  (I/O wait)
```

- The **scheduler** multiplexes CPUs across ready processes/threads. Preemptive schedulers (Linux CFS — Completely Fair Scheduler) time-slice with virtual-runtime accounting so every runnable task gets a fair share.
- **Context switch**: the kernel saves the outgoing task's registers/PC/stack pointer into its PCB/TCB and restores the incoming task's. Cost comes from direct register work plus indirect cache/TLB pollution.

### fork, exec, and Copy-on-Write

```c
pid_t pid = fork();   // parent gets child PID, child gets 0
if (pid == 0) { execl("/bin/ls", "ls", NULL); }
```

- `fork()` clones the calling process. Modern kernels use **copy-on-write (COW)**: parent and child share physical pages marked read-only until either writes, so `fork` is cheap until memory diverges.
- `exec()` replaces the process image with a new program. Shells, servers (preforking), and container runtimes all build on fork+exec (or `posix_spawn`).

### Threads: Models and Implementations

- **User threads (M:N / green threads)**: scheduled by a runtime (Go goroutines, Erlang processes, Java virtual threads / Project Loom). Creation cost is kilobytes; millions can exist. The runtime multiplexes them onto a few kernel threads.
- **Kernel threads (1:1)**: each user thread maps to a kernel schedulable entity (pthreads, `std::thread`). Creation costs ~1–8 MB of stack plus a kernel object; practical limits are in the thousands.
- **Thread pool pattern**: pre-spawn N workers, feed them a queue. Bounds memory, amortizes creation cost, and provides backpressure. Nearly every production server uses one.

### Synchronization Primitives

| Primitive | Use | Cost/notes |
|---|---|---|
| Mutex | Mutual exclusion on critical sections | Futex-based on Linux: uncontended lock is userspace-only |
| Semaphore | Counting resource slots | Generalizes mutex |
| Condition variable | Wait until predicate true | Always re-check predicate in a loop (spurious wakeups) |
| RWLock | Many readers / one writer | Reader-writer starvation policies matter |
| Atomic / CAS | Lock-free counters, queues | Basis of lock-free algorithms; memory-ordering subtlety |

- **Race condition**: outcome depends on uncontrolled thread interleaving. Fix by establishing invariants protected by a single lock, or by using message passing / immutable data to eliminate sharing.
- **Deadlock** (Coffman conditions): mutual exclusion + hold-and-wait + no preemption + circular wait. Standard cures: global lock ordering, lock timeouts with backoff, or lock-free design.

## Common Pitfalls

1. **Data races on "just a flag"**: an unsynchronized boolean shared between threads is undefined behavior in C++/Rust and visibility-unreliable in Java without `volatile`/atomics. Use atomics or locks, not bare variables.
2. **Holding locks across blocking calls**: sleeping or doing I/O while holding a mutex serializes the whole subsystem and invites deadlock. Keep critical sections tiny.
3. **Thread-per-connection at scale**: 10k connections × 8 MB stacks = 80 GB of virtual memory plus scheduler thrash. Use pools, non-blocking I/O, or green threads instead.
4. **Fork-safety**: only async-signal-safe functions are legal between `fork` and `exec` in a multithreaded program (a forked child inherits a single surviving thread but all mutex states). Call `exec` immediately.
5. **False sharing**: two threads writing adjacent fields on the same cache line bounce the line between cores and destroy scalability. Pad or separate hot fields per thread.
6. **Ignoring the memory model**: lock-free code written with "it works on x86" assumptions breaks on ARM (weaker ordering). Use language-level atomics with explicit orderings.

## Related Concepts

- [[concepts/computer-science/virtual-memory|Virtual Memory]] (per-process address spaces, COW)
- [[concepts/computer-science/caching|Caching]] (CPU caches, false sharing, cache coherence)

## References

- Silberschatz, Galvin, Gagne — *Operating System Concepts* (ch. 3–7: processes, threads, synchronization)
- Bovet & Cesati — *Understanding the Linux Kernel* (process scheduling, CFS)
- Linux man pages: `fork(2)`, `execve(2)`, `clone(2)`, `futex(2)`, `pthreads(7)`
- Ulrich Drepper — "Futexes Are Tricky" (lock implementation fundamentals)
