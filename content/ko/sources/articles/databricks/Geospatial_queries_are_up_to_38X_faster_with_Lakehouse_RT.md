---
title: "Lakehouse//RT로 지리공간 쿼리 최대 38배 빠르게"
description: "Spatial SQL과 공간 조인을 Lakehouse//RT에서 실행해 기존 클라우드 데이터 웨어하우스보다 최대 38배 빠른 성능을 내는 방법입니다."
tags: [source, databricks, data-engineering, geospatial, ko]
locale: ko
source_url: "https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert"
blog: databricks
published_date: 2026-10-15
---

# Lakehouse//RT로 지리공간 쿼리 최대 38배 빠르게

**원문**: [databricks](https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert) · **게시일**: 2026-10-15

## 개요

Databricks는 올해 초 Spatial SQL을 정식 출시하며 GEOMETRY 데이터 타입, 100개 이상의 공간 함수, 고성능 공간 조인, AI/BI 지도, Delta Sharing을 지원했습니다. GEOMETRY와 GEOGRAPHY 타입은 Apache Spark에서 사용할 수 있고, Delta와 Iceberg v3가 쓰는 parquet 파일에서도 동일하게 동작합니다.

이제 Spatial SQL과 공간 조인이 Lakehouse//RT에서도 실행됩니다. 별도의 지리공간 서빙 계층 없이 거버넌스가 적용된 레이크하우스 데이터에서 초저지연·고동시성을 얻을 수 있습니다.

## 핵심 내용

- 50명 동시 사용자 기준으로 기존 데이터 웨어하우스보다 공간 쿼리가 최대 38배 빠릅니다.
- 단일 쿼리 동시성에서는 최대 20배 빠르며, 모든 벤치마크 쿼리가 더 빠릅니다.
- 평균 속도 향상은 3.5배 이상입니다.
- 쿼리 변경이나 추가 라이선스 없이 기존 SQL Serverless 공간 쿼리를 그대로 실행할 수 있습니다.
- Unity Catalog 거버넌스와 100개 이상의 공간 함수를 그대로 활용합니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/geospatial-queries-are-38x-faster-lakehousert
