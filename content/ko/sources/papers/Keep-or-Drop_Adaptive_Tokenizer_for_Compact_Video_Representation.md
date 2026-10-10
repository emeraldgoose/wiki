---
title: Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation
description: en/sources/papers/Keep-or-Drop_Adaptive_Tokenizer_for_Compact_Video_Representation.md 한국어 번역 요약
tags: [source, paper, huggingface, machine-learning, ko]
locale: ko
source_url: "https://arxiv.org/abs/2608.24293"
arxiv_id: 2608.24293
---

# Keep-or-Drop? Adaptive Tokenizer for Compact Video Representation

**arXiv**: 2608.24293 | **게시일**: 2026-08-25 | **기관**: Kakao Corp.

**저자**: Yeonkyeong Lee, Hyunsung Go, Jongmin Kim, Sewoong Lim, Donghoon Lee

## 핵심 기여

- 비디오 표현용 적응형 토큰 셀렉터 탑재 트랜스포머 기반 VAE, KATok 제안. 고정 압축비가 아니라 토큰별 콘텐츠 풍부도를 keep-or-drop 확률로 매겨 데이터 의존 압축
- 토큰 드롭 후 공간 일관성을 지키는 두 가지 위치 예측 전략(캐스케이드·결합 생성)
- 주장: SOTA 압축률에서 강력한 복원/생성 품질. 시공간 중복 감소+정보 없는 토큰 제거가 원인

## 방법론

잠재 토큰과 함께 공동 학습되는 셀렉터가 토큰별 드롭 확률을 계산하고, 위치 예측(캐스케이드/결합)으로 시공간 구조를 복원. 비디오 디퓨전 모델에 장착. 어느 전략이 우세한지, 어떤 해상도·움직임 구간에서인지는 초록에 없고 전문에만 있음.

## 결과

arXiv 초록에는 **수치가 없습니다** (압축률·PSNR/FVD류 점수·베이스라인 표 없음). 이 페이지에서 숫자를 인용하지 마세요. 전문(PDF, v2 2026-08-27)에서 확인할 것:

- 진술: SOTA 압축률 + 강력한 복원·생성 품질
- 진술된 원인: 시공간 중복 감소와 정보 없는 토큰 제거, 정량·정성 결과로 뒷받침 (전문 내)

## 주의

초록 기반 요약입니다. 실제 비율·데이터셋·베이스라인·캐스케이드 vs 결합 우열은 전문 표에서 확인 후 인용하세요.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 디퓨전 기반 이미지/비디오 생성 효율을 높이는 적응형 토큰화 기법을 제시. keep-or-drop 확률 메커니즘은 품질을 유지하며 계산 비용을 줄이는 데이터 의존 압축 방식. 위치 예측 전략(캐스케이드/결합 생성)은 토큰 드롭 시 공간 일관성을 유지하는 프레임워크로, 다중 해상도·다중 스케일 데이터를 다루는 시스템에 활용 가능.

## 관련 개념

- [트랜스포머](../../concepts/machine-learning/transformer.md)
- [어텐션](../../concepts/machine-learning/attention.md)
- [LLM 훈련](../../concepts/ai-engineering/llm-training.md)

## 참고

- 원문: https://arxiv.org/abs/2608.24293
- arXiv HTML: https://arxiv.org/html/2608.24293
- 범위: 초록 기반. 수치표는 PDF 전문에만 있음 (v2 2026-08-27)
