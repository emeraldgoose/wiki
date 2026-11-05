---
title: "어떤 데이터 협업 도구를: OpenSharing, Clean Rooms, Marketplace"
description: "협력자 사이의 관계와 데이터 민감도에 따라 Databricks OpenSharing, Clean Rooms, Marketplace 중 무엇을 쓸지 고르는 기준."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/which-data-collaboration-tool-opensharing-clean-rooms-marketplace"
blog: databricks
published_date: 2026-11-06
---

# 어떤 데이터 협업 도구를: OpenSharing, Clean Rooms, Marketplace

**원문**: [databricks](https://www.databricks.com/blog/which-data-collaboration-tool-opensharing-clean-rooms-marketplace) · **게시일**: 2026-11-05

## 개요

데이터 협업은 테이블을 넘어 모델, 노트북, AI 에이전트 같은 자산까지 확장되었고 안전한 공유는 그 어느 때보다 쉬워졌다. Databricks는 세 가지 협업 방식, 즉 OpenSharing, Clean Rooms, Marketplace를 제공한다. 잘못 고르면 엔지니어링 공수가 낭비되거나 보호해야 할 데이터가 노출될 수 있고, 선택 기준은 대개 데이터 유형보다 상대방과의 관계에 가깝다.

OpenSharing은 가장 단순한 라이브 공유 방식이다. 공유를 만들고 자산을 연결한 뒤 Databricks에 있지 않은 수신자에게도 접근 권한을 부여할 수 있다. 수신자는 원본 라이브 자산에 대한 직접 읽기 전용 접근을 얻으므로 항상 최신 상태를 보고, Power BI나 Tableau 같은 일반 BI 도구도 공유 테이블을 직접 읽을 수 있으며, 권한 부여와 취소가 빠르다. 테이블뿐만 아니라 뷰, 볼륨, 노트북, UDF, 모델, Delta 또는 Iceberg 테이블까지 공유할 수 있고, 외부 조직 간뿐 아니라 내부 비즈니스 단위 간에도 동작한다.

Databricks Clean Rooms는 두 명에서 열 명까지의 당사자가 데이터를 한데 모으되 모든 당사자가 승인한 코드만 실행하는 밀폐된 중립 공간을 제공한다. 모두가 결과의 혜택을 받지만 어느 쪽도 상대의 전체 원본 데이터를 보지 못하므로, 데이터 결합의 가치는 높지만 전체 데이터셋을 공개하고 싶지 않은 경우에 적합하다. Databricks Marketplace는 파일, 테이블, 모델, MCP 서버, 노트북, 응용 프로그램, SaaS 소프트웨어를 공유할 수 있는 공개 전시창이다. 특정 수신자를 전제로 하는 다른 두 방식과 달리 Marketplace는 발견 가능해, 어떤 Databricks 고객이라도 목록을 찾고 평가하고 연결할 수 있다.

## 핵심 내용

- 라이브 읽기 전용 공유가 필요한 알려진 수신자를 위해서는 OpenSharing을 사용한다. Databricks 외부 수신자도 포함된다.
- OpenSharing은 테이블, 뷰, 볼륨, 노트북, UDF, 모델을 지원하며 빠르게 회수할 수 있다.
- 당사자가 전체 원본 데이터를 노출하지 않고 결합 분석만 하려면 Clean Rooms를 사용한다. 코드는 모든 당사자가 승인해야 한다.
- 공개 발견이 필요한 경우, 즉 공급자가 규모 있는 노출을 원하거나 소비자가 외부 데이터와 AI 제품을 찾으려는 경우 Marketplace를 사용한다.
- 세 도구는 상호 배타적이지 않으며 같은 비즈니스가 관계별로 다른 도구를 병용할 수 있다.

## 상세

OpenSharing의 예시는 소매 판매 시점 데이터를 CPG 공급자에게 공유, 브랜드되지 않은 데이터를 연구 파트너와 공유하는 병원 네트워크, 핵심 공급자에게 수요 예측과 재고 위치를 공유하는 사례를 포함한다. Clean Rooms의 사용 사례에는 고객 목록 전체를 교환하지 않는 광고와 미디어 측정, 개인정보 보호 통제 하의 환자 또는 임상 시험 데이터 결합, 공동 프로모션을 위한 소매 충성도와 판매율 매칭이 있다. Marketplace 예시로는 유료 시장 데이터셋, 전 지구 날씨 데이터셋, 산업 특화 ML 모델이나 Genie 에이전트 패키지, 바로 실행 가능한 분석 응용 프로그램, 게시된 MCP 서버가 있다. 링크된 원문에는 나란히 비교 요약과 관계에 맞는 도구 선택 안내도 있다.

## 참고 자료

- 원문: [databricks](https://www.databricks.com/blog/which-data-collaboration-tool-opensharing-clean-rooms-marketplace)
