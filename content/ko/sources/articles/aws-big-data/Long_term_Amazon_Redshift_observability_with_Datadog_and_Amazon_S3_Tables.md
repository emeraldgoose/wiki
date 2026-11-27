---
title: "장기간 Amazon Redshift 관측 가능성 Datadog 및 Amazon S3 Tables"
description: "Amazon Redshift는 쿼리 히스토리를 7일만 보관하다 그 너머의 감사 및 규정 준수 데이터가 사라집니다. Amazon S3 Tables 시스템 테이블 통합은 자동으로 시스템 테이블 데이터를 Apache Iceberg 테이블로 Amazon S3에 지속적으로 제공하며, 사용자는 보존 정책을 설정합니다. AWS와 Datadog가 협력하여 이 데이터를 관측 가능하게 만들었습니다: Datadog Data Observability는 S3 Tables에서 Amazon Redshift 쿼리 히스토리를 읽어 컬럼 레벨 혈연, 주간~개월 단위의 쿼리 분석, 데이터 품질 모니터링을 제공합니다. 추가 SQL 쿼리 없이 워크로드 부하가 사라집니다. 사용자는 데이터를 소유하고 보존 정책을 설정하며 S3 Tables는 컴팩션과 스냅샷 관리를 처리합니다. 내보내기는 무료이며 Amazon Redshift, Athena 또는 Iceberg 호환 엔진으로 쿼리 가능합니다. Redshift + S3 Tables + Datadog는 7일 제한을 월~년 단위의 지속적 관측 가능성으로 대체합니다."
tags: [source, article, aws-big-data, datadog, observability, s3-tables, iceberg, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables"
arxiv_id: ""
authors: []
blog: aws-big-data
published_date: 2026-11-27
---
# 장기간 Amazon Redshift 관측 가능성 Datadog 및 Amazon S3 Tables

**원문**: [AWS](https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables) · **게시일**: 2026-11-18
**저자**: AWS Staff

## 개요

Amazon Redshift는 25개가 넘는 시스템 뷰에서 운영 기록을 캡처합니다. SYS_QUERY_HISTORY의 쿼리 실행 세부사항부터 SYS_QUERY_TEXT의 전체 쿼리 텍스트, 연결 활동, 사용자 변경, 워크로드 관리 이벤트, 리소스 소비 지표까지 다양한 데이터를 포함합니다. 이 상세 기록은 Amazon Redshift 클러스터 및 서버리스 워크그룹의 완전 운영 로그를 형성합니다. 그러나 Redshift는 이 데이터를 7일만 보관합니다. 7일 창이 닫히면 히스토리가 사라지며, 그 너머 감사 활동, 진행성 리전스 조사, 월~년 단위 규정 준수 요건을 만족할 수 없게 됩니다.

Amazon S3 Tables 시스템 테이블 통합은 이 근본적인 제한을 변화시킵니다. 활성화되면 Amazon Redshift가 자동으로 지속적으로 시스템 테이블 데이터를 Apache Iceberg 테이블로 Amazon S3에 제공합니다. 배달 비용이 들지 않으며, 사용자가 데이터를 소유하고 보존 정책을 설정하고 S3 Tables는 컴팩션과 스냅샷 관리를 처리합니다. 내보내진 데이터는 Amazon Redshift, Athena 또는 모든 Iceberg 호환 엔진으로 직접 쿼리할 수 있습니다.

AWS와 Datadog가 협력하여 이 데이터를 관측 가능하게 만들었습니다. Datadog Data Observability는 S3 Tables에서 Amazon Redshift 쿼리 히스토리를 읽어 컬럼 레벨 혈연, 주간~개월 단위의 쿼리 분석, 데이터 품질 모니터링으로 변환합니다. 결정적으로, 시간당 각 창고에 대해 읽기 전용 SQL을 실행할 필요가 사라지며 동일한 히스토리는 S3 Tables에서 직접 제공됩니다. AWS 관리형 Redshift 메트릭 및 로그를 위한 Amazon CloudWatch는 대체 모니터링 채널로 남아 있습니다.

## 핵심 내용

- Redshift 쿼리 히스토리는 7일 제한: 7일이 지나면 감사 및 규정 준수 데이터가 소실됩니다.
- Amazon S3 Tables 통합은 Redshift 시스템 테이블을 Apache Iceberg 테이블로 지속적으로 제공하며 배달 비용이 0입니다.
- 사용자는 데이터를 소유하고 보존 정책을 설정하며 S3 Tables는 컴팩션과 스냅샷 관리를 처리합니다.
- 내보내진 데이터는 Amazon Redshift, Athena 또는 Iceberg 호환 엔진으로 쿼리 가능합니다.
- Datadog Data Observability는 S3 Tables에서 쿼리 히스토리를 읽어 전체 플릿에 대한 컬럼 레벨 혈연, 주간~개월 단위 쿼리 분석, 데이터 품질 경고를 제공합니다.
- 이 솔루션은 각 창고에 시간당 읽기 전용 SQL 쿼리를 실행할 필요가 사라지게 합니다.
- AWS 관리형 Redshift 메트릭 및 로그를 위한 Amazon CloudWatch는 대체 모니터링 채널로 남아 있습니다.

## 상세

통합 구성에서는 Datadog에 S3 Tables 읽기 액세스 권한을 부여합니다. Datadog는 쿼리 히스토리를 컬럼 레벨 혈연 그래프로 파싱하여 테이블이 원료에서 스테이징, 마트로 흐르는 방식을 보여줍니다. 쿼리 분석은 주간 또는 월간 패턴이 느려지거나 더 많은 데이터를 스캔하는지를 드러냅니다. 데이터 품질 모니터는 비정상적인 쿼리, 연결 변경, 워크로드 이벤트를 식별합니다. 솔루션은 Airflow, dbt, Tableau, Looker, Power BI 등 다른 통합으로부터 혈연을 지원하여 자산 그래프를 통합화합니다.

설정 방법: Datadog에 S3 Tables 읽기 액세스 권한을 부여한 다음 Data Observability를 활성화하여 쿼리 히스토리 읽기를 시작합니다. 쿼리 히스토리 시간 창은 사용자 설정 가능하여 주간 또는 월간 패턴을 전체 Redshift 풋프린트 전체에서 분석할 수 있습니다.

## 참고 자료

- 블로그: [장기간 Amazon Redshift 관측 가능성 Datadog 및 Amazon S3 Tables](https://aws.amazon.com/blogs/big-data/long-term-amazon-redshift-observability-with-datadog-and-amazon-s3-tables)
