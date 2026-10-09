---
title: Build AI Agent — Guide (Seminar Level)
description: "Execution guide: build production AI agent (architecture, harness, memory, tools, safety)"
tags: [guide, ai-engineering, agent, system1-system2, harness, safety]
locale: en
---

# Build AI Agent — Execution Guide

**Synthesizes**: `concepts/ai-engineering/agent.md`, `sources/articles/uber-engineering.md`, `sources/articles/databricks-engineering.md`, `sources/papers/PonderPounce.md`, `sources/papers/JIT-Agent.md`, `sources/papers/StepGuard.md`

## Architecture Decision

### System2 / System1 (PonderPounce Pattern)
```
┌─────────────────────────────────────┐
│         System2 (Ponder)            │
│  - Full episode context (KV cache)  │
│  - Subgoal generation               │
│  - Demonstration reasoning          │
│  - Slow (~78ms p50)                 │
└──────────────┬──────────────────────┘
               │ Compressed token + age
               ▼
┌─────────────────────────────────────┐
│         System1 (Pounce)            │
│  - Current obs + instruction        │
│  - Compressed cognition token       │
│  - Fast (~25ms p50, 20Hz)           │
└─────────────────────────────────────┘
```

### Harness (JIT-Agent 4-Module Protocol)
```yaml
harness:
  memory:
    working: "KV cache (System2 context)"
    episodic: "Vector DB (past episodes)"
    semantic: "Knowledge graph / embeddings"
    procedural: "This harness config"
  
  planning:
    strategy: "plan-and-execute"  # or CoT, ToT, ReAct
    decomposition: "high-level → low-level"
    reflection: "post-action verification"
  
  action:
    protocol: "JSON schema validation"
    pre_execution_guard: "StepGuard (step-level safety)"
    post_execution_verify: "result schema + semantic check"
  
  tools:
    orchestration: "sequential / parallel / conditional / loop"
    skills: ["rag_retrieve", "sql_query", "code_exec", "api_call"]
    registry: "dynamic (JIT-Agent synthesized per task)"
```

## Implementation

### 1. System2 (Deliberative)
```python
class System2:
    def __init__(self, llm, vector_db):
        self.llm = llm
        self.memory = vector_db  # episodic
    
    def deliberate(self, episode_context, instruction):
        # Retrieve relevant past episodes
        similar = self.memory.search(episode_context, k=5)
        
        # Generate subgoals + reasoning
        prompt = f"""
        Episode: {episode_context}
        Instruction: {instruction}
        Similar past: {similar}
        
        Generate: subgoals, demonstration reasoning, risk assessment
        """
        return self.llm.generate(prompt, max_tokens=2048)
```

### 2. System1 (Reactive)
```python
class System1:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.guard = StepGuard()  # Step-level safety
    
    def act(self, observation, instruction, cognition_token):
        # Validate action before execution
        action = self.llm.generate(f"""
        Obs: {observation}
        Instruction: {instruction}
        Cognition: {cognition_token}
        
        Next action (JSON): {{"tool": "...", "args": {...}}}
        """)
        
        # Pre-execution guard
        if not self.guard.check(action, observation):
            raise SafetyError("Action blocked by StepGuard")
        
        # Execute
        result = self.tools.execute(action)
        
        # Post-execution verify
        if not self.verify(result):
            raise ExecutionError("Result verification failed")
        
        return result
```

### 3. Harness (JIT-Agent Synthesized)
```python
class Harness:
    def __init__(self, config):
        self.memory = config.memory
        self.planning = config.planning
        self.action = config.action
        self.tools = config.tools
    
    @classmethod
    def synthesize(cls, task, jit_agent):
        """JIT-Agent generates harness for this task"""
        return jit_agent.generate_harness(task)
    
    def execute(self, instruction):
        episode = []
        while not self.is_done():
            # System2: deliberate (periodic)
            if self.should_deliberate():
                cognition = self.system2.deliberate(episode, instruction)
            
            # System1: act
            action = self.system1.act(episode[-1], instruction, cognition)
            result = self.tools.execute(action)
            episode.append({"action": action, "result": result})
        
        return episode
```

## Safety (StepGuard Integration)

```python
class StepGuard:
    def __init__(self):
        self.model = load_model("ninty-seven/StepGuard")
    
    def check(self, action, context):
        """Return True if action is safe"""
        # Contrastive: same context, safe vs unsafe action
        safe_score = self.model.predict(context, action, label="safe")
        unsafe_score = self.model.predict(context, action, label="unsafe")
        
        # Balance-GRPO: dynamic threshold based on observed accuracy
        threshold = self.compute_threshold()
        return safe_score > threshold
```

## Deployment (from Sources)

### Uber Software Factory
- 3,600+ skills = harness variants
- Benchmark-driven model selection per skill
- Cost equation: Users × Sessions × Turns × Requests × Tokens × Price

### Databricks Lakebase
- Database per agent/session/branch
- Instant branching (pointer to LSN)
- Point-in-time restore (read at historical LSN)
- LTAP: unified OLTP+OLAP for agent memory

## Checklist
- [ ] System2/System1 decoupling implemented
- [ ] Harness 4-module config (memory, planning, action, tools)
- [ ] StepGuard pre-execution validation
- [ ] Episode memory (KV cache + vector DB)
- [ ] Tool registry with schema validation
- [ ] Cost monitoring (per-skill unit economics)
- [ ] Database per agent (Lakebase) for isolation

## Related Concepts
- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/rag.md`

## Related Guides
- `guides/ai-engineering/build-rag.md`
