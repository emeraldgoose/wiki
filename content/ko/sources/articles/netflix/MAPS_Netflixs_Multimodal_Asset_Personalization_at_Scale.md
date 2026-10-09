---
title: "MAPS: Netflix's Multimodal Asset Personalization at Scale"
description: CLIP·MediaFM 멀티모달 임베딩으로 신규 타이틀 콜드스타트를 해결하는 아트워크·비디오 프리뷰 개인화
tags: [source, article, netflix, personalization, multimodal, embedding, recommendation, ko]
locale: ko
source_url: "https://netflixtechblog.com/maps-netflixs-multimodal-asset-personalization-at-scale-32f96320785e"
blog: netflix
published: 2026-08-28
---

# MAPS: Netflix's Multimodal Asset Personalization at Scale

저자: Emma Yanyang Kong, Aditya Deshpande, Asad Abbasi, Bowei Yan, David Fagnan, Ashish Rastogi, Dhaval Patel, Ray Zhang.

넷플릭스의 모든 시각 자산(타이틀 아트워크, 자동재생 비디오 프리뷰)은 그 자체로 개인화 문제다. 기존 모델은 자산을 불투명 ID로 취급해 출시 직후 상호작용 데이터가 없을 때 인기 휴리스틱으로 후퇴했다. MAPS는 멀티모달 임베딩으로 모델이 자산을 "보고 듣게" 하여 출시 직후부터 개인화를 가능하게 한다.

## 배경: 콜드스타트 문제

신규 타이틀의 자산은 학습할 행동 데이터가 없어 탐색(exploration)과 인기도 기반 노출에 의존했고, 충분한 상호작용이 쌓인 뒤에야 개인화가 작동했다.

## 방법론

**콘텐츠 인식 자산 표현.** CLIP 이미지 임베딩(768차원)과 학습된 ID 임베딩을 concat → MLP로 자산 표현 생성. 신규 아트워크도 생성 즉시 CLIP 벡터를 가지므로, 시각 테마·출연진·색감에 대한 회원 선호가 임베딩 공간에서 즉시 — 타이틀을 넘어 — 전이된다.

**5개 모델 → 1개 통합 모델.** 5개 캔버스(빌보드, 세로/가로/숏/랜드스케이프 패널)별 모델이 존재했으나, CLIP 임베딩은 크롭·리사이즈·종횡비에 불변하므로 동일 장면의 렌더링이 거의 같은 벡터가 된다. 단일 통합 모델이 전 캔버스 신호를 풀링하고, 데이터 부족 캔버스에서 이득이 최대다.

**보상 기반 가중치 학습.** 캔버스별 노출량 편중을 피하기 위해 각 학습 예시에 상호작용 유형의 장기 보상 점수 ρ로 가중 (넷플릭스 장기 보상 모델링 기반). 수작업 가중치 없이 장기 회원 만족을 최적화한다.

**IPS 오프라인 평가.** 프로덕션 로그 평가는 로깅 정책 편향이 있으므로, 무작위 정책의 탐색 트래픽에서 정확히 기록된 성향(propensity)으로 역성향점수(IPS) 추정. 온라인과 일치하는 오프라인 지표의 핵심 요인이며, IPS에서 이겨야 A/B 트래픽을 받는다.

**질의 인식 아트워크 랭킹.** 검색에서는 질의의 CLIP 텍스트 임베딩과 자산 이미지 임베딩의 코사인 유사도를 개인화 점수와 혼합(α는 A/B로 튜닝) — 추가 모델링 없이 얻는다.

**MediaFM 비디오 프리뷰.** 프레임 평균(SeqCLIP)은 소리·대사·음악을 놓친다. 8천만 샷으로 학습한 사내 멀티모달 파운데이션 모델 MediaFM이 시각(SeqCLIP)+오디오(발화/오디오 임베딩)+텍스트(자막 인코더)를 샷별 융합하며, 기존 인프라 그대로 자산 표현에 삽입된다.

**선형 프로브로 임베딩 사전 선별.** 전체 파이프라인 실험은 비용이 크므로, 임베딩만으로 탐색 데이터의 편향보정 인기 승자를 예측하는 선형 프로브로 후보를 거른다. 프로브 정확도 순서(MediaFM > SeqCLIP)가 오프라인 IPS·온라인 A/B 순서와 일치해, 이후 모든 MediaFM 버전의 게이트가 되었다.

**Netflix Embedding Store.** 모든 임베딩을 학습·서빙 시점에 동일 벡터로 제공하고(스키 없음), 파운데이션 모델 업데이트와 개인화 모델 배포를 분리 — 설정만으로 신규 임베딩 소비 가능.

## 결과

- V1(임베딩만)·V2(통합만)는 온라인 지표 무변화, V3(둘 다)만 통계적 유의 상승 → 프로덕션 적용. 숏패널 상승폭 5.691%는 V1+V2 합을 초과 (상승작용).
- TV 홈 대개편(숏패널 지배) 직전 출시, 한 달 홀드백 A/B에서 발견 지표·시청 시간 유의 상승.
- 비디오: MediaFM > SeqCLIP > ID-only (오프라인·5주 온라인 모두, TV에서 최대). MediaFM이 전 플랫폼 기본값.

## 한계·열린 질문

- IPS는 전용 탐색 트래픽이라는 영구 비용에 의존한다.
- 선형 프로브는 인기도 신호만 검출하고 개인화 가치는 보장하지 않는다.
- 캔버스별 표현 효과가 통합 과정에서 희석될 수 있다.

## SW 엔지니어 시사점

- 신규 아이템은 ID가 아니라 "내용"으로 표현하면 콜드스타트가 전이학습이 된다.
- 이질 데이터 풀링 시 노출량이 아닌 장기 가치로 가중하라.
- 비싼 종단 실험 앞에 온라인 결과와 상관이 있는 저렴한 프록시 과제를 두라.
- 학습/서빙 일관성과 분리 배포를 보장하는 공유 임베딩 저장소가 기반 인프라다.

## 관련 개념

- `concepts/ai-engineering/rag.md`
- `concepts/machine-learning/embedding.md`
- `concepts/machine-learning/attention.md`
