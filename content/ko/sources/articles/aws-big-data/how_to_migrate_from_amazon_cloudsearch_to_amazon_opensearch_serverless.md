---
title: "Amazon CloudSearch에서 Amazon OpenSearch Serverless로 마이그레이션하기"
description: "CloudSearch 도메인을 평가, 데이터 변환, 쿼리 마이그레이션, 보안 정책 이관을 거쳐 Amazon OpenSearch Serverless로 옮기는 과정을 요약한다."
tags: [source, article, aws-big-data, search, opensearch, cloudsearch, migration, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/"
blog: "AWS Big Data"
published: "2026-09-09"
---

# Amazon CloudSearch에서 Amazon OpenSearch Serverless로 마이그레이션하기

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/) · **게시일**: 2026-09-09

## 개요

Amazon CloudSearch에서 Amazon OpenSearch Serverless로 옮기는 작업은 기존 검색 계층을 유지 보수 가능한 관리형 인프라로 전환하는 절차다. 먼저 현재 CloudSearch 도메인의 configuration, query pattern, security, index 구성과 data volume을 평가한다. 이후 field type mapping, indexing rule, query syntax, access policy를 OpenSearch에 맞게 변환하여 기능 parity를 확보한다. 마이그레이션은 일반적으로 assessment, data migration, query migration, security wrapping, validation, cleanup의 순서로 진행된다.

OpenSearch Serverless는 capacity planning과 node administration 부담을 줄여주지만, CloudSearch의 단순한 모델에 익숙한 운영자라면 새로운 개념을 학습해야 한다. field mapping과 replication, access policy가 핵심이며, data conversion 단계에서는 source schema와 text analysis 설정을 검토하여 검색 품질 저하를 방지한다. validation 단계에서는 query result를 비교하고 latency, relevance, ingestion throughput을 점검한다.

## 핵심 내용

- CloudSearch 도메인을 먼저 평가하여 인덱스, 쿼리 패턴, 보안, 비용을 정리한다.
- OpenSearch Serverless의 field type mapping에 맞게 데이터 스키마를 변환한다.
- 검색 쿼리와 suggest, autocomplete, filter 조건을 OpenSearch 구문으로 migration한다.
- access policy와 network policy를 재정립하여 최소 권한 원칙을 유지한다.
- 데이터 migration 이후 query result와 latency, relevance를 검증한다.
- 기존 CloudSearch domain을 cleanup하기 전에 rollback plan을 준비한다.
- stepwise migration을 사용해 downtime과 data loss risk를 줄일 수 있다.

## 주의점

fully managed serverless architecture로 전환하면서도 production handling unchanged behavior를 보장하기 위해 blue/green 또는 staged validation을 사용한다. Direct switchover는 ingestion mismatch나 analyzer difference 때문에 검색 품질이 갑작스럽게 저하될 수 있다. 또한 OpenSearch의 access policy와 CloudSearch의 domain-level access가 차이 나므로 인증과 monitoring을 함께 migrate해야 한다.

## 참고

- Source: [How to migrate from Amazon CloudSearch to Amazon OpenSearch Serverless](https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/)