---
title: "Genie One MCP: 모든 AI 에이전트에 올바른 비즈니스 컨텍스트를"
description: "승인된 지표·관계·권한을 담은 Genie Ontology 컨텍스트를 모든 MCP 호환 AI 어시스턴트로 확장하는 Genie One MCP."
tags: [source, databricks, genie, mcp, unity-catalog, ko]
locale: ko
source_url: "https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context"
blog: databricks
published_date: 2026-09-22
---

# Genie One MCP: 모든 AI 에이전트에 올바른 비즈니스 컨텍스트를

**출처**: [Databricks Blog](https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context) · **발행**: 2026-09-22

## 개요

범용 어시스턴트는 기업 데이터에 닿아도 "최대 고객 순매출이 왜 8% 줄었나" 같은 질문에 흔들린다. 팀마다 용어 정의가 다르고 소스가 충돌하며 사용자별 권한이 다르기 때문이다. Genie One MCP는 거버넌스된 Genie Ontology 컨텍스트에 기반한 Genie One을 모든 MCP 호환 어시스턴트(ChatGPT, Claude, Copilot, 코딩 에이전트)의 도구로 노출해, 비즈니스 의미를 한 번 정의해 어디서든 재사용하게 한다.

## 직접 연결만으로는 부족한 이유

테이블 직결은 접근은 주되 공유된 의미는 주지 못해 네 가지 문제를 낳는다. 정확도 불확실(어떤 소스·정의·조인이 승인됐는지 모름), 스키마 반복 탐색에 따른 비용·지연 증가, 연결마다 다른 거버넌스, 클라이언트·세션별 상이한 답변이다. Genie Ontology는 승인 지표·정의·관계·소유권·접근 정책과 신뢰 자산에서 추론한 컨텍스트를 결합해 Genie One이 권위 있는 소스를 고르고 호출자 권한을 강제하게 한다.

## 동작 방식

서버는 질의·폴링·전체 결과 조회·취소·MCP Apps 대화형 뷰의 5개 도구와 웨어하우스 지정 파라미터를 제공한다. 사용자 대신(On-Behalf-Of) OAuth로 신원이 흘러 Unity Catalog 권한·행 필터·컬럼 마스크가 호출자별로 적용되므로, 같은 질문도 사용자마다 범위가 다른 답을 받는다. 매니지드 서버는 Agents > MCPs에 등록되고 감사 로그·쿼리 이력·과금 텔레메트리를 남긴다. 운영 지침은 클라이언트 프롬프트가 아닌 Databricks에서 Genie를 튜닝하고, 맞는 경우 단일 도메인 Genie Agent MCP 서버를 선호하며, 클라이언트별 OAuth 앱을 등록하고, 그룹별 가장(impersonation) 질의로 거버넌스를 검증하라는 것이다.

## References

- [Genie One MCP: Give any AI Agent the Right Business Context](https://www.databricks.com/blog/genie-one-mcp-give-any-ai-agent-right-business-context)
