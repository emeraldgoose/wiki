---
title: AI Agent 구축 — 가이드 (번역)
description: en/guides/ai-engineering/build-agent.md 한국어 번역 요약
tags: [guide, ai-engineering, agent, system1-system2, ko]
locale: ko
---

# AI Agent 구축 — 실행 가이드

## 아키텍처 결정

### System2 / System1 (PonderPounce)
```
System2 (Ponder)          System1 (Pounce)
- 전체 에피소드 컨텍스트    - 현재 관측 + 지시
- 서브골 생성              - 압축된 인지 토큰
- 느림 (~78ms p50)        - 빠름 (~25ms p50, 20Hz)
```

### 하네스 (JIT-Agent 4모듈)
```yaml
harness:
  memory:
    working: "KV 캐시 (System2 컨텍스트)"
    episodic: "벡터 DB (과거 에피소드)"
    semantic: "지식 그래프 / 임베딩"
    procedural: "이 하네스 설정"
  
  planning:
    strategy: "plan-and-execute"
    decomposition: "고수준 → 저수준"
    reflection: "사후 검증"
  
  action:
    protocol: "JSON 스키마 검증"
    pre_execution_guard: "StepGuard (단계별 안전성)"
    post_execution_verify: "결과 스키마 + 의미 검증"
  
  tools:
    orchestration: "순차/병렬/조건/루프"
    skills: ["rag_retrieve", "sql_query", "code_exec", "api_call"]
    registry: "동적 (JIT-Agent가 태스크별 합성)"
```

## 구현

### System2 (숙고형)
```python
class System2:
    def deliberate(self, episode_context, instruction):
        similar = self.memory.search(episode_context, k=5)
        return self.llm.generate(f"Episode: {episode_context}\nInstruction: {instruction}\nSimilar: {similar}\nGenerate: subgoals, reasoning, risk")
```

### System1 (반응형)
```python
class System1:
    def act(self, observation, instruction, cognition_token):
        action = self.llm.generate(...)  # JSON 액션
        if not self.guard.check(action, observation): raise SafetyError
        result = self.tools.execute(action)
        if not self.verify(result): raise ExecutionError
        return result
```

### 하네스 (JIT-Agent 합성)
```python
class Harness:
    @classmethod
    def synthesize(cls, task, jit_agent):
        return jit_agent.generate_harness(task)
```

## 안전성 (StepGuard)
- 실행 전 단계별 가드
- 77.3% 공격 감소, 2.8pp 유틸리티 감소

## 배포 패턴
- **Uber**: 3,600+ 스킬 = 하네스 변종, 단위 경제성 최적화
- **Databricks Lakebase**: 에이전트당 DB, 즉시 브랜칭, PITR
