---
title: "ODA 웜 처리량으로 Kinesis Data Streams 온디맨드 용량 축소하기"
description: "Kinesis 온디맨드 Advantage 스트림의 웜 처리량 축소 신기능: 버스트 후 샤드 용량 해제, 최근 1시간 피크 하한선, CloudWatch 모니터링."
published: "2026-09-14"
source_url: "https://aws.amazon.com/blogs/big-data/scale-down-kinesis-data-streams-on-demand-capacity-with-oda-warm-throughput/"
blog: "AWS Big Data"
locale: "ko"
tags: [aws, kinesis, streaming, serverless, cost-optimization, cloudwatch, ko]
---

# ODA 웜 처리량으로 Kinesis Data Streams 온디맨드 용량 축소하기

[English version](../../../../en/sources/articles/aws/Scale_Down_Kinesis_Data_Streams_On_Demand_Capacity_with_ODA_Warm_Throughput.md)

**저자**: Pratik Patel, Varsha Palepu, Priyanka Chaudhary · **발행**: 2026-09-14 · **출처**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/scale-down-kinesis-data-streams-on-demand-capacity-with-oda-warm-throughput/)

## 문제

Kinesis 온디맨드 모드는 버스트에 자동 확장되지만(샤드 분할), 일시적 스파이크가 끝난 뒤에도 높아진 용량이 그대로 남았다 — 플래시 세일, 배치 마이그레이션, IoT 펌웨어 버스트 등. 글의 예: 100 MB/s 스트림(100 샤드)이 +50 MB/s 스파이크로 150 샤드가 되면, 스파이크 후에도 150 샤드가 유지된다. 병렬화 계수 2의 Lambda 컨슈머는 호출량이 200→300 (+50%)으로 뛰고(쿼터·비용 압박, 작은 배치 처리), KCL 컨슈머는 샤드당 DynamoDB 리스(하트비트마다 스캔/갱신/체크포인트)를 더 먹는다. 기존 탈출구는 프로비저닝 모드 전환(자동 확장 포기) 또는 초과분 감수뿐이었다.

## 해법: 웜 처리량 축소

온디맨드 Advantage (ODA) 스트림이 웜 처리량을 낮춰 용량 축소를 트리거할 수 있게 됐다. 추가 비용 없음. 최종 용량 = max(요청한 웜 처리량, 최근 1시간 피크 수집에 필요한 용량) — 실시간 트래픽 과소 프로비저닝 방지용 하한선. 축소 후에도 반응형 확장은 새 증가에 계속 대응한다. 웜 처리량은 이제 양방향이다: 예측 이벤트 앞당긴 확장(기존) + 일시 현상 후 축소(신규).

## 구현

**사전 요구사항**: 기존 온디맨드 스트림, ODA 모드 on, AWS CLI, `kinesis:UpdateStreamMode` 권한.

```bash
aws kinesis update-stream-mode \
  --stream-arn arn:aws:kinesis:us-east-1:111122223333:stream/my-stream/my-stream \
  --warm-throughput-in-mb 50
```

**모니터링** (CloudWatch): `IncomingBytes` (Sum, 집계 처리량), `IncomingRecords` (트래픽 패턴/버스트 빈도), `WriteProvisionedThroughputExceeded` (축소 후 0이 아니면 목표치가 너무 낮음). 샤드 수는 CloudWatch 지표가 *아니다* — `DescribeStreamSummary` (`OpenShardCount`) 또는 콘솔로 폴링하고, 필요하면 Lambda 기반 커스텀 지표로. 예상 타임라인: 정상 상태(예: 20 MiB/s에 ~67개 오픈 샤드) → 버스트(분할, `OpenShardCount` + `IncomingBytes` 상승) → 버스트 후 고원(트래픽은 복귀, 샤드는 여전히 높음 — 최근 피크의 ~2배 유지) → 축소 후 병합(요청치 방향으로 감소, 1시간 피크가 하한).

## 베스트 프랙티스

1. 목표치를 정하기 전 **24시간 `IncomingBytes`/`IncomingRecords` 분석** — 베이스라인 파악이 먼저.
2. 평균이 아니라 **정상 피크 이상을 목표**로 — 온디맨드는 관측 피크의 ~2배를 수용하므로 정상 변동 여유를 둔다.
3. 축소 후 수 시간 ** `WriteProvisionedThroughputExceeded` 감시** — 스로틀링 시 다시 확장(자동 복구도 있지만 모니터링이 임팩트 단축).
4. **식별된 일시 현상 후** 사용 (마이그레이션, 마케팅 이벤트, 백필). 불확실/증가 중인 트래픽에서는 자제.
5. 확신 없으면 **1시간 하한선을 활용** — 낮은 값을 설정하고 피크 하한선이 과소 프로비저닝을 막게 한다.

## 왜 중요한가

- **컨슈머 비용 통제**: 샤드 수가 Lambda 동시성과 KCL/DynamoDB 오버헤드를 결정하므로, 웜 처리량 튜닝은 곧 하류 컴퓨트 튜닝이다.
- **대칭이 된 탄력성**: 온디맨드가 확보뿐 아니라 해제까지 하게 돼, 자동 확장의 이점을 잔여분 없이 유지한다.
- **운영 단순성**: 프로비저닝 모드 마이그레이션 대신 CLI 값 하나로 해결.

## 세미나 시사점

- 공식을 기억하라: 최종 용량 = max(요청치, 최근 1시간 피크 필요량).
- 샤드 수가 숨은 비용 레버다. 바이트가 아니라 API의 `OpenShardCount`를 플롯할 것.
- 축소는 식별된 일시 현상 후의 사후 조치이지, 평소 돌리는 다이얼이 아니다.

## 관련 개념

- `concepts/data-engineering/stream-processing.md`, `concepts/data-engineering/apache-kafka.md`

## 참고 자료

- [Amazon Kinesis Data Streams 온디맨드 Advantage 출시](https://aws.amazon.com/blogs/big-data/amazon-kinesis-data-streams-launches-on-demand-advantage-for-instant-throughput-increases-and-streaming-at-scale/)
- [개발자 안내서의 온디맨드 용량 모드](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html)
- [DescribeStreamSummary API](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_DescribeStreamSummary.html)
