---
title: 트랜스포머 (Transformer)
description: "세미나 수준 개념: Transformer 아키텍처, attention 메커니즘, 스케일링 법칙, 훈련 동역학"
tags: [concept, machine-learning, transformer, attention, llm, scaling, ko]
locale: ko
---

# 트랜스포머 (Transformer)

**출처**: 소스 기사 (Netflix GenRec, Spotify LLM A/B 테스팅, Databricks 모니터링, HuggingFace 논문: Unified Dynamics, PonderPounce, JIT-Agent)

## 아키텍처

### 핵심 구성 요소
```
Input → Embedding → [Encoder/Decoder Layers] → Output
```

**인코더 레이어** (BERT 방식):
```
Multi-Head Self-Attention → Add & Norm → Feed-Forward → Add & Norm
```

**디코더 레이어** (GPT 방식):
```
Masked Multi-Head Self-Attention → Add & Norm
Cross-Attention (to encoder) → Add & Norm
Feed-Forward → Add & Norm
```

### 멀티헤드 Attention
```
Q = X·W^Q, K = X·W^K, V = X·W^V
Attention(Q,K,V) = softmax(Q·K^T / √d_k) · V
MultiHead = Concat(head_1...head_h) · W^O
```

### 핵심 특성
- **병렬화 가능**: 순환(recurrence) 없음 (RNN/LSTM과 다름)
- **전역 수용 영역**: 모든 토큰이 모든 토큰에 어텐션
- **확장 가능**: 깊이 + 너비 + 데이터 → 예측 가능한 성능 향상

## 스케일링 법칙 (소스에서)

### Netflix GenRec
- 2단계 훈련: 파운데이션 LLM (1단계) → 랭킹 포스트트레인 (2단계)
- 피처 엔지니어링 대신 verbalization + 컨텍스트 엔지니어링
- Prefill 전용 vLLM 서빙

### HuggingFace: Unified Dynamics (2608.20965)
- 훈련 = 상태/메모리를 가진 파라미터-옵티마이저 시스템 진화
- 학습 = 지속적인 기능적 재조직
- 추론 = 훈련-학습 동역학의 동결된 프로젝션
- 크로스 아키텍처 검증: Transformer/Adam, ResNet/SGD, Diffusion/AdamW

### HuggingFace: JIT-Agent (2608.25593)
- 하네스 지능은 모델 스케일링과 직교함
- JIT 생성 하네스가 OpenCode/Claude Code와 경쟁 가능
- 하네스 = 4개 모듈: 메모리, 계획, 행동 프로토콜, 도구 오케스트레이션

## 훈련 동역학

### 1단계: 사전 훈련
- 대규모 코퍼스에서 다음 토큰 예측
- 학습 내용: 언어, 세계 지식, 추론 패턴
- 스케일링: 손실 ∝ compute^(-α) (거듭제곱 법칙)

### 2단계: 포스트트레이닝 / 파인튜닝
- 지시 튜닝, RLHF, DPO, GRPO
- 작업별 적응
- **컨텍스트 엔지니어링** (Netflix): 히스토리 verbalize, 토큰 예산 관리

### 3단계: 정렬 / 전문화
- 보상 모델링 (Netflix: 장기 멤버 가치)
- 카탈로그 인식 헤드 (Netflix GenRec)
- System2/System1 분리 (PonderPounce)

## 핵심 최적화 (소스에서)

### 메모리/효율성
- **FlashAttention**: IO-aware 정확한 attention (H100+)
- **KV 캐시**: 디코딩 단계에 걸쳐 key/value 재사용
- **양자화**: FP8, INT4, GPTQ, AWQ
- **Prefill 전용 서빙** (Netflix): 랭킹용 디코드 비용 회피

### 병렬성
- **텐서 병렬**: 레이어를 GPU들에 분할
- **파이프라인 병렬**: 레이어를 스테이지들에 분할
- **데이터 병렬**: 모델 복제, 데이터 샤딩
- **시퀀스 병렬**: 시퀀스 길이 분할

## 사용 시점 (대안과 비교)
| 작업 | Transformer | RNN/SSM | 트리/그래프 NN |
|------|-------------|---------|---------------|
| 언어 모델링 | ✅ | | |
| 긴 컨텍스트 (>100K) | | ✅ (Mamba, RWKV) | |
| 구조적 추론 | | | ✅ |
| 멀티모달 | ✅ (CLIP, Flamingo) | | |

## 관련 소스
- `sources/articles/netflix-techblog.md` (GenRec 2단계)
- `sources/articles/spotify-engineering.md` (LLM A/B 테스팅)
- `sources/papers/Training_Learning_and_Inference.md` (훈련 동역학)
- `sources/papers/PonderPounce.md` (System2/System1)
- `sources/papers/JIT-Agent.md` (하네스 지능)

## 관련 가이드
- `guides/ai-engineering/build-rag.md`
- `guides/ai-engineering/build-agent.md`
