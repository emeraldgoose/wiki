---
title: Graphs
description: "Seminar-level concept: graph representations, BFS, DFS, shortest paths, and classic graph algorithms"
tags: [concept, computer-science, data-structures, graphs, bfs, dfs, shortest-path]
locale: en
published: 2026-09-06
---

# Graphs

> A graph models entities as vertices connected by edges, and two traversals — breadth-first and depth-first search — unlock shortest paths, connectivity, topological ordering, and cycle detection across networks, maps, and dependency systems.

## Definition

A **graph** G = (V, E) consists of **vertices** (nodes) and **edges** (links between pairs of vertices). Key distinctions:

- **Directed vs. undirected**: edges have a direction (follower → followee, dependency → dependent) or not (friendship, roads).
- **Weighted vs. unweighted**: edges carry costs (distance, latency, price) or are uniform.
- **Cyclic vs. acyclic**: a **DAG** (directed acyclic graph) has directed edges but no directed cycles — the shape of build dependencies, task schedules, and version histories.
- **Connected vs. disconnected**: whether a path exists between every pair of vertices.
- **Degree**: number of edges incident to a vertex (in-degree / out-degree in directed graphs).

## Why It Matters

- **The world is a graph**: social networks, road maps, the web link graph, package dependencies, circuit layouts, and ML computation graphs.
- **Two traversals, dozens of applications**: BFS gives shortest paths in unweighted graphs; DFS gives topological order, cycle detection, and connected components.
- **Routing and planning**: shortest-path algorithms (Dijkstra, Bellman-Ford, A\*) run navigation, network routing, and logistics.
- **Scheduling**: topological sort on a DAG orders builds, course prerequisites, and task pipelines.

## How It Works

### Representations

| Representation | Space | Edge query | Iterate neighbors | Best for |
|----------------|-------|------------|-------------------|----------|
| Adjacency list | O(V + E) | O(degree) | O(degree) | Sparse graphs (most real graphs); default choice |
| Adjacency matrix | O(V²) | O(1) | O(V) | Dense graphs; fast edge-existence tests |
| Edge list | O(E) | O(E) | O(E) | Kruskal's algorithm; simple serialization |

```python
# Adjacency list (directed, unweighted)
graph = {
    "a": ["b", "c"],
    "b": ["d"],
    "c": ["d"],
    "d": [],
}
```

### BFS vs. DFS

```python
from collections import deque

def bfs(graph, start):
    seen = {start}
    queue = deque([start])
    order = []
    while queue:
        v = queue.popleft()          # FIFO → level by level
        order.append(v)
        for w in graph[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return order                     # O(V + E)

def dfs(graph, start, seen=None, order=None):
    if seen is None:
        seen, order = set(), []
    seen.add(start)
    order.append(start)
    for w in graph[start]:           # LIFO (recursion) → go deep first
        if w not in seen:
            dfs(graph, w, seen, order)
    return order                     # O(V + E)
```

| Aspect | BFS (queue) | DFS (stack/recursion) |
|--------|-------------|----------------------|
| Explores | Level by level | One path to the end first |
| Shortest path (unweighted) | Yes | No |
| Memory | O(V) frontier can be wide | O(V) but usually slimmer |
| Natural uses | Shortest path, nearest neighbors, bipartite check | Topological sort, cycle detection, components |

### Classic Algorithms

| Problem | Algorithm | Complexity | Notes |
|---------|-----------|-----------|-------|
| Shortest path, unweighted | BFS | O(V + E) | From a single source |
| Shortest path, non-negative weights | Dijkstra (with binary heap) | O((V + E) log V) | Fails on negative weights |
| Shortest path, negative weights allowed | Bellman-Ford | O(V·E) | Detects negative cycles |
| Shortest path with heuristic | A\* | O(b^d) typical | Dijkstra + heuristic; game pathfinding |
| All pairs | Floyd-Warshall | O(V³) | Simple DP; small dense graphs |
| Minimum spanning tree | Kruskal / Prim | O(E log E) / O((V+E) log V) | Connect all vertices cheapest |
| Topological order (DAG) | Kahn's / DFS finish order | O(V + E) | Build systems, schedulers |
| Strongly connected components | Kosaraju / Tarjan | O(V + E) | Directed-graph clusters |

### Topological Sort Example

For course prerequisites `intro → algorithms → ML`, DFS finishing order (or Kahn's in-degree peeling) yields a valid study order. If a cycle exists (A requires B requires A), no topological order exists — the cycle itself is the diagnosis (deadlock, circular dependency).

## Common Pitfalls

- **Dijkstra on negative weights.** Even one negative edge breaks Dijkstra's greedy assumption; use Bellman-Ford (and check for negative cycles, which make "shortest" undefined).
- **Forgetting the visited set.** Without it, traversals loop forever on cyclic graphs or blow up exponentially re-visiting shared subgraphs (a DAG is not a [[concepts/computer-science/trees|Tree]] — nodes have multiple parents).
- **Recursion depth on large graphs.** Recursive DFS on a million-node graph overflows the call stack; use an explicit stack.
- **Adjacency matrix for sparse graphs.** A million-vertex social graph as a matrix needs 10¹² entries — always use adjacency lists for sparse real-world graphs.
- **Treating disconnected graphs as connected.** Always loop traversals over all vertices (`for v in V: if unseen: search(v)`) or later components are silently missed.
- **Confusing BFS order with weighted shortest path.** BFS levels count *edges*, not cost — with weights, few edges can still mean huge cost.

## Related Concepts

- [[concepts/computer-science/trees|Trees]] — connected acyclic graphs; BFS/DFS traverse both
- [[concepts/computer-science/dynamic-programming|Dynamic Programming]] — Floyd-Warshall and Bellman-Ford are DP over paths
- [[concepts/computer-science/big-o-notation|Big-O Notation]] — O(V + E) linear-time traversal analysis

## References

- Cormen et al. — *Introduction to Algorithms* (CLRS), Ch. 22–26 (graph algorithms, MST, shortest paths).
- Sedgewick & Wayne — *Algorithms*, 4th ed., Ch. 4 (graphs).
- Dijkstra — "A Note on Two Problems in Connexion with Graphs" (1959).
