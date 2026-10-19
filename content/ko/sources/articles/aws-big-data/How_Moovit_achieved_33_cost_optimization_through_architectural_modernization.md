---
title: "아키텍처 현대화로 비용 33%를 절감한 Moovit 사례"
description: "과부하된 Redshift 단일 클러스터를 EMR과 Redshift Serverless를 곁들인 멀티엔진 레이크하우스로 나누어 클러스터를 절반으로 줄이고 파이프라인 비용 33%를 절감." (한국어 번역)
published: "2026-09-03"
source_url: "https://aws.amazon.com/blogs/big-data/how-moovit-achieved-33-cost-optimization-through-architectural-modernization"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, redshift, emr, ko, ko]
---

# 아키텍처 현대화로 비용 33%를 절감한 Moovit 사례

## 개요

Moovit의 Amazon Redshift 단일 클러스터는 10년간 성장해 전체 데이터 플랫폼의 중추가 되었지만, 무거운 ETL부터 실시간 모니터링, Tableau BI, 데이터 사이언스, 애드혹 쿼리까지 한 엔진에 몰리면서 큐가 길어지고 노드를 늘려도 효과가 없었다. 워크로드 측정, 낭비 제거, 엔진별 적재적소 배치를 거쳐 Redshift 클러스터를 절반으로 줄이고 전체 파이프라인 비용을 33% 절감했다. 무거운 집계는 EMR, BI 서빙은 프로비저닝 Redshift, 애드혹·데이터 사이언스는 Redshift Serverless가 맡는다.

## 먼저 측정하고, 먼저 정리하기

이전에 앞서 자동화된 쿼리 귀속 분류를 구축했다. 실행 주체와 쿼리 시그니처, 오케스트레이터 메타데이터로 모든 쿼리를 소유자·실행 맥락별로 분류하고, CPU 시간을 핵심 지표로 Tableau 대시보드에 올렸다. 이를 근거로 오프로드 후보를 증거 기반으로 우선순위화했다.

마이그레이션 전 정리 작업을 먼저 했다. 미사용 프로세스(CPU 약 7%), 과도한 실행 빈도, 어긋난 WLM 우선순위를 바로잡아, 진짜로 무거운 워크로드만 이전 대상으로 남겼다. 1차 후보는 S3 원천 데이터를 읽어 무거운 세션화·집계를 수행하던 파이프라인이었다. 최종 소비자는 집계 결과만 필요로 했기 때문이다.

## EMR POC와 프로덕션 이전

EMR Serverless + Spark SQL로 POC를 수행했고, 기존 Redshift SQL은 사소한 문법 수정으로 이식됐다. 초기 실행은 느렸으나(100 익스큐터로 4시간), Spark 분산 실행 모델에 맞게 셔플 유발 패턴과 고비용 DISTINCT를 다시 쓰자 50개 미만 익스큐터로 약 10분까지 단축됐다. 행 수, 고유 사용자 수, 지표, 추세, 샘플 대조를 여러 연속 실행에 걸쳐 통과해야 컷오버했다. 안정 단계에서는 기존 컴퓨팅 예약을 활용하려고 EMR Serverless에서 EMR on EC2로 옮겼으며, 애플리케이션 변경은 없었다.

## 라이트사이징과 워크로드 격리

무거운 작업이 빠진 뒤 프로비저닝 클러스터를 탄력적 리사이즈로 두 노드씩 점진 축소하며 매 단계 SLA를 검증했고, 최종적으로 용량이 절반이 됐다. 분석가 애드혹 쿼리와 데이터 사이언스는 데이터 공유를 통해 Redshift Serverless로 옮겨 예측 불가 부하를 격리했고, WLM 우선순위를 Tableau 서빙 쪽으로 재조정했다. 집계 작업 p90 실행 시간은 5.48시간에서 2.77시간으로 줄었다.

## 참고 자료

- [원문: How Moovit achieved 33% cost optimization through architectural modernization](https://aws.amazon.com/blogs/big-data/how-moovit-achieved-33-cost-optimization-through-architectural-modernization)
