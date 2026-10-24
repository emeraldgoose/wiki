---
title: "Amazon OpenSearch Service로 멀티 에이전트 파이프라인의 보안 위협 추적하기"
description: "프롬프트 인젝션 전파와 테넌트 간 데이터 유출을 OpenSearch와 Bedrock로 추적하는 방법을 설명합니다."
tags: [source, aws-big-data, data-engineering, security, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/trace-security-threats-in-multi-agent-pipelines-with-amazon-opensearch-service"
blog: aws-big-data
published_date: 2026-10-19
---

# Amazon OpenSearch Service로 멀티 에이전트 파이프라인의 보안 위협 추적하기

**원문**: [aws-big-data](https://aws.amazon.com/blogs/big-data/trace-security-threats-in-multi-agent-pipelines-with-amazon-opensearch-service) · **게시일**: 2026-10-19

## 개요

멀티 에이전트 시스템은 에이전트 사이에서 일어나는 상호작용을 기존 보안 도구로 관찰하기 어렵습니다. 외부 문서에 숨겨진 프롬프트 인젝션은 도구 권한을 가진 하위 에이전트를 탈취할 수 있고, 민감한 데이터는 경보 없이 테넌트 경계를 넘을 수 있습니다. 문제는 에이전트 간 트래픽에서 발생하지만 표준 로그만으로는 경로를 재구성하기 어렵습니다.

이 글은 Amazon OpenSearch Service와 Amazon Bedrock를 사용해 프롬프트 인젝션 전파와 테넌트 간 데이터 유출이라는 두 가지 보이지 않는 위협을 추적하는 방법을 보여줍니다. 각 에이전트 호출 구간을 계측하고, Titan Text Embeddings V2로 임베딩한 뒤, OpenSearch의 kNN 검색으로 유사한 보안 이벤트를 연결하는 구조입니다.

## 핵심 내용

- 지원 티켓에 숨긴 악성 지시가 하위 에이전트로 전파되는 경로를 추적합니다.
- 테넌트 필터가 없는 공유 벡터 저장소에서 개인정보가 다른 테넌트에 노출되는 상황을 재현합니다.
- 각 홉을 계측해 에이전트 간 이동 경로와 데이터 접근을 하나의 흐름으로 재구성합니다.
- OpenSearch 2.19의 세밀한 접근 제어와 kNN 워크로드용 인스턴스 구성을 사용합니다.

## 참고 자료

- 원문: https://aws.amazon.com/blogs/big-data/trace-security-threats-in-multi-agent-pipelines-with-amazon-opensearch-service
