---
title: "Lakeflow Connect로 생산성과 AI 데이터 통합하기"
description: "Lakeflow Connect가 생산성 및 협업 데이터를 거버넌스된 Unity Catalog 테이블로 수집해, 하위 AI 에이전트가 기업 전체 맥락을 얻도록 하는 내용을 다룹니다."
tags: [source, databricks, data-engineering, ingestion, lakeflow, ko]
locale: ko
source_url: "https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect"
blog: databricks
published_date: "2026-10-26"
---

# Lakeflow Connect로 생산성과 AI 데이터 통합하기

**원문**: [databricks](https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect) · **게시일**: 2026-10-26

## 개요

Lakeflow Connect가 모든 업무 라인에 완전 관리형 데이터 수집을 가져오는 방식을 다루는 연재의 두 번째 글입니다. 마케팅 데이터 통합에 대한 심층 분석에 이어, 이번 글은 조직의 생산성 스택에 갇힌 기업 지식을 해제하는 데 초점을 둡니다. 위키, 프로젝트 관리 도구, AI 파운데이션 모델 데이터에 대한 네이티브 커넥터가 하위 AI 에이전트에 완전한 비즈니스 맥락을 제공합니다.

Lakeflow Connect는 SaaS 애플리케이션, 데이터베이스, 파일 소스 전반에 걸쳐 완전 관리형 네이티브 커넥터를 제공해 데이터를 Databricks 플랫폼으로 직접 수집합니다. 각 커넥터는 포인트 앤 클릭 UI 또는 간단한 API로 설정할 수 있으며, 데이터는 Unity Catalog의 거버넌스된 관리형 테이블로 증분 수집됩니다. 별도의 인프라 프로비저닝이나 확장은 필요하지 않습니다.

## 핵심 내용

- 생산성 및 협업 도구는 귀중한 기업 지식을 담고 있지만, 각 소스마다 개별 API 통합을 요구하며 역사적으로 사일로화되어 왔습니다.
- 네이티브 커넥터는 협업 도구(Jira, Monday.com, Smartsheet, Aha!, GitHub), 기업 지식 저장소(Confluence, Notion, Glean, SharePoint, Google Drive), 커뮤니케이션(Outlook, Gmail), AI 제공자(OpenAI, Anthropic)를 포괄합니다.
- Toyota Finance Australia, Seguros SURA, VaxCare는 무유지보수 파이프라인과 거버넌스된 분석 준비 완료 Delta 테이블을 보고했습니다.
- 문서, 페이지, 메시지 같은 비정형 콘텐츠는 Unity Catalog의 거버넌스된 테이블에 저장되며 `ai_parse_document`로 파싱해 검색에 인덱싱할 수 있습니다.
- OpenAI 및 Anthropic 커넥터는 사용량, 비용, API 키, 프로젝트, 사용자, 감사 로그를 노출해 AI 지출을 거버넌스합니다.
- M3 Accounting은 며칠 안에 GitHub와 SharePoint 문서를 Databricks로 통합했습니다.

## 상세

평균적인 생산성 스택은 프로젝트 트래커, 위키, 문서 저장소, 받은 편지함, AI 도구로 이루어져 있으며 각각 업무 수행 방식의 일부만 담고 있습니다. 커스텀 파이프라인은 구축이 느리고 유지보수가 힘들어, 내부 지식에 기반한 AI 에이전트 같은 강력한 활용 사례가 실현되지 못합니다.

Lakeflow Connect는 내장 커넥터로 흩어진 생산성 데이터를 통합 거버넌스 기반으로 가져와 통합 병목을 제거합니다. 데이터는 증분으로 Unity Catalog의 관리형 Delta 테이블에 수집되며, 거버넌스와 접근 제어는 중앙에서 처리됩니다.

AI 활용을 위해 비정형 콘텐츠는 소스별로 파일 또는 메시지당 한 행으로 거버넌스된 테이블에 저장됩니다. 구조화 파일은 직접 Delta 테이블로 저장할 수 있고, 문서 바이트는 Databricks의 내장 문서 인텔리전스로 텍스트로 변환한 뒤 청킹과 임베딩을 통해 검색에 사용합니다.

생산성 데이터 외에도 파운데이션 모델 커넥터는 AI 사용량, 비용, 규정 준수에 대한 가시성을 제공합니다. 리더는 팀·모델·애플리케이션별 지출을 귀속하고, 생산성·엔지니어링·비즈니스 데이터를 동일 플랫폼에서 통합할 수 있습니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect
