---
title: Distributed Consensus
description: "Agreement in the presence of faults: Paxos, Raft, BFT, quorums, and the FLP impossibility result"
tags: [concept, computer-science, distributed-systems, consensus]
locale: en
published: 2026-09-06
---

# Distributed Consensus

> 한국어: [한국어 버전](/ko/concepts/computer-science/distributed-consensus)

**Summary:** Distributed consensus lets a group of machines agree on a single value (or an ordered log of values) even when some machines crash or messages are delayed. It is the foundation of replicated state machines — etcd, ZooKeeper, Consul — and therefore of leader election, configuration stores, and strongly consistent metadata in every orchestrator. The core results: **FLP impossibility** (no deterministic protocol in fully asynchronous networks with one faulty process), and practical protocols **Paxos** and **Raft** that work around it with timeouts, majorities, and leader election.

## Definition

- **Consensus problem:** N processes each propose a value; all correct processes must eventually *decide* the same value, which must have been proposed by someone (validity), with termination guaranteed.
- **State-machine replication:** run consensus repeatedly to agree on an ordered log of commands; every replica executes the same log and stays identical. This is what Raft/etcd actually ship.
- **Fault models:** *crash-stop* (a node halts silently) vs. *Byzantine* (a node behaves arbitrarily, including maliciously). Crash tolerance needs 2f+1 nodes for f failures; Byzantine needs 3f+1.
- **Quorum:** any majority (⌊N/2⌋+1). Two majorities always overlap, so a value accepted by a majority cannot be silently overwritten — the intersection property every protocol below relies on.

## Why It Matters

- **Every control plane depends on it.** Kubernetes stores cluster state in etcd (Raft); service discovery, locks, and config in Consul/ZooKeeper all assume a consistent log.
- **It draws the consistency boundary.** If you need linearizable metadata across failures, you need consensus — there is no lighter primitive. Knowing this stops teams from hand-rolling "simple" leader election that splits brain under partitions (see [[cap-theorem]]).
- **Blockchains are consensus under Byzantine faults.** PBFT, Tendermint, and Nakamoto consensus are the same problem with an adversarial fault model.

## How It Works

### FLP impossibility (Fischer–Lynch–Paterson, 1985)

In a *fully asynchronous* network (no bounds on message delay) with at least one faulty process, **no deterministic consensus protocol guarantees termination**. Intuition: the protocol can never distinguish a crashed node from a slow one, so an adversarial schedule keeps the system bivalent (undecided) forever. Practical escape: add partial synchrony — timeouts and failure detectors (which is what real systems do).

### Paxos (Lamport, 1998)

- **Roles:** proposers, acceptors, learners. Protocol runs in two phases per ballot number n:
  1. **Prepare(n)/Promise:** proposer asks a majority to promise to ignore ballots < n; acceptors return the highest-numbered value they already accepted.
  2. **Accept(n, v)/Accepted:** proposer sends v (its own value, or the returned one with the highest ballot — this rule preserves agreement); acceptors accept unless they promised a higher ballot.
- A value accepted by a majority is *chosen*; the "highest-ballot" rule guarantees later ballots propose the same value.
- Famously hard to implement correctly from the original paper; Multi-Paxos (steady leader skipping phase 1) is what systems approximate.

### Raft (Ongaro & Ousterhout, 2014)

Designed for understandability; decomposes consensus into three pieces:

1. **Leader election:** followers time out (randomized 150–300 ms) and become candidates; a candidate with a majority of votes becomes leader for a *term*. Randomization prevents split votes.
2. **Log replication:** leader accepts client commands, appends them, replicates via AppendEntries RPCs; a command is *committed* once on a majority, then applied to the state machine.
3. **Safety:** election restriction — a candidate wins only if its log is at least as up-to-date as a majority's — guarantees a leader holds every committed entry, so committed entries are never lost or overwritten.

### Byzantine fault tolerance (PBFT, Castro–Liskov 1999)

- 3f+1 replicas tolerate f Byzantine faults. Three-phase protocol (pre-prepare → prepare → commit) with 2f+1 matching messages per phase; message authentication (MACs/signatures) prevents forgery.
- Cost: O(n²) messages per decision — the reason BFT historically stayed in small clusters, and why modern chains invest in linear-complexity variants (HotStuff).

## Common Pitfalls

- **Hand-rolled leader election without a quorum.** Time-based "highest IP wins" or database-flag schemes double-elect under partitions. Use a real consensus store for leadership.
- **Ignoring the FLP assumption.** Protocols that are "correct" in tests hang in production when DNS/GC pauses look like asynchrony — always pair consensus with timeouts, retries with jitter, and pre-vote (Raft pre-vote prevents disruptive re-elections).
- **Reading from the leader without a check.** A partitioned leader serves stale reads. Use read-index/lease reads, or route linearizable reads through a quorum.
- **Even node counts.** 4 nodes tolerate the same 1 failure as 3 but need 3 for quorum — slower with no extra resilience. Prefer odd numbers (3, 5).
- **Confusing consensus with gossip.** Epidemic/gossip protocols disseminate data but do not agree on order under faults — use them for membership (SWIM), not for the metadata log.

## See Also

- [[cap-theorem]] — why consensus systems choose consistency over availability during partitions
- [[complexity-classes]] — impossibility and hardness as neighboring ideas

## References

- Fischer, Lynch & Paterson, "Impossibility of Distributed Consensus with One Faulty Process" (1985).
- Lamport, "The Part-Time Parliament" (1998); Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" (2014).
- Castro & Liskov, "Practical Byzantine Fault Tolerance" (1999).
