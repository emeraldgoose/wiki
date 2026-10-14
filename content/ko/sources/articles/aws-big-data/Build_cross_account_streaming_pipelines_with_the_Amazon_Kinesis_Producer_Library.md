---
title: "Kinesis Producer Library와 Kinesis Client Library로 크로스 계정 스트리밍 파이프라인 구축하기"
description: "중앙 Kinesis 스트림에 KPL 프로듀서·KCL 3.5 컨슈머를 붙이는 3계정 레퍼런스 아키텍처 — 크로스 계정 IAM 역할, 리소스 기반 정책, 고객 관리형 KMS 키, Enhanced Fan-Out을 CloudFormation으로 배포하는 전 과정을 안내한다."
tags: [source, aws-big-data, kinesis, streaming, cross-account, iam, kms, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library"
blog: aws-big-data
published: "2026-10-12"
---

# Kinesis Producer Library와 Kinesis Client Library로 크로스 계정 스트리밍 파이프라인 구축하기

**Source**: AWS Big Data Blog, 2026-10-12

**핵심**: 멀티 계정은 스트리밍 파이프라인에 보안 격리와 비용 귀속을 주지만, 프로듀서·컨슈머가 계정 경계를 넘어야 한다 — IAM 정책·KMS 키·CloudWatch 관측성을 조율해야 한다. 이 글은 가장 격리된 구성, 즉 KPL 프로듀서·Kinesis 스트림·KCL 컨슈머가 각각 다른 AWS 계정에 있는 형태를 단계별로 안내하고, 각 단계의 CloudFormation 템플릿과 샘플 Java 애플리케이션을 제공한다.

## 배경

Amazon Kinesis Data Streams는 초당 수백만 레코드를 서브초 지연으로 수집하고 Lambda·Data Firehose·Managed Service for Flink와 네이티브 통합되며, 이때 크로스 계정 접근은 보통 Kinesis 리소스 정책으로 처리한다. 커스텀 애플리케이션은 두 오픈소스 라이브러리를 쓴다: Kinesis Producer Library(KPL — 최대 1MB 레코드 집계, 지수 백오프 재시도, 속도 제한, 인스턴스별 CloudWatch 지표)와 Kinesis Client Library 3.5(자동 샤드 탐색, DynamoDB 조정 리스, 체크포인팅, 부하 분산, 리샤딩 시 우아한 리스 인계, Enhanced Fan-Out). 둘 다 Java 지원, KCL은 MultiLangDaemon으로 타 언어 추가 지원.

## 멀티 계정 스트리밍의 과제

- **계정 경계 강제**: 기본 거부이므로 프로듀서 쓰기·컨슈머 읽기 경로를 각각 명시 부여해야 하고, 암호화 스트림은 양쪽의 KMS 키 접근도 필요하다.
- **정책 복잡도**: 세 정책이 맞아떨어져야 한다 — 스트림의 리소스 기반 정책, 프로듀서·컨슈머의 ID 기반 정책, KMS 키 공유.
- **암호화**: AWS 관리형 키로 암호화된 스트림은 계정 간 공유 불가, 고객 관리형 KMS 키가 필수다.
- **관측성**: 프로듀서 처리량·스트림 사용률·컨슈머 지연 지표가 서로 다른 계정에 있어 크로스 계정 관측성이 필요하다.

## 배포 패턴

| 패턴 | KPL(프로듀서) | 스트림 | KCL(컨슈머) |
|---------|----------------|--------|--------------|
| 단일 계정 | A | A | A |
| 크로스 계정 컨슈머 | A | A | B |
| 크로스 계정 프로듀서 | A | B | B |
| 완전 분리(워크스루) | A | B | C |

## 솔루션 아키텍처

- **계정 A(프로듀서)**: EC2의 KPL 앱이 `KPLProducerRole`로 실행, 시작 시 계정 B의 `KinesisProducerCrossAccountRole`에 `sts:AssumeRole`(external ID 포함) 호출 후 임시 자격증명으로 `PutRecords`. CloudWatch 지표는 계정 A에 로컬 게시.
- **계정 B(스트림)**: 스트림·고객 관리형 KMS 키·프로듀서용 크로스 계정 역할 소유, 컨슈머에 `GetRecords`/`GetShardIterator`/`DescribeStream`/`ListShards`를 주는 리소스 기반 정책, 사전 등록된 Enhanced Fan-Out 컨슈머(샤드당 전용 2MB/s, `SubscribeToShard`로 ~70ms, 컨슈머 ARN 공유).
- **계정 C(컨슈머)**: KCL 3.5 앱이 로컬 `KCLConsumerRole`로 읽기 — 역할 가정 없이 스트림 리소스 정책으로만 인가 — 자체 DynamoDB 리스 테이블과 CloudWatch 지표 사용.

## 배포 워크스루

사전 준비: CLI 프로필이 있는 3개 AWS 계정, CLI v2, Java 11+·Maven, 동반 레포(`aws-samples/sample-kinesis-cross-account-kpl-kcl`).

1. **스트림 스택(계정 B)**: `stream-account-stack.yaml`을 프로듀서·컨슈머 계정 ID와 함께 배포, `StreamArn`·`KMSKeyArn`·`ProducerCrossAccountRoleArn`·`EFOConsumerArn` 기록.
2. **프로듀서 스택(계정 A)**: `producer-account-stack.yaml`을 역할·스트림·키 ARN과 함께 배포 후 SSM으로 `CrossAccountKPLProducer`를 빌드·실행(스트림 ARN, 리전, 역할 ARN 인자).
3. **컨슈머 스택(계정 C)**: `consumer-account-stack.yaml`을 스트림·EFO 컨슈머·키 ARN과 함께 배포 후 SSM으로 `CrossAccountKCLConsumer`를 로컬 자격증명으로 빌드·실행.
4. **검증**: 프로듀서 시작, 컨슈머 시작 후 종단 흐름과 각 계정의 CloudWatch 지표 확인.

## 소프트웨어 엔지니어를 위한 시사점

- **쓰기는 역할 가정, 읽기는 리소스 정책**: 글의 비대칭 패턴(프로듀서는 역할 가정, 컨슈머는 스트림 정책 의존)은 크로스 계정 데이터 플레인의 재사용 가능한 템플릿이다.
- **고객 관리형 키는 필수**: 크로스 계정 암호화 스트림 설계는 공유 CMK를 upfront에 준비해야 한다 — AWS 관리형 키는 공유를 조용히 막는다.
- **EFO 컨슈머 사전 등록**: `SubscribeToShard`는 별도 인가된 사전 등록 컨슈머 ARN이 필요, 리더 배포 전 팬아웃 토폴로지를 먼저 계획한다.
- **컨슈머 계정별 리스 테이블**: KCL의 DynamoDB 체크포인팅은 컨슈머에 로컬이므로 장애 복구가 스트림 소유 계정에 의존하지 않는다.

## 참고문헌

- 원문: [https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library](https://aws.amazon.com/blogs/big-data/build-cross-account-streaming-pipelines-with-the-amazon-kinesis-producer-library-and-kinesis-client-library)
- 동반 레포: `aws-samples/sample-kinesis-cross-account-kpl-kcl`(원문 내 링크)
