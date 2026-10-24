---
title: "시계열 티어드 스토리지 여정: Kafka/Flink 스트림에서 네이티브 Cassandra 콜드 리드까지"
description: "페타바이트 규모 시계열 데이터의 보관 비용을 줄이기 위해 Netflix가 티어드 스토리지를 구축한 두 가지 접근을 설명합니다."
tags: [source, netflix, data-engineering, timeseries, cassandra, ko]
locale: ko
source_url: "https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60"
blog: netflix
published_date: 2026-10-14
---

# 시계열 티어드 스토리지 여정: Kafka/Flink 스트림에서 네이티브 Cassandra 콜드 리드까지

**원문**: [netflix](https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60) · **게시일**: 2026-10-14

## 개요

Netflix의 TimeSeries Abstraction은 대규모 시계열 이벤트 데이터를 저장·조회하는 고처리량·저지연 플랫폼입니다. 이 글은 그 플랫폼이 Netflix의 가장 큰 데이터셋, 현재 수 페타바이트 규모의 운영 백본이 된 이후의 이야기를 다룹니다.

보관 기간 요구가 늘면서 스토리지 비용이 커지고, 자주 접근하지 않는 과거 데이터를 위해 거대한 고밀도 클러스터를 유지하는 비용이 부담이 되었습니다. 대부분의 쿼리는 최근 이벤트를 대상으로 하지만, 오래된 데이터도 감사와 조사를 위해 즉시 접근 가능해야 합니다.

## 핵심 내용

- 해법 1: Apache Kafka와 Flink로 데이터를 S3에 직접 스트리밍합니다.
- 해법 2: S3의 Cassandra 백업과 플러그형 Memtable을 활용해 S3에서 직접 읽습니다.
- 보관 기간 요구가 늘수록 스토리지 비용도 증가합니다.
- 자주 쓰지 않는 과거 데이터를 위한 고밀도 클러스터 유지 비용이 큽니다.
- 핫 노드의 높은 저장 밀도는 확장·배포·클러스터 안정성을 어렵게 만듭니다.
- 콜드 데이터를 분리해 비용을 줄이면서 감사·조사 접근성은 유지합니다.

## 참고 자료

- 원문: https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60
