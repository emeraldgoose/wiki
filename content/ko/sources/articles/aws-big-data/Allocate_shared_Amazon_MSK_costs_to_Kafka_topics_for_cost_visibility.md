---
title: "공유 Amazon MSK 비용을 Kafka 주제별로 집계하여 비용 가시성 확보"
description: "클러스터 수준의 Amazon MSK 요금을 비용 및 사용 보고서(CUR)에서 가져와 Kafka 주제 처리량 비율로 분배해 팀별 비용 비중을 보여주는 서버리스 파이프라인."
tags: [source, aws-big-data, kafka, msk, cost-allocation, cost-visibility, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility"
blog: aws-big-data
published_date: 2026-11-12
---

# 공유 Amazon MSK 비용을 Kafka 주제별로 집계하여 비용 가시성 확보

**원문**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility) · **게시일**: 2026-11-11

## 개요

Amazon MSK는 클러스터 수준에서 요금을 매기며, 클러스터당 요금 항목이 하나씩 나온다. 한 클러스터를 여러 팀이 쓰고 각 팀이 각자의 Kafka 주제를 소유하는 경우, 그 항목만으로는 누가 얼마나 쓰는지 알 수 없다. 이 글은 비용 및 사용 보고서(CUR)의 클러스터 수준 요금에 Kafka 주제별 처리량 지표를 결합하여 팀별 비용 비중을 산출하는 방법을 보여준다.

핵심 아이디어는 비례 분배다. 클러스터와 일별로, 파이프라인은 각 주제의 진입 바이트 비율을 계산해 그날의 클러스터 비용에 곱한다. 브로커 컴퓨팅과 스토리지 비용은 별도로 계산한다.

```
주제 실행 비용 = 일일 브로커 비용 × (주제 바이트 / 클러스터 전체 바이트)
주제 스토리지 비용 = 일일 스토리지 비용 × (주제 바이트 / 클러스터 전체 바이트)
```

처리량이 30%를 차지하는 주제에 비용의 30%를 할당하며, 할당액은 항상 그날 전체 비용을 합한다. 부분 장애 시에는 지표가 구성된 주제에만 비용을 분배하며, `allocation_method` 열로 그 동작을 기록한다.

## 핵심 내용

- 파이프라인은 일일 Lambda 함수로 5단계로 동작한다. CUR에서 클러스터 ARN과 일별 클러스터 비용을 읽고, ListClustersV2로 클러스터 이름과 ARN을 연결하며, 각 주제의 일일 처리량을 읽고, 비례 분배하고, 결과를 S3에 Parquet으로 기록해 Athena 테이블을 갱신하고 Quick Sight로 시각화한다.
- 주제별 사용량 수집은 환경 변수 하나로 선택하는 두 가지 방식이 있다. 향상된 모니터링(Enhanced Monitoring, PER_TOPIC_PER_BROKER로 CloudWatch에 지표 게시) 또는 Amazon MSK 오픈 모니터링에 Amazon Managed Service for Prometheus를 사용하는 방법이다. 오픈 모니터링은 추가 요금 없이 JMX 지표를 긁어오며, 주제 수가 늘어날수록 지표 비용 증가도 낮다.
- 주제 발견(Topic Discovery)은 네 단계 계층 구조를 따른다. 환경 변수의 정적 주제 맵, MSK ListTopics API, CloudWatch ListMetrics, 또는 전날 할당 출력을 사용하는 방식이다. 향상된 모니터링을 쓰지 않아도 함수가 동작한다.
- 비용 가이드: 모니터링 비용이 MSK 지출의 5% 미만이면 옵션 A를, 10% 이상이면 옵션 B의 초기 비용이 빠르게 회수된다. 정확한 청구 분담이 필요한 클러스터에만 향상된 모니터링을 켜고, 필요하면 환경 변수 하나로 옵션 B를 다시 쓸 수 있다.
- 이 파이프라인은 다중 계정 환경으로도 확장된다. 중앙 계정에서 통합 CUR을 읽고, Lambda가 각 구성원 계정의 읽기 전용 역할을 맡아 클러스터를 나열하고 사용량을 읽으며, 모든 구성원 계정의 스크래퍼에서 온고잉 쓰기(remote-write)를 받는 단일 중앙 Prometheus 워크스페이스가 존재한다.
- 두 가지 트리거가 복원력을 제공한다. 새 CUR Parquet 파일이 도착하면 S3 이벤트 알림이 작동하고, CUR 배송이 지연될 때를 대비해 Amazon EventBridge가 매일 06:00 UTC에 일정 규칙을 실행한다.
- 유휴 주제는 행을 생성하지 않는다. 20개 중 3개만 트래픽을 보고하면 그 3개가 전체 비용을 흡수하며, 할당 방법 열로 이를 표시한다. 클러스터-일 단위로 트래픽을 보고하는 주제가 없으면 모든 구성된 주제에 균등하게 배분한다.

## 상세

해결책에는 트래픽을 처리하는 주제를 가진 Amazon MSK 프로비저닝 클러스터가 필요하다. Amazon MSK 서버리스는 범위 밖이다. 요금 방식이 다르고 주제별 BytesInPerSec를 노출하지 않기 때문이다. 그 외 필요 조건은 CUR(또는 CUR 2.0용 AWS 데이터 내보내기)가 리소스 ID를 활성화하여 S3에 Parquet을 전달하고, CUR 데이터 위에 올바른 파티션 설정을 둔 Glue 카탈로그 테이블, Lambda 함수, IAM 역할, Athena 테이블, Quick Sight 리소스를 생성할 권한, 그리고 SPICE 데이터셋과 행 수준 보안을 위한 Quick Sight Enterprise 에디션이다.

Lambda 함수는 Python 3.11, 1GB 메모리, 10분 제한시간이며, Parquet 처리를 위해 AWS SDK for pandas 계층을 사용한다. CUR은 Athena를 통해 읽으며, 파티션 열로 필터링해 Athena가 전체 파티션을 정리(prune)하게 한다. `line_item_product_code = 'AmazonMSK'` 및 `line_item_resource_id LIKE 'arn:aws:kafka:%'`로 필터링하고, AWS가 첫 배송 이후 CUR 항목을 업데이트할 수 있으므로 두 개월치를 읽는다. 결과는 청구 기간별로 파티션된 Snappy 압축 Parquet으로 기록되며, 각 실행이 해당 청구 기간 파일을 덮어쓰기해 CUR 재배송 시 이중 계수를 막는다. 할당된 총액을 청구된 클러스터 비용과 비교하는 대조 쿼리가 있고, 빈 결과면 할당이 일치한다는 의미다.

보고 계층은 Athena 데이터 소스를 Quick Sight SPICE 데이터셋으로 가져오고, 팀·주제·월별 비용 상세 테이블, 클러스터·주제·기간 필터 컨트롤, 클라이언트 ID 기준 행 수준 보안(팀이 자신의 숫자만 보게 함)을 포함한다. 소유자는 주제 명명 규칙에서 유추되며, 규칙이 실패하면 명시적 주제-팀 매핑을 쓸 수 있다.

파이프라인 자체는 Lambda, Athena, S3, EventBridge가 적어 비용이 낮지만 두 가지 항목이 지배적이다. 지표 소스의 경우 예시 클러스터에서 옵션 A가 월 약 90달러, 옵션 B가 약 11달러다. Quick Sight 사용자 라이선스는 접근하는 사람 수에 따라 규모가 커지며 종종 최대 비용이 된다. 금융 데이터는 SSE-KMS로 정지 시 암호화하고 TLS로 전송 시 암호화하며, 여기에는 스크래퍼 원격 쓰기와 Athena 연결도 포함된다. 옵션 B의 경우 포트 11001은 스크래퍼의 보안 그룹으로 제한해야 한다. 데이터 전송, 계층별 스토리지, MSK Connect 같은 미할당 요금은 재무팀이 전체 그림을 볼 수 있도록 명시적으로 보고해야 한다.

## 참고 자료

- 원문: [Allocate shared Amazon MSK costs to Kafka topics for cost visibility](https://aws.amazon.com/blogs/big-data/allocate-shared-amazon-msk-costs-to-kafka-topics-for-cost-visibility)
