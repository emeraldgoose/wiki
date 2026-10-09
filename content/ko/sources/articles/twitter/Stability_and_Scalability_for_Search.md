---
title: 검색의 안정성과 확장성
description: 트래픽 급증 속에서도 Twitter Elasticsearch 플랫폼을 지켜낸 프록시·Kafka 기반 인제스트 서비스·백필 서비스
tags: [source, twitter, x, search, elasticsearch, kafka, scalability, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/stability-and-scalability-for-search"
blog: twitter
date: '2022-10-14'
---

# 검색의 안정성과 확장성

## 요약

Twitter 검색 인프라 팀은 search-as-a-service를 운영한다. **Open Distro for Elasticsearch** 위에서 트윗·사용자·DM 등의 실시간 검색을 제공하며, 전체 Elasticsearch API에 프라이버시·보안·Twitter 서비스 연동 플러그인을 얹어 노출한다. Twitter 규모에서 Elasticsearch는 세 가지 방식으로 한계를 넘었고, 각각 전용 가드레일로 해결했다: **리버스 프록시**, Kafka 기반 **인제스트 서비스**, **백필 서비스**.

## 문제 1: 연결 병목 → 리버스 프록시

고객이 쿼리·인덱싱·모니터링·메트릭 모두를 Elasticsearch에 직접 붙었다. 평상시에는 괜찮았지만 인제스트 위주 트래픽이 클러스터 전체를 쓰러뜨릴 수 있었고, 중앙에서 라우팅·스로틀·관측할 지점이 없었다. 해법: 읽기/쓰기 트래픽을 분리하는 단순 HTTP 리버스 프록시. 모든 클라이언트 인증을 처리하고, 쓰기는 인제스트 서비스의 앞단이 되며, 요청 유형별 메트릭(성공률, 읽기/쓰기량, 클러스터 상태)과 유연한 라우팅·스로틀링을 제공하는 단일 진입점이 됐다 — 고객에게는 투명하다.

## 문제 2: 트래픽 급증 → 인제스트 서비스

공적 대화(public conversation) 트래픽 급증은 갑작스럽고 거대하다. 기본 Elasticsearch는 큐잉·재시도·백오프를 클라이언트에 맡기고 자동 스로틀링이 없어, 급증 시 인덱싱/쿼리 지연이 치솟고 최악의 경우 인덱스 전체가 소실됐다. 인제스트 서비스가 쓰기를 완충한다: 클라이언트 요청을 **클러스터당 하나의 Kafka 토픽**에 큐잉하고, 워커가 소비·전달하면서 **배치·백프레셔 대응·자동 스로틀·백오프 재시도**를 적용한다. 급증은 클러스터가 아니라 Kafka가 흡수하며, 인제스트 지연은 약간만 늘어난다.

## 문제 3: 데이터 사전 적재 → 백필 서비스

백필(빈 클러스터 부트스트랩, 스키마 변경, 장애 후 공백 메우기)은 테라바이트·수십억 문서를 옮겨 정상 인제스트 처리량을 아득히 넘는다. 기존 방식(Hadoop 리듀서당 HTTP 클라이언트를 여는 Scalding 싱크, 무스로틀)은 라이브 쿼리 성능을 망가뜨리거나 클러스터를 죽였고, 실패가 늦게 드러나고 안전 재개가 불가했다. 백필 서비스는 작업을 분리한다. **싱크**(쉬운 마이그레이션을 위해 기존 Scalding 코드와 동일 진입점)가 스트림을 인덱싱 요청으로 변환·파티셔닝해 **임시 스토리지**에 적재하고 **오케스트레이터**를 호출하면, 동적 워커 풀이 스테이징된 요청을 읽어 속도 제한·백프레셔 대응·벌크 내 문서별 재시도로 인덱싱한다. 효과: 데이터 준비 작업 재실행 없이 재개, 라이브 클러스터 collateral damage 제거, 전 데이터센터에 걸친 단일 백필.

## 결과

세 가드레일로 급증·백필 유발 인덱스 손실 시대가 끝났다. 가동 시간이 유지되고 충돌이 방지되며, 제품 팀은 셀프서비스로 검색 사용량을 확장한다.

## SW 엔지니어를 위한 시사점

- 규모가 있는 곳에서는 무제한 클라이언트가 상태 저장소에 직접 붙지 않게 한다. 인증·스로틀·테넌트별 메트릭용 프록시를 사이에 둔다.
- 버스트 생산자와 백프레셔 없는 저장소 사이에는 내구성 큐(Kafka)를 둔다. 워커에서 배치 + 스로틀 + 백오프 재시도.
- 대량 적재는 *스테이징*(내구성·파티셔닝·재개 가능)과 *적용*(백프레셔 대응 적응형 워커 풀) 단계로 분리한다. 백필은 정상 인제스트와 다른 워크로드이며 전용 서비스가 마땅하다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/stability-and-scalability-for-search (Shelby Cohen, Jesse Akes, 2022-10-14)
- 관련: `concepts/data-engineering/apache-kafka.md`, `concepts/data-engineering/stream-processing.md`
