---
title: 규모라는 저장 난제를 푼 Twitter Sparrow
description: 시간 단위 배치에서 스트리밍으로 이벤트 파이프라인을 재설계해 지연을 수 시간에서 수 초로 줄인 Sparrow 프로젝트
tags: [source, twitter, x, streaming, beam, dataflow, pubsub, bigquery, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/twitter-sparrow-tackles-data-storage-challenges-of-scale"
blog: twitter
date: '2022-06-28'
---

# 규모라는 저장 난제를 푼 Twitter Sparrow

## 요약

Twitter는 수만 마이크로서비스에서 매일 수조 이벤트(모든 클릭·스와이프·스크롤)를 로깅했고, 기존 배치 수집 파이프라인은 처리량 최적화(분당 수십억 이벤트) 대가로 소비 가능까지 **수 시간**의 종단 지연을 냈다. 2020년 Hack Week 프로젝트에서 출발한 **Sparrow**(Lohit Vijayarenu, Zhenzhao Wang 팀)는 파이프라인을 스트리밍 우선으로 재설계해 지연을 **분·초 단위**로 줄이면서도 과거 처리를 위한 배치 접근을 유지했다. IEEE BigData 2021 논문 *"Twitter Sparrow: Reduce Event Pipeline latency from hours to seconds"* 로 발표됐다.

## 아키텍처: 전후 비교

- **이전**: 서비스 → 배치 집계(온프레미스 Flume/Kafka 계열 단계, HDFS/Tez/Mesos) → 수 시간 늦은 고정 목적지 전달. 클라우드 발생 데이터 미지원.
- **이후(스트리밍 우선)**: **스트리밍 이벤트 애그리게이터**가 로그 이벤트를 수집해 Kafka·Google Pub/Sub에 발행(전송 중 압축, 온프레미스·클라우드 투명한 통합 클라이언트 라이브러리, 교체 가능한 메타데이터 관리). **스트리밍 이벤트 프로세서** 계층(데이터셋당 Apache Beam 작업 1개 + 구독 1개)이 큐를 읽어 변환·포맷 전환(thrift → Avro → TableRow, 전체 Dataflow/MR 작업 없이 가벼운 ETL을 위한 UDF/SQL 지원)을 적용하고 **BigQuery·GCS·Kafka/PubSub**에 스트리밍 — 실시간과 과거 소비자를 동시에 serve. 프로세서 플릿은 Airflow가 오케스트레이션.

## Google Cloud에서 Twitter 규모 운영하기

Sparrow 처리량 목표(연 ~50% 성장에 분당 30~50억 이벤트, 단일 데이터셋 10~18GB/s·초당 수천만 건, 단일 Beam 작업 최대 ~20GB/s)는 Cloud 컴포넌트의 기본 성능을 넘었다. 최적화: BigQuery IO 커넥터의 셔플 제거(Beam 리소스 −80~86%, Dataflow 팀과 협업), Pub/Sub 처리 전 데이터 압축(워커 사용량 ~−20%), 중첩 thrift→Avro→TableRow 스키마 변환 간소화. 함께 추가된 가드레일: PDP(개인정보 보호) 준수, 과금 지원, 비용 추정기 — 투명한 기존 고객 마이그레이션을 곁들인 무관리형 서비스로 제공.

## 결과

GCP의 저지연 스트리밍 수집 파이프라인으로 실시간에 가까운 질의(예: 실시간 사용자 행동 분석)가 가능해졌다 — 이전에는 물을 수 없던 질문이다. 장기 윈도우 리포트를 위한 배치 의미는 유지됐다.

## SW 엔지니어를 위한 시사점

- 처리량 최적 배치 파이프라인은 제품 반복을 막는 지연 부채를 쌓는다. 같은 이벤트에서 배치 소비자를 계속 serve하는 스트리밍 우선 재설계로 상환한다.
- 극한 규모에서는 관리형 클라우드 컴포넌트와의 공동 엔지니어링(맞춤 IO 커넥터, 압축 위치, 스키마 변환 튜닝)이 필요하다. 제공자와 공동 최적화 예산을 잡는다.
- 가벼운 변환에는 전체 파이프라인 작업 작성을 강제하지 말고 함수/SQL 수준 ETL 훅을 제공한다. 마이그레이션 최대 채택 장벽을 없앤다.
- 컴플라이언스(PDP)·과금·비용 추정은 후속이 아니라 플랫폼의 일부로 배송한다. 그래야 마이그레이션이 실제로 출하 가능하다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/twitter-sparrow-tackles-data-storage-challenges-of-scale (Daniel Templeton, 2022-06-28)
- 논문: Lohit VijayaRenu 외, *Twitter Sparrow: Reduce Event Pipeline latency from hours to seconds*, IEEE BigData 2021, https://doi.org/10.1109/bigdata52589.2021.9671438
- 관련: `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-kafka.md`
