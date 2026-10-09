---
title: AI 에이전트 (AI Agent)
description: en/concepts/ai-engineering/agent.md 한국어 번역 요약
tags: [concept, ai-engineering, agent, ko]
locale: ko
---

# AI 에이전트 (AI Agent)

**원전**: Netflix GenRec (prefill-only 서빙), Uber software factory (agent skills), Databricks Lakebase (agentic DB), PonderPounce (System2/System1), JIT-Agent (harness intelligence), StepGuard (step-level guard)

## 에이전트 아키텍처

### 핵심 루프
```
Observe → Reason/Plan → Act (Tool) → Observe → ...
```
관찰하고, 추론·계획한 뒤, 도구로 행동하고, 다시 관찰하는 루프가 에이전트의 기본 동작 단위다. 모델 단독이 아니라 이 루프를 돌리는 전체 시스템이 에이전트다.

### System2 / System1 (PonderPounce에서 차용)
| 측면 | System2 (Ponder) | System1 (Pounce) |
|--------|------------------|------------------|
| 속도 | 느림 (숙고형) | 빠름 (반응형) |
| 컨텍스트 | 전체 에피소드 히스토리 | 압축된 토큰 |
| 역할 | 서브골, 추론, 데모 생성 | 액션 실행 |
| 빈도 | 낮음 (인지 리프레시 ~78ms) | 높음 (액션 ~25ms, 20Hz) |

느린 추론(System2)과 빠른 실행(System1)을 분리된 클록으로 돌리면, 숙고하면서도 실시간으로 행동할 수 있다.

### 하네스 (JIT-Agent에서 차용)
**4모듈 프로토콜** (기계 생성 가능한 아티팩트):
1. **메모리 관리(Memory Management)**: 무엇을 기억하고, 어떻게 검색하며, TTL은 어떻게 둘 것인가
2. **계획 전략(Planning Strategy)**: 분해, 순서화, 성찰(reflect), 백트래킹
3. **액션 프로토콜(Action Protocol)**: 도구 호출 포맷, 검증, 에러 처리
4. **도구/스킬 오케스트레이션(Tool/Skill Orchestration)**: 어떤 도구를, 언제, 어떻게 조합할 것인가

### 하네스 인텔리전스
- 모델 스케일링과 직교하는, 학습 가능하고 전이 가능하며 복리로 누적되는 차원
- JIT-Agent는 태스크에 맞는 하네스를 실행 시점에(on-the-fly) 합성한다
- (task, harness, performance) 튜플 아카이브를 통해 스스로 진화한다

## 메모리 시스템

| 메모리 유형 | 구현 | 수명 | 용도 |
|-------------|----------------|----------|----------|
| 워킹 (KV 캐시) | Transformer KV cache | 단일 에피소드 | 즉시 컨텍스트 |
| 에피소드 | Vector DB / 구조화 로그 | 세션/에피소드 | 과거 상호작용 |
| 시맨틱 | Knowledge graph / embeddings | 장기 | 사실, 절차 |
| 절차적 | Harness / skills | 영속 | 작업 수행 방법 |

### 네이티브 인과 컨텍스트 (PonderPounce)
- MLLM의 KV 캐시 자체가 에피소드 메모리다
- 별도의 메모리 모듈이 필요 없다
- 클록 분리: System2가 컨텍스트를 구축하고, System1은 압축된 토큰을 전달받는다

## 계획(Planning)

### 분해 전략
- **Chain-of-Thought**: 단계별 추론
- **Tree-of-Thought**: 여러 분기를 탐색
- **Plan-and-Execute**: 상위 계획 → 하위 실행
- **ReAct**: 추론(Reason)과 행동(Act)을 교차 수행

### 하네스 내의 계획
- JIT-Agent는 태스크마다 계획 전략을 생성한다
- 지속적 스킬 최적화(Uber 방식): 계획 모듈을 수리·진화시킨다

## 도구 사용(Tool Use)

### 프로토콜
```
Tool Call: {name: "tool_name", args: {...}}
Tool Result: {output: "...", error: null}
```

### 검증
- 스키마 검증 (JSON Schema)
- 실행 전 가드 (StepGuard: 단계 수준 안전 검사)
- 실행 후 검증

### 오케스트레이션
- 순차: A → B → C
- 병렬: A + B → C
- 조건: if A then B else C
- 루프: while condition do A

## 안전성 (StepGuard에서 차용)
- **단계 수준 가드**: 도구 액션을 실행하기 *전에* 검사한다
- **대조 학습(Contrastive training)**: 동일 컨텍스트의 안전/불안전 쌍으로 학습
- **Balance-GRPO**: 안전성과 유용성의 동적 균형
- **결과**: 공격 77.3% 감소, 유용성 하락 2.8pp

## 프로덕션 패턴 (원전에서 차용)

### Uber Software Factory
- SDLC 전반에 3,600개 이상의 에이전트 스킬
- 하루 30K+ 회 실행
- 비용 방정식 최적화 (6개 항)
- 스킬별 벤치마크 기반 모델 선택

### Databricks Lakebase
- 에이전트/세션/브랜치별 데이터베이스 분리
- 인스턴트 브랜칭 (LSN에 대한 포인터)
- 시점 복원 (과거 LSN 시점 읽기)
- LTAP: 에이전트 메모리용 OLTP+OLAP 통합

### Netflix GenRec
- Prefill-only 서빙 (생성이 아닌 랭킹)
- 토큰 예산을 위한 컨텍스트 엔지니어링

## 핵심 세미나 포인트

1. **에이전트 = 모델 + 하네스 + 메모리 + 도구** (모델만이 아니다)
2. **System2/System1 분리**로 느린 추론과 빠른 액션을 양립시킨다
3. **하네스 인텔리전스**는 학습 가능하며 모델 스케일링과 직교한다
4. **단계 수준 가드**(StepGuard)가 프로덕션 안전에 필수다
5. **에이전트별 데이터베이스**(Lakebase)로 격리를 저렴하게 만든다

## 관련 원전
- `sources/articles/uber-engineering.md` (software factory)
- `sources/articles/databricks-engineering.md` (Lakebase)
- `sources/papers/PonderPounce.md` (System2/System1)
- `sources/papers/JIT-Agent.md` (harness intelligence)
- `sources/papers/StepGuard.md` (step-level guard)

## 관련 가이드
- `guides/ai-engineering/build-agent.md`
- `guides/ai-engineering/build-rag.md`
