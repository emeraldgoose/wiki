---
title: "Amazon Managed Service for Apache Flink로 사전 녹화된 스트림 배증하기"
description: "살균한 Kinesis 녹화 스트림을 multiple.factor 배율로 재생하며 레코드마다 원본과 DataFaker 변형을 함께 내보내는 스트림 배증 패턴을 정리했다. 공개 테스트에서 25배 배율로 초당 약 176,000 레코드에 도달했다."
tags: [source, aws-big-data, amazon-kinesis, apache-flink, load-testing, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/multiply-pre-recorded-streams-with-amazon-managed-service-for-apache-flink"
blog: aws-big-data
published_date: 2026-11-14
---

# Amazon Managed Service for Apache Flink로 사전 녹화된 스트림 배증하기

**원문**: [AWS 빅데이터 블로그](https://aws.amazon.com/blogs/big-data/multiply-pre-recorded-streams-with-amazon-managed-service-for-apache-flink) · **게시일**: 2026-11-10

## 개요

스트리밍 파이프라인을 현재 피크 이상으로 검증하려면 프로덕션 규모의 테스트 데이터가 필요한데, 기존 방식은 어딘가 부족하다. 전체 용량의 사전 녹화 스트림을 재생하는 방법은 충실하지만 보관 비용이 크다. 초당 50,000 레코드 기준으로 2시간 녹화 창이 3억 6천만 레코드에 이르고, 검증하는 처리량 등급마다 녹화를 따로 확보해야 한다. DataFaker 같은 합성 데이터 생성기는 스키마만으로 어떤 속도든 내보낼 수 있지만 설정된 분포를 따를 뿐 관측된 분포가 아니어서, 실제 트래픽의 자연스러운 왜도, 마이크로 버스트, 필드 간 상관관계를 재현하지 못한다. 카나리 배포와 섀도 파이프라인은 실제 프로덕션 데이터를 쓰지만 테스트가 현재 프로덕션 처리량에 묶인다.

스트림 배증 패턴이 이 간극을 메운다. Amazon Kinesis Data Streams에서 가져온 비교적 작은 살균 녹화 스트림을 매개변수 multiple.factor 하나로 증폭한다. 이 값이 입력 하나가 몇 개의 레코드로 늘어나는지를 정한다. 교체 대상으로 지목하지 않은 필드는 원본 녹화의 분포를 그대로 유지하고, 지목한 필드는 DataFaker 값으로 다시 생성되므로, 증폭된 스트림은 배로 늘어난 용량에서도 실제 트래픽의 통계적 형태를 보존한다.

예시는 차량 호출 회사 AnyCompany Rides다. 이 회사의 Apache Flink 파이프라인은 피크에 약 초당 15,000개의 이동 이벤트를 처리하며, 지역 확장 전에 초당 75,000개를 견디는지 확인해야 한다. 10시간짜리 살균 녹화에 5배 배율을 설정하면 레코드마다 원본 이벤트를 그대로 내보내고 합성 변형 네 개를 추가로 내보낸다. 배증기 자체는 Amazon Managed Service for Apache Flink에서 구동되는 RichFlatMapFunction이며, Amazon CloudWatch가 처리량, 백프레셔, 체크포인트 시간, 힙 지표를 수집한다.

## 핵심 내용

- 솔루션은 AWS 서비스 셋과 오픈소스 라이브러리 하나로 구성된다. Amazon Kinesis Data Streams가 원본 녹화와 증폭 스트림을 나르고, Managed Service for Apache Flink가 배증기를 구동하며, Amazon CloudWatch가 상태 지표를 수집한다. DataFaker가 코드 대신 faker-config.yaml 선언에 따라 대체 값을 만든다.
- 런타임 속성이 동작을 결정하므로 하나의 아티팩트로 어떤 스키마든 처리한다. source.type(kinesis는 증폭 모드, datagen은 순수 합성 모드), multiple.factor, key.fields, updatable.fields, random.seeds, rate.limit.per.second다.
- 증폭 모드에서 이벤트는 다섯 단계를 거친다. 읽고 역직렬화하고, 원본을 그대로 내보내고, 키 필드와 반복별 난수 시드로 결정적 해시를 계산하고, updatable.fields에 나열된 필드의 합성 값을 생성하고, 모든 레코드를 싱크에 기록한다.
- 애플리케이션은 시작 시 multiple.factor를 검증해 1부터 100 범위를 벗어나면 거부한다. 잘못 입력된 배율이 싱크 샤드 용량이나 애플리케이션 힙을 소진하는 사고를 막는다.
- 키 필드는 변형 간에 보존되므로 trip ID로 묶어 보는 소비자는 여전히 하나의 개체로 본다. timestamp처럼 어느 목록에도 없는 필드는 손대지 않고 그대로 지난다.
- 생성기는 결정적이며 반복 가능하다. 시드는 레코드 키 필드와 반복별 시드에서 나오고 레코드마다 다시 시딩되므로 재생 순서나 서브태스크 배정에 좌우되지 않는다. 벽시계 시간이나 UUID.randomUUID() 같은 값을 쓰면 이 성질이 깨진다.
- 검증된 버전: JDK 17, sbt 1.9.9, Scala 2.12.20, FLINK-2_3 런타임의 Apache Flink 2.3.0, aws-kinesisanalytics-runtime 1.2.0, Kinesis 커넥터 6.0.1-2.0, DataFaker 2.7.0, Jackson 2.15.2, Log4j 2.24.3.
- 평균 약 181바이트인 NYC 택시 이동 스키마와 240샤드 싱크로 3 KPU(처리 2, 오케스트레이션 1)에서 배율 스윕을 실행한 결과, 5배에서 초당 약 128,000개, 25배에서 약 176,000개의 출력을 냈다. CPU는 모든 구간에서 96-100퍼센트로 고정됐고 힙은 평균 31-38퍼센트 대역에 머물렀으며, 체크포인트는 17-73KB 크기로 226-460밀리초에 끝났다.
- 실제 처리량의 상한은 싱크가 정한다. Kinesis 샤드는 쓰기에 초당 1,000 레코드 또는 1MB를 받으므로, 1KB 미만 레코드라면 목표 출력 속도를 1,000으로 나눠 싱크를 잡는다. 10배에서 싱크 샤드 20개는 초당 약 20,505 레코드에서 심하게 스로틀됐고 CPU는 16퍼센트였으며, 180개에서는 스로틀이 사라지고 약 143,000 레코드의 연산 한계가 드러났다.
- 검증은 애플리케이션이 아니라 Kinesis 쪽에서 하라. 소스 스트림의 GetRecords.Records와 싱크 스트림의 IncomingRecords 비율이 배율과 같아야 한다. 10배 실행에서 초당 2,056 입력 대 20,505 출력, 비율 9.97로 측정됐다.
- source.type을 바꾸면 잡 그래프가 달라져 이전 스냅샷 복원이 KinesisShardSplitSerializer EOFException으로 실패한다. 배증기는 상태가 없으므로 SKIP_RESTORE_FROM_SNAPSHOT으로 시작하면 된다.
- 비용: 기본 배포(샤드 3개, 7일 보존, KPU 3개)는 시간당 약 0.45달러, 하루 약 11달러다. 240싱크 샤드로 2시간 25배 실행은 PUT 페이로드 단위 약 13억 개(17.75달러), 싱크 샤드시간 480개(7.20달러), KPU시간 6개(0.66달러)를 썼고 보존 비용을 포함해 약 35달러였다.

## 세부 사항

### 팬아웃 동작 방식

flatMap은 원본을 먼저 내보내고 N-1개 변형을 뒤따라 내보내므로, 배율 3은 원본과 변형 둘, 세 레코드를 만든다. faker-config.yaml의 DataFaker 항목은 식과 타입을 짝지으며, 예로 distance는 0-20에서, amount는 5-150에서 뽑힌다. tripId는 키 필드라서 모든 변형에서 같다. 파티션 키가 배율이 아니라 레코드 해시에서 나오므로 샤드 부하가 고르게 유지된다. 240개 샤드를 연 25배 실행에서 모든 샤드가 초당 671~678 레코드를 실었다.

### 처리량과 용량

출력은 배율에 따라 올라가지만 초당 약 176,000 레코드 근처에서 평평해진다. 입력마다 읽기와 역직렬화 고정 비용이 들고 출력마다 변형별 필드 생성 비용이 들기 때문이다. 제약은 메모리나 상태가 아니라 CPU다. 용량 계획은 처리 KPU당 출력으로 잡는다. 5배에서 초당 약 64,000 레코드, 높은 배율에서 약 88,000까지 오른다.

### 싱크 크기 조정과 복원력

비동기 KinesisStreamsSink는 스로틀된 레코드를 다시 큐에 넣고 재시도한다. 스윕 전체에서 일시적 시도당 실패는 수천만 레코드 대비 창당 73개 이하에 그쳤고 영구 손실은 없었으며, 쓰기 지연은 평균 40-54밀리초, 간헐적 스파이크는 약 1.1초였다. 출력이 배율 곱 입력 속도에 못 미치면 WriteProvisionedThroughputExceeded와 backPressuredTimeMsPerSecond를 확인하고, 소스가 뒤처지면 Enhanced Fan-Out과 SubscribeToShardEvent.MillisBehindLatest로 전환한다.

### 한계와 정리

증폭은 볼륨을 늘리면서 샘플의 시간 형태를 그대로 가져가므로 녹화에 있던 버스트는 더 큰 진폭으로 이어진다. 생성 필드는 서로 독립적이라 0.5마일 이동에 150달러 요금이 붙을 수 있다. 순서는 파티션 안에서는 보존되지만 파티션 간에는 보장되지 않는다. 샘플은 JSON만 읽고 쓴다. 정리할 때는 애플리케이션을 멈추고 READY 상태를 확인한 뒤 CloudFormation 스택을 삭제한다. 스택이 만든 AWS KMS 키는 30일 대기 후 삭제 예약된다.
