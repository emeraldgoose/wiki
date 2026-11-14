---
title: "OpenAI와 Databricks: 거버넌스된 기업 데이터 위의 엔터프라이즈 AI"
description: "OpenAI와 Databricks의 파트너십은 2025년 9월에 시작된 다년간 계약으로, OpenAI의 프런티어 모델과 Databricks의 거버넌스 데이터·컨텍스트를 연결한다. 글은 ChatGPT의 Genie 플러그인, Unity Gateway를 통한 Codex, Model Serving과 Databricks Apps의 GPT 모델이라는 세 가지 도입 패턴을 소개하고 통합 아키텍처와 추가 통합 목록을 정리한다."
tags: [source, databricks, openai, genie, unity-gateway, ko]
locale: ko
source_url: "https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data"
blog: databricks
published_date: 2026-11-14
---

# OpenAI와 Databricks: 거버넌스된 기업 데이터 위의 엔터프라이즈 AI

**원문**: [Databricks 블로그](https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data) · **게시일**: 2026년 11월 13일

## 개요

OpenAI 공동창업자이자 사장인 그렉 브록맨은 회사 데이터 없이 굴러가는 AI를 한 줄로 요약했다. 박사 학위자 20명을 고용해 놓고 정작 회의에 한 번도 부르지 않는 것이라고. OpenAI와 Databricks의 파트너십은 바로 이 지점을 고치기 위해 만들어졌다. OpenAI는 사람들이 매일 쓰는 프런티어 모델, Codex, ChatGPT를 제공하고, Databricks는 그 도구들이 회사 안에서 동작하는 데 필요한 컨텍스트, 즉 거버넌스된 데이터와 비즈니스 정의, 접근 규칙을 제공한다. 글은 Genie Ontology를 그 정의를 담는 컨텍스트 계층으로 짚으며, Genie를 쓰는 ChatGPT가 일을 시작하기 전에 그 회사에서 "매출"이나 "활성 고객"이 무엇을 뜻하는지 알게 된다고 설명한다.

글은 기업 도입을 세 가지 패턴으로 정리한다. ChatGPT와 Genie 플러그인으로 비즈니스 사용자의 업무를 가속하는 것, Codex와 Unity Gateway로 거버넌스를 갖춘 코딩을 하는 것, 그리고 GPT 모델, Model Serving, Databricks Apps로 비즈니스 프로세스를 바꾸는 사용자 지정 에이전트다. 그 뒤에는 2025년 9월에 시작된 다년간 계약이 있고, 두 회사는 서로의 고객이다.

이번 발표에는 챗봇에서 자율 에이전트로의 전환을 다룬 Databricks 공동창업자 겸 CEO 알리 곳시와 브록맨의 대화 영상이 함께했다. Databricks는 앞으로 몇 주간 패턴별 후속 글에 아키텍처 세부 사항, 설정 절차, 고객 교훈을 담아 연재하겠다고 예고한다.

## 핵심 내용

- Genie 플러그인을 쓰면 임직원이 ChatGPT에서 데이터 질문을 직접 던진다. 예컨대 플랜 등급별로 주간 활성 사용자 도입이 목표 대비 어떤지 묻는 식이다. Genie가 지표 정의를 이해하고 관련 데이터를 찾아 Databricks에서 쿼리를 실행한 뒤 그래프와 차트로 돌려준다.
- 플러그인은 Genie MCP 위에서 동작하며, Genie는 Genie Ontology에 담긴 회사의 승인된 지표와 정의를 적용한다. 그래서 ChatGPT 안의 매출이 재무 보고서의 매출과 일치한다.
- 사용자는 이미 권한이 있는 데이터만 보고, 각 답변은 Databricks 안의 출처로 연결된다.
- ChatGPT Work는 다음 단계와 관련 담당자를 추천하고, 슬랙이나 이메일로 결과를 공유하며, 사용자가 승인한 작업을 연결된 도구로 실행한다.
- Codex는 Databricks 자격 증명으로 로그인하고 OpenAI 키는 Unity Gateway 안에 머문다. 모든 요청이 기록되며 엔지니어링 리더는 예산을 걸고 팀별 지출을 검토하고 어떤 작업에 어떤 GPT 모델을 쓸지 고른다.
- 두 번째 패턴의 시작은 짧다. Unity Gateway CLI를 설치하고 ug codex를 실행하면 된다.
- Databricks에서는 OpenAI 프런티어 모델이 Unity Catalog 거버넌스 아래 데이터 바로 옆에서 구동된다. Databricks가 모델을 서빙하면 관리할 외부 API 키가 없다.
- 팀은 Agent Bricks에서 에이전트를 만들고 평가하거나, OpenAI Agents SDK로 작성해 워크스페이스 템플릿으로 Databricks Apps에 배포할 수 있다.
- 파트너십은 2025년 9월 시작된 다년간 계약이며 상호적이다. OpenAI는 Databricks의 최대 고객 중 하나이고, Databricks의 모든 엔지니어에게 Codex 접근권이 제공된다.
- Databricks는 새 OpenAI 모델에 조기 접근하고, OpenAI 모델은 실제 문서 작업 벤치마크인 Databricks의 OfficeQA에서 선두다.
- Model Serving은 회사 데이터 옆에서 GPT 모델을 구동해 SQL, 노트북, 에이전트에서 호출하게 하고, 관리형 Postgres 데이터베이스인 Lakebase는 에이전트의 메모리와 상태를 보관한다.
- 사용 가능한 모델에는 GPT-6 계열과 오픈 웨이트 모델 gpt-oss가 있으며 SQL, 노트북, 에이전트에서 호출할 수 있다.

## 세부 사항

### 패턴 1: ChatGPT와 Genie 플러그인

예전에는 숫자가 필요한 임직원이 SQL을 못 쓰면 분석가를 불러야 했고, 회사 정의를 모르는 AI 도구에 데이터를 붙여 넣어야 했다. 분석가를 기다리는 동안 결정은 늦어졌고, 엉터리 정의 위에 세운 답은 엉터리 결정으로 이어졌다. 이제 제품 관리자가 ChatGPT에 직접 묻는다. Genie가 승인된 지표 정의를 읽고 관련 데이터를 찾아 Databricks에서 쿼리를 돌린 뒤 그래프로 답한다. 시작 절차도 일부러 가볍게 설계됐다. 플러그인을 설치하고, Databricks 관리자가 Genie를 켜면, 각 사용자는 자신이 볼 수 있는 데이터만 보며 ChatGPT에 연결한다.

### 패턴 2: Unity Gateway를 통한 Codex

AI 코딩 에이전트는 보통 한 팀씩 퍼지고, 리더는 누가 쓰는지, 비용이 얼마인지, 코드와 데이터가 어디로 가는지 놓치기 쉽다. Unity Gateway는 이 확산을 통제하면서 전사 배포를 가능하게 하는 경로로 제시된다. 개발자는 오늘처럼 Codex를 쓰고, 로그인은 Databricks 자격 증명이며, OpenAI 키는 게이트웨이를 떠나지 않고 모든 요청이 기록된다. 주변 통합도 있다. Codex용 Neon 플러그인은 Codex 안에서 Neon 서버리스 Postgres 프로젝트를 만들고 SQL을 실행하며 마이그레이션을 관리하고, Databricks Agent Skills는 Databricks CLI와 SDK를 다루도록 Codex를 가르치는 공식 지침서다.

### 패턴 3: Model Serving과 Databricks Apps의 GPT 모델

핵심 비즈니스 프로세스를 바꿀 수 있는 에이전트는 필요한 데이터가 엄격한 보안과 거버넌스 규칙 뒤에 있어 출시 전에 좌초하곤 한다. Databricks에서는 프런티어 모델이 Unity Catalog 거버넌스 아래 그 데이터 바로 옆에서 구동된다. Agent Bricks가 에이전트 구축과 평가를 담당하고, OpenAI Agents SDK 경로는 워크스페이스의 에이전트 템플릿으로 Databricks Apps에 배포된다. Databricks Model Serving이 GPT 모델을 호스팅하므로 SQL, 노트북, 에이전트 어디서든 별도 API 키 없이 호출한다.

### 통합 지도 전체

두 플러그인이 그림을 완성한다. Codex Data Science 플러그인은 Codex 데이터 과학 워크플로를 레이크하우스 위에서 돌리고, ChatGPT Data Analyst 플러그인은 Genie로 연결된 데이터 위에서 ChatGPT 안에서 대시보드를 만들고 편집한다. 원클릭 ChatGPT 연결은 관리자 설정 없이 ChatGPT를 Databricks에 연결하며 각 사용자의 기존 권한을 그대로 적용한다. 모든 패턴에서 같은 Unity Catalog 권한과 Unity Gateway 비용 통제가 적용되며, Databricks는 이미 ChatGPT와 Codex에 살고 있는 팀에게 Genie 플러그인과 Unity Gateway를 출발점으로 권한다.
