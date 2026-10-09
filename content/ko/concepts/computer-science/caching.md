---
title: 캐싱
description: "세미나 수준 개념: 캐시 계층, 축출 정책, TTL, 무효화, 스탬피드 방어, CDN과 앱 캐시"
tags: [concept, computer-science, caching, redis, cdn, performance, eviction, ko]
published: 2026-09-06
locale: ko
---

# 캐싱

**캐시**는 느린 원본(source of truth) 앞의 더 빠르고 작은 저장소로, 반복 요청을 재계산·재조회 없이 처리한다. 캐싱은 가장 가성비 좋은 성능 기법이며, 무효화는 Phil Karlton의 유명한 말대로 컴퓨터 과학의 두 가지 어려운 문제 중 하나다.

## 정의

- **캐시**: 요청 정체성을 키로 하는 조회 구조로, 이전에 계산/조회한 값을 축출·만료 정책과 함께 보관한다. 적중하면 백엔드 저장소를 건너뛰고, 빗나가면 전체 비용 + 채우기 비용을 낸다.
- **적중률(hit ratio)**: 적중 / 전체 조회. 판가름 지표다 — 적중률 95%는 백엔드가 트래픽의 1/20만 본다는 뜻이다. 전체가 아니라 캐시 계층별로 측정한다.
- **TTL**: 엔트리를 신선하다고 보는 기간. 오래됨(staleness)을 묶어두는 무딘 도구다. TTL이 짧을수록 신선하지만 적중률은 낮다.
- **무효화(invalidation)**: 원본이 바뀌면 엔트리를 선제 제거/갱신한다 — 정확하지만 영향받는 모든 키를 알아야 한다.

## 왜 중요한가

- **지연·비용 붕괴**: 메모리는 ~100 ns, SSD는 ~100 µs, 리전 간 조회는 ~100 ms — 여섯 자릿수의 차이. 캐시 계층 하나를 건너뛸 때마다 다른 지연 우주다.
- **원본 보호**: 캐시가 반복되는 99%를 흡수하므로 DB와 오리진이 스파이크에서 산다. 용량 계획은 보통 캐시 계획이다.
- **일관성 맞바꿈**: 모든 캐시는 읽는 쪽이 오래된 데이터를 보는 구간을 만든다. TTL과 무효화를 고르는 것은 기능별 허용 오래됨을 고르는 것이다.
- **계층적 현실**: CPU L1/L2/L3 → 페이지 캐시 → 애플리케이션 캐시(Redis/Memcached) → CDN 엣지 → 브라우저 캐시. 요청 하나가 캐시 다섯 개를 거칠 수 있고, 추론은 계층별로 해야 한다.

## 동작 원리

### 계층 구조

```
레지스터 → L1 (~1ns) → L2 (~4ns) → L3 (~15ns) → RAM (~100ns)
  → SSD (~100µs) → 같은 AZ 네트워크 (~0.5ms) → 리전 간 (~100ms) → 원본 연산?
```

- 각 단계는 이전보다 ~10–1000배 느리고 ~10–100배 크다. 설계 규칙: 핫 셋은 담기는 가장 빠른 계층에 두고, 계층 크기는 추측이 아니라 측정된 워킹 셋에서 정한다.
- **페이지 캐시**(OS): 파일·mmap 읽기를 빈 RAM에서 처리 — 한 박스에서 가장 큰 "캐시"인 경우가 많고, DB들이 "워킹 셋을 메모리에"를 외치는 이유다.
- **애플리케이션 캐시**(Redis, Memcached): 쿼리 결과·세션·렌더 조각·rate-limit 카운터용 명시적 KV 저장소. 네트워크 1홉(~0.5 ms)이 들지만 앱 인스턴스가 공유한다.
- **CDN 엣지**: 지리적으로 분산된 리버스 프록시(CloudFront, Cloudflare, Fastly)가 정적·캐시 가능 동적 콘텐츠를 사용자 가까이서 내주고, TLS 종결과 DDoS 흡수도 맡는다.
- **브라우저 캐시**: `Cache-Control`/`ETag` 구동. 적중하면 요청 자체가 사라진다(가장 싼 요청은 안 보내는 요청).

### 축출 정책

| 정책 | 규칙 | 장단점 |
|---|---|---|
| LRU | 가장 오래 안 쓴 것 축출 | recency 워크로드에 강함, 스캔에 오염됨 |
| LFU / TinyLFU | 가장 덜 쓰인 것 축출 | 스캔에 강함, 변화 적응에 aging 필요 |
| FIFO | 가장 먼저 들어온 것 축출 | 단순, 유용성 무시 |
| Random | 균일 랜덤 축출 | 의외로 경쟁력 있고 구현이 trivial |
| TTL 전용 | 시간 만료 후 축출 | 오래됨 예측 가능, 가치/크기 무시 |
| ARC / LRU-K / S3-FIFO | 적응형/고스트 이력 하이브리드 | 혼합 워크로드에 near-optimal (Redis, Caffeine) |

- 실전: Redis는 `allkeys-lru/lfu/random`, `volatile-*`(TTL 키만) 제공, Caffeine(Java)은 Window-TinyLFU, 최신 연구는 **S3-FIFO**(SOSP'23) — FIFO 큐 + 고스트 이력으로 LRU를 적은 관리 비용으로 이긴다.
- **스캔 저항성**이 중요하다: 밤샘 배치가 차가운 키 1000만 개를 쓸어도 뜨거운 10만 개를 쫓아내면 안 된다. 보호/예비 세그먼트 분리 설계가 정확히 이를 위한 것이다.

### 패턴: Aside, Through, Write-Behind

```
Cache-aside (지연):      앱 → 캐시? 빗나감 → DB → 캐시 채움 → 반환
Read-through:            앱 → 캐시 → (빗나감: 캐시가 직접 DB 로드)
Write-through:           앱 → 캐시 → DB 동기 기록 (일관, 느린 쓰기)
Write-behind (back):     앱 → 캐시 → ACK → DB 비동기 (빠름, 손실 구간)
```

- **Cache-aside**가 기본값이다. 요청받은 데이터만 캐시(차가운 채우기 낭비 없음)하지만 무효화 로직은 앱의 몫이다.
- **Write-through**는 쓰기 비용을 치르고 캐시-DB 일치를 유지 — 작고 중요한 데이터셋에 맞다. **Write-behind**는 쓰기 버스트(메트릭, 카운터)를 흡수하지만 크래시 시 승인된 쓰기를 잃을 수 있다. 손실 구간을 의도적으로 정한다.
- **Refresh-ahead**: TTL 만료 전 핫 키를 백그라운드 갱신해 지연을 편평화(Guava/Caffeine `refreshAfterWrite`) — 가끔 중복 로드 비용이 든다.

### 스탬피드 방어

- **Thundering herd**: 핫 키 만료 → 동시 빗나감 1000개 → 동일한 DB 쿼리 1000개 → DB 사망, 그리고 1000개가 같은 값을 채운다.
- 처방: **요청 합치기**(singleflight — 키당 진행 중 로드 하나로 대기자가 결과 공유. Go `singleflight`, Redis `SET NX` 락 + 대기, Caffeine 내장 합치기), **확률적 조기 갱신**(XFetch식: TTL 종료가 가까울수록 rising 확률로 미리 갱신), **stale-while-revalidate**(`Cache-Control: stale-while-revalidate=N` — 오래된 것을 즉시 내주고 백그라운드 갱신).
- 네거티브 캐싱(빗나감/404를 잠깐 캐시)은 없는 키의 반복 고비용 조회를 막는다. 큰 키 공간엔 블룸 필터를 곁들인다.

## 흔한 함정

1. **TTL 없음("영원히 캐시")**: 모든 엔트리가 영구 오래됨 위험 + 무한 메모리 증가가 된다. 모든 키에 TTL을 준다. "영원"은 무효화 스토리를 갖춘 명시적 선택이어야 한다.
2. **적중률 측정 없는 캐싱**: 적중률 40% 캐시는 요청의 60%에 네트워크 1홉을 더하면서 DB는 barely 가린다. 크기·정책 튜닝 전에 키 접두어별 적중/빗나감/축출을 계측한다.
3. **키 설계 충돌**: `user:{id}` vs `user:{id}:profile` vs 로케일/통화 변형을 한 키에 담으면 엉뚱한 사용자에게 엉뚱한 콘텐츠를 준다. 키에 네임스페이스를 주고(`v1:profile:{locale}:{id}`) 달라지는 차원을 전부 포함한다.
4. **배포/재시작 후 콜드 스타트 붕괴**: 배포 때마다 캐시를 비우면 전체 트래픽이 DB로 간다. 점진 가온(롤링 재시작, 영속 Redis, 사전 가온 스크립트) 또는 캐시 인프라를 앱 배포와 분리한다.
5. **돈과 맞닿은 플로우의 오래된 읽기**: 잔액·재고·인증 결정을 분 단위 TTL로 캐시하면 오버셀/마이너스 구간이 생긴다. 표현 데이터는 공격적으로 캐시하고, 거래 판단 시점의 사실은 그때 확인한다.
6. **무한 키 카디널리티**: 사용자별×쿼리스트링별 키는 메모리를 무한히 키우고 적중률을 박살낸다. 키를 정규화(추적 파라미터 제거, 시간 창 버킷팅)하고 maxmemory 정책을 둔다(실전 Redis의 `noeviction`은 메모리 폭탄 — 알람을 곁들인 `allkeys-lru` 선호).
7. **CDN 오리진 집중**: 엣지 TTL이 너무 짧거나 `Vary: *` 의미론이면 모든 엣지 요청이 오리진으로 간다. 계층화(엣지 → 실드/부모 → 오리진)하고 오리진에서 `Vary`/`Cache-Control`를 고친다.

## 관련 개념

- [[concepts/computer-science/virtual-memory|가상 메모리]] (페이지 캐시, 하드웨어 캐시로서의 TLB)
- [[concepts/computer-science/http|HTTP]] (Cache-Control, ETag, CDN 의미론)
- [[concepts/computer-science/database-indexing|데이터베이스 인덱싱]] (버퍼 풀 vs 앱 캐시 계층화)

## 참고 문헌

- Nygard — *Release It!* (캐시 주변 안정성 패턴: 타임아웃, 서킷 브레이커, 벌크헤드)
- Redis docs — "Eviction policies", "Latency"; Memcached docs — LRU/crawler 동작
- 고전: LRU-K (O'Neil et al. 1993), ARC (Megidson & Modha 2003), TinyLFU (Eini & Mansour 2017), S3-FIFO (SOSP'23)
- Google SRE Workbook — "Handling Overload" (thundering herd, 부하 차단, 백프레셔)
- Cloudflare / Fastly learning centers — 실전 CDN 캐싱 의미론
