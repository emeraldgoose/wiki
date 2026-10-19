---
title: "CASTLE: 첫 실제 쿼리 전 자연어 검색 학습하기"
description: "Airbnb가 비식별화된 예약 데이터에서 합성 쿼리와 관련도 레이블을 공동 생성해 자연어 검색의 콜드-스타트 문제를 해결한다. CASTLE은 9.2배 더 나은 분포 정렬(KL 발산 1.01 대 9.33 기준선)과 91-93% 인간 레이블 동의를 달성한다." (한국어 번역)
tags: [source, airbnb, natural-language-search, cold-start, synthetic-data, information-retrieval, ko, ko]
locale: ko
source_url: "https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query"
blog: airbnb
published: "2026-10-13"
---

# CASTLE: 첫 실제 쿼리 전 자연어 검색 학습하기

**Source**: Wei 외, Airbnb Engineering, 2026-10-13

**핵심**: Airbnb는 비식별화된 예약 세션에서 합성 학습 쿼리와 관련도 레이블을 *공동으로* 생성하는 CASTLE(Contrastive And Seed-guided Training for natural Language sEarch) 프레임워크를 소개한다—실제 사용자 트래픽 없이 자연어 검색의 콜드-스타트 문제를 해결한다.

## 콜드-스타트 문제

자연어 검색은 게스트가 필터 탐색 대신 자유롭게 의도를 표현하게 한다("스키장 근처 로맨틱한 통나무집", "8인 숙박 가능한 반려동물 친화적 비치 하우스"). 하지만 모델 학습에는 쿼리와 쿼리를 리스팅에 매핑하는 관련도 레이블이 모두 필요하다. 이전 트래픽이 없으면 둘 다 처음부터 합성해야 한다.

기존 접근법(InPars, Promptagator)은 문서에서 쿼리를 생성한 후 별도 LLM 판단으로 레이블을 추가해—두 번째 오류 원인을 도입하고 실제 사용자와 먼 쿼리 분포 생성(KL 발산 9.33-26.2).

## CASTLE의 해결책: 예약 세션에서 대조적 리스팅 쌍

게스트가 대안들을 본 후 특정 리스팅을 예약하면, 그 이벤트는 선호도를 암묵적으로 인코딩한다: 예약된 리스팅이 다른 것들보다 선택됐다. CASTLE은 이 **(양성, 음성) 리스팅 쌍**을 쿼리 생성을 위한 구조적 입력으로 사용한다.

핵심 통찰: LLM에 양성 리스팅은 만족하지만 음성 리스팅은 만족하지 않는 쿼리를 생성하도록 지시하므로, **관련도 레이블이 구성적으로 정확하다**—사후 판단 불필요. 양성/음성 구분이 실제 사용자 행동에서 오며 LLM에서 오지 않아 순환성 회피.

**쿼리 생성 변형들**(다양성을 위해 결합):
- **템플릿 기반**: 일반적인 패턴 전반의 구조적 다양성
- **퓨-샷**: 사용자 연구에서 수집한 ~500개 시드 쿼리를 언어적 예시로
- **속성 기반**: 구분되는 속성(벽난로, 스키장 근접성)에 집중
- **명시적 다양성 메커니즘**: "쿼리 붕괴"(짧은 반복 구문으로 수렴) 방지

## 결과

| 지표 | CASTLE | 최고 기준선 (Promptagator) |
|--------|--------|------------------------------|
| KL 발산 (전체) | **1.01** | 9.33 |
| KL 발산 (속성 유형) | **0.08** | 0.09 (설문 시드) |
| 쿼리 길이 σ | 2.48 | 0.99 |
| 인간 레이블 동의 | **91-93%** | — |

CASTLE의 1.01 KL 발산은 Promptagator 대비 **9.2배 개선**. 속성 유형 KL(0.08)은 수작업 선별 설문 시드(0.09)조차 능가해, 생성된 쿼리가 실제 게스트 의도 다양성을 시드 자체보다 더 충실히 포착함을 의미.

**콜드-스타트 이후**: CASTLE의 합성 데이터는 실제 트래픽이 쌓인 후에도 장기 꼬리 의도(드문 숙소 유형, 편의시설 조합)를 자연스럽게 과대 샘플링해 지속적 가치 제공—유기적 트래픽에서 드물게 나타나지만 나타날 때 중요함.

## 프로덕션용 CASTLE-R

CASTLE-R은 이미 일부 실제 트래픽이 쌓인 설정으로 프레임워크 확장, 예약 이력 없는 리스팅에 Virtual Judge(LLM 평가자) 사용 및 실제 쿼리 시드 통합.

## 소프트웨어 엔지니어를 위한 시사점

**콜드-스타트 검색/추천 시스템**을 구축하는 팀에게: CASTLE은 **행동적 그라운딩 + LLM 생성**이 경쟁 아닌 보완 관계임을 보인다. 사용자 행동의 대조적 쌍이 분포 정렬과 구성적 레이블 제공; LLM 프롬프팅이 언어적 다양성 제공. 둘이 합쳐져 어느 쪽도 혼자 달성 못 한 합성-실제 격차 해소.

전체 논문: [arXiv:2605.21812](https://arxiv.org/abs/2605.21812) (CIKM 2026, DOI: 10.1145/3799682.3841071)

## 참고문헌

- 원문: [https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query](https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query)
- Jeronymo 외 (2023) InPars-v2: IR을 위한 효율적 데이터셋 생성기로서의 LLM. arXiv:2301.01820.
- Dai 외 (2023) Promptagator: 8개 예시로부터 퓨-샷 밀집 검색. ICLR.