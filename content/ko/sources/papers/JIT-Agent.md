---
title: 'JIT-Agent: Just-in-Time 하네스 진화를 통한 하네스 지능 스케일링'
description: 'JIT-Agent: Just-in-Time 하네스 진화를 통한 하네스 지능 스케일링 (한국어 전체 번역)'
tags: [paper, source, huggingface, ai-engineering, agent-harness, harness-intelligence, ko]
locale: ko
arxiv_id: 2608.25593
---

# JIT-Agent: Just-in-Time 하네스 진화를 통한 하네스 지능 스케일링

**arXiv**: 2608.25593 | **저자**: National University of Singapore | **프로젝트**: https://bingreeky.github.io/JIT-site/ | **GitHub**: https://github.com/bingreeky/JIT

## 전체 세미나 요약

### 문제

에이전트 능력 ≠ 모델 단독. **에이전트 하네스**(메모리 관리, 플래닝 전략, 액션 프로토콜, 도구/스킬 오케스트레이션)의 기여가 기반 파운데이션 모델을 압도할 수 있다. 그런데 하네스 설계는 수동적이고, 태스크-특정적이며, 근본적으로 확장 불가능하다.

### 해법: JIT-Agent

임의의 기성 에이전틱 LLM을 위해 태스크-적응적 에이전트 하네스를 온더플라이로 합성하는 **하네스 지능 모델**.

### 정식화: 조합 가능한 아티팩트로서의 에이전트 하네스

**4모듈 프로토콜** (고정, 기계-생성 가능):
1. **메모리 관리** — 무엇을 기억하고 어떻게 검색할지
2. **플래닝 전략** — 어떻게 분해하고, 순서화하고, 반성할지
3. **액션 프로토콜** — 도구 호출 포맷, 검증, 에러 처리
4. **도구/스킬 오케스트레이션** — 어떤 도구를 언제 어떻게 조합할지

### JIT-Agent의 능력

1. **합성(Synthesize)**: 당면 태스크에 대한 하네스 생성
2. **수리(Repair)**: 안정적/신뢰 가능한 실행을 위한 하네스 수정
3. **자기-진화(Self-Evolve)**: 이전 하네스 설정 아카이브에서 성능 신호를 증류

### 훈련

- 다양한 태스크 + 하네스 설정으로 훈련
- (모델, 태스크) 쌍마다 하네스를 맞춤화하도록 학습
- 이전 하네스 아카이브가 복리(compounding) 지식 기반 제공

### 결과

| 베이스 모델 | 벤치마크 | JIT-Agent 이득 | 비교 |
|------------|-----------|----------------|------|
| DeepSeek-V4-Flash | DeepSearchQA | **+9.1** | GPT-5.6 추월 |
| DeepSeek-V4-Flash | OdysseyBench | **+4.3** | GPT-5.6 추월 |
| GLM-5.2 | (복수) | **최대 +20.2** | 이미 강한 모델 |
| 멀티스케일 패밀리 (DeepSeek V4, Mimo-V2.5, Qwen3.6) | 통제 평가 | 일관된 향상 | OpenCode, Claude Code와 경쟁 가능 |

### 핵심 통찰

**하네스 지능**은 모델 스케일링과 **직교하는**, 훈련 가능하고 전이 가능하며 복리로 쌓이는 에이전트 능력 차원이다. JIT-Agent는 하네스 생성을 모델 패밀리와 태스크를 가로질러 향상되는 학습 가능한 스킬로 정립한다.

### 아키텍처

- JIT-Agent는 "하네스 헬퍼"로 동작 — 사용자 태스크와 에이전틱 LLM 사이에 위치
- 하네스 설정 생성 → 에이전틱 LLM이 그 하네스로 실행
- 아카이브는 (태스크, 하네스, 성능) 튜플을 축적해 자기-진화

### SW 엔지니어와의 관련성

모델만 키우기 전에 하네스를 태스크별로 합성하는 레이어를 두라. 메모리/플래닝/액션/도구 4모듈을 고정 스키마로 표준화하면 하네스를 기계가 생성·수리할 수 있고, (태스크, 하네스, 성능) 아카이브를 쌓으면 다음 태스크에서 재사용되는 복리 효과가 난다. 통제 평가에서 여러 모델 패밀리에 걸쳐 일관된 향상이 확인되었다.

### 관련 개념

- `concepts/ai-engineering/agent.md` (에이전트 하네스, 메모리/플래닝/액션/도구 모듈)
- `guides/ai-engineering/build-agent.md` (하네스 설정 모범 사례)
- `concepts/ai-engineering/rag.md` (도구 오케스트레이션, 메모리 관리)

### 참고문헌

- arXiv: https://arxiv.org/abs/2608.25593
- 프로젝트: https://bingreeky.github.io/JIT-site/
- GitHub: https://github.com/bingreeky/JIT
- 원문: en/sources/papers/JIT-Agent.md
