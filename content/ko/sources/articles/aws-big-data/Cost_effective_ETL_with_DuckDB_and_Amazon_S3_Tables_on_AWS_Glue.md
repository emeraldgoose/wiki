---
title: "AWS Glue에서 DuckDB와 Amazon S3 Tables로 비용 효율적인 ETL"
description: "Glue 6.0에 내장된 DuckDB로 SQL 중심 ETL을 수행해 S3 Tables에 Iceberg로 기록하고 Spark 대비 시간·비용을 절반으로 줄입니다."
tags: [source, aws-big-data, glue, duckdb, etl, iceberg, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/cost-effective-etl-with-duckdb-and-amazon-s3-tables-on-aws-glue"
blog: aws-big-data
published_date: 2026-10-06
---

# AWS Glue에서 DuckDB와 Amazon S3 Tables로 비용 효율적인 ETL

## 개요

많은 통합 잡은 필터·조인·집계를 정해진 주기로 수행하는 SQL 중심 작업이라 시작 속도가 중요합니다. AWS Glue 6.0은 표준 `glueetl` 잡 안에서 DuckDB(임베디드 인프로세스 벡터화 SQL 엔진)를 실행할 수 있습니다. DuckDB가 S3의 Parquet을 읽어 REST 카탈로그로 S3 Tables에 Iceberg 테이블을 직접 씁니다. Spark를 대체하는 것이 아니라 보완하는 패턴으로, 단일 노드 SQL 작업은 DuckDB, 분산 작업은 PySpark를 고르되 인프라·IAM·트리거는 동일하게 씁니다.

## 사용 시점과 동작 원리

실행당 데이터가 단일 워커에 들어가고, 단일 노드 병렬로 충분하며, 집계·조인·윈도우 함수 중심 SQL이고, 실행당 비용·시간 최소화가 중요하면 DuckDB를 씁니다. 수평 확장이 필요한 규모, 복잡한 그래프 연산·커스텀 UDF·ML 파이프라인, 대규모 네이티브 Spark Iceberg 통합에는 Spark를 씁니다.

두 가지가 맞물려 동작합니다. Glue 6.0의 현대적 런타임(Amazon Linux 2023, glibc 2.34, Python 3.13)에서 DuckDB 1.5.x와 네이티브 확장이 `--additional-python-modules`나 가상환경으로 설치됩니다. DuckDB는 셔플·스케줄러 오버헤드 없는 단일 노드 벡터화 실행, `httpfs` 경유 네이티브 S3/Parquet 접근(잡 역할의 자격증명 체인), S3 Tables로의 네이티브 Iceberg 쓰기, `/tmp` 스필로 메모리 초과 데이터 처리를 제공합니다. 결과물은 Athena·Redshift·EMR이 조회하는 표준 Iceberg 테이블입니다. 워커는 입력에 맞춰 잡습니다. 실습은 2×G.1X(각 4 vCPU·16GB)이며 더 큰 입력은 G.2X/G.4X/G.8X로 올립니다.

## 따라하기: 일별 주문 요약

S3에 쌓인 원시 Parquet을 Glue 6.0 잡의 DuckDB SQL로 변환해 S3 Tables에 Iceberg 스냅샷으로 커밋하고(Athena·QuickSight 조회, Lake Formation 거버넌스), Glue 트리거·EventBridge 스케줄러·S3 이벤트+Lambda·Glue 워크플로로 실행합니다. 이커머스 예제는 완료/처리 중 주문만 남기고 수익 컬럼을 파생한 뒤 일·리전·카테고리별 일 매출과 주문 수를 집계하고, 일자별 멱등 재적재(없으면 생성, 배치 일자 범위 삭제 후 삽입)로 기록합니다. 삭제+삽입은 원자적이지 않으므로 `MaxRetries` 1이나 스테이징 테이블 방식을 씁니다.

- **구성:** DuckDB 홈·확장 디렉터리를 쓰기 가능한 `/tmp`로 지정하고 `httpfs`·`aws`·`iceberg`를 로드한 뒤 자격증명 체인 방식 S3 시크릿을 만듭니다. 코드에 키가 없습니다. Iceberg REST 쓰기에는 DuckDB 1.4+가 필요합니다.
- **변환:** S3 glob 패턴의 `read_parquet()`을 임시 테이블 집계에 바로 연결합니다(`GROUP BY ALL`은 DuckDB 전용 문법임에 유의).
- **쓰기:** 테이블 버킷을 Iceberg REST 카탈로그로 attach하고 스키마·테이블을 없으면 만든 뒤 일자별 삭제-삽입과 행 수 로깅을 합니다. 잡에는 Lake Formation 범위 권한(대상 테이블 `SELECT`·`INSERT`·`DELETE`, 네임스페이스 `CREATE_TABLE`)과 `lakeformation:GetDataAccess`가 필요합니다.

## 측정 결과

2 DPU Glue 6.0에서 840만 행(약 94MB Parquet) 기준, DuckDB는 약 56초 실행·1분 과금($0.0103), Spark는 약 117초 실행·2분 과금($0.0205)으로, Athena 검증 출력 1,176행이 동일하면서 시간·비용이 약 절반이었습니다. 하루 20회 실행이면 연간 약 $75 대 $150입니다. 표준 Glue CloudWatch 지표(드라이버 힙 압박, S3 읽기량)와 구조화 로깅으로 모니터링합니다. DuckDB 내부는 CloudWatch에 노출되지 않습니다.

## References

- 원문: [Cost-effective ETL with DuckDB and Amazon S3 Tables on AWS Glue](https://aws.amazon.com/blogs/big-data/cost-effective-etl-with-duckdb-and-amazon-s3-tables-on-aws-glue)
