---
title: "Netflix 파운데이션 모델을 개인화 애플리케이션에 통합하기"
description: "Netflix가 파운데이션 모델의 임베딩을 여러 개인화 애플리케이션에 통합한 세 가지 접근법과 운영 방식을 설명합니다."
tags: [source, netflix, data-engineering, personalization, foundation-model, ko]
locale: ko
source_url: "https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb"
blog: netflix
published_date: 2026-10-14
---

# Netflix 파운데이션 모델을 개인화 애플리케이션에 통합하기

**원문**: [netflix](https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb) · **게시일**: 2026-10-14

## 개요

Netflix 홈페이지는 여러 특화 모델로 구동되며, 각 모델을 유지하고 혁신하려면 많은 시간과 자원이 필요합니다. Netflix는 회원 선호 학습을 중앙화하고, 방대한 상호작용 이력과 콘텐츠 데이터로 하나의 강력한 파운데이션 모델을 학습시켜 그 학습 결과를 다른 모델에 분배하는 방식을 택했습니다.

이전 글들이 파운데이션 모델 개발을 다뤘다면, 이 글은 완성된 모델을 다양한 애플리케이션에 통합하는 방법을 설명합니다. 대규모 모델의 학습·추론에 관한 연구는 많지만, 실제 개인화 제품에 어떻게 연결하는지는 별개의 문제입니다.

## 핵심 내용

- 세 가지 통합 접근법을 실험했고, 지금은 사용 사례별로 프로덕션에서 사용합니다.
- 각 접근법은 동기, 트레이드오프, 복잡성, 학습 내용이 다릅니다.
- 트랜스포머 기반 파운데이션 모델은 사용자 프로필과 아이템 표현을 생성하는 데 자연스럽게 맞습니다.
- 임베딩은 마지막 사용자 임베딩의 은닉 상태를 활용해 생성합니다.
- 모델은 매월 처음부터 사전학습하고, 매일 최신 데이터로 파인튜닝해 임베딩을 갱신합니다.

## 참고 자료

- 원문: https://netflixtechblog.com/integrating-netflixs-foundation-model-into-personalization-applications-cf176b5860eb
