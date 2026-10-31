---
title: "Amazon SageMaker Unified Studio의 Designations로 최소 권한 접근 구현하기"
description: "Amazon SageMaker Unified Studio의 designations는 도메인 관리자가 한 번 정의하여 프로젝트별로 할당하는 재사용 가능한 명명 기반 권한 세트로, 단일 프로젝트 안에서 각 페르소나에 필요한 최소 권한만 부여합니다."
tags: [source, aws-big-data, data-governance, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio"
blog: aws-big-data
published_date: 2026-10-30
---

# Amazon SageMaker Unified Studio의 Designations로 최소 권한 접근 구현하기

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio) · **게시일**: 2026-10-30

## 개요
데이터 및 AI 작업이 실험 단계에서 프로덕션으로 넘어가 공유 환경에서 운영되기 시작하면, 누가 어떤 작업을 할 수 있는지에 대한 질문은 피할 수 없습니다. Amazon SageMaker Unified Studio는 designations라는 명명된 권한 세트로 이 문제에 답합니다. 관리자는 designation을 한 번 정의하고 이를 프로젝트 구성원에게 할당합니다. 구성원이 AWS IAM 역할, IAM 사용자, IAM Identity Center 사용자 또는 그룹을 통해 로그인하더라도 designation은 각 역할이 책임에 필요한 액세스만 부여하도록 돕습니다. 그 결과 데이터는 단일 프로젝트에 통합된 채로 유지되고, 권한만 페르소나별로 세분화됩니다. Designations는 AWS CloudFormation과 연동되며 SageMaker Unified Studio 사용료 외에 추가 요금이 없습니다. 다만 유효 액세스는 여전히 정체성 및 리소스 정책, 서비스 제어 정책, 권한 경계, 그룹 멤버십 등에 의존하므로, designations는 기존 IAM 제어를 대체하기보다 보완하는 수단으로 설계되었습니다.

## 핵심 내용
- 도메인 관리자는 Catalog, Project, Subscriptions, Connections, Notebooks 카테고리로 그룹화된 세분화 권한을 선택하여 designation을 정의하며, 권한은 Cedar 정책 언어를 기반으로 합니다.
- 프로젝트 소유자는 각 구성원에게 designation 하나를 할당하고, 포털이나 API를 통해 구성원이 작업을 수행하면 SageMaker Unified Studio가 해당 designation을 평가한 뒤 작업을 허용합니다.
- 구성원은 SSO 그룹 멤버십을 통해 designation을 상속할 수 있으며, 직접 할당과 그룹 상속이 겹치면 두 권한 세트의 합집합이 적용되므로 과도한 액세스를 피하려면 SSO 그룹 할당을 정기적으로 검토해야 합니다.
- 인증은 두 계층으로 동작합니다. AWS 경계에서 IAM이 API 호출 가능 여부를 판단하고, 그 다음 designation이 프로젝트 내 특정 액션 권한을 확인합니다. designation이 허용해도 IAM Deny는 무조건 호출을 차단합니다.
- 모든 도메인은 프로젝트 수준에서 Owner(구성원 관리 포함 전체 제어)와 Contributor(구성원 관리 및 프로젝트 삭제를 제외한 전체 액세스)라는 두 AWS 관리 designation을 기본 제공합니다.
- designation은 한 번 정의한 뒤 프로젝트별로 할당되므로 정책을 다시 만들지 않고도 모든 프로젝트에서 일관된 권한을 유지할 수 있으며, 노트북 접근 분리, 탐색과 프로덕션 파이프라인 분리, 데이터 steward 구독 승인과 같은 거버넌스 워크플로우에 적합합니다.

## 상세
단일 SageMaker Unified Studio 프로젝트에는 서로 다른 액세스 요구를 가진 데이터 엔지니어, 데이터 steward, 분석가, 머신러닝 엔지니어가 함께 참여하는 경우가 많습니다. 금융 서비스 사례에서는 엔지니어가 ETL 파이프라인을 구축·스케줄링하고 steward가 구독 요청을 승인하며, 분석가가 대시보드용 정제 테이블을 질의하고 ML 엔지니어가 노트북에서 모델을 반복 개발합니다. Designations 이전에는 비슷한 권한을 모두에게 부여하거나, 액세스 격리를 위해 프로젝트를 페르소나별로 나누는 방식이 흔했습니다. 전자는 프로덕션 워크로드를 끊을 수 있는 연결 삭제 같은 사고를, 후자는 프로젝트 간 데이터 파편화와 프로비저닝 및 구성원 관리 오버헤드를 초래했습니다.

Designations는 정책 정의와 구성원 할당을 분리합니다. 인증은 IAM과 designation의 두 계층으로 동작하므로 레거시 IAM 정책을 다시 작성할 필요 없이 도입할 수 있습니다. 예를 들어 AmazonSageMakerDomainExecution 역할이 에셋 게시를 위한 IAM 권한인 `datazone:CreateListingChangeSet`을 보유하더라도, 구성원의 designation에 자산 게시 권한이 포함되어 있어야 게시가 성공합니다. IAM Deny는 어떤 경우에도 게시를 차단합니다. 따라서 IAM은 AWS API 경계에서 principal을 계속 제한하고, designations는 스튜디오 내에서 IAM 정책을 직접 부여할 수 없는 SSO 사용자 및 그룹을 포함해 모든 principal 유형에 대해 일관된 인증 계층을 추가합니다. 결론적으로 designations는 IAM 제어를 보완하며 모든 사용자 유형에 걸쳐 거버넌스를 균일하게 유지하고, 추가 요금 없이 CloudFormation 기반 자동화까지 지원합니다.

## 참고 자료
- 원문: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/implement-least-privilege-access-with-designations-in-amazon-sagemaker-unified-studio)
