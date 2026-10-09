---
title: "모든 팀은 데이터 팀입니다 — Amazon Redshift 분석 기능을 ChatGPT Work로 가져오세요"
description: "AWS Data Analytics 플러그인을 사용하여 ChatGPT Work에서 Amazon Redshift 데이터에 대한 자연어 질의 및 대시보드 생성을 구현하는 방법을 알아봅니다."
source_url: "https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/"
blog: "AWS Big Data"
published: 2026-09-10
locale: "ko"
---

# 모든 팀은 데이터 팀입니다 — Amazon Redshift 분석 기능을 ChatGPT Work로 가져오세요

데이터 기반의 의사 결정은 종종 SQL이라는 기술적 장벽에 가로막히곤 합니다. 분석가와 엔지니어는 데이터 웨어하우스를 쉽게 쿼리할 수 있지만, 영업, 운영, 재무와 같은 비즈니스 리더들은 사전에 만들어진 보고서에 의존해야 하므로 병목 현상이 발생합니다. AWS는 **ChatGPT Work**의 **Data agent**를 위한 새로운 **AWS Data Analytics 플러그인**을 통해 이 간극을 메우고 있습니다.

이 플러그인을 통해 권한이 있는 모든 팀원은 자연어로 질문을 하고, Amazon Redshift 및 데이터 레이크의 관리되는 데이터를 분석하며, 공유 가능한 대시보드를 생성할 수 있습니다. 이 모든 과정은 ChatGPT Work의 대화형 인터페이스 내에서 이루어집니다.

[English Version](/en/sources/articles/aws-big-data/Every_team_is_a_data_team_bring_Amazon_Redshift_analytics_to_ChatGPT_Work)

## 개념: 데이터 접근의 민주화

핵심 개념은 **데이터 민주화(Data Democratization)**입니다. 즉, 데이터를 전문가만이 다룰 수 있는 특수 자원으로 보는 모델에서, 모든 역할의 사용자가 쉽게 사용할 수 있는 유틸리티로 보는 모델로 전환하는 것입니다.

- **전통적 모델**: 분석가가 SQL 작성 $\rightarrow$ 데이터 추출 $\rightarrow$ 비즈니스 팀에 보고서 전달.
- **대화형 모델**: 비즈니스 사용자가 자연어로 질문 $\rightarrow$ 에이전트가 SQL로 변환 $\rightarrow$ 즉시 데이터 분석 및 시각화.

## 출처

- **제목**: Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work
- **블로그**: AWS Big Data
- **URL**: [https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/](https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/)
- **날짜**: 2026-09-10

## 가이드: 플러그인 작동 방식

AWS Data Analytics 플러그인은 대화형 LLM과 Amazon Redshift의 구조화된 데이터 환경 사이를 연결하는 지능적인 브리지 역할을 합니다.

### 1. 핵심 기능

플러그인 기반의 Data agent는 다음과 같은 중요한 작업을 수행합니다:
- **메타데이터 검색**: 사용자에게 허용된 스키마, 테이블, 컬럼 및 데이터 유형을 자동으로 식별합니다.
- **자연어-SQL 변환 (NL-to-SQL)**: 자연어 질문을 최적화된 Amazon Redshift SQL로 변환합니다.
- **쿼리 실행**: 생성된 SQL을 사용자의 기존 Redshift 환경에서 실행합니다.
- **대화형 드릴다운 (Drill-down)**: 채팅 세션의 문맥을 유지하여 사용자가 추가 질문(예: "이 지역의 매출이 왜 감소했나요?")을 통해 분석을 심화할 수 있도록 합니다.
- **시각화**: 표 형태의 결과를 인터랙티브하고 공유 가능한 대시보드로 변환합니다.

### 2. 보안 및 거버넌스

엔터프라이즈 데이터에서 가장 중요한 것은 기존의 보안 정책을 유지하는 것입니다.
- **액세스 제어**: 플러그인은 사용자의 기존 **IAM 및 Redshift 액세스 제어**를 준수합니다. 사용자가 특정 테이블을 볼 권한이 없다면, 에이전트도 해당 데이터에 접근할 수 없습니다.
- **관리되는 데이터셋**: 분석 팀이 이미 정의한 정제된 데이터셋과 비즈니스 정의를 그대로 사용하므로, 조직 전체에서 "매출" 등의 지표가 일관되게 정의되도록 보장합니다.

### 3. 기반 기술: Agent Toolkit for AWS

플러그인의 지능은 **Agent Toolkit for AWS**의 **Amazon Redshift skills**를 기반으로 구축되었습니다. 이 스킬들은 에이전트에게 다음과 같은 기능을 제공합니다:
- 메타데이터 탐색을 위한 검증된 서비스별 프로시저.
- 복잡한 다중 조인 SQL 쿼리 생성을 위한 검증된 워크플로우.
- Redshift 전용 기능과 상호작용하기 위한 가이드라인.

## 소프트웨어 엔지니어를 위한 요약

- **통합**: Amazon Redshift 프로비전드 클러스터와 서버리스 워크그룹을 모두 지원합니다.
- **확장성**: Redshift 외에도 AWS Glue Data Catalog, Amazon S3 Tables, Amazon Athena 및 벡터 검색과의 연동을 지원합니다.
- **영향**: 비기술직 이해관계자의 "통찰력 도달 시간(time-to-insight)"을 단축하는 동시에, 분석가들이 더 가치 있는 모델링 및 아키텍처 작업에 집중할 수 있도록 돕습니다.

## 참고 문헌
- [ChatGPT Work Data agent](https://chatgpt.com/plugins/Plugin_fc9843a6fb34819195d6c7802398a8a7)
- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [Amazon Redshift Documentation](https://docs.aws.amazon.com/redshift/)
