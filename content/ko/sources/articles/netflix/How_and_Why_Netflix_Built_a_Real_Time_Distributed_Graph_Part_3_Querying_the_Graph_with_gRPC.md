---
title: "How and Why Netflix Built a Real-Time Distributed Graph Part 3: Querying the Graph with gRPC"
description: 80억 노드·1500억 엣지 실시간 그래프의 gRPC 서빙층 — 너비우선 비동기 탐색, 조기 필터링, 선별 캐싱
tags: [source, article, netflix, distributed-systems, graph, grpc, serving, ko]
locale: ko
source_url: "https://netflixtechblog.com/how-and-why-netflix-built-a-real-time-distributed-graph-part-3-querying-the-graph-with-grpc-0f3468349607"
blog: netflix
published: 2026-08-07
---

# How and Why Netflix Built a Real-Time Distributed Graph Part 3: Querying the Graph with gRPC

저자: Nilesh Mishra, Ajit Koti. RDG 시리즈 3부작의 마지막(1부 Flink 수집 파이프라인, 2부 10억 규모 저장층). 수집·저장이 아무리 좋아도 복잡한 질의가 그래프가 계속 커지는 와중에 100ms 안에 답해야 한다. 80억 노드·1500억 엣지, 수만 QPS를 감당하는 서빙층 설계가 주제다.

## 배경: 상반된 두 질의 형태

- **얕고 넓게**(이 계정이 30일간 쓴 디바이스는?): 1홉이나 fan-out 폭발 — I/O 처리량 압박.
- **깊고 좁게**(계정 X의 Stranger Things 시청 여정): 2~4홉 체인, 순차 의존성(Hop 1 결과 없이 Hop 2 불가) — 홉마다 네트워크 왕복이면 100ms 초과.

## 방법론

**깊이우선 대신 너비우선.** 레벨 단위로 전 노드 병렬 확장(프로필 전부 → 시청 엣지 전부 → 콘텐츠 상세). 순차 체인 대신 수 차례 병렬 라운드. 비용은 레벨 너비에 비례하며 엣지 타입별 상한으로 제한.

**스레드-퍼-요청 대신 비동기 우선.** 지연의 대부분이 I/O이므로 전체 파이프라인을 비동기 합성으로 — 16~24개 스레드로 수천 동시 요청 처리(블로킹 없음).

**3층 아키텍처.** Graph Query Service(gRPC 진입·탐색 명세 검증) → 실행 엔진(너비우선 오케스트레이션) → KVDAL 위 저장 추상층(노드 조회·엣지 스트리밍·EVCache) → 옵트인 Enrichment층(외부 메타데이터 배치 조회, fail-open).

**질의 여정(2홉 예시).** (1) 필터/상한 계층(앱 기본 → 전역 오버라이드 → 깊이별 → 엣지타입별)으로 실행 계획 확정, 과다 조회 사전 차단. (2) 인접 리스트 직접 조회로 "X의 이웃"을 인덱스 읽기로, 대량 인접은 100개씩 스트리밍하며 소스 측 필터링(기간·제목) 후 조기 종료. (3) 명시적 동시성 상한 + 건강 시 확장·압박 시 축소의 리미터. (4) 선별 캐싱: 안정적·핫 노드만 EVCache에 변동성 맞춤 TTL(적중률 70–80%, 저장 호출 3–4배 감소), 그래프 보관 만료 임박 노드는 스킵(smart TTL).

**명시적 트레이드오프.** 최종적 일관성(최근접 레플리카 읽기 — "최근"이면 충분), enrich는 요청별 옵트인(호출자가 필요를 안다).

## 결과

- 1홉: P50 15–30ms, P99 < 100ms. 3홉: P99 100–150ms, fan-out 증가에도 안정.
- 16–24 스레드로 수천 동시 처리, 인기 엔티티 캐시 적중 70–80%.

## 한계·열린 질문

- 비동기 합성은 인프라 비용을 줄였지만 디버깅을 어렵게(스택 추적 난독, 예외 유실) — 단계별 지표로 보완.
- 캐싱은 시행착오 끝에 선별+smart TTL로 정착.
- 프론티어 너비에 비례하는 메모리 — 적대적 넓은 질의는 엣지 상한에 의존.

## SW 엔지니어 시사점

- 기능이 아니라 프론티어로 생각하라: API는 탐색할 프론티어를 기술하고 시스템이 걷는 법을 정한다.
- 일찍 필터하라: 저장층 가까이로 필터/상한을 밀어넣고, 가져와서 자르지 마라.
- 병렬화는 다이얼이다: 명시적 상한 + 동적 조절.
- 캐싱은 1급 설계: 무엇을 얼마나 기억할지, 데이터 변동성에 TTL을 맞춰라.

## 관련 개념

- `concepts/data-engineering/stream-processing.md`
- `concepts/system-design/distributed-systems.md`
