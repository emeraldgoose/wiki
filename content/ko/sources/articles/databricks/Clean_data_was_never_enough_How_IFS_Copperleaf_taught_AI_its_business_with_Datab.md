---
title: "깨끗한 데이터만으로는 부족했다: IFS Copperleaf가 Databricks Genie One으로 AI에게 비즈니스를 가르친 방법"
description: "IFS Copperleaf는 Databricks Genie One 기반의 전사 AI 어시스턴트 IONA를 만들어 약 30개의 거버넌스된 소스 시스템 전반에 자연어로 답한다. 2026년 7월 출시 이후 70% 활성화율, 4개월 만에 운영 비용 회수."
tags: [source, databricks, ko]
locale: ko
source_url: "https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0"
blog: databricks
published_date: "2026-11-19"
---

# 깨끗한 데이터만으로는 부족했다: IFS Copperleaf가 Databricks Genie One으로 AI에게 비즈니스를 가르친 방법

**출처**: [databricks](https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0) · **게시일**: 2026-11-16

## 개요

IFS Copperleaf는 자산집약형 조직이 더 나은 투자 결정을 내리고, 리스크와 가치의 균형을 맞추고, 자본 투자의 효과를 극대화하도록 돕는 Asset Investment Planning(AIP) 소프트웨어의 글로벌 선도 기업이다. 25년 이상의 경험으로 AIP 카테고리를 개척했으며, 지금은 엔터프라이즈 클라우드와 Industrial AI 소프트웨어의 글로벌 리더인 IFS의 일부다. 2025년 가을, Misagh Jebeli(IFS Copperleaf Enterprise Data Architect)와 Lisa Richter(Director of Technology and AI)는 "2년 뒤 데이터 작업은 어떤 모습일까"라는 질문에 시간을 내어 답을 찾기로 했다. 그들의 베팅: 2027년이면 사람들은 리포트를 찾아 헤매지 않을 것이고, 매일 쓰는 도구가 비즈니스를 이해하고, 평이한 언어로 답하고, 사람을 대신해 행동할 것이다.

그 베팅은 Databricks Genie One 위에 구축한 전사 AI 어시스턴트 IONA가 되었다.

## 핵심 내용

- **Genie One 위의 IONA**: IFS Copperleaf 누구나 Salesforce, HubSpot, M365를 포함한 약 30개 시스템의 거버넌스된 데이터에 평이한 영어로 질문할 수 있다.
- **깨끗한 데이터만으로는 부족했다**: 팀마다 "활성 고객" 같은 지표를 다르게 정의했다. IONA는 원시 데이터에 답하고, 비즈니스 팀이 Skills(Genie Ontology와 거버넌스된 컨텍스트 기반)로 데이터의 의미를 가르친다.
- **결과**: 2026년 7월 출시 이후 약 70% 활성화율, 4개월 만에 운영 비용을 회수했다.
- **비교 기준의 이동**: 사용자들은 IONA를 기존 리포트가 아니라 매일 쓰는 AI 네이티브 도구와 비교했다 — 컨텍스트 기억, 후속 초안 작성, 시스템 간 행동을 원했다.
- **데이터가 한곳에 있다고 의미가 한곳에 있는 것은 아니다**: 세 명의 리더에게 활성 고객 수를 물으면 여전히 세 개의 숫자가 나올 수 있었다. AI는 모든 테이블을 읽을 수 있어도 다운셀과 이탈을 구분하지 못했다.
- **IONA는 근거를 보여준다**: 답이 이상하면 해당 시스템의 데이터 소유자를 지목한다 — 사람들은 도구를 포기하는 대신 소스를 고친다.
- **조달이 아닌 파트너십**: 팀은 프로토타입과 피드백을 공유해 Genie One, Genie Agents, Genie Ontology의 기능 형성에 기여했다.

## 세부 내용

팀은 어려운 부분이 데이터 품질일 것이라 예상했지만, 실제로는 의미였다. 대부분의 기업처럼 IFS Copperleaf도 여러 시스템 위에서 운영된다 — CRM, 마케팅, 지원, 계약, 재무 도구가 각각 다른 부서 소유다. 부서 횡단 답변은 과거에 수작업 내보내기, 스프레드시트 버전 지옥, 조정, 그리고 "누구 숫자가 맞는가" 회의를 의미했다.

**첫 번째 전환 — 모든 것을 모델링하지 말 것.** 교과서적 접근은 질의 전에 모든 테이블을 정제·모델링해야 한다고 말한다. 약 30개 소스 시스템과 수만 개의 테이블로는 그 큐가 결코 비지 않는다. 팀은 뒤집었다: 이해관계가 가장 큰 재무와 마케팅→세일즈 퍼널은 완전히 모델링하고, 나머지는 IONA가 원시 데이터에 직접 답한다. 데이터는 몇 달 더 일찍 쓸 수 있게 되었고, 모델링 노력은 정확도가 중요한 곳에 집중됐다.

**두 번째 전환 — 비즈니스가 AI를 가르친다.** 자신 있게 틀린 답을 내거나 컨텍스트가 없으면 멈춰버리는 일반 AI 도구와 달리, Genie 위에 구축되고 Genie Ontology에 기반한 IONA는 스스로 개선하고 필요할 때 추가 정보를 요청하도록 설계됐다. 비즈니스 팀은 데이터의 의미(무엇이 "활성 고객"인지, 다운셀과 이탈을 어떻게 구분하는지)를 Skills로 인코딩해, 의미가 사람의 머릿속이 아니라 데이터와 함께 살게 한다.

사용자 반응은 팀을 놀라게 했다. 사람들은 IONA를 지금까지 써본 최고의 AI와 비교하며, 차트만이 아니라 기억된 컨텍스트, 후속 작업 초안, 시스템 간 행동을 기대했다. 그리고 IONA는 답이 이상할 때 추론 과정을 보여주고 책임 있는 데이터 소유자를 지목하기 때문에, 조직은 나쁜 답을 우회하는 대신 소스에서 데이터를 고친다.

## 참고 자료

- 원문: [Clean data was never enough: How IFS Copperleaf taught AI its business with Databricks Genie One](https://www.databricks.com/blog/clean-data-was-never-enough-how-ifs-copperleaf-taught-ai-its-business-databricks-genie-one-0)
