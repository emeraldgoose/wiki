---
title: Amazon MSK 커스텀 도메인 (기술 심화)
description: MSK 브로커의 OAuth audience 기반 인증 구조 — EKS IAM/STS 웹 아이덴티티 흐름과 Keycloak SSO 운영자 흐름, 제공자별 리소스 서버와 AMQPS.
date: 2026-08-25
tags: [aws, kafka, msk, auth, oauth, iam, kubernetes, ko]
locale: ko
blog: aws
---

# Amazon MSK 커스텀 도메인 (기술 심화)

**발행**: 2026-08-25 · **출처**: AWS Big Data Blog (원문 URL 없음; 레거시 집계 `sources/articles/aws-bigdata.md`에서 분리)

> 참고: 이 항목은 현 blogwatcher 피드 이전 자료라 출처 URL이 없다. 아래 요약은 집계 파일에서 보존한 것이다. URL은 절대 임의로 만들지 않는다.

## 동반 문서

네트워킹 측면(NLB + DNS + ACM, ZooKeeper·KRaft 광고 리스너 2단계 롤아웃)은 `Configure_Custom_Domain_Name_for_Amazon_MSK.md` 참조. 이 파일은 커스텀 도메인 뒤의 **인증 아키텍처**를 다룬다.

## 인증 흐름

- **서비스(EKS 워크로드)**: EKS 파드 → IAM 역할(IRSA) → audience `rabbitmq-iam` STS 웹 아이덴티티 토큰 → AMQPS 5671로 브로커 접속. audience 클레임이 브로커 리소스 서버의 올바른 서명 키로 라우팅.
- **운영자(사람)**: Keycloak SSO → 브로커, 별도 OAuth 제공자 바인딩 경유.
- **구조**: 브로커에 OAuth 제공자별 리소스 서버를 두고, 토큰의 audience 클레임으로 제공자와 서명 키를 선택 — 머신(STS)과 사람(Keycloak) 신원이 동일한 리스너에 공존.

## 세미나 시사점

- audience 기반 리소스 서버 덕분에 무관한 두 신원 체계가 하나의 Kafka 엔드포인트를 공유 — 커스텀 도메인이 그 단일 엔드포인트를 안정적·주소 지정 가능하게 만든다.
- 머신 경로(단기 STS 토큰)와 사람 경로(SSO)는 발급자만 다르고, 브로커 측 `aud` 디스패치가 클라이언트별 브로커 설정 없이 둘 다 동작하게 한다.

## 관련 개념

- `concepts/infrastructure/kubernetes.md`, `concepts/data-engineering/stream-processing.md`
