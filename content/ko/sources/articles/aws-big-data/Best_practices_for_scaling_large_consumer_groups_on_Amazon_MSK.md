---
title: "Amazon MSK에서 대규모 컨슈머 그룹 확장을 위한 모범 사례"
description: "컨슈머 그룹 메타데이터 크기를 추정하고 내부 토픽 한도를 올려 MSK 리밸런스 실패를 방지합니다." (한국어 번역)
tags: [source, aws-big-data, kafka, msk, ko, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/best-practices-for-scaling-large-consumer-groups-on-amazon-msk"
blog: aws-big-data
published_date: 2026-09-22
---

# Amazon MSK에서 대규모 컨슈머 그룹 확장을 위한 모범 사례

## 개요

MSK의 대규모 Kafka 컨슈머 그룹은 리밸런스 때 내부 `__consumer_offsets` 토픽에 쓰는 `GroupMetadata` 레코드가 기본 1MB 한도를 넘으면 `RecordTooLargeException`과 리밸런스 재시도 루프에 빠질 수 있습니다. 이 글은 메타데이터가 커지는 이유와 크기 추정법, 네 가지 대응책(한도 상향·그룹 분할·파티션/오토스케일링 적정화·네이밍 정리), 용량 계획·모니터링, 장기 해법인 KIP-848을 정리합니다.

## 메타데이터가 커지는 이유

리밸런스 때 그룹 코디네이터는 멤버별 구독 토픽·보유 파티션·새 할당·클라이언트 ID를 담은 레코드 하나를 `__consumer_offsets`에 비압축으로 저장합니다. Kafka 직렬화 형식은 멤버마다 토픽명을 세 번 반복하고 클라이언트 ID가 멤버당 오버헤드를 더합니다. 대략식:

**레코드 크기 ≈ 멤버 수 × (3 × 토픽명 바이트 + 2 × 클라이언트 ID 바이트 + 약 200바이트)**

멤버 1,000명, 토픽명 50바이트, 클라이언트 ID 40바이트면 이미 약 430KB이며, 이름이 길거나 다중 토픽 구독이면 2,000명 훨씬 전에 1MB를 넘습니다.

## 핵심 처방: 한도 상향

이미 한도를 넘은 그룹에 가장 직접적인 처방입니다:

1. `kafka-configs.sh`로 `__consumer_offsets`의 `max.message.bytes`를 상향(예: 2MB).
2. MSK 클러스터 설정에서 브로커 수준 `replica.fetch.max.bytes`를 같은 값 이상으로 맞춰 팔로워 복제가 가능하게 합니다. 그렇지 않으면 `UnderReplicatedPartitions`가 발생합니다.
3. 비프로덕션에서 먼저 검증: 리밸런스를 유발하고 예외가 없는지, 힙 사용량·복제 지연이 건전한지 확인.

## 보완 전략

- **대규모 그룹 분할:** 서로 다른 `group.id`로 파티션 부분집합을 소비하는 컨슈머를 여러 개 배포합니다. 그룹당 메타데이터가 비례해 줄고, 대신 운영할 그룹이 늘어납니다.
- **파티션 수와 오토스케일링 상한 적정화:** 과도한 파티션은 컨슈머를 늘리고, 무제한 오토스케일링은 그룹을 계획 밖으로 키웁니다. 복제본 상한을 두고 파티션 수를 의도한 최대 컨슈머 수에 맞춥니다. 토픽 설계 시점에 적용하는 것이 가장 좋습니다.
- **네이밍 최적화:** 짧고 표준화된 그룹·클라이언트 ID가 멤버당 오버헤드를 줄이지만, 활성 그룹 개명은 커밋된 오프셋을 잃으므로 신규 배포에 주로 유효합니다.

## 용량 계획, 모니터링, KIP-848

현재 크기를 계산하고 오토스케일링 상한에서 피크 멤버십을 예측한 뒤 2배 안전 마진을 적용해 한도와 브로커 사양을 정합니다(500~1,000명대는 `kafka.m5.xlarge` 이상, 그 이상은 `m5.2xlarge` 이상, 2,000명 초과는 분할 병행). `HeapMemoryAfterGC`(60% 경고·80% 치명 알람), `UnderReplicatedPartitions`(5분 이상 0 초과 시 알람), GC 일시정지, 리밸런스 빈도, 컨슈머 랙을 관찰합니다.

장기적으로 Kafka 4.0의 KIP-848이 서버 측 할당을 기본 프로토콜로 삼아 멤버당 메타데이터를 줄이고 점진적 리밸런스를 제공합니다. MSK 버전 지원 추적, 클라이언트 호환성 확인, 비프로덕션 테스트, 비중요 그룹부터의 단계적 전환으로 준비합니다.

## References

- 원문: [Best practices for scaling large consumer groups on Amazon MSK](https://aws.amazon.com/blogs/big-data/best-practices-for-scaling-large-consumer-groups-on-amazon-msk)
