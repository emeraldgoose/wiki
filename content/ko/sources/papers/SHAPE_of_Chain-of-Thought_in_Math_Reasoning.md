---
title: SHAPE of Chain-of-Thought in Math Reasoning
description: 'CoT의 의미 공간·휴리스틱 분석 — 다양성 장려가 정확도 향상'
tags: [source, paper, huggingface, machine-learning, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.28600"
arxiv_id: 2608.28600
---

# SHAPE of Chain-of-Thought in Math Reasoning

**arXiv**: 2608.28600 | **게시일**: 2026-06-28 | **기관**: Seoul National University

**저자**: Jonghyun Song, Sangjun Song, Minjae Oh, Haesung Pyun, Sungsik Lee, Yohan Jo

## 핵심 기여

- **SHAPE**: 수학교육학 2개 렌즈로 CoT 궤적 분석 — (1) 의미 공간(대수·기하 등 문제 해석의 전개), (2) 휴리스틱(공간 안 행동: 단순화·역행 등)
- **서술 발견**: 모델의 휴리스틱이 정답 여부를 전통 CoT 특징보다 잘 설명. 정답은 많은 공간 탐색이 아니라 소수 공간 집중(인간 일치 패턴)
- **사후학습 발견**: RL이 휴리스틱 사용의 모드 추구(mode-seeking) 유발
- **개입**: 다양한 휴리스틱 장려 사후학습이 정확도 향상

## 방법론

여러 모델의 추론 패턴에 SHAPE 렌즈 적용(패턴 분석) → 사후학습이 수학 숙련을 진짜 키우는지 평가 → 다양성 신호로 학습.

## 결과

구조-정성 결과(초록에 단일 대표 수치 없음). 휴리스틱 프로파일이 CoT 특징을 이기고, 집중>범위 패턴, RL 모드축소 진단, 다양성 학습 효과. 모델별 표는 전문에서 확인.

## SW 엔지니어를 위한 시사점

수학 추론 디버깅에는 CoT 길이가 아니라 *휴리스틱·의미 공간*을 로깅하세요 — 정답을 예측합니다. RL 사후학습이 정체면 휴리스틱 모드 붕괴를 의심하고 다양성을 명시 보상하세요. 코드: https://github.com/holi-lab/SHAPE-of-CoT

## 관련 개념

- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)
- [트랜스포머](../../concepts/machine-learning/transformer.md)
- [어텐션](../../concepts/machine-learning/attention.md)

## 참고

- 원문: https://arxiv.org/abs/2608.28600
- HF Daily Papers: https://huggingface.co/papers/2608.28600
- 범위: 초록 기반. 모델별 분석은 전문에서 확인
