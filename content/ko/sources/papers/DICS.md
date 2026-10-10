---
title: "DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection"
description: '표본 내 일관성(DIC)으로 시각 지시 데이터를 골라 25%로 전체 미세조정 능가'
tags: [source, paper, huggingface, machine-learning, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.30209"
arxiv_id: 2608.30209
---

# DICS: Exploring Data Intrinsic Consistency for Visual Instruction Selection

**arXiv**: 2608.30209 | **게시일**: 2026-08-31 | **기관**: SpatialAxiom

**저자**: Yuyang Hong, Jinhui Guo, Jiaqi Gu, Lubin Fan, Ruixiang Wang, Kun Ding, Yue Wu, Shiming Xiang, Jieping Ye

## 핵심 기여

- **DIC(데이터 내재 일관성)**: 표본 내 결속의 자가 채점 지표 — VIC(시각 내용↔지시문 정렬) + RIC(지시문 대비 응답 결속)
- **DICS 선택**: 데이터 예산별로 표본 내 일관성과 전체 분포 다양성의 균형을 적응 최적화. 다양성·휴리스틱 의존에서 탈피
- **DICS-6M**: 600만 표본 멀티모달 지시 코퍼스. 사상 최대 규모 시각 지시 선택 연구

## 방법론

전 표본을 DIC(VIC+RIC)로 채점한 뒤 고정 비율 제약에서 상위 일관성 표본과 분포 커버리지를 함께 최적화. 데이터 규모·모델 아키텍처별로 평가.

## 결과

| 발견 | 수치 |
|---|---|
| 전체 데이터 미세조정 대비 | LLaVA-1.5-665K의 **25%**만으로 능가 |
| InternVL3-8B-Instruct 공식 대비 | 학습 데이터 **25% 미만**으로 성능의 **94.52%** |
| 일반성 | 규모·아키텍처 전반에서 SOTA 선택법 일관 우세 |

## SW 엔지니어를 위한 시사점

VLM 지시 튜닝 예산이 있다면 다양성 말고 표본 내 일관성(응답이 지시문·이미지와 실제로 결속하는지)으로 거르세요. 25% 데이터로 전체 능가는 직접적 학습비 절감입니다. 코드: https://github.com/cqu-student/DICS

## 관련 개념

- [임베딩](../../concepts/machine-learning/embedding.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)

## 참고

- 원문: https://arxiv.org/abs/2608.30209
- HF Daily Papers: https://huggingface.co/papers/2608.30209
- 범위: 초록 기반. 규모별 표는 전문에서 확인
