---
title: "RADAR: 이상 탐지로 그레이 장애 잡기"
description: "부분적 무음 장애를 4단계 이상 탐지 파이프라인으로 수 분 만에 포착해 탐지 시간을 95% 단축, 정밀도 90% 이상을 달성한다." (한국어 번역)
tags: [source, databricks, observability, anomaly-detection, ko, ko]
locale: ko
source_url: "https://www.databricks.com/blog/radar-catch-gray-failures-anomaly-detection"
blog: databricks
published_date: 2026-09-19
---

# RADAR: 이상 탐지로 그레이 장애 잡기

## 개요

대시보드는 녹색인데 일부 사용자만 조용히 실패하는 그레이 장애는, 지원 티켓으로 발견될 때까지 고객과 매출을 몇 시간씩 갉아먹는다. RADAR(Reliability Anomaly Detection, Alerting, and Root-cause analysis)는 Databricks 내부의 4단계·지표-중립 파이프라인으로 이런 장애를 수 분 만에 표면화하며, 탐지 시간 95% 단축에 정밀도 90% 이상을 보고했다.

## 그레이 장애가 교묘한 이유

부분적이라서(특정 카드 종류·특정 리전만 실패, 페이징할 서버 다운 없음) 커지고, 사용자 실수처럼 보이는 고립 사례로 오인된다. 고객 제보에만 의존하면 세 가지로 실패한다. 트리아제가 수동이고, 탐지가 몇 시간·며칠 늦으며, 피해자 대다수는 제보조차 하지 않는다. 해법은 평소보다 훨씬 많은 사용자가 같은 이슈를 동시에 겪는 순간 자동으로 울리는 탐지이다. 예컨대 특정 "사용자 과실" 에러 코드가 한 리전에서 급증하면 실은 제공자 과실이다.

## RADAR의 4단계

첫째, 신뢰성 지표를 시계열로 기록한다. 에러 수와 영향받은 distinct 사용자 수를 에러 코드·리전별로 나눈 풍부한 시계열이다. 둘째, 수동 임계값 대신 비지도 스트리밍 이상 탐지(SPOT 모델, 14일 히스토리 학습·단일 리스크 파라미터)를 돌린다. 셋째, 알림을 보강·필터링·중복 제거한 뒤 담당 팀으로 티켓을 라우팅한다. 넷째, 이상 심층 분석과 Genie 기반 대시보드 링크를 티켓에 붙여 온콜이 데이터 수집이 아닌 진단부터 시작하게 한다.

## Databricks에서 직접 만들기

패턴은 지표에 구애받지 않는다. 결제 이상, 체크아웃 전환율, 청구 처리량, 모델 드리프트 어디든 같다. 각 단계는 네이티브 구성요소에 매핑된다. 지표는 Zerobus + Unity Catalog/Metric View + Delta Lake, 탐지는 MLflow·Model Serving·Workflows, 알림은 SQL Alerts, 원인 분석은 Genie·AI/BI 대시보드이며, 전체를 하나의 애셋 번들로 배포한다. 팀은 스캐폴드 레시피와 데모 프롬프트를 공개했으므로, AI 에이전트에게 지표와 함께 넘기면 전체 시스템을 생성할 수 있다.

## References

- 원문: [RADAR: Catch gray failures with anomaly detection](https://www.databricks.com/blog/radar-catch-gray-failures-anomaly-detection)
