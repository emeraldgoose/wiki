---
title: Amazon MSK 커스텀 도메인 이름 구성
description: NLB·DNS·ACM 인증서로 MSK Provisioned 클러스터(ZooKeeper·KRaft 공통)에 커스텀 advertised 리스너를 적용하는 2단계 롤아웃.
date: 2026-08-25
tags: [aws, kafka, msk, networking, dns, ko]
locale: ko
blog: aws
---

# Amazon MSK 커스텀 도메인 이름 구성

**발행**: 2026-08-25 · **출처**: AWS Big Data Blog (기존 피드에 URL이 남아 있지 않아 레거시 집계 `sources/articles/aws-bigdata.md`에서 분리)

> 참고: 이 항목은 현행 blogwatcher 피드 이전의 구 항목이라 원문 URL이 없다. 아래 요약은 집계 파일 내용을 보존한 것이다. URL을 임의로 만들지 않는다.

## 문제

MSK는 AWS가 생성한 호스트명을 브로커 엔드포인트로 알린다. 사내 DNS 규칙·사설 CA·방화벽 허용 목록을 적용해야 하는 기업은 클라이언트 전체를 재설정하지 않고도 `kafka.corp.example.com` 같은 **커스텀 도메인**으로 접속해야 한다.

## 해법

- **NLB + DNS + ACM 인증서**: 브로커 앞에 Network Load Balancer를 두고 커스텀 DNS를 매핑, ACM 인증서로 해당 도메인의 TLS를 종료.
- **Advertised 리스너 변경**: 브로커별 커스텀 advertised 리스너 설정(기존 `custom.advertised.listeners` CLI 대체 방식의 현대적 형태)으로 브로커가 클라이언트에게 커스텀 호스트명으로 재접속하도록 지시.
- **2단계 롤아웃**: 1) 네트워킹 경로(NLB·DNS·인증서) 먼저 구축 → 2) advertised 리스너 전환으로 자동 컷오버.
- **ZooKeeper/KRaft 동일 동작**: 두 메타데이터 모드에서 동일하게 작동.
- **확장·장애 복구 안전**: 브로커 자동 확장·교체 시 설정이 재적용되어 토폴로지 변경 후에도 커스텀 이름 유지.
- **지원 범위**: 모든 MSK Provisioned 클러스터(Standard·Express 브로커).

## 시사점

- 네트워킹을 먼저 깔고 설정을 나중에 뒤집으면 무중단 전환이 된다 — 클라이언트 동시 재설정이 불필요.
- 커스텀 advertised 리스너는 기업 Kafka 도입(mTLS 신원, DNS 정책, 감사)의 전제 패턴이며, ZooKeeper→KRaft 인플레이스 업그레이드와 충돌하지 않고 함께 쓸 수 있다.

## 관련 개념

- `concepts/data-engineering/stream-processing.md`, `concepts/infrastructure/kubernetes.md`
