---
title: 'StepGuard: 단계별 가드레일 학습'
description: 'StepGuard: 확장 가능한 감독과 안전-유틸리티 균형을 갖춘 단계별 가드레일 학습 (한국어 전체 번역)'
tags: [paper, source, huggingface, ai-engineering, agent-security, grpo, ko]
locale: ko
arxiv_id: 2608.24777
---

# StepGuard: 단계별 가드레일 학습

**arXiv**: 2608.24777 | **저자**: AI45Research 외 | **코드**: https://github.com/zheng977/StepGuard | **가중치**: https://huggingface.co/ninty-seven/StepGuard

## 전체 세미나 요약

### 문제

외부 환경과 도구 호출로 상호작용하는 LLM 기반 에이전트는 파일 수정, 정보 유출, 무단 액션 같은 보안 위험을 도입한다. 기존 가드레일은 완료된 궤적을 평가하므로, **실행 전 단계별 모니터링**은 거의 탐구되지 않았다.

### 해법: StepGuard

**단계별 가드 모델**:
1. 완료된 에이전트 궤적 감사
2. 도구 액션을 **실행 전** 검사

### 훈련 파이프라인

#### StepGen (자동 데이터 엔진)

동일 컨텍스트에서 위험 단계의 액션만 다른 안전/불안전 궤적 쌍을 생성. 정확한 의사결정 지점에서 대조 학습(contrastive learning)을 가능하게 한다.

#### Balance-GRPO (균형 잡힌 Group Relative Policy Optimization)

**관찰된 정확도**에 기반해 안전/불안전 액션 간 학습을 동적으로 균형 조정. 과잉 방어(false positive)와 과소 방어(false negative)를 모두 줄인다.

### 아키텍처

- 도구 호출에 대한 단계별 분류기
- StepGen 생성 대조 쌍으로 훈련
- 안전-유틸리티 트레이드오프 최적화를 위한 Balance-GRPO

### 결과

- 오픈 가중치 가드 모델 중 **최고 평균 정확도**
- 폐쇄형 **GPT-5.4에 필적**하는 성능
- AgentDojo 및 AgentDyn 벤치마크에서:
  - 무가드 대비 평균 공격 성공률 **77.3% 감소**
  - 유틸리티 하락은 **2.8pp**에 불과 (과잉 방어 최소)
- 모델 가중치 공개: HF `ninty-seven/StepGuard`

### 핵심 통찰

실행 전 단계별 가딩 + 대조 궤적 생성 + 균형 잡힌 RL = 최소 유틸리티 손실로 강력한 보안. 모델 스케일링과 직교하므로 어떤 에이전틱 LLM에도 붙일 수 있다.

### SW 엔지니어와의 관련성

에이전트 하네스의 각 도구 호출 지점에 실행 전 검사 훅을 두라. StepGen처럼 동일 컨텍스트의 안전/불안전 쌍을 합성 데이터로 만들어 분류기를 훈련하면 인간 라벨을 최소화할 수 있고, Balance-GRPO처럼 안전/불안전 정확도를 보고 임계값을 동적 조정하면 과잉 차단을 피할 수 있다. 공개 가중치가 있어 바로 붙여볼 수 있다.

### 관련 개념

- `concepts/ai-engineering/agent.md` (에이전트 하네스, 도구 호출)
- `guides/ai-engineering/build-agent.md` (안전한 에이전트 배포)

### 참고문헌

- arXiv: https://arxiv.org/abs/2608.24777
- 코드: https://github.com/zheng977/StepGuard
- 가중치: https://huggingface.co/ninty-seven/StepGuard
- 원문: en/sources/papers/StepGuard.md
