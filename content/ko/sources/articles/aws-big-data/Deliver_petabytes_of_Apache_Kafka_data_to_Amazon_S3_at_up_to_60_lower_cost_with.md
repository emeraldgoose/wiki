---
title: "Amazon MSK Express 브로커로 Apache Kafka 데이터를 Amazon S3에 최대 60% 낮은 비용으로 전달하기"
description: "Amazon MSK Express 브로커가 Kafka 토픽 데이터를 범용 S3 버킷으로 네이티브 전달하는 방식 — Kafka Connect 없이, 바이트당 과금, 브로커 처리량을 소모하지 않는 전달로 최대 60% 비용 절감."
tags: [source, aws-big-data, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers"
blog: aws-big-data
published_date: "2026-11-19"
---

# Amazon MSK Express 브로커로 Apache Kafka 데이터를 Amazon S3에 최대 60% 낮은 비용으로 전달하기

**출처**: [aws-big-data](https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers) · **게시일**: 2026-11-16

## 개요

많은 Kafka 워크로드는 백업·아카이브, 컴플라이언스 보존, 토픽 보존 기간을 넘는 리플레이, AI/ML 학습 데이터, 예약 ETL 스테이징을 위해 Amazon S3에 지속적인 사본을 필요로 한다. 전통적인 패턴 — Kafka Connect 위의 S3 sink 커넥터 — 은 두 시스템을 운영하게 만든다. 직접 크기를 산정하고 패치하며 과프로비저닝해야 하는 Kafka 브로커와, 24시간 만들고 보안 승인을 받고 비용을 내야 하는 전달 파이프라인이다.

Amazon MSK Express 브로커가 이제 토픽 데이터를 범용 Amazon S3 버킷으로 직접 전달한다. Express 브로커가 수집과 전달을 모두 처리하므로, 자체 관리 대안 대비 수집+전달 비용을 최대 60%까지 낮출 수 있다. 관리할 커넥터나 인프라가 없고, 전달된 데이터에 대해서만(바이트당 과금) 비용을 내며, 전달이 브로커 처리량을 소모하지 않으므로 아카이빙이 실시간 컨슈머와 경쟁하지 않는다.

## 핵심 내용

- **브로커 관리 단순화**: Express 브로커는 사용한 만큼만 내는 스토리지를 자동 확장한다(용량 산정·모니터링 불필요, 트래픽이 줄면 요금도 자동 하락). 실패한 브로커는 자동 복구되고, 가용성·성능을 위한 클러스터/토픽 구성은 AWS가 관리하며, 유지보수 창이 없다. 브로커를 추가하면 몇 분 안에 파티션이 재분배되므로 피크 기준으로 과프로비저닝할 필요가 없다.
- **Kafka Connect 불필요**: 토픽에 전달 채널(channel)을 만들면 MSK가 전달을 실행한다. 커넥터를 찾고, 보안 승인받고, 배포하고, 패치할 필요가 없다. MSK가 재시도와 백프레셔를 처리하며, 처리에 실패한 레코드는 식별자·에러 컨텍스트와 함께 데드레터큐(DLQ) 버킷으로 들어가고 전달은 계속된다.
- **비용 모델**: 피크에 맞춘 용량을 둘 필요가 없고, 전달된 바이트당으로만 과금된다. 표준 S3 요금에 전달 요금 하나만 추가되며, 워커 요금도, 전달에 사용하는 브로커 이그레스 요금도, DLQ 레코드 요금도 없다. 트래픽이 적으면 전달 비용도 적다.
- **경합 없음**: 채널은 브로커 처리량을 소비하지 않고 토픽을 읽으므로, 아카이브가 실시간 애플리케이션과 경쟁하지 않는다. 한 토픽에 채널을 여러 개 추가해도 브로커 부하는 늘지 않는다. 용량 확장과 버전 업그레이드도 전달 중단 없이 진행된다.
- **전달 형식과 제어**: 압축(NONE, GZIP, ZSTD), 스토리지 클래스(S3 Standard, S3 Intelligent-Tiering, S3 Glacier Instant Retrieval), 오브젝트 키 템플릿(예: 날짜 프리픽스 + 파티션/오프셋)을 선택할 수 있다. 레코드는 프로듀서가 쓴 형식을 그대로 유지한다(JSON, UTF-8 문자열, 원시 바이트) — 스키마 레지스트리도 필요 없다. JSON/String 레코드는 검증되며, 실패 시 DLQ로 라우팅된다.
- **버킷을 넘어서**: Express 브로커는 스트리밍 테이블에도 전달한다 — Apache Iceberg 테이블로 지속 구체화되어 Amazon S3 Tables에 저장되고 AWS Glue Data Catalog에 자동 등록되며, Athena·Redshift·Spark에서 질의할 수 있다. 인라인 컴팩션으로 다운스트림 쿼리 비용을 최대 30% 절감한다. 전달이 브로커 부하를 늘리지 않으므로 한 토픽이 S3 버킷과 스트리밍 테이블 양쪽을 동시에 공급할 수 있다.
- **시작하기**: MSK 콘솔에서 채널을 만든다(Channel 탭, 목적지 = 범용 S3). 또는 `aws kafka create-channel` 등 MSK API/CLI를 IaC로 관리할 수 있다. 오픈소스 `managing-amazon-msk` Agent Skill(Agent Toolkit for AWS)은 에이전트가 IAM 역할·트러스트 정책, 키 템플릿 규칙, DLQ 설정, 전달 검증까지 안내한다. 기존 커넥터에서 전환한다면 전달 데이터가 겹치는 것을 확인할 때까지 둘 다 운영한다.

## 세부 내용

Kafka→S3 아카이빙의 두 난제는 브로커 운영과 전달 파이프라인이며, 이 글은 둘 다 다룬다. 브로커 측면에서는 Express가 스토리지 산정, 브로커 복구, 구성 관리, 유지보수 창을 없애 주고, MSK Replicator와 migrate-to-MSK Agent Skill이 자체 관리/서드파티 Kafka를 Express 클러스터로 옮길 때 적정 크기 권장을 제공한다. 파이프라인 측면에서는 채널 모델이 Connect 계층을 아예 없앤다.

아키텍처상 프로듀서는 그대로 쓰고, 채널이 읽고 배칭해 소스 형식 그대로 버킷에 오브젝트를 기록한다. JSON/String 레코드는 검증되고 실패 시 DLQ로 간다. 전달 로그와 메트릭은 CloudWatch(Logs, 메트릭)로 노출되며 S3나 Data Firehose로도 보낼 수 있고, 문제 해결은 채널의 CloudWatch 메트릭·로그 한 곳에서 한다. 컴플라이언스·감사 보존은 원시 이벤트를 S3에 수년간 보관해 충족하고, 리플레이는 아카이브가 S3에 있으므로 토픽 보존 기간과 무관하게 가능하다.

마이그레이션 참고: 계획 전에 Amazon MSK Developer Guide의 "Requirements and supported configurations"에서 지원 Region·계정·구성을 확인하고, 전환 시에는 기존 커넥터를 데이터가 겹칠 때까지 함께 운영하라.

## 참고 자료

- 원문: [Deliver petabytes of Apache Kafka data to Amazon S3 at up to 60% lower cost with Amazon MSK Express brokers](https://aws.amazon.com/blogs/big-data/deliver-petabytes-of-apache-kafka-data-to-amazon-s3-at-up-to-60-lower-cost-with-amazon-msk-express-brokers)
