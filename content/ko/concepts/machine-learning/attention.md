---
title: 어텐션 (Attention)
description: "세미나 수준 개념: Attention 메커니즘, 변형, FlashAttention, KV 캐시, 스케일링"
tags: [concept, machine-learning, attention, transformer, flash-attention, ko]
locale: ko
---

# 어텐션 (Attention)

**출처**: Transformer 개념, HuggingFace Unified Dynamics 논문, PonderPounce System2/System1, JIT-Agent

## 핵심 Attention

### 스케일드 닷-프로덕트 Attention
```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

**복잡도**: 시퀀스 길이 N에 대해 시간/공간 O(N²)

### 멀티헤드 Attention
```
head_i = Attention(Q·W_i^Q, K·W_i^K, V·W_i^V)
MultiHead = Concat(head_1...head_h) · W^O
```

### 조직 조건으로서의 Attention (Unified Dynamics에서)
- "컴포넌트 게이팅과 롤백은 인과적 모집(causal recruitment)을 보여준다"
- "훈련 중에 형성된 쿼리 조건부 서포트의 비가산적(non-additive) 결합"
- **Attention**이 실현하는 조직 조건(organizational conditions)

## 변형 및 최적화

### FlashAttention (IO-Aware)
- **문제**: 표준 attention은 N×N 행렬을 HBM에 구체화(materialize)함
- **해결**: 타일링(tiling) + 재계산; 전체 행렬을 절대 구체화하지 않음
- **결과**: 2~4배 속도 향상, 선형 메모리, 근사가 아닌 정확(exact)한 계산

### FlashAttention-2 / 3
- 향상된 병렬성, 공유 메모리 사용량 감소
- Hopper(H100) 텐서 코어 활용
- FP8 지원

### KV 캐시 (디코딩)
- 이전 토큰들의 K, V를 저장
- **메모리**: 2 × 레이어 수 × 헤드 수 × 차원 × 시퀀스 길이 × 바이트 수
- **최적화**: PagedAttention(vLLM), 프리픽스 캐싱(prefix caching)

### 희소 / 선형 Attention
| 변형 | 복잡도 | 근사 방식 | 사용 사례 |
|---------|------------|---------------|----------|
| Longformer | O(N·w) | 로컬 + 글로벌 | 긴 문서 |
| BigBird | O(N·√N) | 랜덤 + 로컬 + 글로벌 | 긴 문서 |
| Performer | O(N) | 커널 근사 | 긴 컨텍스트 |
| Linear / RWKV | O(N) | 순환형 | 무한 컨텍스트 |

## 소스에서의 Attention

### Netflix GenRec
- Prefill 전용 vLLM 서빙 (디코드 없음)
- Attention 출력 위에 카탈로그 인식 스코어링 헤드(catalog-aware scoring head)

### PonderPounce (System2 MLLM)
- **인과적 컨텍스트** = 에피소드 메모리로서의 MLLM 네이티브 KV 캐시
- Ponder가 인과적 컨텍스트에 관측을 누적
- Pounce는 압축된 인지 토큰(단일 토큰 + age)을 수신

### Unified Dynamics (2608.20965)
- Attention은 서포트 모집을 위한 "조직 조건"을 실현
- 동결된 추론 프로젝션이 훈련에서 형성된 서포트를 모집
- 크로스 아키텍처: Transformer/Adam에서 Attention 구조 보존

## 핵심 세미나 포인트

1. **Attention이 병목**이다 — 긴 컨텍스트 스케일링의 병목(O(N²))
2. **FlashAttention**으로 100K+ 토큰에서도 정확한 attention이 가능해짐
3. **KV 캐시** = 작업 기억(working memory); 프리픽스 캐싱 = 의미 기억(semantic memory)
4. **System2/System1**(PonderPounce): 느린 숙고가 컨텍스트를 구축하고, 빠른 행동은 압축된 토큰을 사용
5. **하네스 지능**(JIT-Agent): 계획 모듈을 통한 도구/행동 공간에 대한 Attention

## 관련 개념
- `concepts/machine-learning/transformer.md` (전체 아키텍처)
- `concepts/ai-engineering/agent.md` (System2/System1, 메모리로서의 KV 캐시)

## 관련 가이드
- `guides/ai-engineering/build-rag.md` (검색 + attention)
- `guides/ai-engineering/build-agent.md` (에이전트 attention 패턴)
