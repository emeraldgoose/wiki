---
title: 고성능 서비스를 위한 Java 힙 메모리와 가비지 컬렉션 튜닝
description: FollowFeed의 JVM 여정 — CMS에서 JDK 21 generational ZGC로, P999 55% 감소·용량 28% 증가
date: 2024-09-13
tags: [source, linkedin, jvm, gc, performance, followfeed, ko]
locale: ko
source_url: "https://www.linkedin.com/blog/engineering/infrastructure/java-heap-memory-and-garbage-collection-tuning-for-high-performance-services"
blog: linkedin
author: Nisheedh Raveendran
---

# 고성능 서비스를 위한 Java 힙 메모리와 가비지 컬렉션 튜닝

LinkedIn 피드의 인덱싱·추천 시스템 FollowFeed(SLA 50 ms 미만)는 회원 행동을 "Activity" 트리플(행위자–동사–객체)로 모델링한다. 폭발적 성장으로 샤드당 힙이 **183 GB**까지 커지며 기존 GC 설정이 붕괴했고, CMS에서 JDK 21의 generational ZGC까지의 여정을 다룬다.

## 문제

- **샤드당 183 GB 힙.** 샤드를 늘리면 힙은 줄지만 fan-out tail latency 악화 — 거대 힙 유지 불가피.
- **가혹한 할당 프로파일:** 초당 최대 12 GB 할당, live set 최대 ~110 GB, Kafka 기반 캐시 eviction으로 old-gen 지속 승격. 읽을 때 역직렬화를 피하려고 값을 POJO로 캐싱.
- **CMS 삭제:** JDK 11 + CMS에서 출발했으나 CMS는 11에서 deprecated, 17에서 삭제. G1GC는 중앙값은 괜찮았으나 거대 live set·복잡한 객체 그래프 위의 mixed collection이 tail latency를 망침. JDK 17의 비세대 Shenandoah/ZGC는 거대 live set을 상시 재스캔하며 mutator를 멈추고 CPU를 고갈.

## 1단계: 할당 자체를 줄이기 (JFR 기반)

- **이벤트 로깅**이 로그용으로 Avro 객체 전체를 역직렬화 — 실제 사용은 이벤트 ID뿐 → ID만 기록, **바이트 배열 할당 50%↓**.
- 요청 서빙·이벤트 소비 **핫패스 위 Optional**은 호출당 객체 할당 → 제거 리팩터링.
- 결과: 할당률 **12 GB/s → 1–2 GB/s** — 이후 모든 작업의 전제조건.

## 2단계: live set 축소 (JXRay 기반)

- 중복 문자열 제거, 인메모리 객체 표현 평탄화(객체당 헤더 오버헤드↓).
- 결과: **힙 사용량 34%↓** — 성장 여유 확보 + GC 스캔 대상 축소.

## 3단계: JDK 21 generational ZGC

할당·live set을 다잡은 뒤 ZGC 개발자 Erik Österlund와의 협업으로 JDK 21 세대별 ZGC로 이전:

- `-XX:SoftMaxHeapSize`로 할당 스파이크 완충.
- fragmentation limit 상향, tenuring threshold 하향, proactive collection 비활성화로 load-barrier storm 진정.
- **OS 튜닝:** ZGC 공유 메모리 매핑에 transparent huge page 활성화(최대 +15%), 대용량 힙 매핑용 `vm.max_map_count` 상향.

## 결과 (450 qps 기준)

- **P999: 100 ms → 45 ms(−55%)**, P99: 40 ms → 30 ms, 스레드 정지 시간 제로.
- 지연 감소만으로 **서빙 용량 +28%**.

## 실무 시사점

1. 컬렉터 쇼핑보다 **데이터 이해**가 먼저 — 힙 덤프 분석(JXRay).
2. **할당률이 지배적** — JFR 할당 프로파일링, 핫패스의 Optional·로깅 낭비 제거.
3. 거대 힙 + fan-out 제약이면 "샤드 증설"이 답이 아님 — 세대별 concurrent collector(ZGC)가 정답인 영역.
4. OS 레벨(huge page, map count) 예산 편성 — 관리형 런타임도 커널 위에 있음.

## 참고

- 원문: https://www.linkedin.com/blog/engineering/infrastructure/java-heap-memory-and-garbage-collection-tuning-for-high-performance-services
- 후속: FishDB (`sources/articles/linkedin/FishDB_A_Generic_Retrieval_Engine_for_Scaling_LinkedIn_Feed.md`) — GC 자체를 우회하는 Rust 후계자.
