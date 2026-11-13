---
title: "삼성 애즈가 Amazon Cognito로 Snowflake Iceberg 테이블을 연합한 방법"
description: "삼성 애즈는 피처 데이터를 Snowflake 관리형 Iceberg 테이블로 Amazon S3에 두고 AWS Lake Formation으로 연합한다. Amazon Cognito가 Snowflake가 신뢰하는 OAuth2 client_credentials 토큰을 발급하고, 사전 토큰 생성 Lambda가 필수 aud 클레임을 주입하며, Athena는 Lake Formation 거버넌스 아래 데이터 사본 하나를 질의한다. 두 번째 파이프라인도 중복 권한도 없다."
tags: [source, aws-big-data, data-federation, lakehouse, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-samsung-ads-federated-snowflake-iceberg-tables-using-amazon-cognito"
blog: aws-big-data
published_date: 2026-11-14
---

# 삼성 애즈가 Amazon Cognito로 Snowflake Iceberg 테이블을 연합한 방법

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/how-samsung-ads-federated-snowflake-iceberg-tables-using-amazon-cognito) · **게시일**: 2026-11-11

## 개요

삼성전자 광고 부문 삼성 애즈(Samsung Ads)는 피처 데이터를 Snowflake에 Apache Iceberg 테이블로 보관하고, ML 팀은 Amazon SageMaker AI에서 대규모 모델을 학습해 삼성 스마트 TV·커넥티드 TV 시청자를 타깃하는 프로그래매틱 바이어를 지원한다. 일반적인 다리 역할은 일정에 따라 데이터를 Amazon S3로 복사하는 것이지만, 이는 운영할 파이프라인 하나 더, 저장할 사본 하나 더, 합의를 유지해야 하는 권한 두 벌을 의미한다. 삼성 애즈 ML 플랫폼 엔지니어 Ajay Gunasekaran과 공동 집필한 이 글의 패턴은 복사를 없앤다. 파이프라인의 마지막 단계가 Snowflake 관리형 Iceberg 테이블을 Amazon S3에 쓰고, 그 테이블을 AWS Lake Formation으로 연합하며, Amazon Cognito가 Snowflake가 신뢰하는 OAuth2 토큰을 발급한다. 양쪽 모두 S3의 데이터 사본 하나를 읽는다. Snowflake가 테이블을 관리하고, Lake Formation이 어떤 주체가 읽을 수 있는지 통제하며, 모델 엔지니어는 학습 작업에 맞는 쿼리 엔진을 고른다.

솔루션은 기계 간(machine-to-machine) OAuth2로 Snowflake Horizon Catalog를 Lake Formation으로 연합한다. AWS Glue 연결은 Amazon VPC 내 프라이빗 서브넷에서 실행되어 AWS PrivateLink로 Snowflake에, NAT 게이트웨이로 Cognito 토큰 엔드포인트에 도달한다. 워크플로는 8단계로 흐른다. Athena가 연합 테이블을 참조하는 SQL 질의를 받아 카탈로그 해석과 권한 검사를 Lake Formation에 위임하고, Lake Formation은 AWS Glue Data Catalog를 통해 참조를 해석해 프라이빗 서브넷의 Glue 연결을 호출하며, 연결이 클라이언트 ID·시크릿·스코프를 실은 client_credentials 요청을 Cognito 토큰 엔드포인트로 보내고, 사전 토큰 생성(Pre Token Generation) Lambda 트리거(V3_0)가 Snowflake External OAuth 검증에 필요한 aud 클레임을 추가하고, 연결은 그 토큰으로 Snowflake Horizon Catalog의 Iceberg REST 엔드포인트를 호출해 스키마와 데이터 파일의 S3 위치를 담은 테이블 메타데이터를 받는다(Snowflake 엔드포인트 서비스는 프라이빗 DNS를 제공하지 않으므로 Route 53 프라이빗 호스팅 영역이 호스트명을 해석). Lake Formation은 임시·범위 제한된 S3 자격 증명을 Athena에 발급하고, Athena는 그 자격 증명으로 등록된 S3 위치에서 Iceberg 메타데이터와 Parquet 파일을 직접 읽어 질의를 실행한다.

삼성 애즈가 중앙 기업 ID 공급자 대신 Cognito를 고른 실무적 이유는 셋이다. Snowflake 테이블 조회마다 공급자의 토큰이 필요하므로 팀이 솔루션의 나머지와 함께 발급자를 소유하기를 원했다. 기업 ID 공급자는 대개 중앙 보안팀이 관리해 기계 간 클라이언트 하나 추가가 부서 간 요청이 되지만, 사용자 풀을 소유하면 셀프서비스가 된다. 그리고 보안 통합이 개별 클라이언트가 아니라 사용자 풀을 신뢰하므로 하나의 통합이 각자 자체 읽기 전용 Snowflake 역할을 가진 여러 워크로드를 지원할 수 있다.

## 핵심 내용

- 아키텍처: Amazon Cognito의 기계 간 OAuth2로 Snowflake Horizon Catalog를 AWS Lake Formation으로 연합. Glue 연결은 프라이빗 서브넷에서 실행되어 PrivateLink로 Snowflake에, NAT 게이트웨이로 공개 Cognito 토큰 엔드포인트에 도달하며, Athena-Lake Formation-Glue Data Catalog-Glue 연결이 질의 경로를 이룬다.
- 8단계 질의 워크플로: Athena의 SQL → Lake Formation 권한 평가 → Glue Data Catalog가 Snowflake 연결 해석 → Cognito로 client_credentials 요청 → 사전 토큰 생성 Lambda(V3_0)가 aud 클레임 주입 → Glue 연결이 PrivateLink와 Route 53 프라이빗 DNS를 거쳐 Snowflake Iceberg REST 엔드포인트에서 메타데이터(스키마 + S3 데이터 파일 위치) 조회 → Lake Formation이 임시 범위 S3 자격 증명 발급 → Athena가 Iceberg 메타데이터와 Parquet 파일을 직접 읽고 질의 실행.
- 설정은 두 CloudFormation 스택 + 명시적 SQL/CLI. snowflake-federation-oauth(Cognito 사용자 풀, 기계 간 앱 클라이언트, aud 클레임 Lambda, Glue 연결이 기대하는 형식으로 Secrets Manager에 앱 클라이언트 시크릿 기록, Snowflake SQL 생성), snowflake-federation-network(VPC, PrivateLink 엔드포인트, Route 53 프라이빗 호스팅 영역, Lake Formation 데이터 액세스 역할). Snowflake 보안 통합·권한 부여는 SQL로, S3 위치 등록·Glue 연결·연합 카탈로그·Lake Formation 권한은 CLI로, 검증은 Athena 콘솔에서.
- 구성 전 토큰 검증: 생성된 VerifyAudClaimCommand를 CloudShell에서 실행해 aud 클레임이 Cognito 클라이언트 ID와 같고 스코프가 snowflake/catalog.read인지 확인. 클레임 누락은 일찍 실패하지 않고 몇 단계 뒤 인증 불가 연결로 나타나 원인 규명이 어렵다.
- Snowflake 측: CREATE SECURITY INTEGRATION lakeformation_cognito_oauth를 EXTERNAL_OAUTH/CUSTOM으로 생성, Cognito 발급자·JWKS URL 지정, 토큰 사용자 매핑 클레임 sub를 login_name에 매핑, 대상 목록에 Cognito 클라이언트 ID, EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE(Cognito 커스텀 스코프는 Snowflake의 session:role:ROLE_NAME 형식을 담을 수 없음), 차단 역할 목록에 ACCOUNTADMIN·SECURITYADMIN·USERADMIN·SYSADMIN 포함(Snowflake 기본 목록보다 넓음).
- 서비스 신원: 읽기 전용 역할 lakeformation_catalog_reader와 LOGIN_NAME이 Cognito 클라이언트 ID인 서비스 사용자(토큰의 sub 클레임이 클라이언트 ID를 실고 통합이 sub를 login_name에 매핑), TYPE = SERVICE. 권한은 데이터베이스·스키마 USAGE와 스키마 내 모든·미래 Iceberg 테이블 SELECT.
- 스키마 위생 규칙: Snowflake 관리형 Iceberg 테이블만 있는 스키마만 연합 — 외부 관리 테이블 하나가 테이블 목록 전체를 실패시킬 수 있다. 변환(converted) 테이블, Iceberg 호환 Parquet에서 적재된 테이블, 역할이 접근할 수 없는 원본을 가진 클론은 미지원. 대소문자 혼용 인용 이름은 연합되지 않는다(연결이 CATALOG_CASING_FILTER를 UPPERCASE_ONLY로 설정).
- 보안 주의: Athena가 연합 테이블을 읽을 때는 Snowflake 마스킹·행 액세스 정책이 적용되지 않는다(Lake Formation이 S3 자격 증명을 발급하고 Athena가 Parquet를 직접 읽음). 이런 테이블은 연합 스키마에서 빼거나 통제를 Lake Formation에서 재구성해 시험해야 한다.
- 시크릿 처리: 연결이 검증되면 AWS Glue가 발급한 토큰을 Secrets Manager 시크릿에 기록해 캐시하므로, 그 시크릿에 대한 읽기 접근은 연합 테이블에 대한 읽기 접근으로 취급해야 한다.
- 외부 볼륨 세부: DESC EXTERNAL VOLUME으로 STORAGE_BASE_URL(버킷 + 선택적 접두사 — 접두사가 좋다. Lake Formation 데이터 액세스 역할을 그 경로로 한정)과 ENCRYPTION_TYPE 확인. 고객 관리 KMS 키의 경우 외부 볼륨 세션 역할에 kms:Decrypt/DescribeKey/GenerateDataKey가 키 정책에 있어야 하고, 없으면 Glue 연결이 no-session-policy-allows-kms:Decrypt 오류로 실패. Iceberg 테이블을 소유한 Snowflake 역할은 외부 볼륨 USAGE를 유지해야 발급 자격 증명 작업이 실패하지 않는다.
- PrivateLink 승인 특이점: SYSTEM$AUTHORIZE_PRIVATELINK는 IAM 사용자 장기 키의 연합 토큰이 필요(sts:GetFederationToken은 역할 세션 자격 증명 거부). Snowflake가 승인을 영속하므로 4단계 직후 임시 키와 사용자를 삭제해도 된다.
- 사전 요건: 동일 리전의 AWS 호스팅 Snowflake(PrivateLink에 Business-Critical 이상), CATALOG = 'SNOWFLAKE'와 S3 버킷을 가리키는 외부 볼륨으로 만든 Snowflake 관리형 Iceberg 테이블, Lake Formation 데이터 레이크 관리자 주체, Iceberg 데이터 파일이 있는 S3 버킷.

## 세부 사항

### aud 클레임에 Lambda가 필요한 이유

OAuth2 client_credentials 그랜트는 aud 클레임을 정의하지 않지만 Snowflake의 External OAuth 검증은 그것을 요구한다. Cognito의 사전 토큰 생성 트리거(V3_0)가 모든 기계 간 토큰에 클라이언트 ID를 aud로 주입해 간극을 메운다. 글의 조언은 나중에 디버깅하는 대신 생성된 명령으로 주입된 클레임을 즉시 검증하는 것이다. 클레임 누락은 조기 실패를 만들지 않고 여러 단계 아래에서 인증 불가 연결로만 나타나기 때문이다.

### 두 정체성 모델을 잇는 역할 매핑

Snowflake는 통상 session:role:ROLE_NAME 스코프에서 역할을 가져오는데, Cognito 커스텀 스코프는 resourceServer/scope 형식이라 그 형식을 표현할 수 없다. EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE가 서비스 사용자에게 부여된 역할이면 무엇이든 세션이 쓰게 하여 이를 해결하므로, 설정은 그 사용자를 단일 읽기 전용 역할로 유지하고 기본 목록이 놓치는 특권 역할을 명시적으로 차단한다. 정체성 사슬은 클라이언트 ID → sub 클레임 → login_name이며 서비스 사용자의 LOGIN_NAME이 Cognito 클라이언트 ID로 설정된다.

### 연합이 거버넌스를 바꾸는 방식

읽기는 두 신뢰 도메인에서 일어난다. Lake Formation은 누가 연합 테이블을 해석·읽을 수 있는지 거버넌스하고 Athena에 단기 S3 자격 증명을 발급하며, Snowflake 측 정책(마스킹, 행 액세스 정책)은 데이터가 S3에서 Parquet 파일로 읽히므로 질의를 결코 본다. 이 패턴을 채택하는 팀은 연합 스키마에 대해 Snowflake 수준 데이터 보호를 Lake Formation으로 옮기고, Lake Formation 데이터 액세스 역할을 외부 볼륨의 S3 접두사에 촘촘히 한정해야 한다.
