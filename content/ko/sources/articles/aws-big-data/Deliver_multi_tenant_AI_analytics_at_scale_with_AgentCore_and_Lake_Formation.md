---
title: "AgentCore와 Lake Formation으로 멀티테넌트 AI 분석을 규모 있게 제공하기"
description: "AgentCore Gateway에서 Cognito와 Lake Formation을 적용해 데이터 에이전트가 테넌트별 행·열 수준 보안을 강제하는 방법."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation"
blog: aws-big-data
published_date: 2026-11-06
---

# AgentCore와 Lake Formation으로 멀티테넌트 AI 분석을 규모 있게 제공하기

**원문**: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation) · **게시일**: 2026-11-05

## 개요

거버넌스가 적용된 멀티테넌트 데이터 접근은 AI 기반 분석을 내장하는 소프트웨어와 B2C 제품에 필수적인 요구사항이다. 데이터 에이전트는 구조화된 데이터에 대해 자연어 질의에 답함으로써 큰 가치를 더하지만, 외부 사용자를 대상으로 동작할 때 가장 어려운 문제는 자연어를 SQL로 변환하는 것이 아니다. 각 테넌트가 자신에게 권한이 부여된 행, 열, 테이블, 셀에만 접근할 수 있도록 보장하는 일이다.

이 글은 대상 사용자에 따라 적합한 인증 모델을 구분한다. AWS IAM Identity Center와 Trusted Identity Propagation은 SAML 2.0과 SCIM을 통한 워크포스 인증과 엔터프라이즈 페더레이션을 위해 설계되므로 엔터프라이즈 사용자에 적합하다. 외부 대면 B2C나 멀티테넌트 응용 프로그램에서는 Amazon Cognito가 더 적합하다. Cognito는 OIDC를 통한 모바일 및 단일 페이지 응용 프로그램 통합, 소셜 ID 페더레이션, 대규모 외부 사용자 기반을 위한 셀프서비스 사용자 관리를 제공하기 때문이다. 이어서 글은 전통적인 Cognito와 Lake Formation 패턴을 Amazon Bedrock AgentCore의 기능인 AgentCore Gateway에 적용하는 방법을 보여주며, 인증된 사용자 신원에 기반해 행·열 수준 보안을 강제하는 데이터 에이전트를 완성한다.

종단 간 아키텍처는 신원 정보를 전체 호출 체인에 전파한다. 사용자는 Cognito 호스티드 UI를 통해 로그인하고 OAuth 토큰을 받으며, ID 토큰에는 custom:team 클레임이 포함된다. 프런트엔드는 액세스 토큰과 ID 토큰을 함께 AgentCore 런타임으로 호출하고, 런타임은 두 토큰을 에이전트 코드를 통해 MCP Gateway로 전달한다. 게이트웨이는 JWT 인증자로 액세스 토큰을 검증하고 ID 토큰을 최소 권한 Lambda 대상으로 전달한다. Lambda는 Cognito Identity Pool의 GetCredentialsForIdentity를 사용해 ID 토큰을 규칙 기반 매핑으로 선택된 IAM 역할에 범위가 제한된 임시 AWS 자격 증명으로 교환한다. Athena는 이 사용자 범위 자격 증명으로 질의를 실행하고, Lake Formation은 IAM 역할의 LF-Tag 권한과 데이터 셀 필터를 평가하여 사용자가 권한이 있는 데이터만 받도록 한다.

권한은 응용 프로그램의 필터링 로직이 아니라 선언적으로 표현된다. 각 사용자는 Cognito 사용자 풀에서 custom:team으로 태깅되고, 팀 클레임은 Identity Pool 규칙을 통해 IAM 역할로 매핑되며, 역할은 TeamA, TeamB, shared 같은 값을 가진 team 키의 LF-Tag와 연관된 리소스에 대해 Lake Formation 권한을 받는다. 이를 통해 테넌트별 SQL 조건을 응용 프로그램에 직접 작성하지 않고도 태그 기반 테이블과 행을 테넌트별로 노출하거나 숨길 수 있다.

## 핵심 내용

- 멀티테넌트 분석 에이전트는 자연어-SQL 변환이 아니라 세분화된 인가가 필요하다.
- Amazon Cognito는 외부 B2C와 SaaS 테넌트에, IAM Identity Center와 Trusted Identity Propagation은 워크포스 페더레이션에 적합하다.
- Cognito 사용자 풀의 custom:team 속성이 ID 토큰에 담기는 신원 신호가 된다.
- Cognito Identity Pool의 규칙 기반 매핑이 해당 클레임을 테넌트 범위 AWS 자격 증명으로 교환한다.
- Lake Formation의 LF-Tag와 데이터 셀 필터가 질의 시점에 행·열 수준 접근을 강제한다.
- AgentCore Gateway는 신원 토큰을 종단 간 전파하면서 에이전트를 데이터 도구에 연결한다.

## 상세

이 아키텍처는 프런트엔드에서 AgentCore 런타임과 MCP Gateway의 JWT 인증자를 거쳐 Lambda 대상으로 ID 토큰을 전달하고, Lambda가 자격 증명 교환을 수행한 뒤 임시 자격 증명으로 Athena를 실행한다. team 키와 TeamA, TeamB, shared 등의 값을 가진 별도의 Lake Formation 태그가 데이터 자산에 적용되며, 각 역할은 태그 기반 정책을 통해 SELECT와 DESCRIBE 권한을 받는다. 대상 고객은 고객 대면 분석을 구축하는 SaaS 응용 프로그램 아키텍트, 수십만 외부 사용자를 대상으로 하는 B2C 데이터 제품 팀, 파트너 포털 개발자, 테넌트 격리를 갖춘 에이전틱 데이터 기능이 필요한 AWS로 이전하는 ISV이다. CloudFormation 또는 CDK 스니펫과 콘솔 단계를 포함한 전체 배포 구성은 링크된 원문에 있다.

## 참고 자료

- 원문: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-multi-tenant-ai-analytics-at-scale-with-agentcore-and-lake-formation)
