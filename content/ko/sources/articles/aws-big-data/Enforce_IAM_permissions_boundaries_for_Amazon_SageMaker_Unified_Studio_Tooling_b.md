---
title: "SageMaker Unified Studio Tooling 블루프린트에 IAM 권한 경계 적용"
description: "Tooling 블루프린트 역할에 커스텀 권한 경계를 붙여 SCP 거버넌스 계정에서도 SageMaker Unified Studio를 도입합니다." (한국어 번역)
tags: [source, aws-big-data, sagemaker, iam, security, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/enforce-iam-permissions-boundaries-for-amazon-sagemaker-unified-studio-tooling-blueprints"
blog: aws-big-data
published_date: 2026-09-28
---

# SageMaker Unified Studio Tooling 블루프린트에 IAM 권한 경계 적용

## 개요

SageMaker Unified Studio가 Tooling 블루프린트(모든 프로젝트에 필수 배포되는 블루프린트)가 만드는 IAM 역할에 커스텀 권한 경계를 지원합니다. 모든 역할에 경계를 강제하는 SCP를 쓰는 규제 조직에서는 기존에 프로젝트 생성이 `iam:CreateRole` 명시적 거부로 실패했습니다. `PermissionsBoundaryArn` 파라미터 하나로 보안 상태를 해치지 않고 도입이 가능해지며, 데이터 에이전트·노트북 기능만 끄고 SQL 접근은 유지하는 식의 세밀한 제어도 할 수 있습니다.

## 동작 방식

경계는 Tooling 블루프린트의 리전 파라미터에 설정합니다. 이후 해당 블루프린트의 신규 프로젝트는 CloudFormation 스택으로 세 IAM 역할 — 프로젝트 멤버가 맡는 `datazone_usr_role`, Bedrock용 `AmazonBedrockServiceRole`, Bedrock Lambda용 `AmazonBedrockLambdaExecutionRole` — 을 만들 때 각각 경계를 붙입니다. 세 역할에 일괄 적용되고 향후 프로젝트에만 적용되며, 기존 프로젝트는 원래 경계를 유지합니다. 글의 예시 경계는 스튜디오가 쓰는 서비스 네임스페이스를 허용하면서 DataZone 노트북/셀/대화와 에이전트 메시징 액션을 명시적 거부로 막아, 어떤 역할 정책으로도 우회할 수 없는 상한선 역할을 합니다. 어디까지나 예시이므로 비프로덕션 도메인에서 검증해야 합니다. 경계는 세 역할이 실제로 필요로 하는 모든 권한의 상위집합이어야 합니다.

## 경계 구성

- **선택적 SCP:** Organizations 관리 계정에서 승인된 경계 ARN 없이는 `CreateRole`·`PutRolePermissionsBoundary`를 거부하고, 경계 제거를 거부하며, 경계 정책 자체를 보호하는 SCP를 만들고(스스로 잠그지 않도록 브레이크글래스 예외 포함), 대상 OU·계정에 연결합니다.
- **경계 정책 생성** (`SMUSToolingBoundary`) 후 ARN을 기록합니다.
- **ID 확인:** DataZone 목록 API로 도메인 ID와 관리형 Tooling 블루프린트 ID를 찾습니다.
- **백업 후 읽기:** 현재 블루프린트 구성을 백업합니다. `put-environment-blueprint-configuration`은 전체 덮어쓰기이므로 기존 값을 모두 다시 넣고 리전 파라미터에 `PermissionsBoundaryArn`만 추가합니다.
- **검증:** 구성에서 ARN이 읽히는지 확인합니다.

## 검증과 운영

활성화된 프로젝트 프로필로 테스트 프로젝트를 만들어 Active 상태가 될 때까지 기다린 뒤, CloudFormation에서 Tooling 스택의 IAM 역할을 나열하고 `get-role`로 각 역할에 경계가 붙었는지 확인합니다(IAM 콘솔에서도 확인 가능). 예시 거부 정책을 쓰면 노트북 생성이 `datazone:CreateNotebook`에서 실패하고 쿼리 편집기의 에이전트 패널이 Data Agent 접근 불가로 표시되어 경계가 동작함을 알 수 있습니다. 유의점: 경계는 프로젝트 생성 후 불변, 기능은 Tooling 블루프린트 전용(다른 블루프린트는 커스텀 블루프린트로 확장), 정책이 프로비저닝 전에 존재해야 합니다. 테스트 자원 정리는 프로젝트 삭제 후 백업값으로 경계 필드 없이 구성을 다시 적용하면 됩니다.

## References

- 원문: [Enforce IAM permissions boundaries for Amazon SageMaker Unified Studio Tooling blueprints](https://aws.amazon.com/blogs/big-data/enforce-iam-permissions-boundaries-for-amazon-sagemaker-unified-studio-tooling-blueprints)
