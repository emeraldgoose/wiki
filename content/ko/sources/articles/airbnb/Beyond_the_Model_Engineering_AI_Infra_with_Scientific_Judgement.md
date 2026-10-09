---
title: "모델을 넘어서 - 과학적 판단력을 갖춘 AI 인프라 엔지니어링"
description: "Airbnb의 Insight Miner 에이전트 하네스는 과학적 방법론을 비정형 텍스트 분석 인프라로 코드화: 추출-임베딩-클러스터링 코어, 대규모 라벨링, 에이전트 기반 유지보수."
published: "2026-09-15"
source_url: "https://airbnb.tech/ai-ml/beyond-the-model-engineering-ai-infra-with-scientific-judgement/"
blog: airbnb
locale: "ko"
tags: [airbnb, ai-agents, agent-harness, data-science, evaluation, methodology, unstructured-data, ko]
---

# 모델을 넘어서 - 과학적 판단력을 갖춘 AI 인프라 엔지니어링



**저자**: Wren Dougherty · **발행**: 2026-09-15 · **출처**: [Airbnb Engineering & Data Science](https://airbnb.tech/ai-ml/beyond-the-model-engineering-ai-infra-with-scientific-judgement/) ([Medium에도 게재](https://medium.com/airbnb-engineering/beyond-the-model-engineering-ai-infra-with-scientific-judgement-371316d43261))

## 문제

코딩 에이전트에게 10만 건의 고객 지원 대화를 분석시키면 몇 분 만에 세련된 분류 체계와 정확한 비중 수치, 임원 보고용 요약을 내놓는다. 그러나 그 뒤의 조사 과정은 보이지 않는다: 어떤 방법을 선택했는지, 어떤 근거를 저울질했는지, 얼마나 신뢰할 수 있는지, 다시 실행하면 같은 결과가 나올지. 모델은 지능적이지만, 방법론 없는 지능은 과학이 아니다. Airbnb는 2025년 AI 고객 서비스 어시스턴트 출시 준비 과정에서 이를 직접 겪었다. 실제 상황에서 마주할 케이스(특히 AI가 다루기 위험한 희귀 이벤트)의 분류 체계와 비중을 파악하고 대표 데이터셋을 만드는 데 수개월의 장인적(artisanal) 고밀착 반복 작업이 필요했다 — 노트북·테이블·문서·전문가 판단을 넘나들며. 한 번은 괜찮지만, 새로운 언어·지역·LLM 제품으로 주 단위 확장이 이어지자 작업량이 프로세스를 앞질렀다. 해법은 더 똑똑한 모델이 아니라 방법론 자체의 복제였다.

## 해법: 비정형 텍스트용 에이전트 하네스 Insight Miner

글의 핵심 주장: 답만큼이나 방법이 곧 프로덕트다. [에이전트 하네스](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)란 모델을 둘러싼 인프라로 구축된 방법론으로, 에이전트가 질문을 구성하고 증거를 선택하며 결정을 기록하는 방식을 규율한다. 결과는 재현·감사·반박 가능해지고, 방법은 공유·점검·개선될 수 있다.

**Insight Miner의 동작 방식:**

1. **엔지니어링 우선**: 쿼리, 대규모 라벨링·임베딩, 클러스터링·트래킹을 미리 제공하므로, 대규모 분석을 위해 새로운 인프라를 배울 필요가 없다.
2. **검증된 코어 — 추출-임베딩-클러스터링**: 그 주변에 팀이 의존해 온 기법들(프롬프트 튜닝, 하드 예제 마이닝, 대조 라벨링, 비지도 탐색 우선 후 분류로 성숙시키기)을 배치. 과거에는 복사-붙여넣기 노트북에 흩어져 있던 것들이 이제 하나의 공유 패키지로, 개별 조사에서 배운 개선이 전체에 반영된다.
3. **연구 파트너·실행자·방법론 전문가로서의 에이전트**: 조사는 채팅 세션의 연구 질문으로 시작한다. 하네스는 데이터셋·도메인·질문에 구애받지 않는다 — 어떤 비정형 텍스트 원천이든, 어떤 렌즈로든, 동일한 엄밀함으로.
4. **인간 판단의 상향 이동**: 기계적 부분은 확장·병렬화되므로 데이터 사이언티스트는 모호하고 전략적인 부분 — 엣지 케이스 직접 검토, 가설·그루핑 검증, 정성+정량 이해 구축 — 에 시간을 쓴다. 자동화가 인간 판단을 대체하는 것이 아니라 가장 중요한 지점에서 오히려 늘린다.

**측정된 효과**: 커뮤니티 지원 어시스턴트가 새 언어·국가로 확장되는 동안 수개월 걸리던 조사가 수일로 단축됐고, 엄밀함과 속도 모두 상승했다(트레이드오프가 아님).

## 기술 팀을 넘어서

출시 1년 만에 Insight Miner는 수십 개 팀, 수백 종의 조사에 쓰이며, 기술직보다 비기술직 사용자가 많다(운영·제품 인사이트 팀 비중이 특히 높음). 탐색과 에이전트 대화를 쉽게 만드는 UI가 전문가 참여를 넓혔다. 코드를 한 줄도 써본 적 없는 도메인 전문가가 부족한 엔지니어링/DS 리소스를 기다리는 대신 직접 대규모 분석을 수행하고, 과거 수백 건의 수동 리뷰로 뒷받침되던(또는 리소스 부족으로 엄두도 못 내던) 프로젝트들이 공유 베스트 프랙티스로 수 자릿수 더 많은 데이터를 다룬다. 활용 사례는 개방형 설문 코딩, 모델 성능 평가, 사기 패턴 이해 등 다양하다.

## 새로운 인프라 범주

하네스는 개발·유지보수·평가·지속 개선이 필요한 풀스택 시스템이며, 그 일 자체가 에이전트 시스템에 잘 맞는다는 것이 글의 주장이다. Insight Miner는 별도의 에이전트들이 신선하게 유지한다: 새 모델 릴리스용 지침 업데이트, 새 베스트 프랙티스 반영, 실사용 리뷰로 pain point 발굴, 버그 감시·재현·수정 제안. 데이터 사이언스를 넘어 일상 업무를 재편하는 에이전트 환경이다. 결론부 테제(Airbnb CTO의 글과 공명): 모델이 상품화될수록 남는 것은 고유 데이터·깊은 워크플로 통합·취향(taste)이며, 하네스는 세 가지가 축적되는 곳이다. 전문가의 취향이 모든 팀이 실행하는 방법이 되고, 매 실행이 모두를 위한 하네스 개선으로 이어진다.

## 세미나 시사점

- 모델 지능과 과학적 타당성을 구분하라: 에이전트 출력을 신뢰 가능하게 만드는 것은 벤치마크 점수가 아니라 감사 가능성(선택한 방법, 저울질한 근거, 기록된 결정)이다.
- 추출-임베딩-클러스터링 코어 + 공유·버전관리되는 방법 패키지는 bespoke 노트북 작업을 paved-path 인프라로 바꾸는 구체적 패턴이다.
- 2차 루프를 주목하라: 하네스를 유지보수하는 에이전트(지침 업데이트, 버그 감시, 베스트 프랙티스 반영)가 모델 교체 속에서도 엄밀함이 부식되지 않고 복리로 쌓이게 하는 메커니즘이다.

## 관련 개념

- `concepts/ai-engineering/agent.md`, `concepts/ai-engineering/agent-evaluation.md`, `concepts/ai-engineering/rag.md`

## 참고 자료

- [방법론을 인프라로 (저자의 companion 글)](https://wrenchatwork.substack.com/p/rigorous-work-with-fallible-ai)
- [에이전트 하네스에 대한 ThoughtWorks 보고서](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future_of_software_engineering_europe_2026.pdf)
- [Airbnb 2026 여름 릴리스 (새 언어/국가)](https://news.airbnb.com/airbnb-2026-summer-release/)
