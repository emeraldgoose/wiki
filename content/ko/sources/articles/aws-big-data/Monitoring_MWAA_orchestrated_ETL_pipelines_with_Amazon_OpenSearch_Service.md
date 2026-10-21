---
title: "Amazon OpenSearch Service로 MWAA 기반 ETL 파이프라인 모니터링하기"
description: "CloudWatch 구독 필터로 MWAA, Glue, EC2 로그를 OpenSearch에 실시간 수집하고 Bedrock 기반 MCP 서버로 자연어 질의·장애 원인 분석."
published: "2026-10-06"
source_url: "https://aws.amazon.com/blogs/big-data/monitoring-mwaa-orchestrated-etl-pipelines-with-amazon-opensearch-service"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, mwaa, opensearch, ko, ko]
---

# Amazon OpenSearch Service로 MWAA 기반 ETL 파이프라인 모니터링하기

## 개요

MWAA가 Glue 잡, EC2 스크립트, Airflow DAG에 걸친 파이프라인을 조율하면, 컴포넌트마다 CloudWatch 로그 그룹이 따로 있어 새벽 장애 triage가 도구를 넘나드는 탐색 작업이 된다. 이 솔루션은 모든 로그를 Amazon OpenSearch Service에 실시간으로 모아 AI 에이전트를 앞단에 둔다. 엔지니어는 자연어로 실패 원인을 묻고, 원인 분석과 해결 제안을 받아 평균 해결 시간을 줄인다.

## 아키텍처

MWAA(프로비저닝·서버리스)가 파이프라인을 조율하고, Glue 잡과 EC2 파이썬 스크립트는 각각 기본 로그 설정과 통합 CloudWatch 에이전트로 CloudWatch에 로그를 남긴다. 각 로그 그룹의 구독 필터가 Lambda를 거쳐 이벤트를 압축 해제·보강해 소스별 인덱스와 통합 ETL 인덱스에 대량 색인한다. OpenSearch 안에서는 ML Connector가 Bedrock의 Claude를 호출해 의미를 파악하고, Bedrock AgentCore 위의 OpenSearch MCP 서버가 인덱스 탐색·검색 도구를 AI 어시스턴트에 노출하므로 DSL을 직접 쓸 필요가 없다.

## 배포

세 CloudFormation 스택을 순서대로 배포한다. `opensearch-cfn`(도메인, SageMaker AI 노트북, IAM 역할), `etl`(VPC, MWAA 환경, Glue 잡, EC2, 스트리밍 파이프라인), `agentcore-mcp-server`(Cognito 인증 포함 Bedrock AgentCore MCP 런타임) 순이다. 이후 노트북에서 자격 증명 연결, Lambda 기반 구독 필터 생성, 데모 DAG 실행(플래그로 프로비저닝·서버리스 선택), OpenSearch에 Claude 커넥터 등록, ETL 분석 에이전트 기동(로컬 또는 AgentCore)을 수행한다.

## 활용과 확장

로그가 흐르기 시작하면 "ERROR 로그 보여줘", "새벽 3시 Glue 잡이 왜 실패했어" 같은 질문에 소스를 넘나드는 상관 분석으로 답한다. SNS 알림 연동, 구독 필터 추가로 로그 소스 확장, 오류율·실행 지연 대시보드, 인덱스 매핑 반영 프롬프트 튜닝이 자연스러운 확장 방향이다. 정리는 스택 삭제면 된다.

## 참고 자료

- [원문: Monitoring MWAA-orchestrated ETL pipelines with Amazon OpenSearch Service](https://aws.amazon.com/blogs/big-data/monitoring-mwaa-orchestrated-etl-pipelines-with-amazon-opensearch-service)
- [샘플 코드: sample-etl-troubleshooting-using-genai](https://github.com/aws-samples/sample-etl-troubleshooting-using-genai)
