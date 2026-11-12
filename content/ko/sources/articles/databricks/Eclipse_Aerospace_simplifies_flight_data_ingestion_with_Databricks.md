---
title: "Eclipse Aerospace, Databricks로 비행 데이터 수집을 단순화하다"
description: "Eclipse Aerospace는 Rust 비행 데이터 디코더를 Arrow 네이티브 PySpark 커스텀 데이터 소스로 감싸 약 20년 치 독점 포맷 텔레메트리를 Databricks Serverless에서 직접 읽는다. Lambda 홉도, Avro 사본도, 상시 전용 컴퓨트도 없다."
tags: [source, databricks, data-engineering, pyspark, aerospace, ko]
locale: ko
source_url: "https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks"
blog: databricks
published_date: 2026-11-13
---

# Eclipse Aerospace, Databricks로 비행 데이터 수집을 단순화하다

**원문**: [Databricks 블로그](https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks) · **게시일**: 2026-11-12

## 개요

데이터 집약 산업이 현대화되면서 센서·텔레메트리·과학 데이터는 주류 분석 엔진이 직접 읽지 못하는 특수·독점 포맷으로 쌓인다. 팀은 느리고 메모리를 많이 쓰는 커스텀 변환, 관리해야 하는 전용 커넥터, 분석 전 추가 디코딩 단계 중 하나를 골라야 한다. 초경량 제트기 제조·운영사 Eclipse Aerospace가 마주한 것이 정확히 이 문제다. 근실시간 위성 텔레메트리, 전체 비행 이력의 대량 업로드, 외부 데이터 소스에서 모은 100만 비행 시간 이상, 3TB가 넘는 약 20년 치 비행 데이터가 모두 커스텀 디코더를 요구하는 독점 파일 포맷으로 저장되어 있고, 그 디코더는 이미 Rust와 Scala로 작성되어 있었다.

PySpark 커스텀 데이터 소스가 Databricks Runtime 15.4 LTS에 도입되기 전에는 세 가지 선택지가 있었지만 모두 결함이 있었다. 파일을 바이너리로 읽고 Python UDF로 쪼개는 방식은 성능을 가독성과 바꾸며, 가변 길이 메시지에서 메모리 부족 위험이 커서 쓸 수 없었다. 기존 Scala 디코더로 네이티브 Data Source v1/v2를 구현하려면 전용 컴퓨트가 필요했고, 빠른 업로드·조회 기대를 충족하려면 상시 가동이 필수라 비용이 더 컸다. 결국 남은 것은 AWS Lambda의 Rust 디코더로 파일을 중간 포맷(Avro)으로 변환하는 길이었는데, 다단계 지연, Lambda 디코더와 다운스트림 Spark 잡 사이의 스키마 로직 중복, 비행마다 두 벌씩 저장되는 데이터가 따라왔다.

선택된 설계는 Arrow 네이티브 PySpark 커스텀 데이터 소스다. 기존 Rust 디코더를 얇은 Python DataSource로 감싸 레코드를 Apache Arrow로 전달해, 파일 읽기 로직이 서버리스 컴퓨트의 Spark 내부에서 돌게 한다. Python은 제어 흐름을, Rust와 Arrow는 고성능 디코딩과 데이터 전송을 담당한다. 상시 전용 컴퓨트도, 중간 파이프라인도 없다. 결과는 이렇다. 업로드 후 시작 시간을 포함해 1분 안에 레코드 처리가 시작되고, 수 기가바이트 대량 배치는 병렬로 보통 2분 안에 처리되며, 인프라 계층 하나가 통째로 사라지고, 스키마는 이제 두 코드베이스가 아니라 디코딩 로직 옆의 버전 관리되는 커넥터 하나에 산다.

## 핵심 내용

- 기존 세 가지 선택지와 실패 이유. 바이너리 + Python UDF(가변 길이 메시지에서 메모리 부족 위험), 전용 컴퓨트의 Scala 네이티브 Data Source(상시 가동 비용), Lambda의 Avro 변환(다단계 지연, 스키마 로직 중복, 저장 중복).
- 패턴. 도메인 특화 Rust 디코더를 그대로 두고 얇은 Python DataSource로 감싸 Apache Arrow로 레코드를 전달한 뒤, 파티셔닝·실행·관측성·다운스트림 처리는 Databricks Serverless의 Spark에 맡긴다.
- 속도. 업로드 후 시작 시간 포함 1분 안에 레코드 처리. 수 기가바이트 대량 배치를 병렬로 보통 2분 이내에 처리해 대형 비행 이력도 몇 분 만에 분석한다.
- 비용. Lambda 홉과 Avro 중간 단계 제거로 운영·감시·비용을 치르던 인프라 계층이 통째로 사라졌다. 원본 바이너리와 Avro 변환본 두 벌을 저장하지 않게 된 것은 약 20년 보관 이력 기준으로 유의미한 중복 저장소 절감이다.
- 저장 방침. 대부분의 파일은 AWS Glacier에 두고, 원본이 다시 필요하면 디코딩을 쉽게 반복한다.
- 관측성. 디코딩이 Spark 내부에서 일어나므로 Spark UI와 표준 잡 지표에 다른 스테이지처럼 나타난다. CSV/JSON 로더를 모방한 커스텀 badRecordsPath로 잘못 형식화된 데이터를 잡고, 데이터 품질 파이프라인이 디코더에서 직접 통계를 수집한다.
- 엔지니어링 시간. 스키마 로직은 예전에 두 번 정의됐다. Avro를 만드는 Lambda 디코더와 그것을 소비하는 Spark 잡. 포맷이 바뀔 때마다 두 코드베이스를 모두 고쳐야 하고 정의가 어긋날 위험이 있었다. 이제 단일 버전 관리 커넥터가 디코딩 로직 옆에서 스키마를 한 번만 정의한다.
- 재사용성. Rust 디코더를 감싼 얇은 Python DataSource라는 같은 아키텍처 패턴을 Eclipse Aerospace가 지원하는 다른 독점 포맷에도 적용할 수 있다. 포맷마다 새로 발명하지 않아도 된다.
- 가용성. PySpark 커스텀 데이터 소스는 Databricks Runtime 15.4 LTS 이상 또는 서버리스 환경 버전 2에서 제공된다.

## 세부 사항

- PySpark 커스텀 데이터 소스는 Python으로 구현한 사용자 정의 Spark 데이터 소스다. 별도 JVM 커넥터를 만들지 않고 표준 Spark 워크플로 안에서 특수 파일 포맷을 읽게 한다.
- Databricks Serverless는 이 설계를 경제적으로 만드는 완전 관리형 컴퓨트 계층이다. 인프라 프로비저닝 없이 워크로드를 돌리고 컴퓨트를 자동 할당·확장·최적화한다. 빠른 업로드-조회 워크플로에 딱 맞는 성질이다.
- 커넥터는 PySpark 커스텀 데이터 소스로 서버리스 컴퓨트의 Spark 내부에서 파일 읽기 로직을 실행한다. 독점 파일을 상시 전용 컴퓨트나 Avro 중간 파이프라인 없이 직접 읽는다.
- 스키마 중복 문제를 다시 쓰면 이렇다. 구 설계는 메시지 포맷을 Avro를 만드는 Lambda 디코더에 한 번, 그것을 소비하는 다운스트림 Spark 잡마다 한 번씩 인코딩했고, 두 정의는 시간이 지나며 어긋났다.
- 독점·산업 특화 포맷을 다루는 팀을 위한 결론. 포맷 주변에 별도 수집 플랫폼을 세우는 대신, 이미 신뢰하는 디코딩 로직을 PySpark 커스텀 데이터 소스로 노출하라.
