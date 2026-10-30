---
title: "From Problem to Fix in Minutes: Amazon OpenSearch Service Relevance Agent로 검색 관련성 튜닝 자동화"
description: "NDCG 저하 문제를 수 분 내 쿼리 개선안으로 전환하는 Relevance Agent."
tags: [source, aws-big-data, opensearch, search-relevance, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/from-problem-to-fix-in-minutes-automating-search-relevance-tuning-with-the-amazon-opensearch-service-relevance-agent"
blog: aws-big-data
published_date: 2026-10-27
---

# From Problem to Fix in Minutes: Amazon OpenSearch Service Relevance Agent로 검색 관련성 튜닝 자동화

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/from-problem-to-fix-in-minutes-automating-search-relevance-tuning-with-the-amazon-opensearch-service-relevance-agent) · **게시일**: 2026-10-27

## 개요

검색 관련성 튜닝 자동화는 "NDCG 점수가 낮다"에서 "더 나은 검색 쿼리는 이것이다"로 수 분 안에 이동하는 것을 뜻한다. Amazon OpenSearch Service Search Relevance Agent는 UI 안에서 문제를 기술하면 agent가 행동 데이터를 조사하고 연속 평가를 실행한 뒤 검색 품질 목표에 맞춘 개선 쿼리를 생성한다. 이전 글에서 다룬 UBI/SRW 측정은 진단을 제공하고, agent는 더 어려운 action 단계를 처리한다.

## 핵심 내용

- 수동 쿼리 재작성에서 agent 주도 워크플로로 relevance tuning을 이동한다.
- 행동 데이터 조사와 연속 평가를 자동 실행한다.
- 검색 품질 목표에 대해 개선 쿼리를 생성/검증한다.
- User Behavior Insights와 Search Relevance Workbench 스킬을 바탕으로 한다.
- 워크플로가 OpenSearch Service UI 내에 머문다.

## 상세

Relevance Agent는 진단과 조치 사이의 루프를 닫아 팀이 서비스 UI를 벗어나지 않고 NDCG 갭에 대응하도록 한다.

## 참고 자료

- 원문: [https://aws.amazon.com/blogs/big-data/from-problem-to-fix-in-minutes-automating-search-relevance-tuning-with-the-amazon-opensearch-service-relevance-agent](https://aws.amazon.com/blogs/big-data/from-problem-to-fix-in-minutes-automating-search-relevance-tuning-with-the-amazon-opensearch-service-relevance-agent)
