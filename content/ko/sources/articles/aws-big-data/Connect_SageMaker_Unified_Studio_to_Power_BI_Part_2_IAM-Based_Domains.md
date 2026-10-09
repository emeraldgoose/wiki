---
title: "SageMaker Unified Studio를 Power BI에 연결하기 Part 2 - IAM 기반 도메인"
description: "Athena ODBC SageMakerIam 인증으로 IAM 기반 도메인의 SageMaker Unified Studio에 Power BI를 직접 연결: SSO 권한 세트, DSN 및 DSN-less 구성, 게이트웨이 IAM 역할."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/"
blog: "AWS Big Data"
locale: "ko"
tags: [aws, sagemaker, athena, power-bi, odbc, iam, iam-identity-center, bi, ko]
---

# SageMaker Unified Studio를 Power BI에 연결하기 Part 2 - IAM 기반 도메인



**저자**: Ramesh H Singh, Krishna Atluru, Armando Segnini, Saushthav Saxena, Gaurav Sharma · **발행**: 2026-09-15 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/)

## 문제

시리즈 Part 1에서는 IDC(IAM Identity Center) 기반 도메인에 대해 Power BI 연결을 구성했다. Athena ODBC 드라이버 2.2.0+가 브라우저 기반 SSO(`SageMakerBrowserIdc`)를 지원하기 때문이다. 그러나 IAM 기반 도메인에는 IDC 브라우저 플로우가 없어 드라이버가 다른 경로로 AWS 자격 증명을 확보해야 한다. UC Irvine 사례가 보여주듯 분석가는 Power BI에 살고, 거버넌스된 데이터는 Unified Studio 프로젝트에 있는데, 기존에는 서드파티 ODBC-JDBC 브리지(추가 라이선스 필요)가 필요했다. 이 글(2부작 중 Part 2)은 기본 자격 증명 체인에서 가져오는 `SageMakerIam` 인증으로 IAM 기반 도메인에 동일한 직접 연결을 만든다.

## 해법 개요

아키텍처는 Part 1과 동일하다: Power BI Desktop → Athena ODBC → SageMaker Unified Studio 프로젝트(거버넌스 경계) → Athena/Glue Catalog/S3, 그리고 EC2 위 온프레미스 데이터 게이트웨이가 Power BI Service로 이어준다. 달라지는 것은 인증과 준비 과정이다:

| | Part 1 (IDC 도메인) | Part 2 (IAM 도메인, 본문) |
|---|---|---|
| 인증 모드 | `SageMakerBrowserIdc` + `SageMakerIam` | `SageMakerIam` 전용 |
| 자격 증명 원천 | Identity Center 경유 브라우저 SSO | 기본 자격 증명 체인 (여기서는 `aws configure sso`의 Identity Center 권한 세트) |
| 추가 관리자 작업 | 프로젝트 멤버십 외 없음 | 권한 세트 + SSO 프로파일 + SSO 역할의 프로젝트 멤버십 |
| 게이트웨이 인증 | `SageMakerIam` (EC2 인스턴스 역할) | 동일하게 `SageMakerIam` — 변함없음 |

두 가지 연결 방식을 모두 다룬다: **방법 1 (DSN 기반)** Athena 커넥터 경유 (DirectQuery + Import 지원), **방법 2 (DSN-less)** ODBC 커넥터 + 연결 문자열 (Import 전용). 게이트웨이는 브라우저가 없는 Windows 서비스로 동작하므로 두 방식 모두 게이트웨이에서는 `SageMakerIam`으로 수렴한다.

데모 데이터셋은 동일한 PUDL EIA-860 발전기 테이블(`core_eia860__scd_generators`)이며, `technology_description`별 `capacity_mw`를 `operational_status`로 쌓은 막대 차트를 만든다.

## 구현

**사전 요구사항** (Part 1 + 추가): Windows 머신에 최신 AWS CLI, Identity Center SSO가 활성화된 SageMaker Unified Studio IAM 기반 도메인.

**관리자 설정 — Identity Center를 통한 자격 증명 배관:**

1. IAM Identity Center에 **권한 세트** `SageMakerDataAnalyst` 생성. 인라인 정책은 메타데이터 조회 전용 (`datazone:GetConnection/ListConnections/GetDomain/GetProject`, `sts:GetCallerIdentity`, `Resource: "*"` — 이 액션들은 리소스 단위 권한을 지원하지 않으므로 `*` 필수). 데이터 접근 권한이 아니며, 실제 데이터 게이트는 프로젝트 멤버십이 유지한다. Athena/S3 권한은 프로젝트 IAM 역할이 별도로 제공한다.
2. 대상 계정에 SSO 사용자/그룹을 해당 권한 세트로 **할당**.
3. 머신에 **SSO 프로파일** 구성: `aws configure sso` (세션명 예 `smus`, 시작 URL, 리전, `sso:account:access` 스코프) → `~/.aws/config`에 `sso_session` 블록 생성. 일상 갱신은 `aws sso login` 한 줄, 검증은 `aws sts get-caller-identity`.
4. **프로젝트 멤버십**: 드라이버에 자격 증명을 공급하는 IAM 정체성(예: `AWSReservedSSO_SageMakerDataAnalyst_…`)을 Unified Studio 프로젝트 멤버로 추가. Project → ⋯ → Project details → JDBC and ODBC details에서 도메인 ID, 프로젝트 ID, 리전, Athena 워크그룹을 복사.

**방법 1 — DSN (`pbi-iamdomain`)**: Athena ODBC 드라이버로 System DSN 생성 — 리전, Catalog `AwsDataCatalog`, Database `default`, 워크그룹, 인증 `SageMakerDomainId` (`dzd-…`), `SageMakerProjectId`, `SageMaker Region`, 타입 `SageMakerIam`. Test로 연결 확인(브라우저 Allow Access). Power BI: 데이터 가져오기 → Amazon Athena → DSN → DirectQuery → Use Data Source Configuration → `AwsDataCatalog` → 발전기 테이블 → 로드 → `generation-iamdomain`으로 게시.

**방법 2 — DSN-less**: 프로젝트 개요에서 **Using IAM auth** ODBC 연결 문자열을 복사, 예: `Driver={Amazon Athena ODBC (x64)};AwsRegion=…;Catalog=AwsDataCatalog;Schema=default;Workgroup=…;SageMakerDomainId=…;SageMakerProjectId=…;SageMakerDomainRegion=…;AuthenticationType=SageMakerIam;`. Power BI: 데이터 가져오기 → ODBC → (None) → 고급 → 문자열 붙여넣기 → Default or Custom → 로드 → `generation-iamdomain-dsnless`로 게시. 머신에 기본 체인의 다른 자격 증명이 이미 있으면 관리자 SSO 설정 전체를 건너뛰어도 된다.

**게이트웨이 + Service**: `pbi-gateway-role` 생성 (EC2 신뢰, 동일 인라인 정책) → 게이트웨이 EC2에 연결 → 도메인 사용자 + 프로젝트 멤버로 추가. 방법 1: 게이트웨이 머신에 **System** DSN을 Desktop과 동일한 이름으로 복제. 방법 2: 머신 설정 불필요, Service에서 직접 구성. Service: 작업 영역 → 시맨틱 모델 ⋯ → 설정 → 게이트웨이 및 클라우드 연결 → 연결 추가(일치하는 DSN 이름 또는 완전히 동일한 연결 문자열) → 인증 **익명** → 매핑 → 적용 → 보고서 열기.

## 왜 중요한가

- **IAM 도메인에서도 브리지 비용 제거**: 네이티브 `SageMakerIam` 인증으로 이미 운영 중인 도메인 유형에 서드파티 라이선스가 불필요해진다.
- **거버넌스 유지**: `Resource: "*"` 정책은 겉보기에 넓지만 메타데이터 범위에 한정되며, 실제 읽기는 프로젝트 멤버십 + Lake Formation이 통제하고 세션별 단기 자격 증명이 발급된다.
- **자동화 가능**: ENGIE의 Power BI용 Athena 데이터 소스 자동화 사례와, 프로젝트 생성 시 게이트웨이 역할을 자동 추가하는 셀프서비스 블루프린트(`ProjectMembership` 리소스)를 안내한다.

## 세미나 시사점

- IAM 도메인에서는 Part 1의 인증 매트릭스가 단일 모드로 축소된다: Desktop·게이트웨이 모두 `SageMakerIam`.
- 자격 증명 원천은 교체 가능하다 — 오늘은 Identity Center SSO 프로파일, 게이트웨이에서는 EC2 인스턴스 역할, 내일은 기본 체인의 다른 원천. ODBC 파라미터는 바뀌지 않는다.
- 게이트웨이 규칙은 그대로: System DSN (User 아님), 이름/문자열은 Desktop과 정확히 일치, Service에서는 익명 인증.

## 관련 개념

- `concepts/data-engineering/trino.md`, `concepts/data-engineering/data-modeling.md`

## 참고 자료

- [Part 1 - IDC 기반 도메인](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/)
- [Unified Studio 통합으로 분석 강화하기](https://aws.amazon.com/blogs/big-data/power-up-your-analytics-with-amazon-sagemaker-unified-studio-integration-with-tableau-power-bi-and-more/)
- [Athena ODBC v2 드라이버 문서](https://docs.aws.amazon.com/athena/latest/ug/odbc-v2-driver.html)
- [ENGIE의 Power BI용 Athena 데이터 소스 자동화](https://aws.amazon.com/blogs/big-data/how-engie-automates-the-deployment-of-amazon-athena-data-sources-on-microsoft-power-bi/)
