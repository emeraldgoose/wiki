---
title: "Document Intelligence로 실시간 애플리케이션과 에이전트 구동하기"
description: "문서가 도착하는 즉시 파싱·분류·추출해 실시간 업무 흐름과 에이전트를 만드는 방법입니다."
tags: [source, databricks, data-engineering, document-ai, ko]
locale: ko
source_url: "https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence"
blog: databricks
published_date: 2026-10-14
---

# Document Intelligence로 실시간 애플리케이션과 에이전트 구동하기

**원문**: [databricks](https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence) · **게시일**: 2026-10-14

## 개요

Databricks의 기업 고객은 매일 수백만 건의 문서를 받습니다. 이 비정형 문서에는 운영·고객·재무에 관한 중요한 맥락이 담겨 있지만, 문서가 도착한 뒤 데이터를 실제로 활용하려면 누군가 읽고 필요한 값을 추출해야 합니다. 이 수작업이 하류 업무 전체를 늦추고, 문서량이 늘수록 병목과 비용이 커집니다.

기존 문서 워크플로는 비동기 배치 파이프라인 위주라서 대화형이나 사람이 개입하는 실시간 의사결정에는 늦습니다. Document Intelligence의 실시간 REST API를 사용하면 문서가 도착하는 즉시 읽고 처리할 수 있습니다.

## 핵심 내용

- `ai_parse_document`, `ai_decide`, `ai_classify`, `ai_extract`를 파일 업로드 시점에 호출합니다.
- Databricks Apps나 사용자 정의 에이전트에 REST API를 붙여 대화형 문서 워크플로를 만듭니다.
- 계약서에서 당사자·발효일·갱신 조건을 추출하거나, 청구서에서 공급업체·PO 번호·금액을 뽑는 작업을 자동화합니다.
- 보험 청구처럼 여러 문서를 조합해야 하는 흐름도 에이전트가 실시간으로 처리할 수 있습니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/power-real-time-applications-and-agents-document-intelligence
