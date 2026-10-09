---
title: "How Netflix Simplified Batch Compute with Kueue"
description: 커스텀 CMB 스케줄러에서 Titus 위 Kueue로 수백만 배치 잡을 무중단 이전 — 선점 기반 공정 공유
tags: [source, article, netflix, kubernetes, kueue, batch, platform-engineering, ko]
locale: ko
source_url: "https://netflixtechblog.com/how-netflix-simplified-batch-compute-with-kueue-87860682629c"
blog: netflix
published: 2026-06-22
---

# How Netflix Simplified Batch Compute with Kueue

저자: Alvin Bao, Alex Petrov, Jennifer Lai, Aidan Sherr, Samartha Chandrashekar. 컴퓨트의 쿠버네티스 네이티브 전환 과정에서 자사 Compute Managed Batch(CMB, 2018년)의 커스텀 큐잉·스케줄링을 Titus 컨테이너 플랫폼 위 클라우드 네이티브 잡 큐잉 시스템 Kueue로 교체했다. 동기·수백만 잡 이전법·플랫폼 제공 기능이 주제다.

## 배경: CMB와 Titus

CMB는 완료형 배치 관리형 솔루션: 테넌트 계층(내부 테넌트=조직용, 리프 테넌트=큐 보유), 테넌트별 용량 설정(공정 공유 가중치·자원 차원), 예약 용량(분할·격리) + 버스트용 전역 공유 풀 — 단 공정 공유는 입장 시점만, 선점 없음(입장 잡은 끝까지 실행). Titus는 셀 간 워크로드 연합과 연합 용량 예약을 단일 엔드포인트 뒤에 제공한다.

## 방법론

**왜 Kueue인가.** CMB는 성숙한 오픈소스 배치 옵션 이전에 태어났고, 생태계가 따라잡는 동안(공정 공유·계층 테넌트·용량 관리·우선순위 큐잉) 클러스터와 멀리 떨어진 CMB에 선점 같은 기능 추가는 고통이었다. Kueue 선정 이유: kube-scheduler를 교체하지 않아 Titus 스케줄링 프로파일·배치 효율 유지(YuniKorn/Volcano와 달리), 도입 모멘텀, 이종 하드웨어 다중 테넌트 쿼터, Pod/Job + RayJob/RayCluster 확장성, 선점·all-or-nothing·토폴로지 인식 스케줄링 내장.

**이전("Netflix Batch") 원칙.** 최종 사용자 무작업(완전 투명), 런치율·처리량 무회귀, CMB 큐잉·스케줄링을 Kueue로 교체. 셀별 Kueue에 큐잉 위임(커스텀 라우터의 Titus 연합 경유). 운영자 등록은 UI 버튼 클릭 — 내부 테넌트→Cohort, 리프→ClusterQueue+LocalQueue, 용량 설정→플레이버/공칭 쿼터, 롤백 용이. 교훈: API 동등 유지 + 내부부터 이전(내기 분리, 고객 무영향), 가장 크고 복잡한 고객부터 이전(프로덕션 이전 4주), Titus 모사 부하 시험 후 기본값 훨씬 위의 QPS/Burst/groupKindConcurrency로 운영.

**공정 공유와 선점.** 선점 기반 공정 공유로 예약 의미 유지 + 유휴 예약을 타 테넌트에 대여(`reclaimWithinCohort: Any`, `withinClusterQueue: LowerPriority`): 유휴 예약 버스트, 기아 없는 제출, 핵심 업무 빠른 처리.

## 결과

Kueue 프로덕션 전면 롤아웃, 수백만 워크로드 관리, 예약 용량 활용 상승, 쿠버네티스 네이티브 학습 인프라 팀으로 교훈 확산. Titus 배치 추가 등록 예정.

## 한계·열린 질문

- 비-Kueue Titus 배치는 관리 경험 밖에 남는다.
- 선점 churn 대 활용 트레이드오프는 테넌트별 지속 튜닝 필요.
- 높은 QPS/Burst의 API 서버 부하는 감수된 운영 비용이다.

## SW 엔지니어 시사점

- 생태계가 따라잡으면 자사 확장 고집보다 도입이 낫다 — 단 스케줄러·배치 투자는 보존되는 선택으로.
- 안정 API 뒤 내부부터 이전하고, 가장 어려운 고객을 먼저 옮겨 꼬리를 제거하라.
- 컨트롤 플레인 노브(QPS·버스트·동시성)는 프로덕션 모사 환경 부하 시험 후 롤아웃하라.
- 선점은 정적 예약을 격리 보장 유지 채 탄력 공유로 바꾼다.

## 관련 개념

- `concepts/system-design/kubernetes.md`
- `concepts/data-engineering/apache-spark.md`
