---
title: "차세대 프로토콜로 Amazon MSK 컨슈머 리밸런싱 최적화하기"
description: "Kafka 4.0의 KIP-848 서버 주도 컨슈머 프로토콜을 MSK에서 활성화해 리밸런스 스톰을 없애고, 잔여 저속 리밸런스 진단법 정리."
published: "2026-10-01"
source_url: "https://aws.amazon.com/blogs/big-data/optimize-consumer-rebalancing-on-amazon-msk-with-next-generation-protocol"
blog: aws-big-data
locale: ko
tags: [source, aws-big-data, msk, kafka, ko]
---

# 차세대 프로토콜로 Amazon MSK 컨슈머 리밸런싱 최적화하기

## 개요

기존 Kafka 리밸런스 프로토콜은 멤버 하나가 들어오거나 나가면 전체 컨슈머를 전역 동기화 장벽 뒤에서 멈추게 해서, 대규모 그룹에서 리밸런스 스톰을 일으킨다. Kafka 4.0의 KIP-848 컨슈머 프로토콜은 조율을 브로커 측 그룹 코디네이터로 옮기고 지속 하트비트와 증분 서버 주도 조정으로 영향받는 파티션만 이동시킨다. Kafka 4.x의 MSK Standard·Express 브로커에서 쓸 수 있으며, 대규모 그룹, 고가용성 워크로드, 빈번한 재배포 환경, 동적 파티션 확장에 효과가 크다.

## MSK에서 활성화하기

클러스터가 Kafka 4.0 이상인지 확인하고, 클라이언트에 `group.protocol=consumer`를 설정한다(기본값은 classic). 서버가 관리하게 된 클라이언트 설정(`heartbeat.interval.ms`, `session.timeout.ms`, `partition.assignment.strategy`)은 제거한다. 하트비트·세션 타임아웃은 서버 측 설정이다. 클라이언트 지원 여부부터 확인한다. Java 4.0+, confluent-kafka-python 2.12.0+, librdkafka 기반 2.12.0+다. 롤링 재시작으로 그 자리에서 전환할 수 있고, 코디네이터는 두 프로토콜 멤버를 나란히 처리한다.

## 저속 리밸런스 진단

먼저 CloudWatch 브로커 로그로 실제 프로토콜을 확인한다. 컨슈머 프로토콜은 epoch·타깃 할당·fencing 언급이, classic은 `PreparingRebalance`와 리더 할당이 특징이다. KIP-848이 켜져 있는데도 느리면, 세션 타임아웃 만료(기본 45초, 서버 측 관리)가 흔한 원인이다. 특히 컨테이너에서 `consumer.close()` 없이 죽는 정적 멤버가 그렇다. SIGTERM 우아한 종료 처리 누락, 불안정 컨슈머의 들락날락도 원인이다. 대응은 우아한 종료와 충분한 Kubernetes 종료 유예, `group.instance.id` 기반 정적 멤버십으로 빠른 재시작 시 재할당 생략, 정상 운영 중 타임아웃이면 컨슈머 멈춤 원인 추적이다. 브로커 로그, CloudWatch lag 지표, 컨슈머 그룹 조회로 검증한다.

## 참고 자료

- [원문: Optimize consumer rebalancing on Amazon MSK with next generation protocol](https://aws.amazon.com/blogs/big-data/optimize-consumer-rebalancing-on-amazon-msk-with-next-generation-protocol)
- [KIP-848: The Next Generation of the Consumer Rebalance Protocol](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/217387038/KIP-848+The+Next+Generation+of+the+Consumer+Rebalance+Protocol)
