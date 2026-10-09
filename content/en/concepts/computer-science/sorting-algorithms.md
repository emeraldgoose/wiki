---
title: Sorting Algorithms
description: "Seminar-level concept: comparison and non-comparison sorts, complexity table, stability, and how to choose"
tags: [concept, computer-science, algorithms, sorting]
locale: en
published: 2026-09-06
---

# Sorting Algorithms

[한국어 버전](/ko/concepts/computer-science/sorting-algorithms.md)

> Sorting arranges items in order and is the most-studied algorithm family: comparison sorts cost Ω(n log n) in the worst case, while non-comparison sorts exploit key structure to reach O(n).

## Definition

A **sorting algorithm** takes a sequence and permutes it into non-decreasing (or non-increasing) order according to a key. Two families exist:

- **Comparison sorts** order elements only via pairwise comparisons (`<`, `>`). Mergesort, quicksort, heapsort, insertion sort, bubble sort belong here.
- **Non-comparison sorts** exploit the structure of keys (integers in a range, digits, bits). Counting sort, radix sort, and bucket sort belong here and can beat the n log n barrier.

A sort is **stable** if equal keys keep their original relative order — important when sorting by one key and then another.

## Why It Matters

- **Ubiquity**: sorting underlies search indexes, database `ORDER BY`, ranking feeds, and the `sort()` in every standard library.
- **Complexity theory made concrete**: the Ω(n log n) lower bound for comparison sorts is most engineers' first encounter with a provable limit.
- **Design patterns catalog**: divide-and-conquer (mergesort, quicksort), heap data structures (heapsort), and incremental invariants (insertion sort) recur across all of algorithm design.
- **Performance cliffs**: picking bubble sort (O(n²)) where mergesort (O(n log n)) belongs is a classic production failure at scale.

## How It Works

### Complexity Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable | Notes |
|-----------|------|---------|-------|-------|--------|-------|
| Bubble sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Teaching only; never use in production |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Fast for tiny / nearly-sorted inputs |
| Selection sort | O(n²) | O(n²) | O(n²) | O(1) | No | Minimal swaps (O(n)) |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Predictable; classic divide-and-conquer |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Fastest in practice with good pivot; library default (introsort) |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | In-place with guaranteed bound |
| Counting sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | Integer keys in range k |
| Radix sort | O(d·n) | O(d·n) | O(d·n) | O(n+k) | Yes | d digits; great for fixed-width keys |
| Bucket sort | O(n+k) | O(n+k) | O(n²) | O(n) | Yes | Uniformly distributed keys |

k = key range, d = number of digits.

### The n log n Lower Bound (Sketch)

A comparison sort's decisions form a binary decision tree: each comparison branches two ways, and each of the n! possible permutations needs its own leaf. A binary tree with n! leaves has height at least log₂(n!) = Θ(n log n) by Stirling's approximation. Hence **no comparison sort can beat Ω(n log n) worst-case comparisons** — mergesort and heapsort are asymptotically optimal.

### How the Key Algorithms Work

**Quicksort (divide-and-conquer).** Pick a pivot, partition so smaller elements go left and larger go right, recurse on both sides:

```python
def quicksort(xs):
    if len(xs) <= 1:
        return xs
    pivot = xs[len(xs) // 2]
    left = [x for x in xs if x < pivot]
    mid = [x for x in xs if x == pivot]
    right = [x for x in xs if x > pivot]
    return quicksort(left) + mid + quicksort(right)
```

Average O(n log n); worst O(n²) when pivots are always extreme (e.g. sorted input with first-element pivot). Production libraries use **introsort** (quicksort + heapsort fallback) and median-of-three pivots to avoid the worst case.

**Mergesort (divide-and-conquer).** Split in half, sort each half, merge two sorted runs in linear time. Always O(n log n) but needs O(n) extra space (or a complex in-place variant).

**Heapsort.** Build a max-heap in O(n), then repeatedly extract the max (O(log n) each, n times). In-place, guaranteed O(n log n), but poor cache locality makes it slower than quicksort in practice.

**Counting sort (non-comparison).** For integers in `[0, k)`, count occurrences then write back:

```python
def counting_sort(xs, k):
    counts = [0] * k
    for x in xs:
        counts[x] += 1
    out = []
    for value, c in enumerate(counts):
        out.extend([value] * c)
    return out  # O(n + k) time
```

### Choosing a Sort

1. **General purpose**: trust the standard library (`sort`/`sorted` — usually Timsort or introsort hybrids).
2. **Nearly sorted or tiny (n < ~20)**: insertion sort.
3. **Guaranteed bound + O(1) space**: heapsort.
4. **Stable with guarantees**: mergesort.
5. **Integer keys, small range**: counting/radix sort.

## Common Pitfalls

- **Using an O(n²) sort "because n is small" without measuring.** n grows; today's 100 rows are next year's 10 million. Default to the library sort.
- **Assuming quicksort is always fast.** Adversarial or already-sorted input with a naive pivot degrades to O(n²) — a real denial-of-service vector (hence randomized pivots / introsort).
- **Ignoring stability.** Sorting users by signup date and then by country with an unstable second sort scrambles the first ordering. Chain sorts back-to-front with a stable sort, or sort on a tuple key.
- **Sorting when you don't need to.** Top-k needs only a heap (O(n log k)); membership needs only a [[concepts/computer-science/hash-tables|Hash Table]] (O(1)).
- **Counting/radix sort with huge k.** O(n + k) is only linear when k is small relative to n; a 32-bit key range makes counting sort infeasible.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] — the vocabulary for comparing sorts
- [[concepts/computer-science/trees|Trees]] — heapsort runs on a binary heap; BSTs sort via in-order traversal
- [[concepts/computer-science/hash-tables|Hash Tables]] — the O(1) alternative when order is not needed

## References

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 6–8 (heapsort, quicksort, linear-time sorts).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 2 (sorting).
- Tim Peters — Timsort description (CPython's hybrid merge/insertion sort).
