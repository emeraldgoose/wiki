---
title: Engineering the Next Generation of LinkedIn's Feed
description: LinkedIn 피드 추천 스택 전면 개편 — LLM 기반 통합 리트리벌과 트랜스포머 Generative Recommender 랭킹
date: 2026-03-12
tags: [source, linkedin, feed, ranking, llm, recommender-systems, retrieval, ko]
locale: ko
source_url: "https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed"
blog: linkedin
author: Hristo Danchev
---

# Engineering the Next Generation of LinkedIn's Feed (차세대 피드 엔지니어링)

13억 명 이상의 전문가에게 서비스되는 LinkedIn 피드의 추천 스택 전면 개편기. LLM 기반 통합 리트리벌 파이프라인과 트랜스포머 기반 Generative Recommender(GR) 랭킹 모델을 GPU 위에서 밀리초 단위로 서빙한다.

## 기존 구조의 한계

- **이질적 리트리벌:** 연대순 네트워크 인덱스, 지역 트렌딩, 협업 필터링, 업계 트렌딩, 임베딩 검색 등 각기 다른 시스템이 병렬로 동작 — 유지보수 비용이 크고 전체 최적화가 불가능.
- **독립 인상 평가:** 랭커가 각 후보 포스트를 직전閲覧 맥락 없이孤立 평가 — 관심 궤적(interest trajectory) 무시.

## LLM 기반 통합 리트리벌

공유 LLM이 회원·포스트 프롬프트를 동일 임베딩 공간에 인코딩하고 코사인 유사도로 k-NN 검색하는 단일 듀얼 인코더로 교체. 수백만 포스트 인덱스에서 검색 지연 50 ms 미만.

### 구조화 데이터 → 프롬프트

"프롬프트 라이브러리" 템플릿으로 피처를 텍스트화. 포스트(형식, 작성자 헤드라인, 회사, 업계, 참여 수, 본문), 회원(경력, 스킬, 학력 + 시간순 참여 이력).

**수치형 피처 처리:** "views:12345" 같은 원시 수치는 토큰으로 취급되어 인기도-유사도 상관관계가 거의 0(−0.004). **퍼센타일 버케팅**(`71` = 조회수 상위 71%)으로 단일 토큰의 안정적 표현으로 변환 → 상관관계 30배 개선, recall@10 +15%.

### 듀얼 인코더 학습

- **InfoNCE 손실**, easy negative(미노출 무작위 포스트) + hard negative(노출됐으나 무반응).
- hard negative 2개 추가만으로 recall@10 +3.6%.
- 참여 이력에서 긍정 반응만 남기면 메모리 37%↓, 배치당 시퀀스 40%↑, 학습 반복 2.6배高速 — 품질 동등 이상.
- 8× H100으로 학습.

### 신선도 유지

프롬프트 생성 → 임베딩 추론 → 인덱스 업데이트 3개 nearline 파이프라인이 상시 동작. 신규 포스트는 거의 실시간 임베딩, 반응이 오는 기존 포스트는 동적 갱신.

## 랭킹: Generative Recommender

회원의 과거 상호작용 1,000개 이상을 시퀀스("직업적 이야기")로 보고 인과 어텐션 트랜스포머로 모델링. 포스트 표현과 행동(장시간 체류·좋아요·댓글·공유) 임베딩을 교차 배치.

- **순차 모델 > 포인트와이즈:** 희소 사용자에게 특히 효과.
- **Late fusion:** 트랜스포머 출력에 문맥 피처(기기, 프로필 임베딩, 친밀도 점수)를 이어붙여 예측 — 트랜스포머를 작게 유지.
- **MMoE 헤드:** 수동적 작업(클릭·스킵·장시간 체류)과 능동적 작업(좋아요·댓글·공유)에 전문화된 게이팅.
- **서빙:** CPU 피처 처리/GPU 추론 분리, 공유 문맥 배칭(이력 1회 인코딩 후 전 후보 병렬 스코어링), 커스텀 Flash Attention 변형(GRMIS)으로 PyTorch SDPA 대비 약 2배高速.
- **효과:** 후속 Feed SR 롤아웃 A/B에서 **체류 시간 +2.10%** (기존 DCNv2 대비).

## 실무 시사점

1. LLM 프롬프트에 넣기 전 수치형 피처는 퍼센타일 버케팅.
2. hard negative(노출-무반응)의 가치가 easy negative보다 압도적.
3. 학습 이력은 긍정 반응만으로 필터링 — 저렴하고 품질 동등.
4. 문맥 피처는 late fusion으로, 트랜스포머 입력 확장은 자제.
5. 멀티 아이템 스코어링용 커스텀 어텐션 커널로 서빙 여유 약 2배 확보.

## 참고

- 원문: https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed
- 관련 논문: "An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking" (2026-02)
