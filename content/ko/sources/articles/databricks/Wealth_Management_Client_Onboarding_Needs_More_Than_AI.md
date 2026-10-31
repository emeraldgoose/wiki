---
title: "Wealth Management 고객 온보딩에는 AI 그 이상이 필요하다"
description: "온보딩 작업 속도를 높여도 시스템 간 인수인계 마찰은 해결되지 않으며, 거버넌스된 버전 케이스 컨텍스트가 에이전트 준비형 웰스 매니지먼트 온보딩의 기초가 됩니다."
tags: [source, databricks, wealth-management, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/wealth-management-client-onboarding-needs-more-ai"
blog: databricks
published_date: 2026-10-30
---

# Wealth Management 고객 온보딩에는 AI 그 이상이 필요하다

**원문**: [Databricks Blog](https://www.databricks.com/blog/wealth-management-client-onboarding-needs-more-ai) · **게시일**: 2026-10-30

## 개요
웰스 매니지먼트 온보딩은 모든 시스템이 제 역할을 마친 뒤에도 막힐 수 있습니다. 서류가 수집되고 심사 결과가 도착하며 워크플로 작업까지 완료되었는데, 무엇이 바뀌었는지, 어떤 증거가 최신인지, 예외의 소유자는 누구인지 누군가 판단하기 전까지 케이스는 여전히 대기 상태입니다. 이 여정은 CRM, 문서, KYC, 스크리닝, custody, workflow 시스템을 가로지르며 각 시스템이 케이스의 일부만 보유하고, 그리고 global asset managers의 15%만 strong CRM integration을 보고합니다. 기업은 각 작업 가속에 투자해 왔고 generative AI가 더 빠르게 만들지만, 다음 팀이 케이스를 재구성하고 증거를 대조하며 완료된 것으로 보이던 작업을 다시 둘러써야 한다면 추출·요약·라우팅 속도 향상은 의미가 크지 않습니다. 이 글은 현대 온보딩 플랫폼이 시스템 간 케이스를 연결하고 조건 변화에 따라 작업을 조정하며 통제와 human judgment를 보존해야 한다고 주장합니다.

## 핵심 내용
- 싱가포르 private banking 계좌 개설에는 평균 약 6주가 걸리며, Capgemini 조사에서 market 전반 relationship manager 시간의 최대 41%가 운영 업무에 소모됩니다.
- wealth executives 60% 이상이 unified client view를 갖지 못하고, 144개 global asset managers 중 절반 이상이 온보딩에 10개 이상 팀을 관여시키며 15%만 strong CRM integration을 보고합니다.
- task-level AI는 추출·심사 요약·라우팅을 가속하지만, 현재 evidence와 변경 기록, stale result 판정이 없으면 handoff는 실패합니다.
- governed case context는 evidence, case state, completed controls, open exceptions, agent activity, decision history를 결합한 각 온보딩 케이스의 현재·버전·소스 링크 뷰입니다.
- 에이전트 준비형 플랫폼은 4개 역량을 지원합니다: 케이스의 현재 상태 유지, 사람이 authority를 유지한 채 agent work 조정, 거버넌스와 permission controls, 고립 작업이 아닌 여정 측정.
- Databricks 구현 예시로는 source system sync를 위한 Lakeflow Connect, 증거 추출·분류를 위한 AI Functions, live transactional state를 위한 Lakebase, access·lineage·auditability를 위한 Unity Catalog, reliable interoperable storage를 위한 Delta 또는 Apache Iceberg가 언급됩니다.

## 상세
웰스 온보딩 지연은 개별 시스템 내부보다 handoff 지점에서 발생하며, shared case state가 완료 상태, stale 상태, 다음 단계를 막는 예외를 보여주지 않으면 AI는 fragmentation을 그대로 재생산합니다. governed case context는 버전 관리되어 teams가 무엇이 바뀌었고, 무엇에 영향을 미쳤으며, 이전 작업을 다시 검토해야 하는지 파악할 수 있게 합니다. core client와 custody records는 각 시스템에 남을 수 있고, evidence, controls, models, workflows는 Databricks에서 실행됩니다. 이 글은 플랫폼이 history를 재구성하지 않고도 4가지 질문에 answer할 수 있는지로 judge합니다: current evidence와 version, complete/stale work, unresolved exception과 다음 permitted action, agent/tool이 수행할 work와 authorized reviewer 결정 지점.그 answers가 case에 attach되면 governed supervisor agent는 work를 resume하고, independent tasks를 dispatch하고, approved tools를 call하고, conflicting evidence를 flag하고, review package를 assemble하여 humans가 decide하게 합니다. 이것은 온보딩 투자를 task acceleration에서 agent-ready coordination과 governance로 재정의합니다.

## 참고 자료
- 원문: [Wealth Management Client Onboarding Needs More Than AI](https://www.databricks.com/blog/wealth-management-client-onboarding-needs-more-ai)
