---
title: Knowledge Distillation (지식 증류)
description: 큰 교사 모델의 지식을 작은 학생 모델로 소프트 타겟, 중간 표현, 행동 매칭을 통해 전달하는 모델 압축 기법
tags: [concept, machine-learning, knowledge-distillation, model-compression, teacher-student, ko]
locale: ko
---

# Knowledge Distillation (지식 증류)

**Knowledge Distillation (KD, 지식 증류)**은 크고 고성능인 **교사 모델(Teacher)**의 지식을 작고 효율적인 **학생 모델(Student)**로 전달하는 모델 압축 기법입니다. 학생은 교사의 행동(출력 분포, 중간 표현, 추론 패턴)을 모방하도록 학습합니다.

## 핵심 개념

```
교사 (큼, 정확함, 느림)  →  지식 전달  →  학생 (작음, 빠름, 배포 가능)
```

- **소프트 타겟**: 교사의 전체 확률 분포 (로짓/소프트맥스 with temperature)
- **하드 타겟**: 정답 레이블 (표준 교차 엔트로피)
- **Temperature (T)**: 분포를 부드럽게 함; 높을수록 클래스 간 관계 더 잘 드러남

## 증류 목적 함수

### 1. 로짓 기반 (출력) 증류 — Hinton et al., 2015
**순방향 KL (표준 KD)**:
```
L_KD = T² × KL(softmax(z_teacher/T) || softmax(z_student/T))
L_CE = CrossEntropy(student_logits, labels)
L_total = α × L_KD + (1-α) × L_CE
```
- **Temperature T**: 보통 2–10; 높을수록 더 부드럽고 정보 많음
- **가중치 α**: 증류 vs 정답 균형 (보통 0.5–0.9)

**역방향 KL**:
```
L_rev = KL(softmax(z_student/T) || softmax(z_teacher/T))
```
- 모드 탐색적; 학생이 교사의 고확률 모드 매칭
- 과도한 평활화 방지하지만 저확률 지식 놓칠 수 있음

### 2. 특징 기반 (중간) 증류
- **힌트 학습**: 중간 활성화 매칭 (어텐션, MLP 출력)
- **어텐션 전이**: 어텐션 맵 매칭
- **FitNets**: 학생의 중간 레이어가 교사의 것을 예측하도록 학습 (Romero et al., 2015)

### 3. 관계 기반 증류
- **인스턴스 관계**: 쌍별 유사도 매칭 (그램 매트릭스)
- **인스턴스-특징 관계**: 샘플-특징 간 상관관계 매칭

### 4. 데이터 프리 증류
- 교사로부터 합성 데이터 생성 (GAN, 역전파, 샘플링)
- 원본 학습 데이터 접근 불필요

## 고급 변형

### 중간 단계 증류 (Meta, 2026)
- **설정**: 사후 학습이 아닌 **지속적 사전 학습 중간(mid-training)**에 증류 수행
- **발견**: 순방향 KL이 사전 학습 vs 중간 단계에서 다르게 동작:
  - 사전 학습: 추론 능력 AND 사실 회상 모두 개선
  - 중간 단계: 추론은 개선되지만 **사실 회상 습득이 느려짐**
- **원인**: 교사 신뢰도 비대칭 (절차적 데이터에서 더 높음, 지식 집약적 데이터에서 더 낮음) + 학생의 진화하는 지식 상태
- **해결**: **Switch Distillation** — 교사 예측 엔트로피로 라우팅:
  - 교사 고신뢰도 (낮은 엔트로피) → 증류 (KD)
  - 교사 저신뢰도 (높은 엔트로피) → 교차 엔트로피
- **결과**: 추론 1.61–1.71×; 지식 1.13–1.19×; 사실 회상 96.7% 보존

### 온라인 / 자기 증류
- **Born Again Networks**: 순차적 증류 (학생 → 새 학생)
- **자기 증류**: 모델이 자신의 이전 체크포인트/앙상블로부터 증류
- **외부 교사 불필요**

### 점진적 증류
- 높은 온도에서 시작해 T=1로 서서히 어닐링
- 커리큘럼: 쉬움(부드러움) → 어려움(날카로움) 타겟

### 양자화 인식 증류
- 증류 + 양자화(PTQ/QAT) 공동 최적화
- 학생을 양자화 노이즈와 함께 학습; 양자화된 교사 행동 매칭

## 학습 전략

### 교사 선택
| 요소 | 권장사항 |
|--------|----------------|
| **용량 차이** | 교사가 학생보다 2–10× 큼 |
| **아키텍처 일치** | 동일 아키텍처 패밀리 선호 (교차 아키텍처도 작동) |
| **품질** | 사용 가능한 최적 교사; 앙상블 > 단일 |

### 데이터 고려사항
- **원본 학습 데이터**: 사용 가능하면 최적
- **레이블 없는 데이터**: 교사가 소프트 레이블 생성 (반지도 학습)
- **합성 데이터**: 교사가 입력+출력 모두 생성 (데이터 프리)
- **도메인 불일치**: 교사를 타겟 도메인에서 먼저 파인튜닝

### 손실 스케줄링
- **정적 α, T**: 단순; 실무에서 잘 작동
- **동적 α**: 학생 성능 향상에 따라 KD 가중치 증가
- **동적 T**: 온도 어닐링 (높음 → 낮음)

## LLM 적용 사례

### 모델 압축
- LLaMA-70B → LLaMA-7B/13B (Alpaca, Vicuna 스타일)
- GPT-4 → 작은 오픈 모델 (API 통해 증류)

### 특수 증류
- **추론 증류**: 교사의 CoT → 학생 (CoT 증류)
- **도구 사용 증류**: 교사의 도구 호출 → 학생
- **다국어 증류**: 교사의 고리소스 → 학생의 저리소스

### 효율적 배포
- **엣지 친화적** 크기(1B–3B)로 증류해 모바일/온디바이스용
- **양자화**(INT4/INT8) + **가지치기**와 결합

## 평가

### 충실도 지표
- **출력 KL**: 홀드아웃 데이터에서 KL(교사 || 학생)
- **일치율**: Top-1 토큰 일치 비율
- **분포 유사도**: JS 발산, 로짓 코사인 유사도

### 능력 유지
- **다운스트림 벤치마크**: MMLU, GSM8K, HumanEval 등
- **상대 성능**: 학생/교사 점수 비율
- **창발 능력**: 학생이 CoT, 도구 사용 등 유지하는가?

### 효율성 이득
- **지연시간**: 토큰/초 개선
- **메모리**: 파라미터 수, KV 캐시 감소
- **처리량**: 배치 추론 속업

## 주요 참고 자료
- Hinton et al. (2015): "Distilling the Knowledge in a Neural Network"
- Romero et al. (2015): "FitNets: Hints for Thin Deep Nets"
- He et al. (2026): "Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall" (Meta)
- Zhang et al. (2024): "Switch Distillation: Adaptive Routing for Knowledge Distillation"
- Agarwal et al. (2024): "Distilling Step-by-Step: Outperforming Larger Models with Less Training Data"

## 관련 개념
- `concepts/ai-engineering/llm-training.md`
- `concepts/ai-engineering/model-quantization.md`
- `concepts/ai-engineering/model-pruning.md`
- `concepts/machine-learning/transformer.md`
- `concepts/ai-engineering/speculative-decoding.md` (드래프트 모델 학습)