---
title: "dbt와 Amazon Redshift 데이터 공유: 데이터를 옮기지 않는 멀티 클러스터 파이프라인"
description: "Redshift 데이터 공유와 dbt Cloud를 결합해 클러스터 간 복사 없이 변환 파이프라인을 운영하는 방법입니다."
tags: [source, aws-big-data, data-engineering, dbt, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte"
blog: aws-big-data
published_date: 2026-10-15
---

# dbt와 Amazon Redshift 데이터 공유: 데이터를 옮기지 않는 멀티 클러스터 파이프라인

**원문**: [aws-big-data](https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte) · **게시일**: 2026-10-15

## 개요

조직이 커지면 Amazon Redshift 클러스터를 여러 개 운영해 워크로드를 분리하거나 비용을 관리하고, 리전별 데이터 거주 요구사항을 맞추는 경우가 많습니다. 하지만 기존에는 클러스터 사이에 데이터를 복사하는 복잡한 ETL 파이프라인이 필요했습니다.

이 글은 Redshift 데이터 공유와 dbt Cloud를 결합해 데이터를 복사하지 않고도 멀티 클러스터 변환 파이프라인을 구성하는 방법을 설명합니다. 생산자 클러스터가 datashare로 스키마를 공유하면, 소비자 클러스터의 dbt가 이를 원본 모델로 읽고 변환 결과를 자신의 클러스터에 materialize합니다.

## 핵심 내용

- Amazon S3 데이터 레이크의 원본을 Glue 또는 COPY로 생산자 클러스터에 적재합니다.
- 생산자는 datashare를 통해 스키마를 제로카피·실시간으로 공유합니다.
- dbt Cloud는 PrivateLink를 통해 JDBC 5439 포트로 연결합니다.
- dbt는 공유된 소스 모델을 읽고 변환 모델을 소비자 클러스터에 생성합니다.
- Amazon Quick Sight가 변환된 모델을 조회해 대시보드에 활용합니다.

## 참고 자료

- 원문: https://aws.amazon.com/blogs/big-data/dbt-and-amazon-redshift-data-sharing-multi-cluster-pipelines-without-moving-a-byte
