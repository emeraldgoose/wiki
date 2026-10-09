---
title: Big-O Notation
description: "Seminar-level concept: asymptotic complexity analysis, Big-O, Big-Omega, Big-Theta, and common complexity classes"
tags: [concept, computer-science, algorithms, complexity, big-o]
locale: en
published: 2026-09-06
---

# Big-O Notation

[한국어 버전](/ko/concepts/computer-science/big-o-notation.md)

> Big-O notation describes how an algorithm's running time or memory usage grows as input size grows — an asymptotic upper bound that lets engineers compare algorithms independently of hardware.

## Definition

Big-O notation characterizes the **asymptotic upper bound** of a function's growth rate. We say `f(n) = O(g(n))` if there exist positive constants `c` and `n0` such that `f(n) <= c * g(n)` for all `n >= n0`. In plain terms: past some input size, the cost grows no faster than `g(n)` up to a constant factor.

Related notations complete the picture:

| Notation | Meaning | Analogy |
|----------|---------|---------|
| `O(g(n))` (Big-O) | Asymptotic **upper** bound (worst case) | `<=` |
| `Ω(g(n))` (Big-Omega) | Asymptotic **lower** bound (best case) | `>=` |
| `Θ(g(n))` (Big-Theta) | **Tight** bound (both above and below) | `==` |
| `o(g(n))` (little-o) | Strictly slower-growing upper bound | `<` |

In practice, "the complexity of quicksort is O(n log n)" means average-case growth; its worst case is O(n²).

## Why It Matters

- **Algorithm selection**: An O(n log n) sort beats an O(n²) sort decisively at n = 10⁶, regardless of language or CPU. Constants rarely overcome a complexity-class gap at scale.
- **System design interviews and code review**: Complexity analysis is the shared vocabulary for arguing that a design will or will not scale.
- **Capacity planning**: Knowing an endpoint is O(n²) in the size of a user's follower list predicts exactly which customer will cause the first outage.
- **Communication**: It abstracts away hardware, compiler, and language so two engineers can compare approaches precisely.

## How It Works

### The Common Complexity Classes

Ordered from fastest- to slowest-growing:

| Class | Name | Example |
|-------|------|---------|
| O(1) | Constant | Hash-table lookup, array index access |
| O(log n) | Logarithmic | Binary search, balanced-tree operations |
| O(n) | Linear | Single scan of an array |
| O(n log n) | Linearithmic | Mergesort, heapsort, efficient sorts |
| O(n²) | Quadratic | Bubble sort, naive nested loops over pairs |
| O(n³) | Cubic | Naive matrix multiplication |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci, brute-force subsets |
| O(n!) | Factorial | Brute-force traveling salesman (all permutations) |

### Worked Examples

**O(1) — constant.** Accessing `arr[i]` costs the same whether the array has 10 or 10 million elements.

**O(n) — linear.** Finding the maximum with one pass:

```python
def find_max(xs):
    best = xs[0]
    for x in xs[1:]:      # n - 1 iterations
        if x > best:
            best = x
    return best           # O(n) time, O(1) extra space
```

**O(log n) — logarithmic.** Binary search halves the search space each step, so ~20 comparisons suffice for n = 10⁶ (2²⁰ ≈ 10⁶).

**O(n²) — quadratic.** Checking all pairs:

```python
def has_duplicate(xs):
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):  # ~n²/2 comparisons
            if xs[i] == xs[j]:
                return True
    return False
```

**Amortized analysis.** Appending to a dynamic array is O(1) amortized: most appends are O(1), and the occasional O(n) resize is spread across many appends.

### Rules of Thumb for Analysis

1. **Drop constants**: O(2n) → O(n). Constants depend on hardware anyway.
2. **Drop lower-order terms**: O(n² + n) → O(n²). The dominant term wins as n grows.
3. **Nested loops multiply; sequential steps add**: two nested n-loops → O(n²); two consecutive n-loops → O(n).
4. **State time vs. space separately**: an algorithm can be O(n) time and O(1) space (e.g. in-place reversal).

## Common Pitfalls

- **Confusing worst case with average case.** Hash-table lookup is O(1) average but O(n) worst case (all keys collide). Quicksort is O(n log n) average, O(n²) worst case. Always say which case you mean.
- **Ignoring the hidden constant.** For small n, an O(n²) algorithm with tiny constants can beat an O(n log n) one with huge constants. Complexity wins asymptotically, not universally — this is why insertion sort is used for tiny subarrays inside mergesort implementations.
- **Treating n inconsistently.** O(n) means different things if n is "number of bits" vs. "numeric value": trial division is O(√n) in the value but exponential in the number of bits — that is why it is not a polynomial-time primality test.
- **Forgetting space complexity.** A O(n) time / O(n) space solution (e.g. memoization) may be unusable under memory constraints where an O(n) time / O(1) space alternative exists.
- **Best-case reasoning about user-facing latency.** Users experience tail latency; analyze the worst case (or amortized worst case), not the best case.

## Related Concepts

- [[concepts/computer-science/sorting-algorithms|Sorting Algorithms]] — where O(n log n) vs. O(n²) decides real performance
- [[concepts/computer-science/hash-tables|Hash Tables]] — O(1) average-case lookups with O(n) worst case
- [[concepts/computer-science/dynamic-programming|Dynamic Programming]] — trading space for time to convert exponential into polynomial

## References

- Cormen, Leiserson, Rivest, Stein — *Introduction to Algorithms* (CLRS), Ch. 3: Growth of Functions.
- Knuth — *The Art of Computer Programming*, Vol. 1: Fundamental Algorithms (asymptotic analysis foundations).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 1.4: Analysis of Algorithms.
