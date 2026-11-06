---
title: "AWS Glue 6.0으로 선언적 ETL 파이프라인 구축"
description: "AWS Glue 6.0과 Spark Declarative Pipelines를 사용해 SQL과 Python 변환을 선언적으로 작성하는 ETL 파이프라인 구축 절차를 요약한다."
tags: [source, article, aws-big-data, etl, aws-glue, spark, pipeline, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-declarative-etl-pipelines-with-aws-glue-6-0/"
blog: "AWS Big Data"
published: "2026-09-09"
---

# AWS Glue 6.0으로 선언적 ETL 파이프라인 구축

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-declarative-etl-pipelines-with-aws-glue-6-0/) · **게시일**: 2026-09-09

## 개요

AWS Glue 6.0에서는 Spark Declarative Pipelines를 통해 ETL 파이프라인을 선언형으로 정의할 수 있다. 개발자는 데이터 흐름과 의존 관계를 코드로 명시하는 대신 SQL과 Python 변환을 함께 사용하며, 파이프라인 실행 엔진이 bronze, silver 단계와 뷰 의존성을 해석하고 실행 계획을 구성한다. 글은 sample 데이터를 준비하고 PySpark 기반 파이프라인 파일을 작성한 뒤 dry-run 검증과 실제 실행을 거치는 전체 과정을 단계별로 보여준다.

파이프라인의 핵심은 각 변환 단계가 자신의 입력과 출력을 선언적으로 표현한다는 점이다. Bronze 계층에서 원시 데이터를 ingest하고 Silver 계층에서 정제하며, materialized view 방식의 배치 변환은 자동 dependency resolution을 통해 필요한 실행 순서를 맞춘다. 개발자는 `spark-pipeline.yml`, bronze Python, silver SQL 등을 분리해 유지할 수 있어 데이터 품질 규칙과 data contract를 파이프라인 정의 안에 통합하기 쉽다.

## 핵심 내용

- AWS Glue 6.0은 Spark Declarative Pipelines를 사용해 ETL 파이프라인을 선언형으로 정의한다.
- bronze와 silver 계층, SQL과 Python 변환이 동일한 파이프라인 안에서 coexist 할 수 있다.
- materialized view 기반 batch transform은 dependency resolution을 자동으로 처리한다.
- `spark-pipeline.yml`과 transformations 디렉터리로 파이프라인 구성을 분리할 수 있다.
- IAM role, 샘플 데이터, 구성 파일 준비가 선행되어야 한다.
- dry-run은 실제 실행 전에 계획과 의존성을 검증하는 데 사용된다.
- 실행 후에는 데이터 결과와 비용을 함께 검토해야 한다.

## 절차와 주의점

실제 적용에서는 파이프라인 파일을 작성하기 전에 IAM 역할과 입력 데이터 접근 권한을 확인하는 것이 중요하다. Dry run으로 정의 파일과 실행 순서를 검증한 뒤 production execution을 수행하며, materially wrong dependency나 스키마 mismatch는 이 단계에서 드러난다. 비용 측면에서는 Glue job의 병렬도, 입력 데이터 양, 새로고침 빈도가 주요 비용 결정 요소가 되므로 proof of concept에서 소규모 데이터로 파이프라인 구조를 먼저 검증하는 것이 좋다.

## 참고

- Source: [Build declarative ETL pipelines with AWS Glue 6.0](https://aws.amazon.com/blogs/big-data/build-declarative-etl-pipelines-with-aws-glue-6-0/)