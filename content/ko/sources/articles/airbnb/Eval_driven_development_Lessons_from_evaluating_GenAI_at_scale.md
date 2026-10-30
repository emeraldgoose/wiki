---
title: "Eval-driven development: GenAI를 대규모로 평가하며 얻은 교훈"
description: "평가를 1급 엔지니어링 규율로 다뤄 신뢰할 수 있는 GenAI를 만드는 Airbnb 방식."
tags: [source, airbnb, evaluation, genai, ko]
locale: ko
source_url: "https://airbnb.tech/ai-ml/eval-driven-development-lessons-from-evaluating-genai-at-scale"
blog: airbnb
published_date: 2026-07-30
---

# Eval-driven development: GenAI를 대규모로 평가하며 얻은 교훈

**원문**: [airbnb 블로그](https://airbnb.tech/ai-ml/eval-driven-development-lessons-from-evaluating-genai-at-scale) · **게시일**: 2026-07-30

## 개요

Airbnb 팀은 GenAI 제품을 만들 때 평가를 사후 부속물이 아니라 1급 엔지니어링 규율로 취급해 신뢰성을 확보한다. GenAI는 전통 소프트웨어 테스트의 많은 가정을 깨뜨린다: LLM 출력은 비결정적이며 "정답"은 주관적이다. 판단이 많이 필요하므로 AI가 AI를 평가하게 되고, 이 자체로 실패 모드를 만든다. 단일 LLM 상호작용은 retrieval, reasoning, tool call, generation을 사슬처럼 엮고, 각각 독립적으로 실패할 수 있다.

## 핵심 내용

- 잘못된 신뢰: 일반적인 "도움됨" 지표가 잘 나와 출시했지만 사용자가 겪는 실패 모드는 잡지 못했다.
- 미탐지 회귀: 프롬프트 변경이 측정하지 않던 차원에서 세밀하게 성능을 떨어뜨렸다.
- 낭비된 노력: 결과와 상관없는 지표에 대규모 평가 파이프라인을 구축했다.
- 목표와 게이트를 먼저 정의하고, 탐색 중에 이를 발견할 수 있음을 받아들인다.
- 실제 오류로 지표를 이끌하고, 관찰된 실패를 기반으로 cross-functional 파트너와 지표를 공동 개발한다.
- 평가자 세트는 3-5개로 작고 날카롭게 유지해 20-30개의 noisy 평가자보다 나은 3-5개 calibrated LLM-as-judge를 둔다.

## 상세

평가를 최종 점검이 아닌 엔지니어링 인프라로 다룬다. 좋은 지표는 실제 실패에 grounding되고, calibration되며, 출시 게이트에 연결된다. 이를 통해 GenAI 릴리스의 신뢰성을 유지하면서 결과와 상관 없는 측정에 노력을 낭비하지 않는다.

## 참고 자료

- 원문: [https://airbnb.tech/ai-ml/eval-driven-development-lessons-from-evaluating-genai-at-scale](https://airbnb.tech/ai-ml/eval-driven-development-lessons-from-evaluating-genai-at-scale)
