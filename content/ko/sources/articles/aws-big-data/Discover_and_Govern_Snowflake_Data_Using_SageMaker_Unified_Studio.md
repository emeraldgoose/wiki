---
title: "SageMaker Unified Studio로 Snowflake 데이터를 검색하고 거버넌스하기"
description: "Glue 연결로 Snowflake를 SageMaker Unified Studio에 연합하고, 거버넌스 자산을 SageMaker Catalog에 게시하며, 데이터 이동 없이 Glue 데이터 품질 점수를 게시."
published: "2026-09-16"
source_url: "https://aws.amazon.com/blogs/big-data/discover-and-govern-snowflake-data-using-sagemaker-unified-studio/"
blog: "AWS Big Data"
locale: "ko"
tags: [aws, sagemaker, snowflake, glue, data-quality, catalog, governance, ko]
---

# SageMaker Unified Studio로 Snowflake 데이터를 검색하고 거버넌스하기



**저자**: Marco Duarte López, Diego Ortiz · **발행**: 2026-09-16 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/discover-and-govern-snowflake-data-using-sagemaker-unified-studio/)

## 문제

많은 조직이 하이브리드 자산을 운영한다: 핵심 테이블은 Snowflake에, 분석 워크로드는 AWS에. 연결 없이는 Snowflake 데이터를 카탈로그에 올리려면 수일이 걸리는 추출 파이프라인을 만들어야 하고, 거버넌스는 두 시스템으로 쪼개지며, 검색 마찰이 중복 노력을 강제한다. 글의 질문: 데이터 복제와 커스텀 ETL 없이 5–15분 만에 Snowflake 데이터를 쿼리·카탈로그·검증할 수 있는가?

## 해법 개요

SageMaker Unified Studio가 AWS Glue 연결을 통해 Snowflake를 연합(federate)한다. 연합 카탈로그 항목이 Glue Data Catalog에 등록되고 Lake Formation이 거버넌스하며, Snowflake 밖으로 데이터는 이동하지 않는다. 5단계 워크플로:

1. SageMaker Unified Studio에서 **Snowflake 연결 생성** (Glue 연결, register-in-catalog on).
2. 게시자 프로젝트에 **테이블 연합** — 수분 내 프로젝트 카탈로그에 테이블 등장.
3. **데이터셋을 SageMaker Catalog에 게시** — 비즈니스 메타데이터 포함 거버넌스 자산으로.
4. Glue Data Quality (Visual ETL 경유 DQDL)로 **품질 검증** 후 카탈로그 자산에 점수 게시.
5. **소비**: 게시자 프로젝트 사용자는 SQL 분석(Athena 푸시다운)으로 쿼리, 소비자 프로젝트는 SageMaker Catalog에서 검색·구독.

연합 쿼리는 Athena를 경유한다: Athena가 Glue Catalog에서 테이블 정의를 읽고 Snowflake에 연결해 쿼리를 푸시다운한 뒤 결과만 반환한다. S3로 복사되는 것은 없다.

## 구현

**사전 요구사항**: 관리자 접근 권한의 Snowflake 계정과 테이블이 있는 데이터베이스/스키마, SageMaker Unified Studio 도메인 + 프로듀서 프로젝트, Glue 자산용 S3 버킷, IAM 권한 (`datazone:SearchListings`, `GetListing`, `ListDomains`, `GetDomain`, `PostTimeSeriesDataPoints`, `GetAsset`, `ListAssetRevisions`). Glue 작업 역할을 도메인 사용자로 추가하고 프로젝트 멤버로 Owner 권한 부여.

**연결 상세** (Project → Data → Add → Add Connection → Snowflake): 이름 `snowflake-connection`, 호스트 `<account>.snowflakecomputing.com`, 포트 443, 데이터베이스/웨어하우스/스키마, 사용자명/비밀번호, **Register in AWS Glue Data Catalog** 체크, 대소문자 충돌 처리 선택. 수분 대기 후 검색으로 연합 객체 확인.

**카탈로그 게시**: Manage → Data Sources → Create Data Source → AWS Glue, Import data lineage 체크, 연결 `project.default_lakehouse`, 카탈로그 `snowflake-connection`, 데이터베이스명, 테이블 선택 `*` 또는 특정 테이블. 소스 실행으로 메타데이터 추출 → Assets 열기 → 필요시 Generate Descriptions (비즈니스 설명, 컬럼 정의, 용어집 제안) → **Publish Asset**.

**데이터 품질 파이프라인** (Glue Studio Visual ETL):

1. aws-samples의 `post_dq_results_to_datazone.py`와 `post_dq_results_to_datazone.json`을 `s3://aws-glue-assets-<account>-<region>/transforms/`에 복사해 **Datazone DQ Result Sink** 커스텀 트랜스폼 등록.
2. 신규 Visual ETL 잡: Snowflake 소스(연결 재사용, 스키마/테이블 선택) → **Evaluate Data Quality** 트랜스폼(DQDL 규칙) → **ruleOutcomes** → **Datazone DQ Result Sink** (도메인 ID, 테이블/스키마, 규칙셋 이름, 최대 결과 수).
3. 잡 파라미터: `--additional-python-modules = boto3>=1.34.105`. 저장 후 실행.
4. SageMaker Catalog → Assets → Data Quality 탭에서 확인 (글의 예: 전체 점수 100, 규칙셋 `movies` 통과 1/1).

## 왜 중요한가

- **데이터 이동 없음**: 수일의 파이프라인 작업 대신 5–15분에 제자리 쿼리·검증.
- **중앙화된 거버넌스**: Snowflake와 AWS를 아우르는 단일 검색·품질 표면 (SageMaker Catalog), Lake Formation 접근 통제.
- **검색 시점의 신뢰**: 소비자는 구독 전에 품질 점수를 확인 — Snowflake 접근이나 자체 검증 실행 불필요.
- **통합 협업**: 계보 임포트를 곁들인 게시자/소비자 프로젝트 분리로 소유권 명확화.

## 세미나 시사점

- 진실 원천이 제자리에 있어야 할 때는 복제보다 연합이 낫다: 메타데이터는 이동하고 데이터는 남는다.
- 날카로운 모서리는 IAM (도메인 사용자 + 프로젝트 Owner인 Glue 역할, `datazone:` 액션)과 커스텀 트랜스폼 배선 (`transforms/` 폴더 + boto3 모듈 핀)이다.
- 품질-메타데이터화 (DQ 결과를 카탈로그 자산에 게시)는 기술적 검사를 조직적 신뢰 신호로 바꾼다.

## 관련 개념

- `concepts/data-engineering/apache-iceberg.md`, `concepts/data-engineering/data-modeling.md`

## 참고 자료

- [Amazon S3 Tables와 SageMaker Catalog로 크로스 계정 레이크하우스 거버넌스](https://aws.amazon.com/blogs/big-data/cross-account-lakehouse-governance-with-amazon-s3-tables-and-sagemaker-catalog/)
- [ETL 파이프라인용 AWS Glue Data Quality 동적 규칙 시작하기](https://aws.amazon.com/blogs/big-data/get-started-with-aws-glue-data-quality-dynamic-rules-for-etl-pipelines/)
- [AWS Glue DQDL 문서](https://docs.aws.amazon.com/glue/latest/dg/dqdl.html)
