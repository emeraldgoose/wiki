---
title: "AWS Glue, Amazon S3 Tables, AWS Quick로 Anthropic 사용량·비용·접근 분석하기"
description: "AnyCompany Retail이 네이티브 AWS Glue 커넥터로 Anthropic Admin API 사용·비용 데이터를 Amazon S3 Tables에 적재하고, Glue 구체화 뷰로 비즈니스 데이터와 조인해 AWS Quick에서 지출·가치·API 키 소유 현황을 분석하는 방법."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick"
blog: aws-big-data
published_date: "2026-11-19"
---

# AWS Glue, Amazon S3 Tables, AWS Quick로 Anthropic 사용량·비용·접근 분석하기

**출처**: [aws-big-data](https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick) · **게시일**: 2026-11-16

## 개요

재무팀은 AI 지출을 사용한 사업부에 배분하고 싶어 하고, 엔지니어링 리더는 그 지출이 무엇을 만들어 내는지 알고 싶어 하며, 보안팀은 각 API 키의 소유자가 누구인지, 퇴사자 키가 남아 있는지 파악하려 한다. Anthropic은 Claude Code 사용량 분석과 Anthropic Admin API를 통해 관리자에게 상세한 사용량·비용 가시성을 제공하지만, 이 데이터를 AWS 기반 분석 스택으로 가져오려면 지금까지 Admin API와의 자체 통합을 만들고 유지해야 했다.

AWS Glue가 Anthropic용 네이티브 커넥터를 제공한다 — AWS Glue가 추가한 100개의 새 네이티브 SaaS 커넥터 중 하나다 — 덕분에 커스텀 코드가 필요 없다. Anthropic API 키를 AWS Secrets Manager에 저장하고 AWS Glue 연결에서 참조하면, 커넥터가 API 호출과 스키마 매핑을 처리한다. 이 글은 가상의 소매업체 AnyCompany Retail이 Anthropic 데이터를 Amazon S3 Tables(완전 관리형 Apache Iceberg 테이블)에 적재하고, AWS Glue 구체화 뷰로 자사 비즈니스 데이터와 조인한 뒤, Amazon Athena로 질의해 AWS Quick에서 리더십이 매주 리뷰하는 대시보드를 게시하는 과정을 다룬다.

## 핵심 내용

- **커넥터 설정**: Anthropic API 키를 AWS Secrets Manager에 저장하고 시크릿을 참조하는 Glue 연결을 만든 뒤, Glue ETL 작업이 Admin 연결을 통해 사용량·비용 리포트, 사용자, 워크스페이스 같은 엔터티(및 워크스페이스 연결을 통한 메시지 배치·파일)를 읽어 변경 없이 raw 네임스페이스에 쓴다.
- **레이크하우스 구조**: ETL 스크립트(`anthropic_usage_etl.py`)는 사용량·비용 리포트를 일별 팩트 테이블로 펼치고, 비용을 센트에서 미국 달러로 변환하며, API 키·사용자·워크스페이스 디멘션 테이블을 curated 네임스페이스에 만든 뒤, 모두 Amazon S3 Tables의 Apache Iceberg 테이블로 기록한다. AWS 분석 서비스(및 다른 Iceberg 엔진)가 직접 읽을 수 있다.
- **비즈니스 컨텍스트 조인**: Anthropic 데이터에는 워크스페이스·키별 지출만 있고, 워크스페이스를 소유한 사업부, 지출이 만들어 낸 결과, 키 생성자의 재직 여부는 없다. AnyCompany는 S3에 저장한 자체 CSV 세 가지 — `workspace_business_unit`(워크스페이스→사업부 매핑), `support_outcomes_daily`(사업부별·일별 대화 수, 완료된 해결 수, QA 점수), `hr_directory`(이메일, employment_status active/departed) — 를 reference 네임스페이스로 적재한다.
- **구체화 뷰**: AWS Glue 구체화 뷰(Iceberg 테이블로 저장)가 curated Anthropic 테이블과 reference 데이터셋을 조인해 지출·가치·접근 팩트셋을 만든다. Glue 역할에는 Secrets Manager 읽기, 스크립트·참조 데이터용 S3 읽기, Data Catalog의 테이블 버킷 읽기/쓰기, 그리고 자기 ARN에 대한 `iam:PassRole`이 필요하다(Glue가 뷰와 함께 역할을 저장하고 뷰 갱신 시 사용하기 때문).
- **질문에 대한 답과 시각화**: Amazon Athena(SQL)로 리더십의 세 가지 질문 — 어느 사업부가 AI 지출을 주도하는가, 지출이 무엇을 만들어 냈는가(예: 지출 대비 완료된 해결 수와 QA 점수), API 키는 누가 소유하는가(퇴사자 키 포함) — 에 답하고, AWS Quick이 자연어 프롬프트 또는 대시보드로 결과를 제공한다.
- **자사 데이터에 맞춰 조정**: 데이터셋이나 컬럼이 다르면 ETL 스크립트의 `REFERENCE_DATASETS`와 구체화 뷰 정의를 그에 맞게 수정한다.

## 세부 내용

솔루션은 세 부분으로 구성된다. Part 1은 Anthropic용 Glue 커넥터(시크릿, 연결, 권한)를 설정한다. Part 2는 AI 사용량 레이크하우스를 구축한다: reference CSV 세 개를 S3 공통 프리픽스 아래(데이터셋마다 폴더 하나)에 업로드하고, 위의 IAM 역할 권한을 부여한 뒤, ETL 작업을 업로드·실행해 S3 Tables 버킷의 raw/reference/curated 네임스페이스를 채우고, 이를 조합하는 Glue 구체화 뷰를 만든다. Part 3은 Quick을 다룬다: Quick이 테이블 버킷에 접근하도록 허용하고, 구체화 뷰에서 데이터셋을 만든 뒤, 대시보드를 작성한다.

글에 나온 예시 행은 각 데이터셋의 그레인을 보여 준다: `support_outcomes_daily`는 2026-10-30 Customer Service 기준 대화 1,216건, 완료된 해결 990건, QA 점수 96%를 기록하고, `hr_directory`는 jane.doe@example.com을 `departed`로 표시한다. 비용은 센트 단위로 전달되며 ETL 작업이 달러로 변환한다. 테이블 생성은 자동이다 — 스크립트가 없으면 테이블을 만들고 스키마가 바뀌면 컬럼을 추가한다.

운영 측면에서 이 구성은 AI 사용량을 데이터 레이크하우스의 또 하나의 거버넌스된 도메인으로 만든다. 같은 Iceberg 테이블을 Athena에서 바로 질의할 수 있고, 나중에는 어떤 Iceberg 호환 엔진에서도 읽을 수 있으며, 구체화 뷰는 사람이 아니라 뷰에 저장된 Glue 역할이 갱신한다. 보안 측면의 이점으로는 `hr_directory` 조인으로 퇴사자가 소유한 API 키를 식별하고, `workspace_business_unit`으로 지출을 사업부에 귀속시킬 수 있다는 점이 있다.

**참고**: 이 글은 샘플 데이터로 진행하는 워크스루다. 그림 세부 사항과 정확한 스크립트 내용은 원문을 참고하라. ETL 스크립트와 구체화 뷰 SQL은 글에서 별도로 내려받는다.

## 참고 자료

- 원문: [Analyze Anthropic usage, spend, and access with AWS Glue, Amazon S3 Tables, and AWS Quick](https://aws.amazon.com/blogs/big-data/analyze-anthropic-usage-spend-and-access-with-aws-glue-amazon-s3-tables-and-aws-quick)
