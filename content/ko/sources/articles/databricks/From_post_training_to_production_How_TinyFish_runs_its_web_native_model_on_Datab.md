---
title: "Post-training부터 프로덕션까지: TinyFish가 Databricks AI Runtime에서 웹 네이티브 모델을 운영하는 법"
description: "TinyFish는 특화 웹 네이티브 모델의 전체 수명주기를 Databricks AI Runtime에서 운영한다 — 관리형 GPU post-training, MLflow 작업 단위 평가, 프로덕션 서빙 — 2,178개 웹 에이전트 작업에서 77.6% 성공률, 에이전트 실행당 $0.088 비용을 기록했다." (한국어 번역)
tags: [source, databricks, ai-agents, llm-post-training, model-serving, mlflow, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime"
blog: databricks
published: "2026-10-09"
---

# Post-training부터 프로덕션까지: TinyFish가 Databricks AI Runtime에서 웹 네이티브 모델을 운영하는 법

**Source**: Databricks Blog, 2026-10-09

**핵심**: TinyFish는 기업의 에이전트가 실시간 웹에서 일하도록 Search, Fetch, Browser, Agent API를 제공한다 — 동적 사이트 탐색, 인증 워크플로, 다단계 작업. 이 일을 위한 특화 웹 네이티브 모델을 직접 훈련하고 전체 수명주기를 Databricks에서 운영한다: AI Runtime 관리형 GPU post-training, MLflow 평가, Model Serving 프로덕션 추론. 내부 go/no-go 벤치마크에서 2,178개 웹 에이전트 작업 기준 77.6% 작업 성공률을 기록했다.

## 배경

범용 파운데이션 모델도 TinyFish 에이전트 아키텍처의 일부지만, 웹 에이전트 작업에 특화된 모델은 팀이 직접 통제·개선할 수 있는 자산이다. 어려운 부분은 주변 인프라였다: post-training용 GPU 컴퓨트, 단일 응답이 아닌 에이전트 전체 행동을 재는 평가, 프로덕션 서빙, 다음 반복을 안내하는 운영 데이터(사용량, 비용). TinyFish는 단계별 별도 시스템 대신 이 모두를 Databricks로 통합했다.

## 에이전트 행동을 더 좋은 모델로

TinyFish는 지도 파인튜닝으로 post-training을 시작해 Direct Preference Optimization(DPO)으로 확장 중이며, AI Runtime의 Databricks 관리형 GPU에서 실행한다. 모델이 대형 에이전트 안에서 동작하므로 평가는 에이전트 전체가 요청 작업을 완수했는지를 본다: LLM 저지가 원 요청·행동 이력·최종 결과를 검토하고, 완전 수행만 통과 — 부분 완성·오답은 실패 처리다.

| 지표 | 값 |
|--------|-------|
| 완수 작업 | 1,691 / 2,178 |
| 작업 성공률 | 77.6% |
| 저지 | 요청 + 행동 이력 + 결과의 LLM 검토 |

이는 모델 개발의 직접 신호가 된다: post-training 변경마다 최종 작업 성능으로 측정되고, 성공한 반복은 Databricks Model Serving으로 프로덕션에 올라간다 — 이미 검색 리랭커와 쿼리 재작성 모델을 서빙 중인 경로다.

## 프로덕션 서빙과 비용 추적

최근 15일 동안 웹 네이티브 모델이 관여한 에이전트 실행 294,781건, 도구 단계 640만 건을 기록했다. 서빙 경제성(전체 에이전트 스택이 아닌 모델 한정):

| 지표 | 값 |
|--------|-------|
| 에이전트 실행당 비용 | $0.088 |
| 도구 단계당 비용 | $0.0040 |

평가 결과·사용 데이터·비용 리포트가 서빙 워크로드와 함께 Databricks에 있어 품질·사용량·경제성을 하나의 기반에서 추적한다.

## 에이전트가 실제 수행하는 일을 위한 모델 구축

글의 넓은 메시지는 조직적이다: 훈련·평가·서빙·운영 데이터를 한 환경에 두면 엔지니어는 GPU 운영과 단절된 시스템 간 데이터 배관 대신 모델·제품 행동에 시간을 쓴다. 자체 모델과 함께 외부 파운데이션 모델 트래픽은 Unity Gateway로 통합해 비용 추적·키 관리·거버넌스를 중앙화한다.

## 소프트웨어 엔지니어를 위한 시사점

- **응답이 아니라 에이전트를 평가하라**: 도구 사용 모델에는 행동 이력 검토를 포함한 작업 완수 벤치마크가 응답별 채점보다 진짜 훈련 신호다.
- **루프를 한 플랫폼에 닫아라**: post-training, 평가 데이터, 서빙, 비용 지표를 같은 곳에 두면 프로덕션 행동 → 재훈련 사이클이 짧아진다.
- **단위 경제를 일찍 추적하라**: 실행당·도구 단계당 서빙 비용은 모델 품질 작업을 예산화 가능한 엔지니어링 결정으로 바꾼다.
- **외부 모델은 게이트웨이로**: Unity Gateway 같은 단일 게이트웨이가 에이전트 스택 확장 시 키·지출·거버넌스를 중앙화한다.

## 참고문헌

- 원문: [https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime](https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime)
