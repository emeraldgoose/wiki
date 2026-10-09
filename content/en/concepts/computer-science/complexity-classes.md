---
title: Complexity Classes
description: "P, NP, NP-completeness, and beyond: what complexity classes tell engineers about tractability"
tags: [concept, computer-science, complexity, algorithms]
locale: en
published: 2026-09-06
---

# Complexity Classes

> 한국어: [한국어 버전](/ko/concepts/computer-science/complexity-classes)

**Summary:** Complexity classes group decision problems by the resources (time, space, randomness) needed to solve or verify them. The most important pair is **P** (solvable in polynomial time) versus **NP** (verifiable in polynomial time); whether they are equal is the most famous open problem in computer science. For engineers, the practical payoff is recognizing **NP-complete** problems so you stop hunting for an exact polynomial algorithm and switch to approximation, heuristics, or parameterized approaches.

## Definition

- **Decision problem:** a yes/no question about an input (e.g., "does this graph have a Hamiltonian cycle?"). Complexity theory classifies these by resource bounds on a Turing machine.
- **P:** problems solvable in polynomial time, O(n^k) for some fixed k. The working definition of "tractable."
- **NP:** problems whose *yes* answers have certificates verifiable in polynomial time. Equivalently, solvable in polynomial time on a *nondeterministic* machine. (NP = "nondeterministic polynomial," **not** "non-polynomial.")
- **NP-complete:** the hardest problems in NP — every NP problem reduces to them in polynomial time. A polynomial algorithm for one would collapse all of NP into P.
- **NP-hard:** problems at least as hard as NP-complete ones, but not necessarily in NP (often optimization versions, e.g., "find the shortest tour" vs. "is there a tour shorter than k?").
- **Beyond NP:** PSPACE (polynomial space), EXP (exponential time), BPP (polynomial time with bounded-error randomness). Known containments: P ⊆ NP ⊆ PSPACE ⊆ EXP; BPP sits between P and PSPACE.

## Why It Matters

- **Stops wasted effort.** Recognizing your scheduling / packing / routing problem as NP-hard (e.g., bin packing, traveling salesperson, graph coloring) tells you to reach for ILP solvers, approximation algorithms, or heuristics instead of a perfect fast algorithm that likely does not exist.
- **Explains scaling cliffs.** An O(2^n) exact algorithm that is fine at n=20 is dead at n=100. Class membership predicts this before you benchmark.
- **Grounds crypto.** Modern cryptography (see [[cryptography-basics]]) assumes certain problems (factoring, discrete log) are hard; complexity theory is the language for stating that assumption.
- **Interview and design relevance.** "Can we do this optimally in production?" is a complexity question in disguise.

## How It Works

### Polynomial-time reduction

Problem A reduces to problem B (A ≤ₚ B) if any instance of A can be transformed into an instance of B in polynomial time, preserving the answer. If B were easy, A would be easy too. Reductions transfer hardness: reduce a *known* NP-complete problem to *your* problem to prove yours is NP-hard.

### The canonical NP-complete problem: SAT

- **SAT:** given a Boolean formula, is there an assignment making it true? The **Cook–Levin theorem** (1971) proved SAT is NP-complete — the first such proof, by showing any NP computation can be encoded as a formula.
- **3-SAT** (each clause has exactly 3 literals) is the usual reduction source because its rigid structure is easy to build gadgets from.
- Thousands of problems were then proven NP-complete by reduction chains: 3-SAT → independent set → vertex cover → Hamiltonian cycle → TSP decision version.

### A concrete example: vertex cover

- **Problem:** does graph G have a set of ≤ k vertices touching every edge?
- **Certificate:** the set itself — verify in O(|E|) by checking each edge has an endpoint in it. So it is in NP.
- **Hardness:** reduce from independent set (complement of a vertex cover is an independent set). Hence NP-complete.
- **Engineering escape hatches:** 2-approximation in linear time (take both endpoints of any maximal matching); fixed-parameter tractable in O(2^k · n); exact branch-and-bound fine for small k.

### The class landscape

```
P ⊆ NP ⊆ PSPACE ⊆ EXP        (all ⊆ believed strict, only P ≠ EXP proven)
RP ⊆ BPP ⊆ PSPACE            (randomized classes)
P ⊆ RP, P ⊆ BPP              (randomness never hurts, conjecturally helps little)
```

- **Savitch's theorem:** NSPACE(s) ⊆ DSPACE(s²), so NPSPACE = PSPACE — nondeterminism buys at most a quadratic space saving.
- **Time hierarchy theorem:** more time provably buys more power (there are problems in EXP not in P).

## Common Pitfalls

- **"NP means non-polynomial / always exponential."** Wrong on both counts: NP is nondeterministic polynomial, and many NP problems (shortest path, 2-SAT, matching) are in P.
- **"NP-hard means hopeless."** It means *exact worst-case polynomial* is unlikely. Approximation ratios (e.g., 3/2 for metric TSP via Christofides), pseudo-polynomial DP (knapsack in O(nW)), and FPT algorithms routinely solve real instances.
- **"P vs NP is settled / irrelevant."** It is open (Clay Millennium Prize), and it matters: P = NP would break most public-key crypto overnight.
- **Confusing decision vs. optimization.** Showing the decision version is NP-complete classifies the optimization version as NP-hard — state which one you mean.
- **Reductions go the wrong way.** To prove your problem H is hard, reduce a *known-hard* problem *to* H, not H to the known problem.

## See Also

- [[cryptography-basics]] — hardness assumptions in practice
- [[distributed-consensus]] — impossibility results (FLP) as the distributed analogue of hardness

## References

- Sipser, *Introduction to the Theory of Computation* (3rd ed.) — Chapters 7–9, the standard textbook treatment.
- Garey & Johnson, *Computers and Intractability* — the NP-completeness catalog.
- Cook–Levin theorem; Karp's 21 NP-complete problems (1972).
