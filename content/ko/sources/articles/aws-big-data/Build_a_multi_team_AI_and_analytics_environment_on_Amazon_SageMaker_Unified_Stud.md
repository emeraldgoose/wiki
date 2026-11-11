---
title: "Amazon SageMaker 유니파이드 스튜디오로 멀티팀 AI 및 분석 환경 구축하기"
description: "Terraform으로 Amazon SageMaker Unified Studio 도메인을 생성하고 팀별 프로젝트 프로필을 구성하는 방법."
tags: [source, aws-big-data, terraform, sage-maker, unified-studio, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform"
blog: aws-big-data
published_date: 2026-11-12
---

# Amazon SageMaker 유니파이드 스튜디오로 멀티팀 AI 및 분석 환경 구축하기

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform) · **게시일**: 2026-11-11

## 개요

플랫폼 엔지니어는 데이터 및 AI 팀을 지원하는 과정에서 반복적으로 발생하는 어려움을 겪습니다. 각 팀이 자체 툴과 인프라를 운영하면 거버넌스가 분산되고 조직은 중복된 노력과 제한된 협업을 경험하게 됩니다. 데이터 엔지니어, 데이터 사이언티스트, AI 개발자는 동일한 기본 데이터를 사용하더라도 별도 콘솔을 관리하고 고유한 IAM 설정을 유지하며 다른 팀의 작업 현황을 공유할 수 없는 상황입니다. Amazon SageMaker Unified Studio는 이러한 기능을 하나의 거버넌스된 워크스페이스에 통합합니다. 모든 실무자는 필요한 도구에 액세스할 수 있습니다: SQL 편집기, JupyterLab 노트북, Amazon Bedrock IDE입니다. 동시에 공통 비즈니스 데이터 카탈로그, 보안 모델, 프로젝트 구조를 공유하며, 중앙에서 거버넌스가 관리됩니다. 팀은 프로젝트 내에서 협업하고 데이터, 계산 리소스, 개발 아티팩트에 대한 액세스는 중앙에서 관리됩니다.

SageMaker Unified Studio에서 이러한 멀티팀 환경을 구성하려면 IAM 역할, 블루프린트, 프로젝트 프로파일, 그리고 사용자 온보딩을 조율해야 합니다. 새로운 역할이나 용도는 도메인에 새로운 블루프린트를 결합하여 새로운 프로젝트 프로파일을 생성하여 지원하도록 확장할 수 있습니다. 멀티테넌시가 보장되도록 Terraform 모듈은 각 팀에 하나의 프로젝트 프로파일을 생성하고, 도메인은 공유 리소스와 네트워크 설정을 제공합니다.

## 핵심 내용

- 다중 공급자: AWS provider와 AWS Cloud Control (AWSCC) provider를 모두 사용하여 Amazon SageMaker Unified Studio의 전체 리소스 커버리지 확보
- 서비스 역할 유연성: 모든 IAM role는 최소 권한 정책으로 자동 생성되며, 기존 role을 사용하도록 지정할 수도 있음
- 도메인과 프로젝트 수준 액세스: IAM과 SSO(IAM Identity Center)를 사용하거나 둘 다 사용 가능
- KMS 암호화: 도메인 메타데이터를 고객 관리형 AWS KMS key로 선택적으로 암호화
- 모델 거버넌스: 도메인이 자동으로 생성한 모델 거버넌스 프로젝트를 통해 Generative AI 관리자가 모델을 사용하거나 사용 중지 가능
- Terraform이 Amazon SageMaker Unified Studio 도메인을 공유 IAM role 및 네트워크와 함께 생성
- 모든 필요한 블루프린트를 도메인에 사용 설정 (DataLake, Redshift Serverless, Bedrock 서비스, EMR 등)
- SQL 분석, 생성형 AI, 모든 기능을 갖춘 세 가지 프로젝트 프로파일 생성 (팀별)
- 초기 terraform apply는 첫 번째 사용 가능한 프로파일에서 프로젝트 생성
- 프로젝트 멤버(SSO 사용자, SSO 그룹, IAM role 또는 IAM 사용자)는 소유자 또는 기여자로 할당

## 상세

Terraform 모듈은 네 개의 레이어로 구성됩니다.

1. **도메인 모듈**: 도메인 생성, 툴 블루프린트, IAM role, S3 버킷 생성
2. **블루프린트 모듈**: for_each를 사용하여 도메인에 블루프린트 사용 설정
3. **프로젝트 프로파일 모듈**: 블루프린트를 팀별 프로파일로 구성
4. **프로젝트 및 프로젝트 멤버 모듈**: 프로젝트 생성 및 멤버 할당

도메인 포털 URL은 teams와 공유되며, 사용자는 principal을 통해 바로 로그인할 수 있습니다. 초기 terraform apply는 하나의 프로젝트를 생성하며, 추가 프로젝트는 project sub-module을 참조하여 다른 프로파일에서 생성할 수 있습니다. 멤버는 SSO 사용자, SSO 그룹, IAM role, IAM 사용자いずれ可以 be added as owner or contributor.

각 팀은 자신 할당된 프로젝트 프로파일에 정의된 기능만 사용할 수 있으며, 이는 팀 고립을 보장하면서도 공유 데이터 카탈로그와 리소스를 이용하게 합니다.

## 참고 자료

- 원문: [Build a multi-team AI and analytics environment on Amazon SageMaker Unified Studio with Terraform](https://aws.amazon.com/blogs/big-data/build-a-multi-team-ai-and-analytics-environment-on-amazon-sagemaker-unified-studio-with-terraform)