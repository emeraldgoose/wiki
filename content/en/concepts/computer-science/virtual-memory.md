---
title: Virtual Memory
description: "Seminar-level concept: address spaces, paging, page tables, TLB, swapping, mmap, copy-on-write"
tags: [concept, computer-science, virtual-memory, paging, mmu, operating-systems]
published: 2026-09-06
locale: en
---

# Virtual Memory

> [한국어 버전](/ko/concepts/computer-science/virtual-memory)

**Virtual memory** gives every process the illusion of a large, private, contiguous address space, while the OS and MMU transparently map virtual pages onto physical RAM (or disk). It is the mechanism behind process isolation, efficient memory use, and memory-mapped files.

## Definition

- **Virtual address space**: the set of addresses a process may use (e.g., 128 TB of user space on x86-64 Linux). Split into **pages** (typically 4 KB; huge pages 2 MB / 1 GB).
- **Physical memory**: actual RAM frames. The **MMU** (Memory Management Unit) translates each virtual address via **page tables**; the **TLB** (Translation Lookaside Buffer) caches recent translations in hardware.
- **Paging**: the OS keeps a per-process multi-level page table mapping virtual page numbers → physical frame numbers plus permission bits (read/write/execute, user/supervisor, present).
- **Demand paging / swapping**: pages not resident in RAM trigger a **page fault**; the kernel loads the page from disk (or allocates a zero page) and resumes the process. Cold pages can be evicted to swap.

## Why It Matters

- **Isolation**: processes cannot name each other's memory — a pointer in process A is meaningless in process B. This is the hardware foundation of OS security and stability.
- **Overcommit and efficiency**: processes routinely map more virtual memory than physical RAM exists (sparse heaps, lazy stacks, shared libraries mapped once). Only touched pages consume frames.
- **Simplified programming**: linkers and loaders see a fixed layout (code, heap growing up, stack growing down, mmap region); programmers never manage physical placement.
- **Performance lever**: page size, TLB hit rate, NUMA placement, and swap behavior directly determine memory-bound workload performance.

## How It Works

### Address Translation Walk (x86-64, 4-Level)

```
virtual addr = [9-bit PML4][9-bit PDPT][9-bit PD][9-bit PT][12-bit offset]
CR3 → PML4 → PDPT → PD → PT → frame + offset = physical address
```

- Each level is a 4 KB table of 512 8-byte entries. A full translation costs up to 4 memory reads — which is why the **TLB** (typically ~64–1500 entries, split L1/L2) exists: hits avoid the walk entirely.
- **Huge pages** (2 MB/1 GB) collapse levels and multiply TLB reach (one entry covers 2 MB instead of 4 KB). Databases and JVMs use them (`hugetlbfs`, Transparent Huge Pages) to cut TLB misses.

### Page Faults: Minor vs Major

- **Minor fault**: page is in RAM but not yet mapped (first touch of anonymous memory, COW break). Handled without disk I/O — just fix up the table.
- **Major fault**: page must be read from disk (file-backed mmap, swap-in). The faulting thread sleeps; the major-fault rate is a first-class latency metric (`time`, `ps -o min_flt,maj_flt`).
- **Thrashing**: working set exceeds RAM → constant major faults → CPU idle while waiting on disk. Cure: add RAM, shrink working set, or move cold data out — never "tune" the pager first.

### mmap: Files as Memory

```c
void *p = mmap(NULL, len, PROT_READ, MAP_PRIVATE, fd, 0);
```

- Maps a file (or anonymous memory) into the address space. **Shared** mappings propagate writes to the file and other mappers (basis of shared libraries, IPC); **private** mappings are COW.
- `madvise()` hints (`SEQUENTIAL`, `RANDOM`, `WILLNEED`, `DONTNEED`, `HUGEPAGE`) let performance-sensitive code steer readahead and eviction.
- Most language runtimes allocate heaps via anonymous `mmap`, not `brk`/`sbrk`.

### Copy-on-Write and fork

- After `fork()`, parent and child share all physical pages read-only. The first write to a page faults, the kernel copies the page, and the writer gets a private copy. Result: fast process creation, lazy cost.
- The same mechanism backs shared libraries (code pages shared across all processes) and `MAP_PRIVATE` file mappings.

## Common Pitfalls

1. **Ignoring page-fault cost in latency budgets**: a single major fault costs ~ms (disk) vs ~ns (TLB hit). Memory-mapping a large file then touching it randomly produces tail latency that looks like "CPU slowness."
2. **Transparent Huge Pages + latency-sensitive allocators**: THP's background compaction (`khugepaged`) can stall processes; Redis's famous latency spikes under THP are the canonical example — `echo never > /sys/kernel/mm/transparent_hugepage/enabled` is standard Redis guidance.
3. **Overcommit surprises**: Linux's default heuristic overcommit lets `malloc` succeed and kills via **OOM killer** at touch time. Either size for it (`vm.overcommit_memory`, cgroup limits) or handle SIGKILL-via-OOM as a design input.
4. **Swapping on SSD treated as free**: swap on fast SSD still costs ~100 µs per fault — fine for cold pages, fatal for hot loops. Monitor `maj_flt` and swap-in rates, not just free RAM.
5. **NUMA blindness**: on multi-socket machines, a page lives on one node; remote access costs 1.3–2×. Pin threads and allocate locally (`numactl`, `mbind`) for memory-bound services.
6. **mmap without madvise**: default readahead assumes sequential access; random access over huge mappings wastes I/O and pollutes page cache. Tell the kernel your pattern.

## Related Concepts

- [[concepts/computer-science/processes-and-threads|Processes and Threads]] (per-process address spaces, fork/COW)
- [[concepts/computer-science/caching|Caching]] (page cache, TLB as a cache, cache hierarchies)

## References

- Silberschatz, Galvin, Gagne — *Operating System Concepts* (ch. 9–10: virtual memory, paging)
- Intel SDM Vol. 3A, ch. 4 — paging structures (authoritative x86-64 reference)
- Linux man pages: `mmap(2)`, `madvise(2)`, `mincore(2)`, `proc(5)` (`/proc/[pid]/maps`, `smaps`)
- Ulrich Drepper — "What Every Programmer Should Know About Memory"
