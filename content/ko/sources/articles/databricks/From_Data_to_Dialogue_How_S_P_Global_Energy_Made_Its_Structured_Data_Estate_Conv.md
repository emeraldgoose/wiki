---
title: "데이터에서 대화로: S&P Global Energy가 정형 데이터 자산을 대화형으로 바꾼 방법"
description: "데이터셋 그룹별 Genie Agent, 매니지드 MCP 서버, FastMCP 프록시 3층 구조로 원자재 데이터를 대화형 엔드포인트로 바꾼 S&P Global Energy 사례."
tags: [source, databricks, genie, mcp, ai-agents, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks"
blog: databricks
published_date: 2026-09-25
---

# 데이터에서 대화로: S&P Global Energy가 정형 데이터 자산을 대화형으로 바꾼 방법

**출처**: [Databricks Blog](https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks) · **발행**: 2026-09-25

## 개요

S&P Global Energy의 데이터는 LNG·화학·원유·정제품·가스전력 등 원자재별 방대한 데이터셋 군으로, Databricks 안팎에 흩어져 있다. 수제 text-to-SQL과 용도별 API로는 도메인 전문가가 늘 엔지니어링 백로그 뒤에 갇혔다. 해법은 Genie Agent를 시맨틱 계층으로, 매니지드 MCP 서버를 연동 규약으로, FastMCP 프록시를 원자재별 묶음으로 삼는 3층 구조였고, 신규 대화형 데이터 상품 출시가 수개월에서 수일로 줄었다.

## 1층: 좁고 전문가가 큐레이션한 Genie Agent

도메인 전문가는 Unity Catalog 테이블을 그대로 쓰고(외부는 Lakehouse Federation으로 신규 ETL 없이 연결) 데이터셋 그룹당 하나의 집중형 Genie Agent를 만든다. 예컨대 LNG는 화물·정전·넷백·가격별로 별도 에이전트다. 각 에이전트 안에 컬럼 설명, 예시 쿼리, 신뢰 자산, floating storage 같은 업무 정의를 넣어 일반 text-to-SQL이 놓치는 맥락을 채운다. 큐레이션이 엔지니어링 티켓이 아니라 도메인 활동이 된 것이 핵심 전환이다.

## 2–3층: 매니지드 MCP 서버와 프록시 조합

각 Genie Agent는 자동으로 거버넌스된 MCP 서버가 되어 질의-폴링 도구 쌍을 노출하고, Unity Catalog 권한으로 사용자가 볼 수 있는 테이블에만 닿는다. FastMCP 프록시는 그룹 에이전트들을 원자재당 하나의 복합 엔드포인트 뒤에 네임스페이스 도구로 묶어, 정전-화물에 걸친 질문을 양쪽에 분기·종합한다. MCP 표준 브리지 하나로 내부 에이전트, 고객 대면 경험, 외부 고객의 어시스턴트까지 모두 같은 관문을 쓴다.

## 성과와 실무 교훈

출시 기간이 수일로 붕괴되고 전문가는 요청자가 아니라 발행자가 됐으며, Genie Agent Benchmark로 정확도를 큐레이션-벤치마크-개선 루프로 유지한다. 교훈은 에이전트는 좁게, 파이프라인보다 페더레이션을 먼저, 시맨틱 계층에 전문가 시간을 투자, 복합 도구는 명확히 네임스페이스, 신뢰 선행지표로 SME의 생성 SQL 동의율을 보라는 것이다.

## References

- [From Data to Dialogue: How S&P Global Energy Made Its Structured Data Estate Conversational](https://www.databricks.com/blog/data-dialogue-how-sp-global-energy-made-its-structured-data-estate-conversational-databricks)
