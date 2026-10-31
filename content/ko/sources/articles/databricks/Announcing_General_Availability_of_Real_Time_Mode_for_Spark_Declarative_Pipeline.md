---
title: "Databricks Spark Declarative Pipeline의 Real-Time Mode 일반 제공 발표"
description: "Spark Declarative Pipeline(SDP)에 Real-Time Mode(RTM)가 일반 제공되어, SDP의 기존 의존성 처리·오케스트레이션·데이터 품질 기능을 유지하면서 밀리초 단위 엔드투엔드 지연 시간을 제공합니다."
tags: [source, databricks, streaming, ko]
locale: ko
source_url: "https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks"
blog: databricks
published_date: 2026-10-29
---

# Databricks Spark Declarative Pipeline의 Real-Time Mode 일반 제공 발표

**원문**: [Databricks Blog](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks) · **게시일**: 2026-10-29

## 개요
Databricks는 Spark Declarative Pipeline(SDP)에 Real-Time Mode(RTM)를 일반 제공하며, 운영 수준의 저지연 스트리밍과 배치/ETL 작업을 단일 프레임워크로 통합합니다. SDP는 이미 의존성 해석, 증분 처리, 오케스트레이션, 실패 복구, 데이터 품질을 자동으로 처리하고, RTM은 그 위에 밀리초 단위의 엔드투엔드 처리 지연 시간을 추가합니다. RTM은 데이터를 지속적으로 스트리밍하고 모든 쿼리 단계를 동시에 실행하며, 데이터가 생성되자마자 다음 단계로 전달합니다. 전통적인 마이크로배치 아키텍처가 수십 배 느린 반면 RTM은 밀리초 반응을 가능하게 합니다. 고객은 이제 Spark 옆에 Flink 같은 전용 엔진을 별도로 유지할 필요가 없어, 중복 코드베이스와 파편화된 거버넌스 및 운영 오버헤드가 사라집니다. RTM은 부정 스코링, 실시간 알림, 라이브 개인화, 추천, ML 피처 계산처럼 스트리밍 데이터에 즉각 반응해야 하는 지연 시간 민감 워크로드로 SDP를 확장합니다.

## 핵심 내용
- SDP 상의 Real-Time Mode가 일반 제공되어, 운영 스트리밍 워크로드에서 밀리초 단위 엔드투엔드 지연 시간을 제공합니다.
- 별도 엔진 운영이 필요 없어져, 모든 파이프라인에서 단일 프레임워크와 하나의 관측성 스택, 하나의 과금 모델을 사용할 수 있습니다.
- RTM 파이프라인은 버전리스 업그레이드와 저다운타임 유지보수 등 SDP 기능을 그대로 보유합니다.
- SDP 서버리스는 클러스터 사이징 없이 서브초 지연을 제공하고, 워크로드에 맞춰 자동 튜닝되며 사용한 코어만 과금합니다.
- 실시간 흐름은 ForEach 싱크를 통해 Lakebase, Redis 등 커스텀 OLTP 싱크로 계산된 피처를 밀리초 단위로 전달할 수 있습니다.
- 주요 활용 사례는 사기 방지 및 개인화를 위한 ML 피처 계산으로, Kafka에서 온라인 피처 스토어까지 p99 지연 200ms를 달성했다고 보고됩니다.

## 상세
RTM은 데이터를 결정으로 바꾸는 데 밀리초가 필요한 모든 워크로드에 적합합니다. 실제 고객 환경의 피처 계산 워크로드에서 Apache Flink와 벤치마크했을 때 RTM은 전용 엔진 대비 최대 92% 빠른 것으로 측정되었습니다. 활성화하려면 파이프라인 모드를 continuous로 설정하고 `spark.databricks.streaming.realTimeMode.enabled`를 true로 지정한 뒤, pipelines.trigger를 RealTime으로 설정하고 싱크를 가리키는 target을 가진 update flow를 정의하면 됩니다. 지원되는 소스와 싱크는 문서에서 확인할 수 있습니다.

싱크 측면에서 피처 계산이나 사기 방지 활용 사례는 단순 계산이 아니라 질의 가능한 저지연 저장소에 결과를 적재해야 합니다. ForEach 싱크를 사용하면 개발자가 open, process, close를 구현하는 writer를 정의해 SDP가 행 단위로 OLTP 스토어에 쓰게 할 수 있으며, 오프라인-온라인 동기화 없이 초저지연으로 최신 데이터를 조회할 수 있습니다. 서버리스 실행에서는 여러 RTM 흐름을 하나의 파이프라인에 bin-pack하여 각 쿼리가 자체 리소스를 띄우지 않게 하고, 시스템이 워크로드에 맞춰 소스 및 셔플 파티션 수를 자동 튜닝합니다. 계획 중인 개선에는 SDP 내 네이티브 Lakebase 싱크, 내장 배치, 자동 재시도, Unity Catalog 관리 인증이 포함됩니다. 요약하면 RTM은 기존 SDP API를 확장하여 단일 governed 파이프라인 안에서 밀리초 지연과 간단한 튜닝을 함께 제공합니다.

## 참고 자료
- 원문: [Announcing General Availability of Real-Time Mode for Spark Declarative Pipelines on Databricks](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks)
