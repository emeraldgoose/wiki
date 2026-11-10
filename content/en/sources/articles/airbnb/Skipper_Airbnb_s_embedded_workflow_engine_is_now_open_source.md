---
title: "Skipper, Airbnb's embedded workflow engine, is now open source"
description: "Airbnb open sources Skipper under Apache 2.0: a workflow engine that runs durable multi-step processes inside the service that owns them, using the service's own database instead of a shared orchestration cluster."
tags: [source, airbnb, workflow-engines, durable-execution, en]
locale: en
source_url: "https://airbnb.tech/open-source/skipper-airbnbs-embedded-workflow-engine-is-now-open-source"
blog: airbnb
published_date: 2026-11-11
---

# Skipper, Airbnb's embedded workflow engine, is now open source

**Source**: [Airbnb Tech Blog](https://airbnb.tech/open-source/skipper-airbnbs-embedded-workflow-engine-is-now-open-source) · **Published**: 2026-11-10

## Overview

Airbnb has released Skipper, the embedded workflow engine already used in production by several teams inside the company, under the Apache 2.0 licence. Skipper lets developers express a multi-step business process as a plain Java or Kotlin class, persist its progress, and recover from crashes and transient failures — all inside the service that owns the process, reusing that service's existing dependencies and database rather than adding a separate orchestration cluster. The repository ships the core engine together with documentation and runnable examples.

The motivation is the familiar set of problems that appear whenever a process spans several services, waits for human input, or mixes synchronous and asynchronous steps: it needs durable storage of what has already happened, what should be retried, and what is still pending. Solving that per process means repeatedly rebuilding the same machinery for partial failure, timers, and recovery, along with its tests and debugging. The established answer is a central orchestration service, self-hosted or managed, which gives many teams one platform to operate and monitor. Airbnb wanted something different: each service owning its workflows inside its existing deployment and database, so that critical services avoid an extra shared orchestration dependency and workflow execution stays in-process with no separate coordinator between steps.

That constraint shapes the architecture. Service replicas also run the workflow runtime and scheduler, and share a database holding workflow state and scheduled work; the scheduler polls for runnable tasks and uses leases to coordinate ownership, so a failed replica's work can be picked up by another, with takeover timing controlled by scheduling and lease settings. The trade-off is explicit: fewer separately deployed systems, but responsibility for workflow execution, database capacity, and recovery moves to the service team.

## Key points

- Two abstractions carry the programming model: a workflow describes orchestration (decisions, ordering, waits) and actions perform side-effecting work such as calling an API or updating a database. Skipper records action results so they can be reused during recovery.
- Waiting is cheap: in the listing-publication example, `waitUntil` hibernates a workflow without holding a thread while a signal method lets an API handler or queue consumer deliver the approval decision, so a redeploy during the wait does not discard the persisted workflow.
- Actions must make their own side effects idempotent — for example by deduplicating the publication and the host notification separately using a stable request ID — because Skipper does not make downstream calls transactionally.
- Recovery works by replay: when an interrupted workflow resumes, the workflow method runs again from the top and actions with durably persisted checkpoints return their saved results. That requires deterministic workflow code, keeping clock reads, randomness, and I/O in actions or explicit checkpoints.
- Checkpointing is batched by default until execution completes or pauses for a wait or retry, which cuts database writes but can re-run several completed actions after a crash; actions can request immediate checkpointing to narrow that window, though a downstream effect and its checkpoint are never one atomic operation, so side effects remain at-least-once.
- Failures are explicit: developers declare which errors are retryable and with what policy, permanent failures and exhausted retries are surfaced for handling, scheduler tasks that exhaust recovery attempts may need manual intervention, and Saga-style compensation covers processes that need explicit undo steps.
- The open-source release includes the core engine, MySQL and SQLite adapters, test utilities, an admin UI, and a Kotlin DSL called Skipper State Machine for processes better described as states, events, and transitions. `WorkflowTest` provides an isolated in-memory runtime with controllable time for exercising waits, signals, retries, and completion.

## Details

Production use already spans multiple teams at Airbnb, and the authors position Skipper for a Java or Kotlin service that owns a multi-step process and wants durable execution inside its existing deployment — especially when the alternative is hand-maintaining retry jobs, state tables, and polling loops for each new process. On the normal path a workflow can run directly in the service process backed by persisted state and scheduled recovery work, removing the round trip to an external orchestrator between actions, although database access and downstream calls still contribute latency. Durability is not a promise that every business operation succeeds, and the authors underline that the duty of running and recovering workflows now sits with the owning team.

Planned work includes additional storage plugins such as Postgres and DynamoDB, better tooling for workflow evolution and replay debugging, and community contributions around automated compatibility checks, migration assistance, and clearer replay visualisation. Skipper's earlier engineering deep dive covers how the engine was built; this announcement focuses on its architecture and where it sits among the options for workflow development.

## References

- Original article: [Airbnb Tech Blog](https://airbnb.tech/open-source/skipper-airbnbs-embedded-workflow-engine-is-now-open-source)
