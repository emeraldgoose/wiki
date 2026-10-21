---
title: "Delivery Hero가 Apache Flink로 실시간 광고 측정을 재구축한 방법"
description: "Delivery Hero가 시간 단위 배치를 실시간 Flink 스트리밍으로 바꿔 비용 57% 절감과 수 초 내 측정을 달성했습니다."
tags: [source, aws-big-data, flink, streaming, kinesis, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-delivery-hero-rebuilt-real-time-ad-measurement-with-apache-flink"
blog: aws-big-data
published_date: 2026-09-24
---

# Delivery Hero가 Apache Flink로 실시간 광고 측정을 재구축한 방법

## 개요

약 65개국·150만 이상 파트너를 둔 베를린 기반 배달 플랫폼 Delivery Hero(2025년 광고 매출 약 15억 유로)가 광고 측정을 시간 단위 배치에서 Amazon Managed Service for Apache Flink 기반 실시간으로 옮겼습니다. 모든 노출·클릭은 정산 가능한 정확도와 광고 서버가 즉시 행동할 수 있는 신선도를 동시에 만족해야 하며, 새 파이프라인은 비용을 약 57% 줄이면서 기존 시스템이 도달 못한 데이터 품질을 달성했습니다.

## 기존 시스템의 문제

트래픽(초당 수만 메시지, 일 수십억 이벤트)이 커지며 다섯 가지 구조적 문제가 쌓였습니다. 이벤트 발생 시각이 아니라 처리 시각으로 버킷팅했고(노출의 91%가 신뢰할 만한 타임스탬프 부재), ROAS 같은 시간 민감 지표 오차가 커졌으며 이벤트-기록 간격이 평균 61분에 달했습니다. 보강(enrichment)이 이벤트마다 블로킹 API 호출이라 백프레셔 없이 급증이 정산·서빙·리포팅에 연쇄 파급됐습니다. 가끔씩 접근하던 문서 DB에 이벤트마다 전체 문서 읽기·쓰기가 걸려 읽기/쓰기 증폭·비용 증가·피크 장애가 났습니다. 재처리는 시스템마다 별도 작업이었고(수제 정산 리플레이, 일별 Airflow 리포팅 리플레이, 일부 이벤트는 리플레이 경로 자체가 없음), 베스트에포트 보강은 불량 이벤트를 그대로 통과시켜 세션 ID 30~40% 누락·고객 ID 5% 누락으로 하류 ML 피처를 오염시켰습니다.

## Managed Flink를 선택한 이유

세 가지 비협상 조건이 선택을 이끌었습니다. 데이터 손실 없는 내결함성 처리, 수일치 이력을 저렴하고 빠른 저장소에 두는 상태 있는 스트림 처리, 완전 관리형 인프라입니다. Flink가 앞의 둘을 네이티브로 제공합니다. 뒤늦은 이벤트를 제자리에 두는 이벤트타임 워터마크와 힙 압박 없이 대용량 키 상태(keyed state)를 디스크에 두는 RocksDB 상태 백엔드입니다. 관리형 서비스가 JobManager·TaskManager·체크포인트 운영을 없앱니다. 인제스천은 이 토폴로지에서 MSK보다 비용 효율적인 Kinesis Data Streams 2개(사용자 행동·주문), 참조 데이터는 DynamoDB를 Async I/O로, 복호화 키는 Secrets Manager, Avro 이벤트 로그와 점증 체크포인트는 S3, MVP 단계의 SQS→Kinesis 연결은 무코드 EventBridge Pipes로 2주를 단축했습니다.

## 파이프라인과 성과

Java 파이프라인 5단계: 광고 토큰 복호화, 30시간 RocksDB 윈도우 중복 제거(약 20GB, 감사본은 S3 보관), DynamoDB 동시 보강, 수일 키 구간 조인 어트리뷰션(약 100GB 상태, 어트리뷰션된 주문을 S3에 배출), 5분마다 리포팅 DB에 메트릭 일괄 업서트이며, CPM/CPC 정산 이벤트는 Kafka로 광고 서버·예산 서비스에 전달됩니다. 최소 한 번 전달에 중복 제거 단계를 더해 사실상 정확히 한 번 정산을 달성하고, S3 체크포인트로 장애 후 복원합니다.

성과: 이벤트-기록 간격이 61분에서 1.2초로, 월 비용이 약 57% 감소, 비동기 보강으로 피크 초당 2만 메시지를 상류 역압 없이 소화, S3 원시 이벤트 보관과 7일 Kinesis 보존으로 재처리가 팀 간 조율 작업이 아닌 결정적 재실행이 됐습니다. 데이터 품질 격차도 크게 좁혀졌습니다. 세션 누락 30~40%→0%, 고객 ID 누락 5%→0.8%, 노출 타임스탬프 누락 91%→0.2%로, 랭킹·전환율·이상감지 모델에 완전한 세션 맥락이 공급됩니다. 다음 단계는 더 많은 광고 포맷, 초 단위 예산 페이싱, 개인화·LLM 추천용 실시간 스트림 확장입니다.

## References

- 원문: [How Delivery Hero rebuilt real-time ad measurement with Apache Flink](https://aws.amazon.com/blogs/big-data/how-delivery-hero-rebuilt-real-time-ad-measurement-with-apache-flink)
