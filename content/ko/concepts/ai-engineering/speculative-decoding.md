---
title: Speculative Decoding (추측적 디코딩)
description: 작은 드래프트 모델로 토큰을 생성하고 큰 타겟 모델이 병렬로 검증하여 LLM 추론 가속화
tags: [concept, ai-engineering, llm-inference, speculative-decoding, optimization, ko]
locale: ko
---

# Speculative Decoding (추측적 디코딩)

**Speculative Decoding**(추측적 디코딩, **Speculative Sampling** 또는 **Assisted Decoding**이라고도 함)은 작은 고속 **드래프트 모델**이 후보 토큰을 생성하면 큰 **타겟 모델**이 병렬로 검증하여 LLM 추론을 가속화하는 기법입니다. 허용된 토큰은 유지하고, 거부된 토큰에서는 롤백 후 타겟 모델이 생성합니다.

## 핵심 아이디어

```
전통적:    타겟 모델이 토큰을 하나씩 순차 생성 (느림)
추측적:    드래프트 모델 → K개 토큰 빠르게 생성 → 타겟이 1회 포워드 패스로 K개 모두 검증
```

- **드래프트 모델**: 작음 (예: 7B), 빠름, 타겟을 모방하도록 학습
- **타겟 모델**: 큼 (예: 70B), 느림, 고품질
- **검증**: 드래프트 토큰 + 컨텍스트에 대한 타겟 모델의 단일 포워드 패스
- **수용**: 첫 토큰부터 순차적으로; 첫 거부에서 중단

## 알고리즘

### 표준 추측적 디코딩 (Chen et al., 2023)
1. 드래프트 모델이 γ개 토큰을 자기회귀적으로 생성
2. 타겟 모델이 KV 캐시와 함께 γ개 토큰을 한 번의 포워드 패스로 스코어링
3. `p_target(t) / p_draft(t) ≥ random()`인 동안 순차적으로 토큰 수용
4. 거부 시: 수정된 분포 `p_target - p_draft`에서 샘플링 (정규화 후)
5. 수용된 접두사부터 재개

### EAGLE (Efficient Accelerated Generation with Lookahead) — Li et al., 2024
- **통찰**: 드래프트 모델이 작은 LLM일 필요 없음; 타겟의 은닉 상태 위에 가벼운 **회귀 헤드**면 충분
- **EAGLE-2**: 특징 기반 드래프팅; 타겟의 마지막 레이어 은닉 상태에서 다음 토큰 예측
- **EAGLE-3**: 동적 드래프트 길이 추가; 검증 인식 학습

### Medusa (Cai et al., 2024)
- 타겟 모델에 **다중 디코딩 헤드** 부착 (백본 동결)
- 각 헤드가 다른 미래 위치 예측 (트리 구조 드래프트)
- 여러 브랜치 병렬 검증; 더 높은 수용률

### Lookahead Decoding (Fu et al., 2024)
- **드래프트 모델 불필요**: 타겟의 로짓에서 n-그램 매칭 또는 야코비 반복 사용
- **야코비 반복**: 타겟의 다음 토큰 분포에 대한 고정점 반복
- 배포 단순; 모든 모델에 적용 가능

## 주요 지표

| 지표 | 정의 | 목표 |
|--------|------|------|
| **수용 길이** | 검증 라운드당 평균 수용 토큰 수 | 높을수록 속업 ↑ |
| **수용률** | 수용 / 생성 | 보통 0.7–0.9 |
| **속업** | 바닐라 대비 월클락 시간 단축 | 보통 1.5×–3× |
| **품질 보존** | 출력 분포 일치 | 이론적으로 타겟과 동일 |

## 드래프트 모델 학습

### 지식 증류 기반
- 드래프트를 타겟의 다음 토큰 분포 모방하도록 학습 (KL 발산)
- 데이터: 타겟 모델 생성물 또는 공통 학습 코퍼스
- 과제: 드래프트 용량 ≪ 타겟 용량 → 근사 오차

### 검증 인식 학습 (VAT) — NAVER AI, 2026
- **검증 헤드**: 각 위치가 검증을 통과할지 예측하는 경량 분류기
- **검증 적응 가중치**: 첫 거부 전까지 완전 가중치; 거기서부터 디케이 재고정
- **결과**: 수용 길이 11.4% 개선; 월클락 속업 8.7%

### 자기 추측적 (별도 드래프트 없음)
- **조기 출구 레이어**: 중간 레이어를 드래프트로 사용
- **레이어 건너뛰기**: 주기적으로 레이어 건너뛰며 드래프트 생성
- 트레이드오프: 배포 단순함 vs 낮은 수용률

## 실용적 고려사항

### 메모리 오버헤드
- 두 모델이 GPU 메모리에 상주 (드래프트 + 타겟)
- 검증 중 양쪽 KV 캐시 필요
- **완화**: 드래프트 양자화 (INT4/INT8); 임베딩 공유; 드래프트를 CPU로 오프로드

### 품질 보장
- **이론적으로 정확**: 적절한 거부 샘플링으로 출력 분포가 타겟과 정확히 일치
- **실질적으로 정확**: 부동소수점 차이는 무시 가능
- **품질 저하 없음** (올바르게 구현 시)

### 가장 잘 작동하는 경우
- **큰 타겟 모델** (70B+): 절대적 속업 더 큼
- **긴 생성**: 드래프트 오버헤드 상각
- **높은 연산 강도**: 타겟이 컴퓨트 바운드 (메모리 바운드 아님)
- **배치 크기 = 1**: 추측적 디코딩은 저배치에서 빛남; 고배치면 타겟이 GPU 포화

### 어려운 경우
- **작은 타겟** (<7B): 오버헤드가 가치 없음
- **고도로 구조화된 출력** (코드, JSON): 드래프트가 제약 위반 가능
- **메모리 제약**: 두 모델이 안 들어갈 수 있음
- **고배치 추론**: 타겟 이미 포화; 추측적이 오버헤드만 추가

## 배포 패턴

### vLLM 통합
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-70B-Instruct",
          speculative_model="meta-llama/Llama-3-8B-Instruct",
          speculative_draft_tensor_parallel_size=1)

outputs = llm.generate(prompts, SamplingParams(max_tokens=512))
```

### TensorRT-LLM / SGLang
- 네이티브 추측적 디코딩 지원
- 검증 패스 최적화 커널
- 양쪽 모델에 대한 멀티 GPU 텐서 병렬화

## 주요 참고 자료
- Chen et al. (2023): "Accelerating Large Language Model Decoding with Speculative Sampling"
- Leviathan et al. (2023): "Fast Inference from Transformers via Speculative Decoding"
- Li et al. (2024): "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty"
- Cai et al. (2024): "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads"
- Gu et al. (2026): "Verification-Aware Training for Speculative Decoding" (NAVER AI)
- Fu et al. (2024): "Lookahead Decoding: Speculative Decoding without Draft Model"

## 관련 개념
- `concepts/ai-engineering/llm-inference.md`
- `concepts/ai-engineering/llm-serving.md`
- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/model-quantization.md`