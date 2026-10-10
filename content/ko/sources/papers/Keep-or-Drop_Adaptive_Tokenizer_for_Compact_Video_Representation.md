---
title: Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation (번역 요약)
description: en/sources/papers/Keep-or-Drop_Adaptive_Tokenizer_for_Compact_Video_Representation.md 한국어 번역 요약
tags: [source, paper, huggingface, machine-learning, ko]
locale: ko
arxiv_id: 2608.24293
---

# Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation — 요약

**arXiv**: 2608.24293 | **게시일**: 2026-08-25 | **기관**: Kakao Corp.

**저자**: Yeonkyeong Lee, Hyunsung Go, Jongmin Kim, Sewoong Lim, Donghoon Lee

## 핵심 기여

- 비디오 표현을 위한 적응형 토큰 셀렉터 탑재 트랜스포머 기반 VAE, KATok 제안
- 적응형 토큰 셀렉터가 각 토큰의 콘텐츠 풍부도를 keep-or-drop 확률로 평가
- 공간 일관성을 보장하는 두 가지 위치 예측 전략(캐스케이드·결합 생성)
- SOTA 압축률에서 강력한 복원/생성 품질 달성

## 방법론

잠재 토큰과 함께 공동 학습되는 적응형 토큰 셀렉터를 갖춘 트랜스포머 기반 VAE. 콘텐츠 풍부도 기반 토큰별 드롭 확률 계산. 토큰 드롭 후 공간 일관성을 유지하는 위치 예측 전략(캐스케이드/결합 생성). 비디오 디퓨전 모델 학습으로 강력한 복원·생성 품질 달성.

## 결과

SOTA 압축률에서 강력한 복원·생성 품질. 시공간 중복 감소와 정보 없는 토큰 제거가 개선의 핵심이며 정량·정성 결과로 뒷받침.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 디퓨전 기반 이미지/비디오 생성 효율을 높이는 적응형 토큰화 기법을 제시. keep-or-drop 확률 메커니즘은 품질을 유지하며 계산 비용을 줄이는 데이터 의존 압축 방식. 위치 예측 전략(캐스케이드/결합 생성)은 토큰 드롭 시 공간 일관성을 유지하는 프레임워크로, 다중 해상도·다중 스케일 데이터를 다루는 시스템에 활용 가능.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## 참고

- 원문: en/sources/papers/Keep-or-Drop_Adaptive_Tokenizer_for_Compact_Video_Representation.md
- arXiv: https://arxiv.org/abs/2608.24293
