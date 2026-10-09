---
title: "Building Service Topology at Scale"
description: 스트리밍 우선 실시간 서비스 의존성 지도 — 3단계 집계, 중개자 해소, 타임트래블과 프로덕션 교훈
tags: [source, article, netflix, distributed-systems, observability, data-engineering, backend, ko]
locale: ko
source_url: "https://netflixtechblog.com/building-service-topology-at-scale-architecture-challenges-and-lessons-learned-f4b792f3f0d8"
blog: netflix
published: 2026-07-13
---

# Building Service Topology at Scale

저자: Parth Jain, Rakesh Sukumar, Yingwu Zhao, Renzo Sanchez-Silva, Nathan Fisher. 앞선 "왜" 포스트의 "어떻게" 편: 통합 실시간 서비스 의존성 뷰 구축기. 로컬에서 완벽하던 첫 버전이 프로덕션에서 Kafka 컨슈머 지연·OOM·100배 트래픽 쏠림·업무 로직을 압도하는 GC 멈춤을 만나 살아남은 학습 여정이다.

## 배경: 스트리밍 우선과 다층 구조

배치 토폴로지(시간·일 단위 스냅샷)는 새벽 3시 장애 때 고고학이다. 넷플릭스는 스트리밍 우선으로: 멀티리전 Kafka 플로우 + SSE IPC 지표의 지속 수집, 배압 있는 리액티브 파이프라인, 수십 분 내 최신성. 물리적으로 분리된 3개 층(용도별 최적 저장소)을 병렬 조회·병합해 1초 미만 응답: Network(eBPF 플로우, 그래프 DB — 전수 커버, 앱 콘텍스트 없음), IPC(앱 지표, 별도 그래프 DB — 상세 엔드포인트, 계측 서비스만), Tracing(Parquet 컬럼나 — 실제 경로, 샘플링).

## 방법론

**버퍼·드롭·배치 대신 배압.** 무한 큐는 OOM, 드롭은 엣지 손실, 배치는 시점상실. 리액티브 스트림이 상류를 늦춘다(Stage 3 → 2 → 1 → Kafka 일시정지): 무손실 우아한 저하 — 대신 코드 추론 난이도가 영구 비용이다.

**중개자 해소의 3단계 집계.** 플로우 로그의 홉(App A → LB → App B)을 논리 의존성(App A → App B)으로. Stage 1(수집): 필터·5분 윈도 배치·초기 집계·일관 해시 분배·SSE. Stage 2: LB/NAT/API 게이트웨이/프록시 중개자 해소. Stage 3: 보강 후 그래프 기록.

**프로덕션 난관과 수정.** ASG 규모 변화 시 해시 파티션 재배분, 수백만 rec/s에서 불변 자료구조의 GC 압박, 파티션 쏠림, 컨슈머 랙 — 측정 주도 최적화(재현→프로파일→수정→규모 검증) 방법론으로 돌파.

**타임트래블 질의.** 버전 스냅샷으로 임의 시점 토폴로지 재구성 — "장애 전 무엇이 바뀌었나" 분석의 핵심.

## 결과

초당 수백만 플로우 처리, 임의 시점 재구성, 1초 미만 병합 조회, 배치의 수 시간·수 일 대비 수십 분 최신성 — 라이브 이벤트 대응, 현재 데이터 기반 장애 분류, 변경 영향 즉시 검증의 기반.

## 한계·열린 질문

- 최신성은 수십 분이지 수 초가 아니다 — 토폴로지에는 충분, 요청 추적에는 부족.
- 리액티브 복잡도는 영구 운영 비용이다.
- 트레이싱층 통합은 후속 포스트로 연기.

## SW 엔지니어 시사점

- 장애 관측은 완전성보다 최신성: 약간 늦은 실시간이 시간 지난 배치나 손실 드롭보다 낫다.
- 처리량·질의·진화 속도가 다른 소스는 만능 저장소 하나보다 소스별 분리 + 조회 시점 병합이 낫다.
- 인프라 중개자를 논리 의존성으로 해소하지 않으면 토폴로지가 로드밸런서로 뒤덮인다.
- 로컬 성공 ≠ 프로덕션 성공: GC·쏠림·리밸런스를 프로덕션형 부하로 프로파일하라.

## 관련 개념

- `concepts/system-design/distributed-systems.md`
- `concepts/data-engineering/stream-processing.md`
- `concepts/system-design/observability.md`
