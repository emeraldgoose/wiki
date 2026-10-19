---
title: "차세대 Amazon OpenSearch Serverless의 네트워크 연결 패턴"
description: "표준 PrivateLink 엔드포인트 기반의 차세대 OpenSearch Serverless 프라이빗 연결 패턴 9가지, 단일 VPC부터 교차 리전까지." (한국어 번역)
published: "2026-09-03"
source_url: "https://aws.amazon.com/blogs/big-data/network-connectivity-patterns-for-the-next-generation-of-amazon-opensearch-serverless"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, opensearch, networking, ko, ko]
---

# 차세대 Amazon OpenSearch Serverless의 네트워크 연결 패턴

## 개요

차세대 OpenSearch Serverless는 VPC 엔드포인트와 수동 DNS 조합 대신 네이티브 프라이빗 DNS를 갖춘 표준 PrivateLink 인터페이스 엔드포인트(`com.amazonaws.<리전>.aoss-data`)를 사용한다. 컬렉션은 `on.aws` 도메인의 리소스 기반 엔드포인트를 노출한다. 컬렉션별 호스트명과, `x-amz-aoss-collection-name` 헤더로 여러 컬렉션을 묶는 계정 단위 리전 엔드포인트다. 이 글은 단일 VPC, 다중 VPC, 온프레미스, 교차 계정, 중앙집중, 다사업부, 교차 리전을 아우르는 9가지 연결 패턴을 정리한다.

## 핵심 동작

프라이빗 DNS를 켠 인터페이스 엔드포인트 하나면 VPC 리졸버를 통해 리전 내 모든 `*.aoss.<리전>.on.aws` 호스트명이 해석된다. 엔드포인트 하나로 리전 전체 컬렉션에 도달하며, 같은 VPC에 두 개를 만들면 충돌한다. 접근 제어는 분리된다. 네트워크 정책이 엔드포인트 ID(`SourceVPCEs`)를 인가하고, 데이터 접근 정책이 IAM 주체를 인가하며, 교차 계정 읽기는 컬렉션 계정의 역할을 수임한다. 계정 단위 리전 엔드포인트로 여러 컬렉션이 하나의 호스트명·커넥션 풀을 공유한다.

## 9가지 패턴

단일 VPC와 다중 VPC는 VPC별 엔드포인트와 정책 등록이면 된다. 온프레미스형은 Resolver 인바운드 엔드포인트, 조건부 포워더, Transit Gateway·Cloud WAN 경유의 Direct Connect/VPN을 추가한다. 교차 계정은 각 소비자 VPC에 엔드포인트를 두고 소유자 네트워크 정책에 ID를 등록한다. 피어링이나 경유 없이 PrivateLink로 끝난다. 중앙집중형은 Transit Gateway 너머의 공용 엔드포인트 하나에 Route 53 Profiles로 DNS를 전달한다(DNS 관리가 필요한 유일한 패턴). 다사업부는 스포크별 엔드포인트 또는 공용 네트워킹 엔드포인트 방식이다. 교차 리전은 내장 복제가 없어 리전별 독립 컬렉션을 두고 이중 쓰기, OpenSearch Ingestion 파이프라인, S3 복제 후 재적재 중 하나로 동기화한다.

## 비용 가이드

규모에 맞게 설계한다. Resolver 인바운드는 온프레미스 패턴에서만, Route 53 Profiles는 자체 엔드포인트가 없는 VPC에서만 필요하다. 다계정 환경에서는 소비자 VPC별 엔드포인트가 대개 가장 단순하고 저렴하다. 로컬 DNS 해석에 추가 비용이 없기 때문이다. 엔드포인트 하나로 모으는 방식은 transit 데이터 처리 요금이 절감을 상쇄할 수 있으니 트래픽 기준으로 비교해야 한다. 유휴 보조 리전 컬렉션은 scale-to-zero로 스토리지 비용만 낸다.

## 참고 자료

- [원문: Network connectivity patterns for next-gen OpenSearch Serverless](https://aws.amazon.com/blogs/big-data/network-connectivity-patterns-for-the-next-generation-of-amazon-opensearch-serverless)
- [OpenSearch Serverless 문서](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
