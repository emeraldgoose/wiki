---
title: "GenPage: Towards End-to-End Generative Homepage Construction at Netflix"
description: 행·엔티티·레이아웃을 함께 생성하는 단일 자회귀 트랜스포머 — 프리트레이닝+WBC/RL 포스트트레이닝
tags: [source, article, netflix, recommendation, generative-models, reinforcement-learning, ai-engineering, ko]
locale: ko
source_url: "https://netflixtechblog.com/genpage-towards-end-to-end-generative-homepage-construction-at-netflix-77146fba8a08"
blog: netflix
published: 2026-06-29
---

# GenPage: Towards End-to-End Generative Homepage Construction at Netflix

저자: Lequn Wang, Jiangwei Pan, Linas Baltrunas. 넷플릭스 홈(행 × 엔티티의 2차원 구조물)은 전통적으로 다단계 파이프라인(행·엔티티별 후보 생성+랭킹)으로 만든다. LLM의 프롬프트-응답 패러다임에서 착안: "사용자+요청이 주어질 때 만족을 최대화하는 홈은?"에 답하는 단일 생성 모델이 행·엔티티·레이아웃을 함께 자회귀 생성한다. 평탄 랭크 리스트 생성기(TIGER·HSTU·OneRec)와 달리 구조 전체를 생성한다.

## 배경: 왜 생성형인가

목표: 종단 모델링(다단계 스택을 단일 트랜스포머로 — 모델 수 감소, 단계 간 목적 불일치 해소, 피처 엔지니어링 축소), RL 페이지 단위 최적화(다양성, Continue Watching 같은 행의 stopping-power 상호작용), 명확한 데이터·연산·용량 스케일링, 신규 콘텐츠·레이아웃·UI·아트워크 개인화로의 확장성. 제약: 실시간 지연, 진화 카탈로그의 엔티티 콜드스타트, 선선도, 비즈니스 규칙 강제.

## 방법론

**도메인 전용 토큰화.** 콘텍스트(참여 히스토리·프로필·요청) = 프롬프트, 페이지(레이아웃 순서의 행+엔티티) = 응답, 피드백은 내부 보상 시스템의 supervisory 신호로. 커스텀 토큰의 이득: "OITNB 50분 30일 전 시청"이 GPT-5 토크나이저 16토큰 → 4토큰(Entity_ID·Action_Type·Time_Bucket·Duration_Bucket)으로 추론 저렴 + 토큰-상품개념 1:1 매핑으로 규칙 강제 용이. 엔티티·행은 단일 토큰, 어휘 매일 갱신, OOV는 의미 임베딩 융합+폴백. 긴 소스(노출 히스토리)는 수작업 요약 — 인정된 프롬프트 엔지니어링 부채. 페이지네이션은 이전 행 + 실시간 참여를 덧붙여 세션 내 반응성 확보.

**보상 시스템.** A/B로 장기 만족에 정렬된 내부 시스템이 노출 엔티티별 스칼라 보상(몰아보기 > 10분 시청, 이탈은 음수), 페이지 보상 = 합.

**아키텍처.** 표준 디코더 전용 트랜스포머. 입출력 가중치 분리 — 프리트레이닝(softmax 다음 토큰)과 WBC 포스트트레이닝(토큰별 sigmoid)의 logit 요구가 다르기 때문.

**학습 레시피(LLM식).** 생산 인상 중 긍정 받은 노출로 처음부터 프리트레이닝 — "홈페이지 언어" 학습이지만 생산 시스템 모방에 그치고 자기생성 학습 시 퇴화 위험. 포스트트레이닝 2종: WBC(토큰 단위 가치 예측, 토큰별 크레딧 할당 내장 — 단순, 기존 랭커 목적과 정합)와 RL(어렵지만 진정한 페이지 단위 최적·테스트시점 추론·다중 토큰 엔티티의 길). 콜드스타트·선선도(일간 증분 업데이트: 최신일 + 과거 샘플로 catastrophic forgetting 방지)·비즈니스 규칙은 주변 장치로 처리.

## 결과

- 온라인 A/B(성숙한 다단계 프로덕션 대비): 핵심 출시 지표 통계적 유의 상승 + 종단 서빙 지연 −20%.
- 오프라인: 현 영역에서는 프롬프트 보강이 모델 용량 확대보다 효과 큼(120M→900M 파워로 감소하나 달러당 맥락이 승리). 다양성 목적 없이도 RL 포스트트레이닝이 홈페이지 다양성 증가.

## 한계·열린 질문

- 긴 콘텍스트는 여전히 수작업 요약 — 종단 압축은 향후 과제.
- 언어·멀티모달·추론 같은 LLM식 능력 미통합. 도메인+텍스트 하이브리드 토큰화 제안.
- 생산 노출 프리트레이닝은 생산 편향을 내재화하고 자기학습 루프 퇴화 미해결.

## SW 엔지니어 시사점

- 출력이 토큰 시퀀스로 직렬화되면 구조 출력 문제도 프롬프트→응답 생성으로 재구성하라 — RL 전체 출력 최적화가 단계별 목적이 놓치는 요소 간 상호작용을 잡는다.
- 도메인 토크나이저는 자릿수급 압축 + 출력 제어의 두 마리 토끼. 토큰을 상품 개념에 1:1 매핑하라.
- 파라미터 확대 전 프롬프트를 보강하라 — 현재 영역의 달러당 승자는 콘텍스트다.
- 선선도는 첫날부터: 일간 어휘 갱신, 리플레이 포함 증분 업데이트, OOV 폴백.

## 관련 개념

- `concepts/ai-engineering/rag.md`
- `concepts/machine-learning/reinforcement-learning.md`
- `concepts/machine-learning/attention.md`
