---
title: CAP Theorem
description: "Seminar-level concept: consistency, availability, partition tolerance, proof intuition, PACELC, CP vs AP design"
tags: [concept, computer-science, cap-theorem, distributed-systems, consistency, availability, partition-tolerance]
published: 2026-09-06
locale: en
---

# CAP Theorem

The **CAP theorem** states that a distributed data store can simultaneously guarantee at most two of three properties: **Consistency**, **Availability**, and **Partition tolerance**. Since network partitions cannot be wished away, the real design choice is how the system behaves *when a partition occurs*: refuse some requests (CP) or serve possibly stale data (AP).

## Definition

- **Consistency (C)** — linearizability in the Gilbert–Lynch formulation: every read receives the most recent write or an error. All nodes agree on a single total order of operations, as if there were one copy of the data.
- **Availability (A)** — every request from a non-failing node receives a (non-error) response, with no guarantee it is the freshest value. The system stays up and answering.
- **Partition tolerance (P)** — the system continues to satisfy its guarantees despite an arbitrary number of messages being dropped or delayed between nodes. A partition splits the cluster into groups that cannot communicate.
- **The impossibility**: under a partition, a node on each side receives a write and a read for the same key. To stay consistent it must coordinate across the partition (impossible — messages are lost), so it must either block/error (sacrifice A) or answer from local state (sacrifice C). Hence: pick CP or AP *during partitions*.

## Why It Matters

- **Partitions are inevitable**: switches fail, cables are cut, GC pauses exceed timeouts, cloud AZs isolate. P is not optional for any system spanning machines — which is why practitioners say "of the three, you must have P; the choice is C vs A."
- **It frames every store's contract**: etcd and ZooKeeper choose CP (minority side refuses writes); Cassandra and Dynamo-style stores choose AP (all sides accept writes, reconcile later). Knowing which side your store is on predicts its failure behavior.
- **Consistency has a latency cost**: linearizable reads/writes need quorum round-trips (Raft/Paxos). AP reads are local and fast. The C-vs-A choice is also a latency-vs-correctness choice, visible in p99s.
- **Business semantics decide**: a ledger that double-spends is worthless (needs C); a shopping cart that errors during a partition loses sales (wants A). CAP forces the product conversation, not just the engineering one.

## How It Works

### The Gilbert–Lynch Proof Intuition

```
Partition:  [Node A]  ✕ ✕ ✕  [Node B]   (no messages pass)
Client 1 → A: WRITE x=1
Client 2 → B: READ x  → ??? (1 requires crossing the partition; stale 0 violates C; error/timeout violates A)
```

- Brewer conjectured it (PODC 2000 keynote); Gilbert and Lynch proved it (2002) for asynchronous networks: no algorithm can provide both safety (atomic consistency) and liveness (availability) under partition.
- The proof hinges on *asynchrony*: a slow node is indistinguishable from a dead/partitioned one, so waiting "long enough" cannot resolve the dilemma.

### CP vs AP in Practice

| Choice | During partition | Examples | Reconciliation |
|---|---|---|---|
| CP | Minority side errors/blocks; majority keeps linearizability | etcd, ZooKeeper, Consul (Raft), HBase, MongoDB (primary) | None needed — one truth preserved |
| AP | All sides serve; values diverge | Cassandra, DynamoDB (certain modes), Riak, CouchDB | Anti-entropy: vector clocks, CRDTs, last-write-wins, read repair |
| "CA" | Only possible on a single node or perfectly reliable network | Single-site RDBMS | N/A — a partition makes CA impossible |

- **Quorum arithmetic**: with N replicas, R + W > N gives read-your-write overlap (used by CP-leaning configs); R + W ≤ N allows availability with staleness (AP-leaning). Tunable consistency (Cassandra's ONE/QUORUM/ALL) is literally a CAP slider.
- **PACELC extension** (Abadi, 2012): "if Partition, A-or-C; Else, Latency-or-Consistency." Even without partitions, synchronous replication trades latency for consistency — the choice never fully disappears.

### AP Reconciliation Machinery

- **Vector clocks / version vectors**: track causality so concurrent writes are detected rather than silently lost (Dynamo paper, 2007).
- **CRDTs** (conflict-free replicated data types): data structures (counters, sets, maps) whose merges are mathematically confluent — AP without application-level conflict code.
- **Read repair and hinted handoff**: background mechanisms that converge replicas after healing (Cassandra); the system is *eventually consistent* — C sacrificed temporarily, restored over time.

## Common Pitfalls

1. **"We chose CA"**: running across availability zones or regions while claiming CA. The first real partition proves otherwise — usually as split-brain writes that no reconciliation handles.
2. **Conflating CAP-consistency with ACID**: CAP-C means linearizability of a single register; ACID serializability is about multi-operation transactions. A system can be ACID on one node and AP across nodes.
3. **Treating the choice as global**: different data wants different letters — auth sessions AP (stale session tolerable), payments CP (double-spend intolerable), often in the same product. Per-dataset tuning beats per-company dogma.
4. **Ignoring the latency half (the ELC)**: demanding linearizability for a global low-latency read path, then discovering every read pays a cross-region round trip. Put CP data close to its writers or relax to causal/eventual reads.
5. **Last-write-wins as default conflict policy**: wall-clock LWW silently drops concurrent writes under clock skew. Prefer CRDTs or explicit application merge for data users actually edit.
6. **No partition drills**: failover logic that never saw a real partition (firewall-drop game days, `iptables` chaos) fails exactly when needed. Test the minority-side behavior before production does.

## Related Concepts

- [[concepts/computer-science/distributed-consensus|Distributed Consensus]] (Raft/Paxos: how CP systems agree)
- [[concepts/computer-science/database-transactions|Database Transactions]] (isolation vs distributed consistency)
- [[concepts/computer-science/cap-theorem|CAP Theorem]] (this page)
- [[concepts/computer-science/tcp-ip|TCP/IP]] (timeouts and failure detection underneath)

## References

- Brewer, "Towards Robust Distributed Systems" (PODC 2000 keynote/invited talk)
- Gilbert & Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services" (ACM SIGACT News, 2002)
- Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design" (PACELC, IEEE Computer, 2012)
- DeCandia et al., "Dynamo: Amazon's Highly Available Key-Value Store" (SOSP 2007)
- Kleppmann — *Designing Data-Intensive Applications*, ch. 5/9 (replication, consistency models)
