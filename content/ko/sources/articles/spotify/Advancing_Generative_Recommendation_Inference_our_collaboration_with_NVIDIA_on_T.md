---
title: "생성형 추천 추론의 발전: NVIDIA TensorRT LLM 협업"
description: "Spotify가 대규모 개인화 언어 모델 추천을 프로덕션 추론 아키텍처로 발전시키며 NVIDIA와 협업한 내용입니다."
tags: [source, spotify, data-engineering, recommendation, inference, ko]
locale: ko
source_url: "https://engineering.atspotify.com/2026/10/advancing-generative-recommendation-inference-our-collaboration-with-nvidia-on-tensorrt-llm"
blog: spotify
published_date: 2026-10-16
---

# 생성형 추천 추론의 발전: NVIDIA TensorRT LLM 협업

**원문**: [spotify](https://engineering.atspotify.com/2026/10/advancing-generative-recommendation-inference-our-collaboration-with-nvidia-on-tensorrt-llm) · **게시일**: 2026-10-16

## 개요

Spotify는 홈 화면의 콘텐츠, 다음에 재생할 곡, 최근에는 Spotify와 대화하는 기능까지 모든 표면과 상호작용을 개인화합니다. 전통적으로는 후보 검색과 순위 계산을 여러 단계로 나누고 표면마다 별도 시스템을 두는 추천 구조가 쓰였습니다.

생성형 AI는 이 구조를 바꾸고 있습니다. Spotify는 대규모 개인화 언어 모델(LPLM)로 여러 표면에 실시간 추천을 제공하는 방법을 연구하고 있습니다. 이 글은 실험실 개념을 대규모 프로덕션 추론 아키텍처로 옮기는 과정의 엔지니어링 과제를 다룹니다.

## 핵심 내용

- 2026년 1월 Spotify는 팟캐스트 추천에 LLM 기반 기술을 도입했습니다.
- 생성형 추천 아키텍처를 프로덕션 규모로 확장하려면 추론 지연과 처리량을 해결해야 합니다.
- Beam search로 LLM 출력 공간을 탐색해 확률이 높은 추천 시퀀스를 찾습니다.
- NVIDIA TensorRT LLM과 협업해 기능 동등성을 유지하면서 추론 성능을 높입니다.
- 여러 표면에 걸친 실시간 개인화를 하나의 추론 아키텍처로 통합하는 것이 목표입니다.

## 참고 자료

- 원문: https://engineering.atspotify.com/2026/10/advancing-generative-recommendation-inference-our-collaboration-with-nvidia-on-tensorrt-llm
