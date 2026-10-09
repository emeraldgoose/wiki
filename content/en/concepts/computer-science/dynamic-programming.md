---
title: Dynamic Programming
description: "Seminar-level concept: overlapping subproblems, optimal substructure, memoization vs tabulation"
tags: [concept, computer-science, algorithms, dynamic-programming, optimization]
locale: en
published: 2026-09-06
---

# Dynamic Programming

[한국어 버전](/ko/concepts/computer-science/dynamic-programming.md)

> Dynamic programming solves problems by breaking them into overlapping subproblems: solve each distinct subproblem once, store the answer, and reuse it — turning exponential brute force into polynomial time.

## Definition

**Dynamic programming (DP)** is a technique for problems with two properties:

1. **Overlapping subproblems**: a naive recursion solves the same subproblems repeatedly (unlike divide-and-conquer, where subproblems are distinct).
2. **Optimal substructure**: an optimal solution is built from optimal solutions of subproblems (e.g. the shortest path to D via C contains the shortest path to C).

Two implementation styles:

- **Memoization (top-down)**: write the natural recursion, cache results in a table (often a [[concepts/computer-science/hash-tables|Hash Table]] or array) so each subproblem is computed once.
- **Tabulation (bottom-up)**: fill a table iteratively from base cases up to the answer — no recursion, usually less memory overhead.

## Why It Matters

- **Exponential → polynomial**: naive Fibonacci is O(2ⁿ); memoized it is O(n). The same leap powers sequence alignment, speech recognition, and resource allocation.
- **Core interview topic**: knapsack, coin change, longest increasing/common subsequence, and edit distance are DP canonicals.
- **Real systems**: Unix `diff` (longest common subsequence), Viterbi decoding in communications, Floyd-Warshall and Bellman-Ford in routing (see [[concepts/computer-science/graphs|Graphs]]), operation scheduling, and inventory optimization.
- **Thinking tool**: the "define the state, write the recurrence" discipline transfers to reinforcement learning (Bellman equations are DP over MDPs).

## How It Works

### The Canonical Example: Fibonacci

Naive recursion recomputes the same values exponentially many times (`fib(5)` calls `fib(3)` twice, `fib(2)` three times, …):

```python
# O(2^n) — recomputes subproblems
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

Memoization (top-down) — each `fib(k)` computed once:

```python
# O(n) time, O(n) space
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

Tabulation (bottom-up) — build from base cases:

```python
# O(n) time, O(1) space (only two prior values needed)
def fib_tab(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### The DP Recipe

1. **Define the state**: what do the subproblem parameters mean? (e.g. `dp[i][w]` = best value using the first `i` items with capacity `w`).
2. **Write the recurrence**: how does the answer combine smaller answers? (e.g. `dp[i][w] = max(dp[i-1][w], dp[i-1][w-w_i] + v_i)`).
3. **Set base cases**: `dp[0][*] = dp[*][0] = 0`.
4. **Choose evaluation order**: iterate so dependencies are already computed (bottom-up), or recurse + memoize.
5. **Reconstruct (optional)**: backtrack through the table to recover the actual choices, not just the optimal value.

### Classic Problems Table

| Problem | State | Recurrence idea | Complexity |
|---------|-------|-----------------|------------|
| 0/1 Knapsack | `dp[i][w]` | Take or skip item i | O(n·W) |
| Coin change (min coins) | `dp[x]` | `1 + min(dp[x-c])` over coins c | O(amount·coins) |
| Longest Common Subsequence | `dp[i][j]` | Match → `dp[i-1][j-1]+1`, else max of neighbors | O(n·m) |
| Edit distance | `dp[i][j]` | Min of insert / delete / substitute | O(n·m) |
| Longest Increasing Subsequence | `dp[i]` | `1 + max(dp[j])` for `a[j] < a[i]` | O(n²), O(n log n) optimized |
| Matrix chain multiplication | `dp[i][j]` | Best split point k between i and j | O(n³) |

### Worked Mini-Example: Coin Change

Coins `[1, 3, 4]`, amount 6. `dp[x]` = fewest coins for amount x:

```
dp[0]=0
dp[1]=1 (1)   dp[2]=2 (1+1)   dp[3]=1 (3)
dp[4]=1 (4)   dp[5]=2 (4+1)   dp[6]=2 (3+3)
```

Answer `dp[6] = 2` (3+3). Greedy (always take 4) would give 4+1+1 = 3 coins — wrong, which is exactly why DP is needed.

## Common Pitfalls

- **Applying DP without optimal substructure.** If the optimal solution does not compose from optimal subsolutions (e.g. longest *simple* path — subpaths of an optimal path need not be optimal), DP gives wrong answers. Verify the property first.
- **Applying DP without overlapping subproblems.** Mergesort's subproblems are distinct — memoizing buys nothing. DP's win comes from reuse.
- **State too small (missing dimensions).** Knapsack needs both item index and remaining capacity; dropping a dimension silently produces greedy, incorrect results. When answers look wrong, a missing state dimension is suspect #1.
- **Wrong iteration order in tabulation.** If `dp[i]` depends on `dp[i-1]`, iterate i upward; iterating downward reads stale values. For 2D tables, check whether the recurrence reads the current row (then iterate carefully or copy).
- **Recursion depth in memoization.** Top-down DP on n = 10⁵ recurses 10⁵ deep — Python's default limit is 1,000. Switch to tabulation or raise the limit with an explicit stack.
- **Pseudo-polynomial confusion.** O(n·W) knapsack is polynomial in the *values* but exponential in input *bits* — it is pseudo-polynomial, not truly polynomial. It breaks down for huge W.
- **Forgetting reconstruction.** Many tasks need the choices (which items? which alignment?), not just the value — keep parent pointers or backtrack.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] — the exponential-to-polynomial payoff, pseudo-polynomial subtlety
- [[concepts/computer-science/graphs|Graphs]] — Bellman-Ford and Floyd-Warshall as DP over paths; DAG shortest path as the simplest DP
- [[concepts/computer-science/hash-tables|Hash Tables]] — memoization storage
- [[concepts/computer-science/trees|Trees]] — recursion trees showing overlap vs. distinct subproblems

## References

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 14–15 (DP: rod cutting, matrix chain, LCS).
- Bellman — *Dynamic Programming* (1957, the origin).
- Kleinberg & Tardos — *Algorithm Design*, Ch. 6 (DP design patterns).
