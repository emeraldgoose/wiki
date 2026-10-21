---
title: "Unity Gateway CLI로 코딩 에이전트를 대규모로 배포·관리하기"
description: "관리자는 모델·도구·예산을 중앙에서 거버넌스하고 개발자는 선호 에이전트를 그대로 쓰는 Unity Gateway CLI(`ug`) 소개."
tags: [source, databricks, unity-catalog, ai-agents, unity-gateway, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli"
blog: databricks
published_date: 2026-09-24
---

# Unity Gateway CLI로 코딩 에이전트를 대규모로 배포·관리하기

**출처**: [Databricks Blog](https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli) · **발행**: 2026-09-24

## 개요

프론티어 코딩 모델이 며칠 간격으로 바뀌면서 플랫폼 팀은 단일 표준화와 접근·예산·로그 분산 사이에서 선택을 강요받는다. Unity Gateway CLI(`ug`)는 이 딜레마를 푼다. 관리자가 승인 모델·MCP 도구·스킬·지출 정책을 중앙에서 설정하면 개발자는 `ug claude`, `ug codex` 같은 명령으로 선호 에이전트를 그대로 쓰면서 설정이 자동 적용된다.

## 중앙 설정, 익숙한 개발 흐름

관리자는 Unity Gateway Govern에서 에이전트 기본값, MCP 서버, 스킬, Smart Routing, 지출 정책을 관리하고 한 번의 설정 게시로 전 팀에 배포한다(신규 모델의 코호트별 단계적 롤아웃 포함). 기기 관리로 `ug`를 배포하면 모두가 동일한 잠금 설정에서 출발하고, 모든 요청에 요청자 단위 귀속이 남는다.

## 비용 통제: Smart Routing, 예산, 트레이싱

작업 난이도가 다르므로 Smart Routing이 쉬운 일엔 저렴한 모델을, 어려운 일엔 고성능 모델을 배정한다(내부 코딩 벤치마크에서 약 35% 절감). 예산 임계치에 도달하면 신규 실행의 기본값을 저비용 옵션으로 유도하고 `ug usage`로 지출을 확인한다. 에이전트 도구 호출 트레이싱을 레이크하우스 통합 트레이스 테이블에 모아 Genie로 낭비 토큰을 찾는데, Databricks 자체 팀은 MCP 도구 버그 7건을 고쳐 연간 약 120만 달러를 회수했다.

## References

- [Deploy and manage coding agents at scale with the Unity Gateway CLI](https://www.databricks.com/blog/deploy-and-manage-coding-agents-scale-unity-gateway-cli)
