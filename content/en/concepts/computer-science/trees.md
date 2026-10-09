---
title: Trees
description: "Seminar-level concept: binary trees, BSTs, balanced trees, heaps, traversals, and complexity"
tags: [concept, computer-science, data-structures, trees, bst, heap]
locale: en
published: 2026-09-06
---

# Trees

> A tree is a hierarchical structure of nodes connected by edges with no cycles: one root, parent–child links, and subtrees that make search, ordering, and priority operations logarithmic.

## Definition

A **tree** is a connected acyclic graph with a distinguished **root** node. Each node has zero or more **children**; nodes with no children are **leaves**. The **depth** of a node is its distance from the root; the **height** of the tree is the maximum depth. A **binary tree** restricts each node to at most two children (left and right).

Key specializations:

- **Binary Search Tree (BST)**: left subtree keys < node key < right subtree keys — in-order traversal yields sorted order.
- **Balanced BST** (AVL, red-black): rebalances on insert/delete to keep height O(log n).
- **Heap** (binary heap): complete tree with the heap property (parent ≥ children for max-heap) — O(1) max/min access, backs priority queues and heapsort.
- **Trie** (prefix tree): nodes keyed by characters/digits; strings sharing prefixes share paths — the structure behind autocomplete and IP routing tables.
- **B-tree / B+ tree**: wide, shallow trees (hundreds of children per node) matching disk-page sizes — the index structure of virtually every relational database.

## Why It Matters

- **Ordered data with dynamic updates**: balanced BSTs give O(log n) insert, delete, search, min/max, and predecessor/successor — something neither arrays nor [[concepts/computer-science/hash-tables|Hash Tables]] offer together.
- **Databases and filesystems**: B+ trees keep billions of rows searchable in 3–4 disk reads; ext4, NTFS, and HFS+ all use tree-structured metadata.
- **Scheduling and graphs**: heaps drive Dijkstra's algorithm, event schedulers, and top-k queries; parse trees and DOM trees model syntax and documents.
- **Ubiquitous in interviews**: tree traversals and BST validation are canonical recursion problems.

## How It Works

### Operations and Complexity

| Structure | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|-------|
| Binary Search Tree (unbalanced) | O(n) worst | O(n) worst | O(n) worst | O(n) |
| Balanced BST (AVL / red-black) | O(log n) | O(log n) | O(log n) | O(n) |
| Binary heap (min/max) | O(n) for arbitrary key | O(log n) | O(log n) for root | O(n) |
| Trie (key length m) | O(m) | O(m) | O(m) | O(total chars) |
| B-tree (branching b, n keys) | O(log_b n) | O(log_b n) | O(log_b n) | O(n) |

### BST Invariant and Example

```
      8
    /   \
   3     10
  / \      \
 1   6      14
```

In-order traversal (left → node → right) visits `1, 3, 6, 8, 10, 14` — sorted. Search for 6: compare with 8 (left), 3 (right), found — 3 comparisons along a root-to-leaf path, hence O(height).

### Traversals (with Uses)

| Traversal | Order | Use |
|-----------|-------|-----|
| In-order | left, node, right | Sorted output from a BST |
| Pre-order | node, left, right | Copying / serializing a tree |
| Post-order | left, right, node | Deleting a tree; evaluating expression trees |
| Level-order (BFS) | level by level | Shortest-path-style problems; printing by depth |

```python
def inorder(node):
    if node is None:
        return
    inorder(node.left)
    visit(node)        # keys emerge in sorted order for a BST
    inorder(node.right)
```

### How Balancing Works (Idea)

Insertions in order (1, 2, 3, 4, …) turn a naive BST into a linked list (height O(n)). Balanced trees restore logarithmic height with **rotations** — local restructurings that preserve the BST invariant:

- **AVL**: tracks per-node balance factors; rotates when any differ by more than 1. Stricter balance → faster lookups, more rotation overhead.
- **Red-black**: colors nodes red/black with invariants guaranteeing height ≤ 2·log₂(n+1). Looser balance → fewer rotations, the default in most standard libraries (`std::map`, Java `TreeMap`).
- **B-trees**: instead of rotating, split/merge wide nodes — minimizing disk reads rather than comparisons.

### Heaps in 30 Seconds

A max-heap keeps the largest element at the root; insert bubbles up, extract-max moves the last element to the root and sifts down — both O(log n). Heapsort and priority queues (task schedulers, Dijkstra's frontier) are the flagship applications.

## Common Pitfalls

- **Assuming a plain BST is O(log n).** Without balancing, sorted input degenerates to O(n). Interview and production code should use a balanced variant or a library ordered map.
- **Deleting from a BST incorrectly.** Deleting a node with two children requires replacing it with its in-order successor (or predecessor) — naively removing it breaks the invariant for its whole subtree.
- **Recursion depth on skewed trees.** Recursive traversals on a degenerate tree recurse O(n) deep and overflow the call stack; use iteration or guarantee balance.
- **Using a trie for everything string-like.** Tries are memory-hungry (a child pointer per alphabet symbol per node); for small sets a sorted list or hash table is leaner. Compressed variants (radix trees) fix this.
- **Confusing heap with sorted order.** A heap exposes only the min/max efficiently; finding an arbitrary element is O(n). Need full ordering? Use a balanced BST.
- **Forgetting B-trees are about I/O, not comparisons.** Their win is one node = one disk page, so depth 3–4 covers billions of keys. In-memory, their constant factors lose to red-black trees.

## Related Concepts

- [[concepts/computer-science/big-o-notation|Big-O Notation]] — O(log n) height arguments
- [[concepts/computer-science/sorting-algorithms|Sorting Algorithms]] — heapsort; BST in-order traversal as sorting
- [[concepts/computer-science/graphs|Graphs]] — trees are connected acyclic graphs; BFS/DFS traverse both
- [[concepts/computer-science/hash-tables|Hash Tables]] — the unordered O(1) alternative to ordered maps

## References

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 12–13, 18 (BSTs, red-black trees, B-trees).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 3.2–3.3, 2.4 (BSTs, balanced trees, heaps).
- Comer — "The Ubiquitous B-Tree" (the database index structure).
