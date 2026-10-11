---
title: "Databricks 위에 에이전트 기반 보안 리뷰를 직접 만든 방법"
description: "Unity Catalog·Lakeflow Jobs·Databricks Apps 위의 7개 전담 리뷰 에이전트로 정형 업무를 자동화하고 어려운 판단은 사람에게 남긴 실전 기록."
tags: [source, databricks, unity-catalog, ai-agents, security, ko]
locale: ko
source_url: "https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks"
blog: databricks
published_date: 2026-09-24
---

# Databricks 위에 에이전트 기반 보안 리뷰를 직접 만든 방법

**출처**: [Databricks Blog](https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks) · **발행**: 2026-09-24

## 개요

정형적 연동과 진짜로 새로운 아키텍처가 같은 보안 큐에서 희소한 전문가 리뷰어를 기다리고 있었다. 저자는 Databricks 위에 에이전트 계층을 올려 접수·위험 등급·요건 초안·후속 조치를 자동화하고, 새롭거나 고위험·모호한 건은 사람에게 넘겼다. Unity Catalog, 호스팅 파운데이션 모델, Lakeflow Jobs, Databricks Apps가 하나의 거버넌스를 공유한 덕분에 첫 버전은 두 시간 만에 돌아갔다.

## 각자 한 가지 일을 맡은 7개 전담 에이전트

범용 리뷰어 하나 대신 역할이 bounded된 에이전트들 — 접수, 위험 평가, 요건, 전문화 리뷰(브라우저 확장 위협 모델링·벤더 평가 등), 검증, 워크플로, 학습 — 을 대화형 접수 앱 뒤의 스케줄 노트북 작업으로 엮었다. 접수는 평서문 설명을 구조화 요청으로 바꾸고 상담 모드를 제공하고, 위험 평가는 불완전하면 상위 등급을 기본값으로 하며, 적격 저·중위험 건은 기준·증거 충족 시 자동 경로로 완결되고 나머지는 요약·증거·미결 질문과 함께 사람에게 도착한다.

## 증거와 측정으로 만드는 신뢰

신뢰는 모델이 아니라 주변 시스템에서 온다. 실제 표준에 근거하고, 증거(설계 문서·데이터 등급·통제 근거)를 강제하고, 불확실하면 낙관적 추정이 아니라 보수적 상향·후속 질문·사람 이관이며, 학습 에이전트가 리뷰어 수정에서 프롬프트를 다듬는다. 같은 Unity Catalog 테이블 위의 임원 대시보드가 물량·위험 분포·자동화율·소요 시간을 운영 기록에서 직접 집계하는데, 수일씩 대기하던 정형 요청이 수 분에 끝나면서 전문가는 새로운 설계에 집중하게 됐다.

## References

- [How I built agent-based security reviews on Databricks](https://www.databricks.com/blog/how-i-built-agent-based-security-reviews-databricks)
