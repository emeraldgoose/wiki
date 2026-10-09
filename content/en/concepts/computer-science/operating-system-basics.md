---
title: Operating System Basics
description: "Seminar-level concept: processes, scheduling, virtual memory, syscalls, filesystems, IPC, concurrency primitives"
tags: [concept, computer-science, operating-systems, kernel, scheduling, virtual-memory, processes, filesystems]
published: 2026-09-06
locale: en
---

# Operating System Basics

An **operating system** multiplexes hardware among programs while giving each the illusion of its own machine: its own CPU (processes/threads), its own memory (virtual address spaces), and its own disk (files). The kernel is the trusted arbiter in the middle — every abstraction is a deal where the OS trades a little overhead for isolation, fairness, and portability.

## Definition

- **Kernel vs user space**: the kernel runs privileged (ring 0), owning hardware and page tables; processes run unprivileged (ring 3) and must ask via **system calls** (`read`, `mmap`, `fork`, `epoll_wait`). The syscall boundary is also the security boundary.
- **Process**: an address space plus resources (fds, threads, credentials) — the unit of isolation. **Thread**: a schedulable stack + registers sharing its process's memory — the unit of execution. Fork copies the space; exec replaces the program.
- **Virtual memory**: per-process address spaces mapped to physical RAM by page tables and the MMU, with paging to disk as overflow. Programs see contiguous memory; the OS handles the fragmented reality.
- **Scheduler**: decides which runnable thread runs on which core and for how long (Linux CFS — Completely Fair Scheduler — tracks virtual runtime and picks the least-served task).
- **Filesystem + IPC**: persistent named bytes (ext4, APFS, NTFS) with permissions and journaling; and communication channels between processes — pipes, sockets, shared memory, signals, message queues.

## Why It Matters

- **Every performance ceiling is an OS ceiling**: page faults, context switches (~1–10 µs), TLB misses, and syscall counts bound what applications achieve. Engineers who read `perf`, `strace`, and `/proc` diagnose in minutes what others guess at for days.
- **Isolation is the security model**: containers (namespaces + cgroups), sandboxes, and mobile app boundaries are all OS primitives composed — not new inventions. Misunderstanding uid/capability semantics is how escapes happen.
- **Concurrency semantics come from the kernel**: mutexes, futexes, condition variables, and `epoll`/`io_uring` define what "simultaneous" even means. Language runtimes (Go scheduler, Tokio) are user-space schedulers negotiating with the kernel one.
- **Resource exhaustion is the common outage**: fd leaks, OOM kills, disk-full journals, zombie accumulation. Capacity thinking — limits, quotas, backpressure — is OS thinking applied upward.

## How It Works

### Processes, Threads, and the Scheduler

```
fork() → child gets copied address space (CoW) → exec() replaces image
clone() → thread shares mm, files, fs → scheduler picks next task by vruntime (CFS)
blocking syscall → task sleeps → wakeup on event → back to runqueue
```

- **Copy-on-write** makes `fork` cheap: parent and child share pages read-only until either writes, so spawning is page-table work, not memory copying.
- **CFS fairness**: each task accrues virtual runtime weighted by niceness; the leftmost node in the red-black tree (least vruntime) runs next. No fixed timeslices — latency target (`sched_latency_ns`) divided among runnable tasks.
- **Preemption + affinity**: timer ticks and wakeups preempt; `sched_setaffinity` and NUMA policy keep hot threads near their memory. Migrating a thread across sockets invalidates caches — locality is performance.

### Memory: Paging, Faults, and Reclamation

- **Paging path**: CPU translates VA → PA via TLB (fast) or page-table walk (slow); on miss the fault handler maps a zero page, reads a file page, or swaps one in — then resumes the faulting instruction transparently.
- **Overcommit + OOM**: Linux overcommits `malloc` (hands out VA beyond RAM) and the **OOM killer** sacrifices low-score processes when memory truly runs out. Containers set the cgroup limit that scopes this bargain.
- **mmap as the universal tool**: file I/O, shared libraries, 1 GB heap arenas, and IPC shared segments are all page-table mappings. `madvise`/`mlock`/`mprotect` tune their behavior per range.

### Files, Descriptors, and IPC

- **"Everything is a file descriptor"**: files, sockets, pipes, epoll instances, timers — uniform `read/write/poll/close` surface with per-fd flags (`O_NONBLOCK`, `CLOEXEC`) and reference-counted lifetime.
- **I/O models ladder**: blocking → nonblocking + `epoll` readiness → `io_uring` completion queues (batched syscalls, zero-copy paths). Each rung removes a context-switch or copy; async runtimes are thin wrappers over the top rungs.
- **Signals vs structured IPC**: signals (`SIGTERM`, `SIGCHLD`) are lossy notifications, not message channels — real coordination uses pipes/sockets/shared memory plus futexes.

## Common Pitfalls

1. **Fork-without-exec in multithreaded programs**: only the calling thread survives `fork`; locks held by dead threads stay locked forever in the child. Fork, then exec immediately — or use `posix_spawn`.
2. **Ignoring file-descriptor limits**: default `ulimit -n` (often 1024) plus leaked sockets equals 3 a.m. EMFILE outages. Set `CLOEXEC`, close aggressively, monitor fd counts like memory.
3. **OOM-score blindness**: the batch job with 90% of RAM gets killed instead of the leaking sidecar — check `/proc/<pid>/oom_score_adj` and set cgroup limits deliberately.
4. **Blocking the event loop on syscalls**: one synchronous DNS lookup or unbuffered read stalls all multiplexed connections. Keep the hot path nonblocking; push blocking work to a pool.
5. **fsync confusion**: `write()` returns after the page cache, not the disk — durability needs `fsync`/`fdatasync` (and directory fsync on file creation). Databases earn their reputation handling exactly this.
6. **Zombie and orphan drift**: parents that never `wait()` accumulate zombies; double-fork daemons and supervisors (systemd) exist to reap reliably. Monitor process counts, not just CPU.

## Related Concepts

- [[concepts/computer-science/processes-and-threads|Processes and Threads]] (deep dive on execution units)
- [[concepts/computer-science/virtual-memory|Virtual Memory]] (paging, TLB, address translation)
- [[concepts/computer-science/concurrency-vs-parallelism|Concurrency vs Parallelism]] (what the scheduler multiplexes)
- [[concepts/computer-science/caching|Caching]] (page cache as the OS cache layer)

## References

- Tanenbaum & Bos — *Modern Operating Systems* (concepts, scheduling, memory, files)
- Love — *Linux Kernel Development*; Bovet & Cesati — *Understanding the Linux Kernel*
- Arpaci-Dusseau & Arpaci-Dusseau — *Operating Systems: Three Easy Pieces* (free, ostep.org)
- Kerrisk — *The Linux Programming Interface* (syscalls, signals, IPC reference)
- Corbet, Rubini & Kroah-Hartman — *Linux Device Drivers*; lwn.net kernel coverage
