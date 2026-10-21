---
title: "Unity Catalog Pages: Genie Ontology 속 비즈니스 지식의 거버넌스 홈"
description: "데이터 스튜어드가 비즈니스 용어의 권위 정의를 한 번만 정의해 Genie One과 에이전트를 grounding하는 Unity Catalog Pages(Beta)."
tags: [source, databricks, unity-catalog, genie, knowledge-management, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/unity-catalog-pages-governed-home-your-business-knowledge-genie-ontology"
blog: databricks
published_date: 2026-09-22
---

# Unity Catalog Pages: Genie Ontology 속 비즈니스 지식의 거버넌스 홈

## 개요

비즈니스 의미가 Slack·Confluence·암묵지에 흩어지면 에이전트는 틀린 답을 자신 있게 내놓는다. Genie Ontology는 이미 대시보드·쿼리·테이블에서 맥락을 자동 학습하는데, Unity Catalog Pages는 사람이 큐레이션하는 층을 더한다. 스튜어드가 핵심 용어·엔티티·약어의 권위 정의를 한 번 정의하면 Genie가 이를 진실의 원천으로 삼는다.

## Genie Ontology에서 Pages의 자리

각 Unity Catalog 시맨틱은 역할이 다르다. 메트릭 뷰는 계산법을, Pages는 개념의 의미를, 도메인은 찾을 곳을, 인증은 신뢰 대상을 말한다. 정의된 개념(예: "활성 고객"의 기준)에 닿는 질문이면 Genie는 추론 대신 Page를 조회하고, 소유자가 보이는 클릭 가능 출처로 인용한다. grounding이 숨은 AI 판단이 아니라 사용자가 검토 가능한 검증 trail이 된다.

## Page의 구조와 대규모 부트스트래핑

Page는 구조화 필드(소유자·동의어·설명)와 링크·이미지·표·카탈로그/워크스페이스 객체 참조를 담은 본문을 결합하고, 도메인 아래 데이터 곁에 정리되며, 관련 에셋과 출처 인용으로 근거를 유지한다. 전부 손으로 쓸 필요는 없다. Genie Code가 첨부 자료나 MCP 연결 도구(Confluence·Slack·Google Docs·GitHub)에서 Page를 작성하고, 대량 가져오기로 수주 걸릴 복붙을 수 분의 대화로 바꾼다. 현재 Beta이다.

## References

- 원문: [Unity Catalog Pages: a governed home for your business knowledge in Genie Ontology](https://www.databricks.com/blog/unity-catalog-pages-governed-home-your-business-knowledge-genie-ontology)
