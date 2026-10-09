---
title: "통합 지식 그래프 인프라로 Airbnb 아이덴티티 그래프 확장하기"
description: JanusGraph + DynamoDB paved-path 그래프 플랫폼 — SaaS에서 아이덴티티 그래프 전환, P99 개선, 쓰기 10배
tags: [source, airbnb, knowledge-graph, janusgraph, infrastructure, trust-and-safety, ko]
locale: ko
source_url: "https://medium.com/airbnb-engineering/scaling-airbnbs-identity-graph-with-a-unified-knowledge-graph-infrastructure-ebac467b7836"
blog: airbnb
date: 2026-05-19
---

# 통합 지식 그래프 인프라로 Airbnb 아이덴티티 그래프 확장하기

**출처**: Airbnb Engineering (Medium) · **발행**: 2026-05-19

## 아이덴티티 그래프

사용자/관계를 정점/간선으로 모델링한 Airbnb 아이덴티티 그래프는 Trust & Safety의 기반: 신원 확인, 연결 계정 탐지, 의심 행위 적발. 두 구성: **그래프 저장**(그래프 DB + KV 캐시, 준실시간 비동기 수집, 저지연 서빙)과 **그래프 서비스**(통합 접근 + 집계/모델층).

**진화**: 관계형 DB + KV 내 JSON 간선 목록(밀도 증가에 조인 비용 폭증) → 2021년 SaaS 그래프 DB(확장되나 롱테일 지연·불안정·튜닝/ACL 불가) → 내부 그래프 인프라. 지속 난제: **70억 노드/110억 간선, 일 +500만 간선**(쓰기), **4~8홉 읽기**(지연), **fanout 편차**(핫 노드에서 P95/P99가 P50 대비 폭발), 느린 쿼리의 자원 독점(안정성).

## 플랫폼: Paved-path 지식 그래프 인프라

이전에는 네 가지 안티패턴에 분산: 관계형 "그래프"(횡단 조인 폭증), 오프라인 웨어하우스 그래프(하루 묵음), DIY 오픈소스(운영 toil), 관리형 PaaS(종속·병목). 2024년 플랫폼이 테넌트(첫 도입: 아이덴티티 그래프)를 격리 네임스페이스에 모아 단일 지원 스택으로 통합.

**기술 선택 — JanusGraph + DynamoDB (+ OpenSearch 인덱싱)**, 기준: 온라인 쿼리 확장, 표현력 있는 스키마/쿼리, 인프라·운영 적합, 확장 가능한 코드베이스. JanusGraph(Apache TinkerPop, labeled property graph, **Gremlin**)를 DynamoDB 위에 올려 **저장 분리**: 분산 영속은 관리형에 맡기고 그래프 로직은 완전 통제, 저장층 추후 교체 가능. 관리 서비스가 스키마 강제·인덱스 관리·Thrift API 제공.

**엔진 최적화**: DynamoDB 조건부 쓰기/트랜잭션 기반 맞춤 트랜잭션(기본 락보다 경량), 고fanout용 `getMultiSlices` 병렬화, 내부 포크에 Airbnb 분산 트레이싱 통합.

## 전환 (양쪽 Gremlin)

4개 앱(이벤트 수집, 벌크 적재, 서빙, 복잡 쿼리 사전계산), 컴퓨트층에서 읽기/쓰기 트래픽 분리. Gremlin 호환으로 **섀도 트래픽 병행 벤치마크** 후 운영 전환·벤더 폐기. 그러나 동일 Gremlin ≠ 동일 성능(플래너 최적화 상이)이라 **클라이언트 쿼리 재작성**: `Path`/`SimplePath` 단계 제거(느린 비배치 백엔드 쿼리로 저장 스레드 점유 → 비순환 조건부 쿼리 체인으로 대체), 부작용(side-effect) 집계 내 연산 최소화.

**성과**: 전 패턴 읽기 API 지연 감소와 **P99 급감**, 안정성(주기적 수동 인스턴스 재부팅 불필요, 빠르고 투명한 장애 대응), 부하 테스트에서 쓰기 QPS **기존 10배** 오토스케일. 사기 탐지·인벤토리 그래프·데이터 리니지로 확대.

## 엔지니어 관점 시사점

- **저장 분리**(관리형 KV 위 플러그형 그래프 로직)가 분산 저장 재구현 없이 반복 속도 확보.
- 동일 쿼리 언어도 플랜은 다름: 엔진 전환에 **클라이언트 재작성** 예산, 섀도 트래픽 우선.
- 테일 지연은 fanout에서 공략: 병렬 슬라이스 + path 단계 제거.
- paved-path 멀티테넌시가 4개 안티패턴을 근원 제거.

## 관련 개념

- Labeled property graph, Gremlin/TinkerPop, KV 기반 그래프 저장 트레이드오프
