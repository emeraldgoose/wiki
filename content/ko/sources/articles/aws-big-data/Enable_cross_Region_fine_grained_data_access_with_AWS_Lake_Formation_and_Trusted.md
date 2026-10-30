---
title: "AWS Lake Formation과 Trusted Identity Propagation으로 리전 간 fine-grained data access 구현"
description: "TIP를 활용한 리전 간 fine-grained 접근과 사용자 단위 감사."
tags: [source, aws-big-data, lake-formation, identity-propagation, data-engineering, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation"
blog: aws-big-data
published_date: 2026-10-23
---

# AWS Lake Formation과 Trusted Identity Propagation으로 리전 간 fine-grained data access 구현

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation) · **게시일**: 2026-10-23

## 개요

AWS에 분석 데이터를 저장하는 조직은 보통 두 가지를 함께 원한다: 각 사용자에게 권한 있는 데이터만 보여주는 fine-grained 접근 제어, 그리고 모든 쿼리가 공유 IAM role이 아닌 실제 실행자에게 추적되는 사용자 단위 감사. AWS IAM Identity Center Trusted Identity Propagation (TIP)은 둘 다 충족한다. 사용자가 한 번 sign-in하면 신원이 client application에서 query engine, Lake Formation, storage layer까지 전파되어 모든 요청이 실제 사용자로 권한화되고 AWS CloudTrail에 기록된다.

## 핵심 내용

- 신원이 end to end로 전파되어 fine-grained authorization과 user-level auditing을 제공한다.
- producer/consumer account, IAM Identity Center 복제, 관련 AWS 서비스 권한 설정이 필요하다.
- producer Lake Formation Data catalog 설정에서 "Use only IAM access control" 옵션을 해제해야 한다.
- trusted identity propagation use case를 양 계정/리전에 통합한다.

## 상세

리전 간 fine-grained 접근을 위해서는 신원 전파와 catalog 구성이 일관되어야 하며 producer/consumer 양 환경의 사전요구사항을 충족해야 한다.

## 참고 자료

- 원문: [https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation](https://aws.amazon.com/blogs/big-data/enable-cross-region-fine-grained-data-access-with-aws-lake-formation-and-trusted-identity-propagation)
