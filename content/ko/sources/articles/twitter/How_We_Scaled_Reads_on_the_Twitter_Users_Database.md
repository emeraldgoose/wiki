---
title: Twitter 사용자 데이터베이스 읽기 확장기
description: Vitess Vtgate를 Aurora Mesos에 올려 사용자 예약 시스템을 수백만 읽기 QPS까지 확장한 사례
tags: [source, twitter, x, mysql, vitess, databases, scalability, data-engineering, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database"
blog: twitter
date: '2023-02-23'
---

# Twitter 사용자 데이터베이스 읽기 확장기

## 요약

Twitter 사용자 예약 시스템(URS)은 세계 최대급 사용자명 예약 저장소로, 원래 quorum read 같은 전용 기능을 가진 구 MySQL 프레임워크 Gizzard 위에 구축됐다. 규모 증가로 QPS·지연·성공률·데이터센터 간 일관성 SLO를 맞추면서 유지비를 낮추는 것이 불가능해졌다. 팀은 URS를 일반 MySQL + [Vitess](https://vitess.io/)로 옮기고, 보통 쓰기 샤딩에 쓰이는 Vitess의 무상태 프록시 **Vtgate**를 *읽기* 확장에 활용해 수백만 QPS를 달성했다.

## 왜 단순히 레플리카를 늘리지 않았나

MySQL 서버는 Twitter 워크로드에 맞춘 온프레미스 범용 하드웨어다. 수백만 읽기 QPS를 감당할 만큼 레플리카를 늘리는 것은 기각됐다: MySQL이 써야 할 자원을 소모하고, 연결 팬아웃과 토폴로지 관리가 남기 때문이다.

## 아키텍처

각 MySQL 인스턴스에 연결 풀링·쿼리 재작성·쿼리 중복 제거를 제공하는 **Vttablet** 프로세스를 pairing하고, **Vtgate**(Vitess의 무상태 라우팅 프록시)가 쿼리를 올바른 Vttablet으로 라우팅해 결과를 애플리케이션에 합쳐 반환한다.

핵심 결정은 Vtgate를 MySQL 호스트 *밖으로* 옮긴 것이다:

1. 함께 두면 Vtgate가 MySQL의 CPU/메모리를 빼앗는다.
2. 읽기를 위해 Vtgate를 *수백 대*까지 늘려야 했다.

Vtgate가 무상태이므로 컨테이너화해 **Aurora Mesos**에 올렸다. 인스턴스 수·CPU·OS 스레드 수·Go GC 값(GOGC)을 튜닝해 수백만 QPS를 달성했고, Vtgate당 수천 연결까지 검증했다.

## 왜 Vitess인가

- 오픈소스이며 MySQL 통합이 좋다.
- 모든 설정 데이터를 저장하는 토폴로지 서비스 내장(Twitter의 고가용 ZooKeeper 클러스터에 구축).
- MySQL 복제 토폴로지 관리자 Orchestrator(VTORC)와 통합되어 클러스터 유지보수 부담을 없애고 고가용 MySQL 클러스터를 제공 — 필요하면 쓰기 샤딩도 가능.

## 보안

전송 중 암호화는 Twitter의 필수 요구사항이며, Vitess는 모든 구간(애플리케이션 ↔ Vtgate ↔ 컴포넌트)의 TLS를 지원한다. 무중단 TLS 전환을 위해 **선택적 TLS** 기능을 오픈소스 Vitess에 업스트림 기여했다. 또한 Vitess가 클라이언트 검증에 단일 인증서만 쓰고 전체 체인을 쓰지 않는 문제를 발견해 전체 체인 검증 패치도 업스트림에 반영했다.

## 결과

URS는 현재 읽기·쓰기 모두 극도의 고가용성을 가진 tier-1 애플리케이션으로 운영 중이며 수백만 읽기 QPS를 처리한다. 팀은 쓰기 샤딩뿐 아니라 읽기 확장에도 Vitess를 업계에 추천한다.

## SW 엔지니어를 위한 시사점

- 무상태 쿼리 라우팅 프록시를 상태 저장소 호스트와 분리해 각각 독립 확장한다. 무상태 프록시는 컨테이너/Mesos/Kubernetes에 이상적이다.
- 태블릿 계층의 연결 풀링 + 쿼리 중복 제거는 애플리케이션 코드 수정 없이 읽기 용량을 배가한다.
- 핵심 경로에 오픈소스를 도입할 때는 업스트림 기여를 예산에 포함한다. 선택적 TLS와 전체 체인 검증이 전제조건이었고, 기여 덕분에 포크 유지보수가 줄었다.
- 인스턴스당 수천 연결을 유지하는 프록시라면 Go 런타임(스레드, GOGC)을 명시적으로 튜닝한다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database (Doyel Mitra Sinha, Ashwin Poojary, 2023-02-23)
- 관련: `concepts/data-engineering/delta-lake.md`
