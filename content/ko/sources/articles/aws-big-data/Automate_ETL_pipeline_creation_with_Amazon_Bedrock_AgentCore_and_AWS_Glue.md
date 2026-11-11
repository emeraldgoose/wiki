---
title: "Amazon Bedrock AgentCore와 AWS Glue를 활용한 ETL 파이프라인 자동화"
description: "AI 기반으로 ETL 파이프라인 설정을 자동화하여 소스 분석, 스키마 매핑, 코드 생성, 테스트 및 AWS Glue 작업 배포를 자동화합니다. 승인 게이트와 품질 검사 기능이 포함되어 있습니다."
tags: [source, aws-big-data, bedrock, agentcore, glue, automation, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue"
blog: aws-big-data
published_date: 2026-11-12
---

# Amazon Bedrock AgentCore와 AWS Glue를 활용한 ETL 파이프라인 자동화

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue) · **게시일**: 2026-11-11

## 개요

ETL 파이프라인 구축 및 유지관리는 시간이 많이 소요되는 작업입니다. 데이터 엔지니어는 필드 매핑, PySpark 코드 작성, 스키마 변경에 따른 재작업을 반복하면서 많은 시간을 소비합니다. Agentic Data Ingestion은 AI를 활용해 이 과정을 자동화합니다. 소스 파일이나 데이터베이스 테이블에 점을 찍으면, 파운데이션 모델(FMs)이 필드 매핑을 제안하고 변환 코드를 작성합니다. 에이전트는 생성된 코드를 Apache Spark에서 테스트한 후 AWS Glue 작업을 배포합니다. 중요한 단계에서는 승인 게이트가 워크플로우를 일시 중단시켜 인간 검토를 기다립니다.

전체 파이프라인은 AWS 관리 서비스에서 실행됩니다. AWS Bedrock은 파운데이션 모델을 제공하고, Amazon Bedrock AgentCore는 Strands Agents SDK로 구축된 AI 에이전트를 호스팅합니다. AWS Step Functions는 10단계 워크플로우를 오케스트레이션하고, AWS Glue는 생성된 데이터 통합 작업을 실행합니다. 솔루션은 AWS Cloud Development Kit (CDK)로 배포됩니다. 시작 전에 사전 조건을 검토하세요.

## 핵심 내용

- 솔루션 아키텍처는 데이터 소스 로그인부터 에이전트 오케스트레이션, Step Functions 워크플로우, AWS Glue 작업 배포까지 이어지며, Amazon S3 Table, Amazon S3 또는 관계형 데이터베이스와 같은 대상을 연결합니다. 상호작용식 React 대시보드는 각 실행의 진행 상황과 승인 상태를 보여줍니다. 사용자가 Amazon S3에 소스 파일을 업로드하면, EventBridge와 SQS를 통해 Lambda 트리거가 10단계 Step Functions 워크플로우를 시작합니다.
- 워크플로우에는 두 개의 명시적 승인 게이트가 있습니다: 스키마 매핑 후(신뢰 점수가阈值 이하이거나 필드 이름이 일치하지 않을 때)와 코드 테스트 후. 매핑은 모든 필드 쌍이 높은 신뢰도와 이름 매칭을 확인할 때만 검토를 건너뛰며, 다른 경우는 기본적으로 검토를 요구합니다.
- 코드 생성에서는 FM이 전체 Glue 스크립트(500줄 이상) 대신 변환 블록(일반적으로 5~15줄)만 작성합니다. 대상 유형별로 인간 작성된 Jinja2 템플릿이 스캐폴드 역할을 하며, 생성된 코드는 배포 전 허용된 구성 요소 목록에 맞는지 검사됩니다.
- 테스트는 AWS Glue 인터랙티브 세션에서 대상 작업과 동일한 Spark 버전으로 100행 샘플 소스에 대해 실행되며, 기록 수, null 값, 스키마 합격을 확인합니다. 데이터베이스 소스는 데이터베이스에 직접 액세스할 수 없으므로 스키마 생성 행을 기반으로 테스트합니다.
- 테스트 실패 시 워크플로우는 더 큰 워커 또는 재생성된 코드로 재시도할 수 있습니다. 자체 치유 에이전트는 스키마/타입 오류 또는 메모리 초과 조건 후 한 번의 새로운 실행 시도를 시도하지만, 데이터 중복이 발생할 수 있거나 오류가 복구 불가능할 경우(예: 권한 문제) 재시도를 건너뛰고 실패 상태를 유지합니다. 에이전트의 진단은 상세 페이지에 표시됩니다. 72시간 이내에 게이트에서 대기하면 실패 처리됩니다. 승인과 거부는 리뷰어의 신원이 기록됩니다.
- 워크플로우가 게이트에서 72시간 이상 대기하면 실패 처리됩니다.
- 고객 사례: Montai Therapeutics는 동일한 패턴을 과학 데이터에 적용합니다. 기존 인증 앱에 파서 생성 에이전트를 내장함으로써 새로운 테스트의 파서 생성 및 출력 확인에 5~10분으로 리드 타임이 단축되었고, 이전에는 하루 또는 주 단위가 소요되었습니다. 가장 큰 비즈니스 영향은 실험 데이터가 인바운드로 유입되는 비율이 증가하여 약물 특이성과 효과 예측 모델을 개선하는 데 기여한 것입니다.

## 상세

고객 로그인은 Amazon Cognito를 통해 MFA가 필요하도록 설정되며, 대시보드는 CloudFront를 통해 WAF 웹 ACL(관리 규칙 + rate limit)과 두 번째 WAF ACL(CloudFront를 통한 API 요청용)을 통해 제공됩니다. 기본적으로 로그인한 사용자는 대시보드에 완전 액세스하며, 솔루션에는 신원 연동 또는 역할 기반 액세스가 포함되지 않으며, README의 "실제 데이터 강화" 섹션에서는 향후 추가로 목록화됩니다.

사용량 비용은 약 15~20달러/월(약 14달러는 두 개의 WAF 웹 ACL 및 규칙, 최대 5달러 CloudWatch 모니터링, 나머지 스토리지 및 단일 비밀)입니다. 샘플 규모 실행 비용은 약 0.10~0.25달러이며, AI 비용은 행이 아닌 필드 수에 따라 결정됩니다. 워크플로우가 스키마가 변경되지 않은 경우 매핑 호출을 건너뛰며, 현재 가격은 Amazon Bedrock, AWS Glue, Amazon Bedrock AgentCore 및 AWS WAF 가격 페이지에서 확인할 수 있습니다.

IAM 역할은 단일 파이프라인에 스코프화되고, 권한 경계를 통해 제한되며, 에이전트 런타임에 별도 역할을 할당합니다. 데이터는 정지 시 및 전송 시 암호화되며, JDBC 자격 증명은 Secrets Manager ARN을 통해 참조되어 작업 인수에 절대 포함되지 않습니다.

테스트 세션은 100행 소스 샘플에 대해 실행되며, 기록 수, null 값, 스키마 합격을 확인합니다. 데이터베이스 소스는 테스트 세션에서 직접 데이터베이스에 액세스할 수 없으므로 스키마 생성 행을 기반으로 테스트합니다. 데이터 품질 규칙은 Glue Data Quality의 기본 설정으로, 파일 업로드 시 Amazon S3 Table(아마존 S3 테이블)에 대해 자동으로 적용되고, 실패한 행은 작업 전 격리됩니다.

결과는 CloudFront를 통해 WAF 보호 기능을 갖춘 CloudFront를 통해 시각화됩니다. 솔루션은 확장 가능하며, "실제 데이터 강화" 섹션에서는 신원 연동 및 역할 기반 액세스가 향후 추가로 계획되어 있습니다. 두 개의 에이전트가 복잡한 매핑과 실패 후 자동 복구를 처리합니다.

## 참고 자료

- 원문: [Automate ETL pipeline creation with Amazon Bedrock AgentCore and AWS Glue](https://aws.amazon.com/blogs/big-data/automate-etl-pipeline-creation-with-amazon-bedrock-agentcore-and-aws-glue)