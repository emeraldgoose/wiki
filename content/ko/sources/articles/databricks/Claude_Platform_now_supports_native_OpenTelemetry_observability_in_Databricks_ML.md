---
title: "Claude Platform이 Databricks MLflow에서 네이티브 OpenTelemetry 관찰성을 지원합니다"
description: "Databricks MLflow가 Claude Platform의 네이티브 OpenTelemetry 내보내기 대상이 되어 에이전트 추적과 평가를 지원한다."
tags: [source, databricks, observability, otel, ko]
locale: ko
source_url: "https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow"
blog: databricks
published_date: 2026-11-04
---

# Claude Platform이 Databricks MLflow에서 네이티브 OpenTelemetry 관찰성을 지원합니다

**원문**: [databricks](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow) · **게시일**: 2026-11-03

## 개요

에이전트는 중요한 발견을 놓치거나 같은 출처를 반복해서 읽으면서도 그럴듯한 답을 낼 수 있다. 답만으로는 그 이유를 설명해 주지 않는다. 트레이스는 그 뒤에 있는 모델과 도구 호출을 보여 주므로, 팀은 실패를 조사하고 관련 사례를 찾고 변경이 도움이 되는지 시험할 수 있다. Databricks MLflow는 이제 Claude Platform의 네이티브 OpenTelemetry 내보내기 대상으로 지원된다. Anthropic SDK, Messages API, Managed Agents를 사용하는 개발자는 네이티브 트레이스를 Databricks로 보내고 MLflow를 이용해 에이전트를 디버깅하고 변경 사항을 평가할 수 있다.

## 핵심 내용

- Claude Platform의 네이티브 OpenTelemetry 내보내기는 공개 베타 단계다.
- 트레이스는 Unity Catalog 아래 MLflow에 저장될 수 있다.
- 트레이스 분석과 MLflow Issues는 나쁜 답과 반복된 도구 호출을 드러낼 수 있다.
- 팀은 도메인 전문가와 함께 답을 검토하고 일관된 테스트 케이스로 평가를 다시 실행할 수 있다.
- 구성 안내는 네이티브 내보내기, Unity Catalog 저장소, 이슈 모니터링을 다룬다.

## 상세

이 통합은 Anthropic SDK, Messages API, Claude Managed Agents를 Databricks MLflow로 가져온다. 트레이스 데이터를 Unity Catalog에 보존하고 디버깅 트레이스를 평가 워크플로에 연결하여 종단 간 에이전트 관찰성을 지원한다. 팀은 에이전트 동작을 조사하고, 변경 사항을 검증하고, 시간이 지나며 반복되는 실패 패턴을 모니터링할 수 있다.

## 참고 자료

- 아티클: [Databricks MLflow의 Claude Platform 네이티브 OpenTelemetry](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow)
