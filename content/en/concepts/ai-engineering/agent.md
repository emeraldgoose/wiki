---
title: AI Agent
description: "Seminar-level concept: AI agent architecture, System1/System2, harness, memory, planning, tool use"
tags: [concept, ai-engineering, agent, system1-system2, harness, planning]
locale: en
---

# AI Agent

**Read from**: Netflix GenRec (prefill-only serving), Uber software factory (agent skills), Databricks Lakebase (agentic DB), PonderPounce (System2/System1), JIT-Agent (harness intelligence), StepGuard (step-level guard)

## Agent Architecture

### Core Loop
```
Observe → Reason/Plan → Act (Tool) → Observe → ...
```

### System2 / System1 (from PonderPounce)
| Aspect | System2 (Ponder) | System1 (Pounce) |
|--------|------------------|------------------|
| Speed | Slow (deliberative) | Fast (reactive) |
| Context | Full episode history | Compressed token |
| Role | Subgoals, reasoning, demonstrations | Action execution |
| Frequency | Low (cognition refresh ~78ms) | High (action ~25ms, 20Hz) |

### Harness (from JIT-Agent)
**Four-module protocol** (machine-generatable artifact):
1. **Memory Management**: What to remember, how to retrieve, TTL
2. **Planning Strategy**: Decompose, sequence, reflect, backtrack
3. **Action Protocol**: Tool calling format, validation, error handling
4. **Tool/Skill Orchestration**: Which tools, when, how to compose

### Harness Intelligence
- Trainable, transferable, compounding dimension orthogonal to model scaling
- JIT-Agent synthesizes task-adaptive harnesses on-the-fly
- Self-evolves via archive of (task, harness, performance) tuples

## Memory Systems

| Memory Type | Implementation | Lifetime | Use Case |
|-------------|----------------|----------|----------|
| Working (KV Cache) | Transformer KV cache | Single episode | Immediate context |
| Episodic | Vector DB / structured log | Session/episode | Past interactions |
| Semantic | Knowledge graph / embeddings | Long-term | Facts, procedures |
| Procedural | Harness / skills | Persistent | How to do tasks |

### Native Causal Context (PonderPounce)
- MLLM's KV cache = episode memory
- No separate memory module needed
- Decoupled clocks: System2 builds context, System1 receives compressed token

## Planning

### Decomposition Strategies
- **Chain-of-Thought**: Step-by-step reasoning
- **Tree-of-Thought**: Explore multiple branches
- **Plan-and-Execute**: High-level plan → low-level execution
- **ReAct**: Reason + Act interleaved

### Planning in Harness
- JIT-Agent generates planning strategy per task
- Continuous Skill Optimization (Uber): repair/evolve planning modules

## Tool Use

### Protocol
```
Tool Call: {name: "tool_name", args: {...}}
Tool Result: {output: "...", error: null}
```

### Validation
- Schema validation (JSON Schema)
- Pre-execution guards (StepGuard: step-level safety)
- Post-execution verification

### Orchestration
- Sequential: A → B → C
- Parallel: A + B → C
- Conditional: if A then B else C
- Loop: while condition do A

## Safety (from StepGuard)
- **Step-level guard**: Check tool action BEFORE execution
- **Contrastive training**: Safe/unsafe pairs with same context
- **Balance-GRPO**: Dynamic safety-utility balancing
- **Result**: 77.3% attack reduction, 2.8pp utility drop

## Production Patterns (from Sources)

### Uber Software Factory
- 3,600+ agent skills across SDLC
- 30K+ executions/day
- Cost equation optimization (6 terms)
- Benchmark-driven model selection per skill

### Databricks Lakebase
- Database per agent/session/branch
- Instant branching (pointer to LSN)
- Point-in-time restore (read at historical LSN)
- LTAP: unified OLTP+OLAP for agent memory

### Netflix GenRec
- Prefill-only serving (ranking, not generation)
- Context engineering for token budget

## Key Seminar Points

1. **Agent = Model + Harness + Memory + Tools** (not just model)
2. **System2/System1 decoupling** enables slow reasoning + fast action
3. **Harness intelligence** is trainable and orthogonal to model scaling
4. **Step-level guards** (StepGuard) essential for production safety
5. **Database per agent** (Lakebase) makes isolation affordable

## Related Sources
- `sources/articles/uber-engineering.md` (software factory)
- `sources/articles/databricks-engineering.md` (Lakebase)
- `sources/papers/PonderPounce.md` (System2/System1)
- `sources/papers/JIT-Agent.md` (harness intelligence)
- `sources/papers/StepGuard.md` (step-level guard)

## Related Guides
- `guides/ai-engineering/build-agent.md`
- `guides/ai-engineering/build-rag.md`
