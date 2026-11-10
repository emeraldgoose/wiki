---
title: "Power BI에 들어온 Unity Catalog 메트릭 뷰: 모든 리포팅과 AI를 위한 단일 거버넌스 시맨틱 레이어"
description: "Databricks가 Publish to Power BI를 추가해 Unity Catalog 메트릭 뷰가 Power BI 시맨틱 모델을 구동하도록 합니다. 정의는 Databricks에서 한 번만 모델링되고 Power BI, AI/BI 대시보드, Genie에서 동일하게 거버넌스를 유지하며 동기화됩니다."
tags: [source, databricks, unity-catalog, semantic-layer, power-bi, ko]
locale: ko
source_url: "https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting"
blog: databricks
published_date: "2026-11-11"
---

# Power BI에 들어온 Unity Catalog 메트릭 뷰: 모든 리포팅과 AI를 위한 단일 거버넌스 시맨틱 레이어

**원문**: [Databricks 블로그](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting) · **게시일**: 2026-11-10

## 개요

Databricks가 Unity Catalog 메트릭 뷰를 Power BI에 연결합니다. 이로써 비즈니스 의미에 대한 하나의 거버넌스가 적용된 정의가 레이크하우스와, 비즈니스 사용자가 매일 여는 리포팅 도구를 함께 구동하게 됩니다. 겨냥한 문제는 정의의 표류입니다. 매출, 마진, 활성 고객은 모든 보고서와 노트북, AI 애플리케이션에서 같은 뜻이어야 하는데 그렇지 않으면 비즈니스 사용자와 AI 에이전트가 같은 데이터를 다르게 읽고, 재무팀과 영업팀이 서로 다른 매출 숫자를 내놓으며, 잘못된 숫자로 의사결정이 이루어집니다. Unity Catalog 시맨틱스의 일부인 Unity Catalog 메트릭 뷰는 이런 핵심 지표를 레이크하우스 위의 개방형 거버넌스 시맨틱 레이어에서 한 번만 정의하기 위해 존재합니다.

문제의 나머지 절반은 Power BI 쪽에 있습니다. 조직은 흔히 워크스페이스를 수천 개 운영하고, 각 워크스페이스가 자체 시맨틱 모델을 갖습니다. 모든 팀이 Power BI 안에서 지표와 관계를 다시 만들면 같은 로직이 여러 곳에 복제되고, 보고서가 서로 어긋나며, 정의가 바뀔 때마다 사본을 모두 고쳐야 합니다. Publish to Power BI는 고객이 요청해 온 답입니다. Databricks는 통합된 개방형 시맨틱 레이어로, Power BI는 프런트 엔드로 남습니다. 비즈니스 사용자는 데이터 팀이 모델링하거나 DAX를 작성할 때까지 기다리지 않고 셀프서비스 보고서를 만들고 어떤 차원으로든 지표를 탐색할 수 있으며, 데이터 팀은 여러 사본 대신 하나의 정의를 관리합니다.

동작 방식은 이렇습니다. 각 메트릭 뷰는 Power BI 시맨틱 모델에서 테이블이 되고, 그 차원은 열이 되며, 측정값은 DAX 측정값이 됩니다. Power BI는 메트릭 뷰 자체를 질의하므로 메트릭 뷰가 계속 원본 역할을 하고, 메트릭 뷰 안에 정의된 조인은 Databricks에서 실행됩니다. 캠페인 채널이나 지역처럼 조인된 차원은 일반 열로 도착하기 때문에 Power BI에서 테이블 관계를 다시 만들 필요가 없습니다.

## 핵심 내용

- 게시는 Catalog Explorer에서 필요할 때 수행하거나, Lakeflow Job에 Power BI 작업을 추가해 자동화할 수 있습니다. 그래서 운영 환경에서 메트릭 뷰와 시맨틱 모델이 동기화된 상태를 유지하며, 일정에 따라 또는 상위 테이블이 갱신된 직후에 변경된 측정값과 새 측정값, 새 차원이 수동 작업 없이 Power BI로 흘러 들어갑니다.
- 글의 마케팅 예시에서 campaign_performance 메트릭 뷰는 채널과 지역 같은 차원, 그리고 총 지출·총 매출·광고 수익률 같은 측정값을 정의합니다. Power BI에서는 이것이 spend 열의 합계, revenue 열의 합계, 그리고 총 매출을 총 지출로 나눈 비율 측정값으로 표현됩니다.
- 거버넌스는 그대로 유지됩니다. DirectQuery를 쓰면 모든 Power BI 질의가 Unity Catalog 접근 제어와 보안 정책을 따르고, 계보는 팀이 AI/BI 대시보드와 Genie, Databricks 레이크하우스에서 이미 쓰는 지표와 연결된 상태로 남습니다.
- 실시간 리포팅은 Lakehouse//RT와 DirectQuery 조합이 담당합니다. 관리형 Delta 테이블 위에서 동작하므로 데이터를 복사해 넣을 별도 서빙 시스템이 필요 없고, Unity Catalog의 행 필터, 열 마스크, ABAC 정책을 동일하게 적용합니다.
- 메트릭 뷰 구체화(materialization)도 곧 Power BI에 혜택을 줍니다. 지표 계산 방식을 바꾸지 않고 결과를 미리 계산해 두는 최적화로, 일치하는 구체화가 있으면 Databricks가 그 결과로 응답하고 없으면 평소처럼 메트릭 뷰를 질의합니다. 어느 쪽이든 정의와 DAX 측정값, 결과는 동일합니다.
- 프리뷰가 지원하는 범위는 대부분의 팀이 일상적으로 쓰는 정의를 아우릅니다. 조인과 관계, 차원, 측정값 등 데이터 모델링 메타데이터, 중복 제거를 포함한 표준 집계, 비율, 필터 측정값, 다른 측정값으로 구성한 측정값, 현재·오프셋·이동 구간(window) 측정값, 그리고 Power BI 필드 속성으로 넘어가는 설명과 통화·소수·백분율 표시 형식입니다.
- 저장 모드는 Lakehouse//RT나 Databricks SQL에 라이브 질의를 보내는 DirectQuery가 기본이고, 데이터를 Power BI로 적재하는 Import 모드도 있습니다.

## 상세

게시 절차는 세 단계입니다. 먼저 측정값 입력값을 차원으로 추가하고 모든 필드에 이름이 있는지 확인해 메트릭 뷰를 준비합니다. 다음으로 Catalog Explorer에서 Publish와 Publish to Power BI를 차례로 눌러 Power BI 자격 증명으로 로그인하고 대상 워크스페이스를 고릅니다. 운영 환경이라면 Lakeflow Job에 Power BI 작업을 추가해 데이터 파이프라인의 일부로 게시되게 합니다. 마지막으로 Power BI에서 시맨틱 모델을 열어 메트릭 뷰가 테이블로, 차원이 열로, 측정값이 DAX 측정값으로 나타나는지 확인합니다. 이 기능은 프라이빗 프리뷰로 제공되며, Databricks는 계정 팀과 함께 시험해 볼 것을 안내합니다.

전략적 구도는 Databricks가 의미 정의의 본거지가 된다는 것입니다. 메트릭 뷰와 관계, Pages를 비롯한 모델링 메타데이터가 여러 도구에 흩어지지 않고 한 곳에서 거버넌스되며, 같은 정의가 Power BI 보고서와 AI/BI 대시보드, Genie에 함께 쓰입니다. 글 말미의 요약도 같은 세 가지를 강조합니다. 의미 정의를 Unity Catalog에 두고, 한 번 모델링해 AI와 BI에서 함께 소비하며, DirectQuery 접근 제어와 작업 오케스트레이션으로 거버넌스와 동기화를 유지하는 것입니다.

## 참고 자료

- 원문: [Databricks 블로그](https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting)
