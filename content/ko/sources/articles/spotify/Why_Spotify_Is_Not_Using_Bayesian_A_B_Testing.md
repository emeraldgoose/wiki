---
title: "Spotify가 베이지안 A/B 테스트를 쓰지 않는 이유"
description: 베이지안 A/B 테스트는 만능이 아니라 설정(중단 규칙×사전분포×우도)의 집합 — 기본값은 빈도주의 peeking을 재현할 뿐이고, 진짜 나은 설정은 유지 비용이 더 크다는 Spotify 통계팀의 주장
tags: [source, spotify, experimentation, statistics, ab-testing, ko]
locale: ko
source_url: "https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing"
blog: spotify
published_date: 2026-09-08
---

# Spotify가 베이지안 A/B 테스트를 쓰지 않는 이유

**저자**: Mattias Frånberg (Senior Data Scientist), Mårten Schultzberg (Senior Manager, Staff Data Scientist)
**출처**: [Spotify Engineering](https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing)
**날짜**: 2026-09-08

## 개요

실험 플랫폼들이 "현대적이고 유연하며 해석이 쉽다"는 베이지안 모드를 앞다퉈 내놓는 가운데, Spotify 실험팀은 반론을 편다. "베이지안 A/B 테스트"는 하나의 방법이 아니라 중단 규칙×사전분포×우도의 설정 집합이며, 통념은 목표와 설정을 뒤섞고 있다는 것이다. 자체 논문([arXiv:2608.12949](https://arxiv.org/abs/2608.12949))을 바탕으로 네 가지 주장을 해체하고, 베이지안과 빈도주의가 겉보기보다 훨씬 가깝다는 점과 Spotify가 빈도주의에 머무는 이유를 설명한다.

## 네 가지 주장 해체

- **엿보기(peeking).** "베이즈는 peeking 보정이 필요 없다"는 두 가지를 뒤섞는다. 거짓 양성 통제에 관심 없다는 목표(우도 원리가 좁게 보장)와, 자동으로 통제해 주는 베이즈 팩터 중단이라는 설정은 다르다. 플랫폼 기본값(평탄 사전분포+사후확률 임계값)의 거짓 양성률은 빈도주의 peeking과 같아진다. 이름만 바뀐 셈이다.
- **다중 지표.** 자동 처리는 까다로운 설정에서만 성립한다. 베이즈 팩터 중단에 프로그램 자체 기록에서 맞춘 경험적 베이즈 사전분포(영점 질량 포함)가 붙어야 하고, 이는 보정 없음이 아니라 정교한 보정이다. 사전분포가 틀어지면 보장은 사라진다.
- **승자의 저주.** 가장 덜 문제적인 주장이다. 0 중심 정보 사전분포는 추정치를 당겨 편향을 줄인다. 그러나 플랫폼 기본값은 평탄 사전분포라 축소가 전혀 없고 빈도주의 점추정과 똑같이 저주를 겪는다. 잘못 맞춘 기록 사전분포(승리 실험만 모으거나 이질 프로그램 합치기)는 저자들의 시뮬레이션에서 기본 그룹 순차 검정보다 나빴다.
- **결정이론.** 흔한 비용함수에서 최적 정책은 베이즈 팩터 임계값이며, 이는 빈도주의 혼합 순차확률비 검정(mSPRT) 곧 그룹 순차 검정의 근사와 같다. 비용과 오류율은 같은 규칙의 두 표현일 뿐이라, 프레임 전환 없이 alpha/beta를 비용 관점에서 고르는 것만으로 대부분 가치를 얻을 수 있다. 진짜로 다른 건 베이즈 팩터 최적과 다른 비용함수(예: 기대손실 중단 — 평탄 사전분포에서 거짓 양성률 약 50%)뿐이다.

## 두 진영의 겹침과 Spotify의 결정

평탄 사전분포+2군 정규모형에서 베이지안과 빈도주의 출력은 수치적으로 동일하다. 사후평균=MLE, B가 A를 이길 사후확률=1−p값. 진짜 우위인 설정 — 지표별·유지보수되는 경험적 베이즈 사전분포 — 은 대규모 대표 코퍼스, 프로그램 간 풀링 금지, 드리프트 감시, 통계학자 유지보수를 요구해 대다수 조직엔 비용이 이득을 넘는다. 협업이 잦은 Spotify에겐 추론 방식이 두 개면 기획·모니터링·해석이 분열된다는 비용도 있다. 권고는 이것이다. 원하는 실험 프로그램의 보장부터 정하고, 특정 베이지안 설정이 가진 것보다 낫냐고 물어라. 오늘의 Spotify에 답은 아니다.

## 참고 자료

- [Why Spotify Is Not Using Bayesian A/B Testing — 원문](https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing)
- [동반 논문 (arXiv:2608.12949)](https://arxiv.org/abs/2608.12949) (원문에서 인용)
- [실험 증거에 대한 Spotify의 글](https://confidence.spotify.com/blog/experimental-evidence) (원문에서 인용)
- [Spotify Experiments with Learning 프레임워크](https://engineering.atspotify.com/2025/9/spotifys-experiments-with-learning-framework) (원문에서 인용)
