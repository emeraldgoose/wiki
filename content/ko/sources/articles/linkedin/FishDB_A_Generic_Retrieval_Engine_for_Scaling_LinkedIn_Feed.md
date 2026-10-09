---
title: "FishDB: LinkedIn 피드 확장을 위한 범용 검색 엔진"
description: FollowFeed를 대체한 Rust 기반 범용 리트리벌 엔진 — scatter-gather 서빙, 람다 인입, 2배 효율
date: 2025-11-17
tags: [source, linkedin, feed, retrieval, rust, infrastructure, ko]
locale: ko
source_url: "https://www.linkedin.com/blog/engineering/infrastructure/fishdb-a-generic-retrieval-engine-for-scaling-linkedins-feed"
blog: linkedin
author: Kenneth Li
---

# FishDB: LinkedIn 피드 확장을 위한 범용 검색 엔진

기존 Java 기반 FollowFeed를 대체하는 Rust製 범용 리트리벌 엔진. **처리 효율 2배**, **하드웨어 50% 절감**, 엄격한 **p99 40 ms** 지연 SLO를 유지한다.

## 배경: FollowFeed의 한계

- **메모리 비효율:** JVM 저장소는 네이티브 표현 대비 약 5배의 메모리 오버헤드, GC 일시정지가 tail latency 위협.
- 인덱스 간 **콘텐츠 중복**, 경직된 데이터 모델.
- 비즈니스 로직이 엔진에 **긴밀 결합**되어 기능 출시가 느림.

## 아키텍처

### Scatter-gather 서빙

요청을 파티셔닝된 샤드에 분산하고 각 샤드의 로컬 후보 스코어링 결과를 병합해 상위 결과를 반환. 파티셔닝 + 인메모리 인덱스로 QPS 증가에도 p99 40 ms 유지.

### 람다 인입

- **스피드 계층:** Kafka 스트림 실시간 업데이트.
- **배치 계층:** 대량 재구축으로 상태 정정·압축.
- 신선도와 정정성을 동시에 확보.

### 저장과 인덱싱

- **역인덱스:** 용어 → 문서 ID 리스트의 인메모리 해시맵.
- **RocksDB 키-값 속성 저장소:** 인메모리 예산을 초과하는 대용량 문서 속성용.
- **그래프 기반 문서 참조:** 관계(작성자 → 활동 엣지 등) 위의 질의 실행.

### 표현력 있는 질의 언어

검색 predicate를 엔진 변경 없이 기술할 수 있는 전용 질의 언어로 비즈니스 로직을 분리 — FishDB의 "범용(generic)"의 의미.

## 왜 Rust인가

소유권 기반 메모리 관리로 GC 일시정지를 제거하고 객체당 오버헤드를 대폭 절감 — 2배 효율·50% 하드웨어 절감의 직접적 원천. 대가로 Rust 엔지니어링 비용(라이프타임, JVM/Kafka 생태계 FFI)을 한 번 지불하고 플릿 전체의 영구 절감을 얻음.

## 실무 시사점

1. 거대 live set의 지연 민감 검색에는 튜닝된 JVM보다 GC 없는 런타임.
2. scatter-gather + 파티셔닝 인메모리 인덱스가 p99 보장 검색의 정석.
3. 질의 언어와 엔진을 분리해 비즈니스 로직 진화 가능하게.
4. 신선도+정정성은 람다 인입(Kafka 스피드 계층 + 배치 정정)으로.

## 참고

- 원문: https://www.linkedin.com/blog/engineering/infrastructure/fishdb-a-generic-retrieval-engine-for-scaling-linkedins-feed
