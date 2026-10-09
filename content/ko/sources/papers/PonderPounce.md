---
title: 'PonderPounce — 논문 소스 (전체 번역)'
description: 'PonderPounce: 에피소드 컨텍스트 엔진으로서의 사전학습 MLLM을 이용한 로봇 제어 (한국어 전체 번역)'
tags: [paper, source, huggingface, ai-engineering, robotics, mllm, system1-system2, ko]
locale: ko
arxiv_id: 2608.24115
---

# PonderPounce: 에피소드 컨텍스트 엔진으로서의 MLLM을 이용한 로봇 제어

**arXiv**: 2608.24115 | **저자**: maum-ai | **프로젝트**: https://worv-ai.github.io/ponderpounce/

## 전체 세미나 요약

### 문제

로봇 작업은 더 이상 보이지 않는 정보(잠깐 보여준 목표물, 이전 지시, 초반 데모)를 기억해야 한다. 사전학습 MLLM은 강력한 장문맥 추론 능력을 갖지만 VLA 모델은 이 컨텍스트를 에피소드 메모리로 활용하지 않는다. 기억-의존 정책들은 별도 목적의 히스토리 메커니즘을 추가하는 방식이었다.

### 해법: PonderPounce

MLLM의 **네이티브 인과 컨텍스트(native causal context)**를 로봇 메모리로 재사용한다. 두 개의 사전학습 시스템을 연결한다.

#### Ponder (System2 MLLM)

- 에피소드 관측, 데모, 이전 인지를 네이티브 인과 컨텍스트에 누적
- 내부 사용을 위한 **서브골 텍스트**와 **데모 추론** 생성
- 느리고 숙고적이며 전체 히스토리에 대해 추론

#### Pounce (System1 VLA)

- 현재 관측, 지시, 고유수용(proprioception)을 직접 수신
- **Ponder–Pounce 인터페이스**를 통해 최신 연속 인지 토큰 1개와 그 age만 비동기로 수신
- 빠르고 반응적이며 20Hz로 액션 실행

### 훈련

- 목적-built 메모리 모듈이나 별도 브리지 사전훈련 없이 **합동 종단간 훈련**
- 분리된 클록: Ponder와 Pounce가 서로 다른 주파수로 동작
- 최적화된 서빙: p50 지연시간 78ms(인지 갱신), 25ms(액션 모델 호출)

### 결과

| 벤치마크 | 훈련 데이터 | PonderPounce | 최고 베이스라인 |
|-----------|---------------|--------------|-----------------|
| RoboMME | 1× | **60.83%** (9B) / 50.04% (0.8B) | 44.51% (FrameSamp+Modul) |
| RoboMME | 9× | **75.54%** | 57.88% (FrameSamp+Modul) |
| RoboCasa-DC | 1× | **12.5%** (액션 supervision만) | 11.6% (demo-conditioned) |

**핵심 발견**: RoboCasa-DC에서 액션 supervision만으로 동일 인터페이스가 학습된다. 인지를 학습된 null 상태로 교체하면 8.6%로 하락 → 인지가 결정적이다.

### 아키텍처 통찰

- **System2 (Ponder)**: 느린 사고, 전체 컨텍스트, 서브골/추론 생성
- **System1 (Pounce)**: 빠른 실행, 압축된 인지 토큰 수신
- **인터페이스**: 단일 연속 토큰 + age — 최소 대역폭, 최대 정보
- **목적-built 메모리 불필요**: MLLM의 네이티브 인과 컨텍스트를 재사용 (트랜스포머 KV 캐시를 에피소드 메모리로)

### 핵심 통찰

네이티브 인과 컨텍스트를 메모리로 쓰는 분리된 System2/System1 아키텍처는 별도 메모리 모듈의 필요성을 제거한다. 합동 훈련이 종단간 최적화를 가능하게 하며 데이터에 따라 스케일된다 (1× → 9×: 60.8% → 75.5%).

### SW 엔지니어와의 관련성

로봇 에이전트를 만들 때 별도 히스토리 인코더를 달기 전에 KV 캐시를 에피소드 메모리로 쓰는 설계를 먼저 검토하라. 느린 계획 루프와 빠른 제어 루프를 분리된 클록으로 돌리고 둘 사이에는 단일 인지 토큰+age 같은 좁은 인터페이스를 두면 지연시간(p50 78ms/25ms)을 관리하기 쉽다.

### 관련 개념

- `concepts/ai-engineering/agent.md` (System1/System2, 에이전트 아키텍처)
- `concepts/machine-learning/attention.md` (KV 캐시로서의 인과 컨텍스트)
- `guides/ai-engineering/build-agent.md` (로봇 에이전트 배포)

### 참고문헌

- arXiv: https://arxiv.org/abs/2608.24115
- 프로젝트: https://worv-ai.github.io/ponderpounce/
- 원문: en/sources/papers/PonderPounce.md
