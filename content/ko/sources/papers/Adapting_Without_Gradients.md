---
title: "Adapting Without Gradients: Affine Statistics Transport and What Its Certificate Can Tell You (번역 요약)"
description: en/sources/papers/Adapting_Without_Gradients.md 한국어 번역 요약
tags: [source, paper, huggingface, ko]
locale: ko
arxiv_id: 2609.00374
---

# Adapting Without Gradients: Affine Statistics Transport and What Its Certificate Can Tell You — 요약

**arXiv**: 2609.00374 | **게시일**: 2026-08-31 | **기관**: Talan

**저자**: Salim Khazem, Ibrahim Mohamed Serouis

## 핵심 기여

- 고정 모델용 그래디언트-프리 테스트타임 적응 방법 CASTER 제안
- 판별 부분공간에 소스 클래스 통계 저장
- 타깃 배치 모멘트에서 클래스 공유 아핀 변환 추정
- 분류 전 소스 클래스 분포를 해석적으로 전이
- 역전파·옵티마이저 상태·소스 특징 뱅크 불필요
- 28개 백본-데이터셋 중 27개 설정에서 k-NN 능가, 상태량은 18배 절감

## 방법론

CASTER는 판별 부분공간에 소스 클래스 통계를 저장. 타깃 배치 모멘트에서 클래스 공유 아핀 변환을 추정. 분류 전 소스 클래스 분포를 해석적으로 전이. 역전파, 옵티마이저 상태, 저장된 소스 특징 뱅크 불필요. 전이 가능성 인증서(transportability certificate)가 신뢰 낮은 업데이트를 차단.

## 결과

동일 고정 특징에서 28개 백본-데이터셋 중 27개 설정에서 k-NN 능가. 기존 TTA 대비 중앙값 기준 18배 적은 상태 유지. ImageNet-C(클래스 1000개당 샘플 64개)에서 무조건 전이는 top-1 21.2점 하락. 인증서 게이팅으로 -3.35점 효과를 +1.69점 이득으로 전환. 넓은 임계값 범위에서 최적 대비 0.3점 이내. Tent 적용 시 업데이트의 4.3%만 수용, 가용 이득의 0.6% 보존.

## SW 엔지니어를 위한 시사점

SW 엔지니어 관점에서 고정·서드파티 모델(운영 배포의 흔한 제약)에 동작하는 실용적 그래디언트-프리 적응 메커니즘. 18배 상태 메모리 절감은 자원 제약 환경에 유의미. 전이 가능성 인증서는 적응이 도움될지 해될지 모른다는 TTA의 핵심 불확실성을 해소하는 신뢰 게이팅. 메커니즘별 게이팅(예: Tent 수용률 4.3%)은 적응형 시스템 설계의 일반 프레임워크. 재학습·파라미터 업데이트 없이 온라인 모델 적응이 필요한 모든 시스템에 직접 적용 가능.

## 관련 개념

- `concepts/ai-engineering/agent.md`
- `concepts/ai-engineering/llm-training.md`
- `concepts/machine-learning/transformer.md`

## 참고

- 원문: en/sources/papers/Adapting_Without_Gradients.md
- arXiv: https://arxiv.org/abs/2609.00374
