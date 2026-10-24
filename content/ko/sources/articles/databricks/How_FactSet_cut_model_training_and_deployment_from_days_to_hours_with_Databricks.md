---
title: "FactSet, Databricks AI Runtime으로 모델 학습·배포를 며칠에서 몇 시간으로 단축"
description: "FactSet이 Text-to-Formula 모델을 서버리스 GPU에서 학습·배포해 개발 주기를 단축한 사례입니다."
tags: [source, databricks, data-engineering, ai-runtime, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime"
blog: databricks
published_date: 2026-10-14
---

# FactSet, Databricks AI Runtime으로 모델 학습·배포를 며칠에서 몇 시간으로 단축

**원문**: [databricks](https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime) · **게시일**: 2026-10-14

## 개요

FactSet의 Text-to-Formula(TTF) 시스템은 투자 전문가의 자연어 요청을 FactSet Query Language(FQL) 수식으로 바꿉니다. 처음에는 검색 증강 생성(RAG)으로 관련 예시를 찾는 구조였지만, 사용량이 늘고 수식이 복잡해지면서 품질 한계에 부딪혔습니다.

FactSet은 복합 AI 아키텍처에 파인튜닝한 오픈 모델을 도입해, 추론 시점의 검색에 주로 의존하지 않고 FQL의 구조와 패턴을 학습하도록 했습니다. 새 데이터가 나올 때마다 2~3주 간격으로 모델을 재학습하므로, 인프라 준비와 배포 속도가 개발 주기의 핵심이 됩니다.

## 핵심 내용

- Databricks AI Runtime에서 워크로드별 서버리스 GPU를 선택할 수 있습니다.
- 기존 레이크하우스 워크플로와 같은 환경에서 학습할 수 있습니다.
- 모델 준비·학습·배포 시간이 며칠에서 몇 시간으로 줄었습니다.
- 잦은 재학습 주기를 감당할 수 있어 최신 데이터 반영이 빨라집니다.

## 참고 자료

- 원문: https://www.databricks.com/blog/how-factset-cut-model-training-and-deployment-days-hours-databricks-ai-runtime
