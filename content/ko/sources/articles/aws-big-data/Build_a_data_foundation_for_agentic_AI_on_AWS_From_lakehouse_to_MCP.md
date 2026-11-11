---
title: "Build a data foundation for agentic AI on AWS: From lakehouse to MCP"
description: "AI용 에이전트가 사용할 수 있는 데이터 파이프라인을 구축하기 위한 네 가지 축 프레임워크: 유니피케이드 레이크하우스(Zero-ETL), 컨텍스트 엔지니어링, MCP 및 오픈 프로토콜 간 다중 에이전트 상호작용, 그리고 데이터/에이전트 거버넌스."
tags: [source, aws-big-data, agentic-ai, bedrock, lakehouse, mcp, governance, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp"
blog: aws-big-data
published_date: 2026-11-12
---

# Build a data foundation for agentic AI on AWS: From lakehouse to MCP

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp) · **게시일**: 2026-11-11

## 개요

AI용 에이전트가 사용할 수 있는 데이터 파이프라인을 구축하기 위해 AWS에서 설계된 네 가지 축 프레임워크를 소개합니다.

Gartner는 2027년까지 40% 이상의 에이전트 AI 프로젝트를 실패하여 기대치를 달성하지 못할 것으로 예측하며, 그 근본 원인은 거버넌스 부족과 불일치한 데이터입니다.

이 글은 AWS에서 AI용 데이터 파이프라인을 구축하는 데 필요한 네 가지 축을 설명합니다.

### 축 1: Zero-ETL로 통합된 유니피케이드 레이크하우스 구축

데이터 파이프라인을 직접 관리하지 않고도 시작할 수 있도록 데이터가 저장되는 곳과 어떻게 쿼리되는지를 먼저 설정합니다. Amazon SageMaker Lakehouse는 데이터 레이크와 데이터 웨어하우스의 장점을 결합하며, S3 Tables의 Apache Iceberg 지원으로 데이터를 Spark, Athena, EMR 또는 Redshift에서 읽고 쓰기 가능합니다. 에이전트가 사용할 수 있는 데이터를 하나의 Governance Foundation으로 통합합니다.

에이전트에게 필요한 세 가지 능력은 다음과 같습니다.
- Zero-ETL 수집 (파이프라인 관리 필요 없음)
- Federated Catalog (S3, Redshift, Snowflake, Databricks 전반의 테이블 통일 뷰)
- Query Federation (다중 소스 interrogate 없이 데이터 복제 없이)

AWS Glue Connector는 Amazon Aurora, DynamoDB, RDS, Salesforce, ServiceNow, SAP 등 운영 소스를, 그리고 Amazon MSK, Kinesis 같은 스트리밍 소스를 가져옵니다.

### 축 2: 고성능 에이전트용 컨텍스트 엔지니어링

데이터 레이크만으로는 부족합니다. LLMs는 stateless이며 유한한 컨텍스트 윈도우를 가집니다. Long-context 연구에서 "lost in the middle" 효과가 나타나는데, 프롬프트 시작이나 끝에서 멀리 떨어진 정보가 사실상 무시됩니다. Context Engineering은 지식 베이스, 세션 상태/역사, 데이터 도구로 구성된 맥락 관리자를 통해 이를 해결합니다.

지식 베이스는 Amazon OpenSearch, Aurora PostgreSQL, Neptune 등 벡터 스토어 옵션을 제공하며, Amazon S3 Vectors는 Raw 데이터와 인코딩된 임베딩이 동일하게 관리되는 Lakehouse Foundation에 resides합니다. AgentCore 메모리는 추출 모듈을 통해 키워드(클라이언트 이름, 프로젝트 등)를 원문 이벤트에서 식별하고 장기 저장소에 기록하며, Short-term Memory은raw session history, Long-term Memory은 벡터화된 레코드를 저장합니다.

### 축 3: MCP 및 오픈 프로토콜을 통한 다중 에이전트 상호작용

에이전트가 올바른 컨텍스트를 얻으면 다음 단계가 나옵니다. 두 개의 오픈 프로토콜이 이를 해결합니다. Agent2Agent(A2A)는 에이전트 간 통신을 처리하고, Model Context Protocol(MCP)은 에이전트를 시스템에 연결합니다.

MCP는 Resources, Tools, Prompts를 통해 에이전트가 데이터와 도구를 접근하도록 표준화합니다. Amazon Bedrock AgentCore Gateway가 이 접근을 중앙화하며, IAM 정책에 따라 권한 제한된 관련 도구만 에이전트가 선택할 수 있습니다.

### 축 4: 데이터 및 AI 거버넌스 (신뢰 및 규정 준수)

에이전트가 MCP를 통해 통신하고 작동하기 때문에 사용해야 할 데이터는 신뢰할 수 있어야 합니다. Foundation 모델(FMs)이 널리 공개되어 있으므로 데이터 관리 방식이 에이전트를 구분짓습니다. Amazon SageMaker Data Catalog은 발견, 거버넌스, 협업 기능을 제공하며, 데이터셋마다 자동으로 요약, 용어집, 데이터 선형성, 품질 지표를 생성합니다. Publish-and-subscribe 모델을 따릅니다.

## 핵심 내용

- 네 축이 AI용 데이터 파이프라인을 구축하는 기초입니다: 유니피케이드 레이크하우스(Zero-ETL), 컨텍스트 엔지니어링, MCP/오픈 프로토콜 간 다중 에이전트 상호작용, 데이터/AI 거버넌스.
- Gartner: 2027년까지 40% 이상의 에이전트 AI 프로젝트를 실패할 것으로 예측; 거버넌스 부족과 불일치한 데이터가 근본 원인.
- Zero-ETL 수집으로 파이프라인 관리를 제거; Federated Catalog + Query Federation으로 다중 소스 데이터 통합.
- 컨텍스트 엔지니어링은 lost-in-the-middle(Liu et al., 2023)을 해결하며, 지식 베이스, 세션 메모리, 데이터 도구로 구성.
- A2A는 에이전트 간 HTTP/JSON 기반 대화; MCP는 에이전트와 시스템의 도구 접근을 표준화.
- SageMaker Data Catalog은 발견, 거버넌스, 협업을 제공하며, 자동으로 요약, 용어집, 데이터 선형성, 품질 지표 생성.

## 상세

Lakehouse는 데이터 레이크와 데이터 웨어하우스의 장점을 결합하며, S3 Tables의 Apache Iceberg 지원으로 Spark, Athena, EMR 또는 Redshift에서 읽고 쓰기 가능합니다. Context engineering에는 Amazon OpenSearch, Aurora PostgreSQL, Neptune, S3 Vectors 등 벡터 스토어 옵션과 AgentCore 메모리가 포함됩니다. MCP는 Agent2Agent와 MCP를 통해 에이전트 간 및 시스템과의 통신을 가능하게 합니다. SageMaker Data Catalog은 데이터 발견, 거버넌스, 협업을 제공하며, 생성된 데이터 마스터는 자동으로 요약, 용어, lineage, 품질 지표를 생성합니다. SageMaker Unified Studio는 생성형 AI 어시스턴트를 제공하여 자연어 요청을 SQL/Python/시각화 셀로 변환합니다.

전체 기술 워크숍은 AWS Summit Paris 녹음 영상에서 확인할 수 있습니다.

## 참고 자료

- 원문: [Build a data foundation for agentic AI on AWS: From lakehouse to MCP](https://aws.amazon.com/blogs/big-data/build-a-data-foundation-for-agentic-ai-on-aws-from-lakehouse-to-mcp)
