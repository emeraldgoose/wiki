---
title: "SageMaker Unified Studio를 Power BI에 연결하기 Part 1 - IDC 기반 도메인"
description: "Athena ODBC 2.2 네이티브 인증으로 Power BI를 SageMaker Unified Studio에 직접 연결: SageMakerBrowserIdc와 SageMakerIam, DSN과 DSN-less 방식, 게이트웨이 배선, IDC 도메인 워크스루."
published: "2026-09-15"
source_url: "https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/"
blog: "AWS Big Data"
locale: "ko"
tags: [aws, sagemaker, athena, power-bi, odbc, iam-identity-center, bi, ko]
---

# SageMaker Unified Studio를 Power BI에 연결하기 Part 1 - IDC 기반 도메인

[English version](../../../../en/sources/articles/aws/Connect_SageMaker_Unified_Studio_to_Power_BI_Part_1_IDC_Based_Domains.md)

**저자**: Ramesh H Singh, Krishna Atluru, Armando Segnini, Saushthav Saxena, Gaurav Sharma · **발행**: 2026-09-15 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-1-iam-identity-center-idc-based-domains/)

## 문제

거버넌스된 SageMaker Unified Studio 데이터가 필요한 Power BI 분석가는 기존에 서드파티 ODBC-JDBC 브리지가 필요했다 — 추가 컴포넌트, 라이선스, 유지보수 부담. UC Irvine의 인용이 이를 압축한다: AWS의 거버넌스 데이터에 접근하려면 우회로가 필요했다. Athena ODBC 드라이버 2.2.0+는 이제 Unified Studio 인증을 네이티브로 지원하며, 이 글(2부작 중 Part 1)은 IAM Identity Center (IDC) 기반 도메인용으로 배선한다.

## 해법 개요

새로운 Athena ODBC 인증 모드 2종: **SageMakerBrowserIdc** (Identity Center + 외부 IdP 경유 브라우저 SSO, 로컬 자격 증명 불필요)와 **SageMakerIam** (기본 자격 증명 체인, 여기서는 Identity Center 발급 자격 증명). 연결 방식 2종:

| | 방법 1: DSN 기반 (Athena 커넥터) | 방법 2: DSN-less (ODBC 커넥터) |
|---|---|---|
| 커넥터 | Amazon Athena | ODBC, 연결 문자열, DSN 없음 |
| 모드 | DirectQuery + Import | Import 전용 (ODBC 커넥터 경유 DirectQuery 불가) |
| 인증 | SageMakerBrowserIdc + SageMakerIam | SageMakerIam 전용 |
| 도메인 | IAM + IDC | IAM + IDC |
| 적합한 경우 | 실시간 대시보드 | DSN 없거나 예약 새로고침 시나리오 |

데모 시나리오: PUDL EIA-860 발전기 데이터셋을 Athena/SageMaker 경유로 조회하는 에너지 분석가가 `capacity_mw`를 `technology_description`별·`operational_status`별 쌓은 막대를 만든다. 흐름: Power BI Desktop → 게시 → Power BI Service → EC2 위 온프레미스 데이터 게이트웨이 (인스턴스 IAM 역할) → Athena → SageMaker 프로젝트 거버넌스 하의 Glue Catalog/S3. Desktop은 온프레미스나 EC2 어디서든 실행 가능하고, 게이트웨이는 항상 SageMakerIam을 쓰며 (브라우저 없는 Windows 서비스) 프로젝트 멤버여야 한다.

## 구현 (IDC 도메인)

**사전 요구사항**: Athena ODBC ≥2.2.0 (Win64), 최신 Power BI Desktop, Pro 라이선스, EC2 위 게이트웨이, 데이터가 있는 Unified Studio IDC 도메인 + 프로젝트 (글에 EIA-860 미리보기 표시).

**방법 1 — DSN (`pbi-idcdomain`)**: SSO 사용자를 프로젝트 멤버로 추가. Project → ⋯ → Project details → JDBC and ODBC details에서 IDC issuer URL, 도메인 ID (`dzd-…`), 프로젝트 ID, 워크그룹, 리전 복사. System DSN: 리전, Catalog `AwsDataCatalog`, Database `default`, 워크그룹, 인증 `SageMakerBrowserIdc` + SSO 시작 URL/리전 + 도메인/프로젝트 ID + 도메인 리전. Test (브라우저 Allow Access). Power BI: 데이터 가져오기 → Amazon Athena → DSN → DirectQuery → Use Data Source Configuration → AwsDataCatalog → `core_eia860__scd_generators` → 로드 → 누적 막대 → 게시 (`generation-idcdomain`).

**방법 2 — DSN-less**: 관리자가 `SageMakerDataAnalyst` 권한 세트 생성 (`datazone:GetConnection/ListConnections/GetDomain/GetProject`, `sts:GetCallerIdentity`, `*` 대상 — 메타데이터 전용이며 데이터는 여전히 프로젝트 멤버십이 통제), 사용자 할당, `aws configure sso` + `aws sso login`. SSO 역할 (`AWSReservedSSO_SageMakerDataAnalyst_…`)을 도메인 IAM 사용자 + 프로젝트 멤버로 추가. 프로젝트 개요에서 **Using IAM auth** ODBC 연결 문자열 복사, 예: `Driver={Amazon Athena ODBC (x64)};AwsRegion=…;Catalog=AwsDataCatalog;Schema=default;Workgroup=…;SageMakerDomainId=…;SageMakerProjectId=…;SageMakerDomainRegion=…;AuthenticationType=SageMakerIam;`. Power BI: 데이터 가져오기 → ODBC → (None) → 고급 → 문자열 붙여넣기 → Default or Custom → 로드 → 게시 (`generation-idcdomain-dsnless`).

**게이트웨이 + Service**: `pbi-gateway-role` 생성 (EC2 신뢰, 동일 인라인 정책) → 게이트웨이 EC2에 연결 → 도메인 사용자 + 프로젝트 멤버로 추가. 방법 1: 게이트웨이에 **System** DSN을 `SageMakerIam`으로, Desktop과 동일한 DSN 이름으로. 방법 2: 머신 설정 불필요, Service에서 직접 구성. Service: 작업 영역 → 시맨틱 모델 ⋯ → 설정 → 게이트웨이 및 클라우드 연결 → 연결 추가 (DSN 이름 또는 정확히 일치하는 연결 문자열) → 인증 **익명** → 매핑 → 적용 → 보고서 열기 (글의 Figure 14에 실시간 표시).

## 왜 중요한가

- **브리지 비용 제거**: 네이티브 드라이버 인증으로 서드파티 라이선스·유지보수가 사라진다.
- **거버넌스 유지**: 프로젝트 멤버십이 여전히 데이터 게이트이며, 정책의 `Resource: "*"`는 메타데이터 범위로 데이터 접근이 아니다.
- **신선도 선택**: 실시간용 DirectQuery 대 예약용 Import, 명확한 인증/방식 매트릭스와 함께.

## 세미나 시사점

- 게이트웨이 경험칙: System DSN (User 아님), 항상 `SageMakerIam`, 이름/문자열은 Desktop과 정확히 일치.
- 브라우저 인증은 게이트웨이 경계를 절대 넘지 않는다 — 방법 2와 게이트웨이가 `SageMakerIam`으로 수렴하는 이유다.
- Part 2는 IAM 기반 도메인을 다루며, 여기 결정 트리 (DSN vs DSN-less, IDC vs IAM)는 그대로 이전된다.

## 관련 개념

- `concepts/data-engineering/trino.md`, `concepts/data-engineering/data-modeling.md`

## 참고 자료

- [Part 2 - IAM 기반 도메인](https://aws.amazon.com/blogs/big-data/connect-amazon-sagemaker-unified-studio-to-microsoft-power-bi-part-2-iam-based-domains/)
- [Unified Studio 통합으로 분석 강화하기](https://aws.amazon.com/blogs/big-data/power-up-your-analytics-with-amazon-sagemaker-unified-studio-integration-with-tableau-power-bi-and-more/)
- [Athena ODBC v2 드라이버 문서](https://docs.aws.amazon.com/athena/latest/ug/odbc-v2-driver.html)
- [ENGIE의 Power BI용 Athena 데이터 소스 자동화](https://aws.amazon.com/blogs/big-data/how-engie-automates-the-deployment-of-amazon-athena-data-sources-on-microsoft-power-bi/)
