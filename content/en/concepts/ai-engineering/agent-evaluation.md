---
title: Agent Evaluation & LLM-as-a-Judge
description: Systematic evaluation of LLM agents — tool-calling, multi-step reasoning, and autonomous workflows — using programmatic metrics, LLM judges, and human validation
tags: [concept, ai-engineering, agent-evaluation, llm-as-judge, benchmarking]
locale: en
---

# Agent Evaluation & LLM-as-a-Judge

**Agent Evaluation** assesses the capability of LLM-based agents to perform multi-step tasks, use tools correctly, reason over dependencies, and complete end-to-end workflows. Unlike single-turn LLM evaluation, agent evaluation must handle sequential decisions, statefulness, and compounding errors.

## Evaluation Dimensions

### 1. Task Success (Outcome-Based)
- **Exact Match**: Final output matches ground truth exactly
- **Functional Correctness**: Code executes, API calls succeed, files created
- **Goal Achievement**: User intent satisfied (may have multiple valid paths)
- **Partial Credit**: Sub-task completion (e.g., 3/5 steps correct)

### 2. Process Quality (Trajectory-Based)
- **Tool Selection**: Right tool for the job; correct parameters
- **Reasoning Coherence**: Logical step progression; no hallucinated actions
- **Error Recovery**: Handles failures gracefully; retries, alternatives
- **Efficiency**: Minimal steps, tokens, latency, cost
- **Safety**: No dangerous actions; respects constraints

### 3. Robustness
- **Distribution Shift**: Performance on unseen task variants
- **Adversarial Inputs**: Prompt injections, malformed tool outputs
- **Long Horizon**: Performance degradation over many steps
- **State Consistency**: Maintains correct world model

## Evaluation Methods

### Programmatic / Automated
| Method | Applicability | Pros | Cons |
|--------|---------------|------|------|
| **Unit Tests** | Code gen, API calls | Deterministic, fast | Narrow coverage |
| **Execution-Based** | Code, SQL, scripts | Ground truth via execution | Sandbox needed |
| **Schema Validation** | Structured output (JSON, XML) | Fast, precise | Limited to schema |
| **State Assertions** | Multi-step workflows | Verifies intermediate state | Requires instrumented env |

### LLM-as-a-Judge
**Core Idea**: Use a strong LLM (GPT-4, Claude, Qwen) to evaluate agent outputs/trajectories

#### Judge Types
| Type | Description | Use Case |
|------|-------------|----------|
| **Pairwise** | Compare A vs B (which better?) | Relative ranking |
| **Pointwise** | Score single output (1–10, rubric) | Absolute quality |
| **Reference-Based** | Compare to ground truth | Correctness verification |
| **Critique** | Generate detailed feedback | Debugging, improvement |

#### Structured Rubrics (Critical for Reliability)
```yaml
# Example rubric for code generation
criteria:
  - name: "Correctness"
    weight: 0.4
    levels:
      5: "Passes all tests, handles edge cases"
      3: "Passes basic tests, minor bugs"
      1: "Fails tests, major logic errors"
  - name: "Code Quality"
    weight: 0.3
    levels:
      5: "Clean, documented, idiomatic"
      3: "Functional but messy"
      1: "Unreadable, anti-patterns"
  - name: "Efficiency"
    weight: 0.2
    levels:
      5: "Optimal complexity, no waste"
      3: "Acceptable performance"
      1: "Unnecessary complexity"
  - name: "Safety"
    weight: 0.1
    levels:
      5: "No security issues"
      1: "Vulnerabilities present"
```

#### Best Practices for LLM Judges
- **Chain-of-Thought**: Require judge to reason before scoring
- **Few-Shot Examples**: Calibrate with human-annotated samples
- **Temperature = 0**: Deterministic judgments
- **Ensemble**: Multiple judges + majority vote / average
- **Calibration**: Regular human-judge alignment checks
- **Bias Mitigation**: Position bias (swap order), verbosity bias, style bias

### Human Evaluation
- **Gold Standard**: For high-stakes decisions; calibrates auto metrics
- **Annotation Schema**: Atomic (per-step) + holistic (overall)
- **Inter-Annotator Agreement**: Cohen's κ, Krippendorff's α
- **Cost**: Expensive; use active learning to select informative samples

## Key Benchmarks

### General Agent Benchmarks
| Benchmark | Focus | Tasks | Metrics |
|-----------|-------|-------|---------|
| **AgentBench** | Web, OS, DB, KG, etc. | 1,000+ | Success rate, steps |
| **WebShop** | E-commerce navigation | 12K | Purchase success |
| **ALFWorld** | Household tasks (text) | 6 envs | Goal completion |
| **Mind2Web** | Web interaction | 2K | Step accuracy |
| **ToolBench** | Tool use (REST APIs) | 16K | API call accuracy |

### Code Agent Benchmarks
| Benchmark | Focus | Tasks |
|-----------|-------|-------|
| **SWE-bench** | Real GitHub issues | 2,294 |
| **HumanEval** | Function completion | 164 |
| **MBPP** | Basic programming | 974 |
| **LiveCodeBench** | Contest problems | 500+ |
| **CodeContests** | Competitive programming | 13K |

### Specialized Agent Benchmarks
- **AgentJudgeBench** (ServiceNow, 2026): LLM judge reliability on agentic tool-calling over workflow DAGs
- **τ-bench**: Dynamic user-API interaction (airline, retail)
- **CRM-Bench**: Customer relationship management workflows
- **WebVoyager**: End-to-end web navigation

## AgentJudgeBench Insights (2026)
- **Judges degrade with task difficulty**: 1.5× faster without ground truth
- **Hard ceiling**: All judges converge to 77–82% alignment on hard tasks without GT
- **Ground truth not always helpful**: Reduces alignment for frontier judges (over-anchoring)
- **Mitigations**: Structured rubrics (+6.5 pp); CoT + temperature negligible
- **Best judges**: QwQ-32B (with GT); GPT-OSS-120B (human-aligned, without GT)

## Evaluation Infrastructure

### Trajectory Logging
```json
{
  "episode_id": "uuid",
  "task": "description",
  "steps": [
    {
      "step": 1,
      "observation": "...",
      "thought": "...",
      "action": {"tool": "search", "args": {"query": "..."}},
      "result": "...",
      "reward": 0.0
    }
  ],
  "final_outcome": "success|failure",
  "metrics": {"steps": 5, "tokens": 3421, "latency_s": 12.3, "cost_usd": 0.004}
}
```

### CI/CD Integration
- **Nightly eval runs**: Regression detection
- **PR gates**: Minimum success rate on held-out set
- **A/B testing**: Champion vs challenger models
- **Drift monitoring**: Performance on static benchmark over time

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Single-turn metrics on agents** | High accuracy, fails in practice | Use trajectory-based eval |
| **Judge without rubric** | High variance, low human agreement | Structured rubrics + CoT |
| **No ground truth for verification** | Judge hallucinates correctness | Execution-based + reference |
| **Only final outcome** | Misses catastrophic mid-trajectory errors | Step-level evaluation |
| **Static benchmarks** | Overfitting, saturation | Regular refresh; live benchmarks |

## Key References
- Liu et al. (2023): "AgentBench: Evaluating LLMs as Agents"
- Verma et al. (2026): "AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling"
- Qin et al. (2023): "ToolBench: Generalized Tool Learning"
- Yao et al. (2022): "WebShop: Towards Scalable Real-World Web Interaction"
- Jimenez et al. (2024): "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"

## Related Concepts
- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-evaluation.md`
- `concepts/ai-engineering/rlhf.md` (reward modeling)
- `concepts/machine-learning/transformer.md`