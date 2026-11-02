---
title: "BigQuery를 AWS Apache Iceberg 오픈 레이크하우스로 마이그레이션"
description: "BigQuery 기반 조직이 왜 AWS 오픈 레이크하우스로 이동해야 하는지, 마이그레이션 패턴과 목표 아키텍처를 정리한다."
tags: [source, aws-big-data, data-engineering, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg"
blog: aws-big-data
published_date: 2026-11-03
---

# BigQuery를 AWS Apache Iceberg 오픈 레이크하우스로 마이그레이션

**원문**: [aws-big-data](https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg) · **게시일**: 2026-11-02

## 개요

기업들은 AI 준비도를 데이터 준비도로 측정하며, 이는 종종 데이터가 열려 있고 이식 가능하게 유지되는 오픈 레이크하우스로의 이동을 의미한다. Amazon S3 저장소와 Apache Iceberg 테이블을 결합한 AWS의 오픈 레이크하우스는 단일 엔진 클라우드 데이터 웨어하우스의 제약 없이 워크로드에 맞는 엔진과 모델을 선택할 수 있게 한다.

## 주요 마이그레이션 패턴

- 대량 마이그레이션: BigQuery의 EXPORT DATA로 테이블을 Parquet 형식 Google Cloud Storage로 내보낸 뒤 AWS DataSync로 이동한다.
- Zero-ETL: Google Analytics, Salesforce, SAP, ServiceNow, HubSpot 등의 SaaS·운영 소스 데이터를 파이프라인 없이 레이크하우스에 적재한다.
- 변경 데이터 캡처(CDC): Amazon MSK Connect의 Debezium 커넥터로 운영 데이터 저장소의 행 단위 변경을 스트리밍한다.
- 스트리밍: Amazon Kinesis Data Streams와 Amazon MSK로 실시간 데이터를 원시 계층에 공급한다.
- 메달리온 계층: 브론즈/원시 데이터는 Apache Iceberg로 적재되고, 실버/신뢰 계층은 AWS Glue나 Amazon EMR Spark로 정제해 쿼리용 테이블을 만든다.

## 아키텍처

저장소, 소비자, 공통 계층이 분리된다. Amazon S3와 Apache Iceberg가 저장소 계층을 제공하고, 여러 컴퓨트 엔진과 대시보드, AI 워크로드가 동일한 테이블을 읽는다. 게시글은 페타바이트 규모에서 무중단 GCP 이전을 완료한 글로벌 기술 기업 사례를 소개한다.

## 참고 자료

- 원문: [BigQuery를 AWS Apache Iceberg 오픈 레이크하우스로 마이그레이션](https://aws.amazon.com/blogs/big-data/migrate-google-bigquery-to-an-open-lakehouse-on-aws-with-apache-iceberg)
