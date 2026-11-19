---
title: "Amazon MSK Express 브로커, AWS Graviton4 기반 M8g 인스턴스에서 제공"
description: "Graviton4 M8g 인스턴스의 Amazon MSK Express 브로커는 브로커-시간 요금을 15% 낮추고 브로커 측 교차-AZ 클라이언트 요금을 없애(교차-AZ 전송 50% 절감) 24xlarge 크기를 추가했으며, 테스트에서 P99 produce 지연 21–54% 감소와 브로커 CPU 9–11%p 감소를 보였다."
tags: [source, article, aws-big-data, kafka, msk, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/amazon-msk-express-brokers-available-on-aws-graviton4-based-m8g-instances"
blog: aws-big-data
published_date: 2026-11-19
---

# Amazon MSK Express 브로커, AWS Graviton4 기반 M8g 인스턴스에서 제공

**Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/amazon-msk-express-brokers-available-on-aws-graviton4-based-m8g-instances)
**게시일**: 2026-11-17

## 개요

Apache Kafka 팀은 흔히 성능과 비용을 맞바꾸게 된다. Amazon MSK Express 브로커가 AWS Graviton4 기반 M8g 인스턴스에서 제공되며 두 가지를 동시에 제공한다. M7g 대비 브로커-시간 요금 15% 인하, 교차-AZ 클라이언트 트래픽에 대한 브로커 측 요금 면제(교차-AZ 데이터 전송 비용 총액 50% 절감), 그리고 더 큰 여유를 주는 새로운 24xlarge 크기다. 동일 크기·동일 부하 테스트에서 M8g의 P99 produce 지연은 21–54% 낮았고, 브로커 CPU는 9–11%p 낮았으며, 뒤처진 컨슈머는 30분 만에 최대 3배 많은 적체를 해소했다.

## 주요 내용

- M8g Express 브로커는 M7g Express 브로커가 지원하는 모든 것을 유지한다: 동일한 Kafka 버전, 인증 방식, 사용자 정의 구성, CloudWatch 지표, Prometheus 기반 Open Monitoring.
- 같은 크기에서 브로커당 처리량, 연결 수 제한, data-in/스토리지 요금은 M7g와 동일하다. 현재 크기 그대로 M8g로 옮겨도 브로커당 처리량을 유지할 수 있다.
- 브로커-시간 요금은 각 크기에서 15% 저렴하다(US East (N. Virginia) 기준 express.m8g.large $0.347/시간 vs express.m7g.large $0.408/시간). data-in 및 스토리지 요금은 변하지 않는다.
- 교차-AZ 클라이언트 트래픽: AWS가 브로커 측 요금을 더 이상 부과하지 않으므로 클라이언트↔브로커 교차-AZ 비용은 총 $0.01/GB(기존 $0.02/GB)로 50% 낮아진다. 랙 인식(replica.selector.class=org.apache.kafka.common.replica.RackAwareReplicaSelector, client.rack에 AZ ID 설정)을 쓰면 컨슈머가 로컬 복제본에서 읽으므로 produce 측 $0.01/GB만 남는다.
- 크기는 express.m8g.large(2 vCPU, 8 GiB, 권장 인그레스/이그레스 15.6/31.2 MBps, 권장 파티션 1,000개 / 최대 1,500개)부터 24xlarge까지. M7g의 최대는 16xlarge였다. 크기별로 권장 파티션·처리량 한도가 적용된다.
- 비용 예시: us-east-1에서 large 브로커 3대, 30 MBps 인그레스, 컨슈머 그룹 2개(교차-AZ 트래픽 약 155,520 GB)인 30일 기준, 브로커 시간 $749.52(M8g) vs $881.28(M7g), 교차-AZ produce 트래픽 $518.40 vs $1,036.80.
- 양 세대 모두에서 제공되는 크기의 브로커당 스토리지·네트워크 처리량은 M7g Express 브로커와 같다.

## 상세

- Express 브로커는 Standard 브로커 대비 브로커당 최대 3배 처리량, 최대 20배 빠른 확장, 최대 90% 빠른 복구를 제공하며 스토리지와 브로커 튜닝을 AWS가 관리한다.
- 벤치마크는 large 크기에서만 수행되었다. AWS는 M8g에서 테스트용 Express 클러스터를 만들어 자체 워크로드를 실행해 본 뒤, 사용 후 삭제할 것을 권장한다.
- Express M8g는 large부터 24xlarge까지 크기를 제공하며, 크기별 권장 인그레스/이그레스 처리량과 파티션 수가 다르다. 크기를 정하기 전에 AWS 문서의 전체 표를 확인해야 한다.
- 마이그레이션은 같은 크기로 클러스터를 M8g로 옮기는 것이다. Kafka 버전·인증·구성이 그대로 이어지므로 애플리케이션 변경이 필요 없다.
