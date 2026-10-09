---
title: Spark 쿼리에서 아이스버그 materialized view로 가속화
description: Amazon EMR 7.12.0 및 AWS Glue 5.1부터 Apache Spark 쿼리 실행 시간을 Apache Iceberg materialized views를 사용하며 SQL을 변경하지 않고 자동 쿼리 재작성을 통해 감소시킬 수 있습니다.
date: 2026-09-10
tags: [aws, data-engineering, spark, iceberg, materialized-views, query-optimization]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/"
blog: aws
---

# Spark 쿼리에서 아이스버그 materialized view로 가속화

**Authors**: AWS Big Data Blog · **Published**: 2026년 9월 10일 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/accelerating-spark-queries-with-iceberg-materialized-views/)

## 쿼리 수정 접근 방식 비교

| 접근 방식 | 저장된 결과 | 리프레시 | 기존 쿼리 수정 필요 |
|---|---|---|---|
| AWS Glue의 표준 뷰 | 아니요 (각각 실행) | n/a | 필요 |
| 사용자 지정 ETL 파이프라인 | 예 | 수동 | 필요 |
| 수동 rewrite | 예 | 수동 | 필요 |
| automatic rewrite 사용 Materialized views | 예 | AWS Glue Data Catalog에서 스케줄에 따라 자동 | 필요하지 않을 때 |

## 선행 조건

아이스버그 materialized views를 사용한 automatic query rewrite를 사용하려면 다음이 필요합니다:

* Amazon EMR release 7.12.0 이상 또는 AWS Glue 5.1 이상.
* Apache Iceberg 또는 Parquet 형식의 소스 테이블, 동일한 AWS 리전 및 계정에서 materialized view에 등록된 AWS Glue Data Catalog. Parquet 소스 테이블은 Amazon EMR 7.14.0 및 AWS Glue 8.1부터 automatic query rewrite에 지원됩니다.
* Apache S3 Tables 버킷( Amazon S3의 기능) 또는 일반 목적 S3 버킷, materialized view 데이터용.
* 정의자(role)의 권한. AWS Identity and Access Management (IAM) 정책 또는 AWS Lake Formation을 사용할 수 있습니다.
* Spark 세션에서 automatic query rewrite 사용: `--conf spark.sql.optimizer.answerQueriesWithMVs.enabled=true`.
* Parquet 소스 테이블의 경우, `spark.sql.materializedView.v1SourceTables.enabled=true` 및 `spark.sql.materializedView.v1ETagVersioning.enabled=true` 설정.

## 작동 원리

* **SQL 쿼리 정의**: 지원되는 소스 테이블에서 aggregate, join 또는 filter가 포함된 SQL 쿼리를 정의합니다.
* **AWS Glue Data Catalog에 precomputed results 저장**: Apache Iceberg table으로, Amazon S3 버킷(일반 목적 S3 버킷 또는 Amazon S3 Tables)에 저장됩니다. 어떤 Apache Iceberg-compatible query engine도 materialized view를 읽을 수 있습니다. Amazon Athena, Amazon EMR, AWS Glue, Amazon Redshift 및 Iceberg-compatible third-party query engine. automatic query rewrite는 Amazon Athena, Amazon EMR, 및 AWS Glue의 AWS 최적화된 Spark 런타임에서 사용 가능합니다. 다른 엔진은 materialized view를 직접 쿼리할 수 있지만, 쿼리를 사용하여 자동으로 rewriting하지는 않습니다.
* **자동 리프레시**: 정의한 스케줄에 따라 MV를 최신 상태로 유지합니다. 예를 들어 `SCHEDULE REFRESH EVERY 1 DAY`. 생성 시점이나 later `ALTER MATERIALIZED VIEW ... ADD SCHEDULE REFRESH`로 설정할 수 있습니다. 예약된 시간에 current Apache Iceberg snapshot ID 또는 Parquet file ETags를 확인하고 소스 테이블 변경 사항이 감지되면 MV를 리프레시합니다.
* **automatic query rewrite**: query optimization 시 matching MV로 쿼리를 리디렉션합니다. Apache Spark의 automatic query rewrite는 두 가지 matching 전략을 사용합니다:
  + **Structural rewrite**: MV가 INNER joins를 포함한 single SELECT-FROM-WHERE-GROUP-BY 블록으로 정의된 경우. optimizer는 MV의 aggregates를 coarser grain으로 롤업하고 extra query predicates를 MV 스캔 onto 할 수 있습니다.
  + **Exact-match rewrite**: window functions 및 outer joins와 같은 다른_shape의 MV를 처리, canonicalized form of the MV body를 query plan의 subtrees와 매칭.

optimizer는 구성된 catalogs에서 MV 메타데이터 캐시를 컨설팅하고 최적의 매칭을 선택합니다. 또한 optimization 중 MV의 staleness를 확인합니다. stale MV는 건너뜁니다. 그렇게 하면 stale 결과를 반환하지 않습니다. 매칭하는 MV가 없으면 original query는 변경되지 않고 실행됩니다.

## 예: 세 가지 potential MV가 있는 한 쿼리

典型적인 analytics 쿼리를 예로 들어보겠습니다: "Top 100 preferred US customers by total store spending." fact 및 dimension tables를 조인하고 customer 차원에서 두 개의 selective filter를 적용하며, customer당 aggregate, window 함수를 사용하여 결과를 ranked하고 상위 100만 남깁니다:

```sql
SELECT c_customer_id, total_revenue, num_transactions, avg_purchase, revenue_rank FROM ( SELECT cust.c_customer_id, SUM(sales.ss_quantity * sales.ss_sales_price) AS total_revenue, COUNT(*) AS num_transactions, AVG(sales.ss_quantity * sales.ss_sales_price) AS avg_purchase, RANK() OVER (ORDER BY SUM(sales.ss_quantity * sales.ss_sales_price) DESC) AS revenue_rank FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_birth_country = 'UNITED STATES' AND cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id ) ranked WHERE revenue_rank <= 100 ORDER BY revenue_rank;
```

**쿼리 1**: any materialized view 적용 전 원래 쿼리. Top 100 preferred US customers by total store spending.

이 쿼리를 커버하는 세 가지 MV 디자인이 진행되며, 단일 테이블 pre-aggregate부터 전체 쿼리 body 자체까지 진행됩니다:

### 티어 1: store_sales만 pre-aggregate, join 및 filter 없음

이 티어는 customer-surrogate-key grain에서 store_sales의 단일 테이블 pre-aggregate입니다. 쿼리는 여전히 customer 테이블을 join하고, 두 필터를 다시 적용하고, c_customer_id grain에서 다시 aggregate를 수행하고, window 함수를 실행해야 합니다.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_1 AS SELECT ss_customer_sk, SUM(ss_quantity * ss_sales_price) AS sum_revenue, COUNT(ss_quantity * ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales GROUP BY ss_customer_sk;
```

*티어 1 MV: customer surrogate key grain의 store_sales 단일 pre-aggregate (join, filter 없음).*

**Plan 비교:**

*Plan 1: 원래 plan. large store_sales 테이블 스캔.*

*Plan 2: Rewritten plan (Tier 1). pre-aggregated customer_tier_1 MV 읽기. optimizer는 MV로부터 aggregates를 롤업하고 residual filters를 적용합니다.*

### 티어 2: store_sales x customer pre-join, one filter (c_preferred_cust_flag = 'Y') 미리 적용

중간 티어는 두 테이블을 pre-join하고 c_preferred_cust_flag 필터를 baked-in 합니다. 쿼리는 여전히 MV scan에서 country filter를 residual로 적용하고 RANK() window 함수를 실행해야 합니다.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_2 AS SELECT cust.c_customer_id, cust.c_birth_country, SUM(sales.ss_quantity * sales.ss_sales_price) AS sum_revenue, COUNT(sales.ss_quantity * sales.ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id, cust.c_birth_country;
```

*티어 2 MV: store_sales와 customer를 pre-join하고 preferred-customer filter를 적용.*

**Rewritten query plan:** Country filter applied as a residual on the MV scan.

### 티어 3: 필터가 둘 다 pre-join된 full query pre-join

이 티어는 두 테이블을 pre-join하고 both filters를 적용합니다. 따라서 쿼리는 창(window) 함수만 실행하면 됩니다.

```sql
CREATE MATERIALIZED VIEW mv_catalog.mv_db.customer_tier_3 AS SELECT cust.c_customer_id, cust.c_birth_country, SUM(sales.ss_quantity * sales.ss_sales_price) AS sum_revenue, COUNT(sales.ss_quantity * sales.ss_sales_price) AS count_revenue, COUNT(*) AS num FROM base_catalog.base_db.store_sales sales INNER JOIN base_catalog.base_db.customer cust ON sales.ss_customer_sk = cust.c_customer_sk WHERE cust.c_birth_country = 'UNITED STATES' AND cust.c_preferred_cust_flag = 'Y' GROUP BY cust.c_customer_id;
```

*티어 3 MV: full pre-join with both country and preferred-customer filters.*

**Rewritten query plan:** Only the window function runs on the residual data.

## 주요 이점

* **Single job**: 여러 좌표된_job을 관리하거나 오케스트레이션 인프라가 필요하지 않습니다.
* **자동 의존성 해결**: SDP가 dataset 참조에서 실행 순서를 해결합니다.
* **통합 데이터 카탈로그**: 모든 dataset은 Glue Data Catalog에 land하고 Athena로 표준 SQL로 쿼리 가능.
* **운영 복잡도 감소**: 수동 DAG wiring, retry logic 또는 checkpoint 관리가 필요하지 않습니다.

## 시작하기

1. Amazon EMR 7.12.0+ 클러스터 또는 AWS Glue 5.1+ 작업을 시작합니다.
2. AWS Glue Data Catalog에서 `CREATE MATERIALIZED VIEW`를 사용하여 가장 비용이 많이 반복되는 쿼리에 MV를 생성합니다.
3. `spark.sql.optimizer.answerQueriesWithMVs.enabled=true`를 Spark 세션 설정에서 automatic query rewrite를 사용 설정합니다.
4. optimized query plan에 MV scan node가 표시되거나 Amazon EMR 7.14.0+에서 INFO-level 로그를 확인하여 rewrite를 검증합니다.

멀티 테이블 조인, heavy aggregation 또는 large fact tables 위의 window 함수가 있는 쿼리는 초기 후보가 됩니다. 고비용 Frequently executed 쿼리 하나부터 시작하여 speedup을 검증한 다음 공유 패턴을 식별하여 더 넓은 범위로 확장하세요.

## 참조

* [Amazon EMR와 materialized views 사용](/docs/emr/latest/ReleaseGuide/emr-spark-materialized-views.html).
* [AWS Glue와 materialized views 사용](/docs/glue/latest/dg/materialized-views.html).
* [Amazon Athena에서 materialized view 쿼리](/docs/athena/latest/ug/querying-iceberg-gdc-mv.html).
* [AWS Glue Data Catalog에서 Apache Iceberg materialized views 소개](/blogs/big-data/introducing-apache-iceberg-materialized-views-in-aws-glue-data-catalog/).
* [AWS Lake Formation에서 materialized views](/docs/lake-formation/latest/dg/materialized-views.html).
* [Amazon S3 Tables 및 Iceberg materialized views 사용 방법](/blogs/big-data/how-to-use-streamlined-permissions-for-amazon-s3-tables-and-iceberg-materialized-views/).

## About the authors

### Resources

* [Amazon Athena](/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon EMR](/blogs/big-data/category/analytics/amazon-emr?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Kinesis](/blogs/big-data/category/analytics/amazon-kinesis?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon MSK](/blogs/big-data/category/analytics/amazon-managed-streaming-for-apache-kafka/)
* [Amazon QuickSight](/blogs/big-data/category/analytics/amazon-quicksight?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Redshift](/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [AWS Glue](/blogs/big-data/category/analytics/aws-glue?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

### Follow

* [Twitter](https://twitter.com/awscloud)
* [Facebook](https://www.facebook.com/amazonwebservices)
* [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
* [Twitch](https://www.twitch.tv/aws)
* [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)