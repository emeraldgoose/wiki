---
title: TensorFlow를 이용한 홈페이지 피드 멀티태스크 학습
description: 홈페이지 피드용 통합 멀티태스크 랭킹 모델 — 공유 표현, 태스크 타워, 공동 최적화
date: 2021-06-03
tags: [source, linkedin, feed, ranking, multi-task-learning, tensorflow, ko]
locale: ko
source_url: "https://www.linkedin.com/blog/engineering/feed/homepage-feed-multi-task-learning-using-tensorflow"
blog: linkedin
author: Ian Ackerman
---

# TensorFlow를 이용한 홈페이지 피드 멀티태스크 학습

피드 랭킹은 클릭·좋아요·댓글·공유·체류·스킵 등 수많은 회원 행동을 동시에 예측해야 한다. 행동별 개별 모델에서 **TensorFlow 기반 통합 멀티태스크 딥러닝 프레임워크**로 전환해 서빙 효율과 회원 참여를 함께 개선한 이야기.

## 왜 멀티태스크인가: 행동별 모델의 한계

- 행동마다 표현을 따로 학습 — 학습·서빙 모두 연산 중복(요청당 모델 수만큼 forward pass).
- 댓글·공유 같은 희소 행동은 단독 학습 신호가 얇고, 관련 태스크 신호를 활용하지 못함.
- 독립 모델 간 불일치를 해소할 원칙적 융합 방법 부재.

## 모델: 공유 하부 + 태스크 타워

- 회원/아이템/문맥 피처 위의 **공유 하부 MLP**가 행동 공통 표현을 학습.
- 각 목적(클릭·좋아요·댓글·공유·체류…)별 **태스크 타워**가 공유 표현을 매핑, 가중 멀티태스크 손실로 **공동 최적화**.
- MTL은 암묵적 정규화: 노이즈 낀 희소 헤드(공유)가 밀집 헤드(클릭)의 구조를 빌려오고, 1회 forward pass로 서빙 비용 상각.

## 태스크 간 차이 다루기

- 핵심 리스크는 **부정적 전이(negative transfer)**: 무관한 태스크가 공유 표현을 서로 다른 방향으로 잡아당김. 태스크 그룹핑과 손실 가중으로 지배적 헤드의 기울기 독점을 방지.
- 이 shared-bottom 설계는 이후 MMoE/GR 진화의 직접적 조상. 2026년 Generative Recommender도 같은 멀티태스크 철학을 유지하되 공유 하부를 순차 트랜스포머 + 태스크별 게이팅(수동/능동 분리)으로 교체.

## 의의

- N개 모델 → 1개 모델로 서빙 공간 통합, 앙상블 대비 참여 개선 — 이후 수년간 LinkedIn 피드 랭킹의 기본형이 된 패턴.
- 2026년 LLM 리트리벌 + GR 스택에 개념적으로 계승됨(무효화가 아닌 확장: 순차 이력과 의미 임베딩 추가).

## 실무 시사점

1. MTL은 shared-bottom으로 시작, 태스크 충돌이 측정될 때만 게이팅(MMoE) 추가.
2. 헤드 간 손실 스케일 주시 — 희소 태스크 기울기가 살아남도록 정규화·가중.
3. 1회 forward/다수 헤드는 일차적으로 서빙 비용 승리이자 정규화 효과.

## 참고

- 원문: https://www.linkedin.com/blog/engineering/feed/homepage-feed-multi-task-learning-using-tensorflow
- 후속: `sources/articles/linkedin/Engineering_the_Next_Generation_of_LinkedIn_Feed.md` (GR + MMoE 후계자)
