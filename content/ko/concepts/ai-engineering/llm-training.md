---
title: LLM 학습 & 파인튜닝
description: "원시 텍스트에서 정렬된 모델까지: 사전 학습, 지속적 사전 학습, 지도 미세조정, 선호도 정렬(RLHF/DPO)의 전체 라이프사이클"
tags: [concept, ai-engineering, llm-training, fine-tuning, pre-training, rlhf, ko]
locale: ko
---

# LLM 학습 & 파인튜닝

**LLM 학습**은 원시 텍스트에서 정렬된 모델까지의 전체 라이프사이클을 포함합니다: 대규모 코퍼스에서의 사전 학습, 도메인 데이터에서의 지속적 사전 학습, 지시 데이터에서의 지도 미세조정(SFT), 인간 가치와의 정렬을 위한 선호도 정렬(RLHF/DPO).

## 학습 단계

### 1. 사전 학습 (Foundation)
**목표**: 대규모 다양한 코퍼스(수조 토큰)에서 다음 토큰 예측
- **데이터**: Common Crawl, Wikipedia, 코드(GitHub), 책, 학술 논문
- **아키텍처**: 디코더 전용 Transformer (GPT, LLaMA 등)
- **스케일링 법칙**: 컴퓨트 최적 할당 (Chinchilla: 토큰 ≈ 20× 파라미터)
- **병렬화**: 3D/4D 병렬화 (DP + TP + PP + CP/EP)
- **체크포인팅**: 분산 체크포인트 (ShardedTensor); 비동기 저장

### 2. 지속적 사전 학습 (도메인 적응)
**목표**: 파운데이션 모델을 도메인별 분포로 적응
- **데이터**: 도메인 코퍼스 (코드, 법률, 의료, 금융, 다국어)
- **비율**: 사전 학습 컴퓨트의 1–10%면 일반적으로 충분
- **기법**:
  - **리허설**: 원본 사전 학습 데이터 일부 혼합해 치명적 망각 방지
  - **학습률**: 더 낮게 (1e-5 → 1e-6); 웜업 + 코사인 디케이
  - **토크나이저 확장**: 필요시 도메인별 토큰 추가

### 3. 지도 미세조정 (SFT / Instruction Tuning)
**목표**: 모델이 지시를 따르고 도구를 사용하도록 학습
- **데이터**: 고품질 지시-응답 쌍 (50K–1M 샘플)
  - 인간 주석 (Alpaca, Dolly, OpenAssistant)
  - 합성 (Self-Instruct, Evol-Instruct, Magpie)
  - 강한 모델에서 증류
- **포맷**: 채팅 템플릿 (ChatML, Llama-3, Gemma 등)
- **손실**: 응답 부분만 다음 토큰 예측 (프롬프트 마스킹)
- **하이퍼파라미터**: LR 1e-5–2e-5; 1–3 에포크; 효율성 위한 패킹

### 4. 선호도 정렬 (RLHF / RLAIF / DPO)
**목표**: 인간 선호도(도움됨, 무해함, 정직함)와 정렬

#### RLHF (Reinforcement Learning from Human Feedback)
1. **보상 모델 (RM)**: 쌍별 비교로 Bradley-Terry 모델 학습
2. **PPO**: SFT 레퍼런스 대비 KL 페널티로 정책 최적화
3. **과제**: 보상 해킹, 학습 불안정, 높은 컴퓨트

#### DPO (Direct Preference Optimization) — Rafailov et al., 2023
- **RM 없음, PPO 없음**: 선호도 쌍에 직접 손실 적용
- **손실**: `log σ(β log π(y_w\|x)/π_ref(y_w\|x) - β log π(y_l\|x)/π_ref(y_l\|x))`
- **단순, 안정, 오프라인**: 실무 배포에 선호됨

#### 변형들
- **IPO**: 레퍼런스 모델 없는 Identity preference optimization
- **KTO**: 이진 피드백만으로 Kahneman-Tversky optimization
- **SPIN**: 자기 대결 파인튜닝 (인간 데이터 불필요)
- **SimPO**: 길이 정규화로 단순화한 DPO

## 핵심 기법

### 데이터 품질 & 큐레이션
- **중복 제거**: 문서/문단 레벨에서 정확 + 퍼지 (MinHash LSH)
- **필터링**: 품질 분류기 (fastText, GPT 기반), 독성, PII
- **혼합**: 도메인 비율을 스케일링 법칙 실험으로 튜닝
- **커리큘럼**: 쉬움 → 어려움; 도메인별 단계

### 메모리 & 컴퓨트 최적화
| 기법 | 메모리 절약 | 용도 |
|-----------|---------------|------|
| **ZeRO-3** | 완전 샤딩 (파라미터/그래디언트/옵티마이저) | 큰 모델 (>13B) |
| **FSDP** | PyTorch 네이티브 샤딩 | PyTorch 2.0+ 표준 |
| **활성화 체크포인팅** | 저장 대신 재계산 | 모든 큰 모델 |
| **FlashAttention** | IO-인어텐션 커널 | 2배 속도, HBM 감소 |
| **시퀀스 병렬화** | 시퀀스를 GPU 간 분할 | 긴 컨텍스트 (>32K) |
| **컨텍스트 병렬화** | 초긴문에 링 어텐션 | 1M+ 컨텍스트 |
| **BF16/FP8** | 정밀도 감소 | H100+ (FP8); A100 (BF16) |

### 분산 학습
- **데이터 병렬화 (DP)**: 모델 복제; 배치 분할
- **텐서 병렬화 (TP)**: 레이어 분할 (어텐션 헤드, MLP)
- **파이프라인 병렬화 (PP)**: 레이어를 GPU 간 분할 (마이크로배치)
- **전문가 병렬화 (EP)**: MoE용; 토큰을 전문가로 라우팅
- **3D/4D 병렬화**: DP+TP+PP(+EP/CP) 결합으로 100B+ 모델

### 지속적 사전 학습 전략
- **지식 증류** (`concepts/machine-learning/knowledge-distillation.md` 참조): 교사 → 학생
- **중간 단계 증류**: 지속적 사전 학습 중 순방향 KL (Meta, 2026)
- **Switch Distillation**: 엔트로피 기반 KD와 CE 간 라우팅

## 학습 중 평가

### 퍼플렉시티 & 손실 곡선
- 학습/검증 손실 수렴; 발산 감시
- 지속적 사전 학습용 도메인별 평가 세트

### 다운스트림 벤치마크
| 카테고리 | 벤치마크 |
|----------|------------|
| **지식** | MMLU, GPQA, TriviaQA |
| **추론** | GSM8K, MATH, BBH, ARC |
| **코드** | HumanEval, MBPP, LiveCodeBench |
| **긴 컨텍스트** | Needle-in-Haystack, RULER, LongBench |
| **정렬** | MT-Bench, AlpacaEval, Arena-Hard |
| **안전성** | TruthfulQA, ToxiGen, WildGuard |

### LLM-as-a-Judge
- 강한 모델(GPT-4, Claude)로 출력 평가
- 단일 점수보다 구조화된 루브릭
- 인간 주석과 캘리브레이션

## 실용적 레시피

### 7B 모델 SFT (단일 노드, 8×A100)
```bash
torchrun --nproc_per_node=8 train.py \
  --model meta-llama/Llama-3-8B \
  --data data/sft.jsonl \
  --lr 2e-5 --epochs 3 --batch_size 4 \
  --gradient_accumulation 4 \
  --bf16 --flash_attn --fsdp full_shard
```

### 70B 모델 DPO (멀티 노드, 32×H100)
```bash
torchrun --nnodes=4 --nproc_per_node=8 train_dpo.py \
  --model meta-llama/Llama-3-70B \
  --data data/preferences.jsonl \
  --beta 0.1 --lr 5e-7 --epochs 1 \
  --bf16 --fsdp full_shard --tp 4 --pp 2
```

## 흔한 함정

| 함정 | 증상 | 해결 |
|---------|---------|-----|
| **치명적 망각** | 사전 학습 지식 상실 | 리허설 혼합; 낮은 LR; LoRA |
| **보상 해킹** | 높은 보상, 넌센스 출력 | KL 페널티; RM 앙상블; DPO |
| **길이 편향** | 장황한 출력 선호 | 길이 정규화 (SimPO); 보상 형성 |
| **학습 불안정** | 손실 스파이크, NaN | 그래디언트 클리핑; LR 웜업; BF16 |
| **데이터 오염** | 벤치마크 유출 | 벤치마크와 중복 제거; 홀드아웃 세트 |

## 주요 참고 자료
- Kaplan et al. (2020): "Scaling Laws for Neural Language Models"
- Hoffmann et al. (2022): "Training Compute-Optimal Large Language Models" (Chinchilla)
- Touvron et al. (2023): "LLaMA 2: Open Foundation and Fine-Tuned Chat Models"
- Rafailov et al. (2023): "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
- He et al. (2026): "Knowledge Distillation During Mid-Training Favors Reasoning over Factual Recall" (Meta)
- Zhao et al. (2024): "SPIN: Self-Play Fine-Tuning Converts Weak Language Models to Strong Ones"

## 관련 개념
- `concepts/machine-learning/knowledge-distillation.md`
- `concepts/ai-engineering/rlhf.md`
- `concepts/ai-engineering/llm-serving.md`
- `concepts/ai-engineering/model-quantization.md`
- `concepts/machine-learning/transformer.md`