---
title: "AWS와 Workday Data Cloud 통합 소개"
description: "AWS와 Workday가 Workday의 거버넌스가 적용된 인사·재무 데이터를 AWS 분석 및 AI 서비스에서 양방향 제로카피로 접근할 수 있게 했습니다. Workday의 Iceberg REST 카탈로그를 AWS Glue에 연합 카탈로그로 등록해 ETL 복사 없이 사용합니다."
tags: [source, aws-big-data, data-lake, iceberg, governance, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws"
blog: aws-big-data
published_date: "2026-11-11"
---

# AWS와 Workday Data Cloud 통합 소개

**원문**: [AWS Big Data 블로그](https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws) · **게시일**: 2026-11-09

## 개요

AWS가 Workday Data Cloud와 AWS 간 통합을 발표했습니다. 이 통합은 AWS의 분석 및 AI 서비스에서 Workday의 거버넌스가 적용된 인사·재무 데이터에 양방향 제로카피로 접근할 수 있게 합니다. 겨냥한 문제는 익숙합니다. 기업 시스템을 분석 플랫폼에 연결하려면 대개 깨지기 쉬운 파이프라인을 만들고 데이터를 중복 저장해야 하며, 그러는 과정에서 데이터를 신뢰할 수 있게 만드는 거버넌스와 업무 맥락을 잃습니다. Workday Data Cloud는 개방적이고 안전한 헤드리스 데이터 플랫폼으로 소개되며, 의미 정의와 권한 모델, 지표 로직, 감사 통제를 그대로 유지한 채 개발자가 이미 쓰는 도구에서 Workday 데이터를 다룰 수 있게 합니다. Workday Data Lake를 통한 정제된 뷰, Apache Iceberg 기반의 Workday Data Connect를 통한 양방향 제로카피 접근, 그리고 Workday Live Data Query를 통한 애플리케이션·에이전트용 준실시간 SQL 접근을 제공합니다.

통합은 양방향이므로 어느 쪽도 데이터를 복사할 필요가 없습니다. 각 플랫폼이 상대의 데이터를 제자리에서 질의하고, 양쪽에 이미 정의된 거버넌스 통제를 그대로 존중합니다. Workday의 Iceberg REST 카탈로그가 AWS Glue에 연합 카탈로그로 등록되면서 Workday 데이터셋은 Glue 데이터 카탈로그를 읽는 모든 서비스, 즉 Amazon Athena, Amazon Redshift, Amazon EMR, Amazon SageMaker AI에서 별도 설정 없이 검색할 수 있게 됩니다. 반대 방향도 같은 방식입니다. AWS Glue 데이터 카탈로그의 Iceberg REST 카탈로그 엔드포인트를 Workday Data Cloud에 외부 카탈로그로 등록하면 Workday 사용자가 Amazon S3에 저장된 Apache Iceberg 테이블을 준실시간으로 조회할 수 있습니다.

AWS 쪽 구성은 이 흐름에 맞춰 연결됩니다. Amazon SageMaker Unified Studio는 개발자가 Workday Data Cloud에 접속해 데이터셋을 대화형으로 탐색하고 SQL을 실행하며 모델을 만드는 통합 개발 환경입니다. Amazon Athena는 Amazon S3에 있는 Iceberg 테이블에 서버리스 SQL을 제공하고, Amazon Redshift는 Glue 데이터 카탈로그 연합을 통해 데이터 이동 없이 Workday 인사·재무 데이터를 결합해 도메인 간 분석을 할 수 있습니다. AWS Lake Formation은 AWS 쪽의 세밀한 권한 계층을 담당해 관리자가 분석가나 애플리케이션을 특정 데이터베이스, 테이블, 행, 열 단위로 제한할 수 있게 하며, Workday가 자체 데이터 계층에 적용하는 거버넌스를 보완합니다.

## 핵심 내용

- 두 가지 접근 방식이 서로 다른 데이터 최신성 요구를 담당합니다. Workday Live Data Query는 SageMaker Unified Studio, Athena, EMR, AWS Glue에서 라이브 Workday 데이터셋에 직접 SQL을 실행하며, 질의는 Workday의 거버넌스 환경 안에서 수행되고 결과가 준실시간으로 돌아옵니다. 최신성이 중요한 운영용 AI 에이전트와 대시보드에 적합합니다.
- 두 번째 방식은 규모가 큰 작업에 맞습니다. Workday의 Iceberg REST 카탈로그를 Glue 데이터 카탈로그나 Lake Formation에 등록하면 모든 Workday 데이터셋이 표준 Iceberg 테이블로 보이고, 연산은 고객의 AWS 계정에서 Athena, Redshift, EMR, SageMaker AI로 수행되며 데이터 자체는 Workday Data Cloud에 남습니다.
- 거버넌스는 합쳐지는 것이 아니라 층층이 쌓입니다. 연합에는 OAuth 2.0 인증을 쓰고, AWS Lake Formation이 Workday 연결이 읽을 수 있는 데이터베이스와 테이블을 정하며, Workday의 구성 가능 보안이 어떤 Workday 주체가 연합 테이블에 접근할 수 있는지 통제합니다.
- 글의 예시는 양방향을 함께 활용합니다. Workday에서 인력 계획을 처리하는 AI 에이전트가 AWS의 Iceberg 테이블에서 매출 전망을 가져와 인원 데이터와 결합해, HR 담당자가 검토할 채용 권고를 만들어 냅니다.
- 표방하는 효과는 ETL 제거입니다. Workday 데이터를 분석 환경에 옮기기 위한 파이프라인을 더 이상 만들고 유지할 필요가 없으므로 복제 없이 데이터 사일로가 사라지고, 데이터 팀은 최신성 모니터링과 중복 정리 대신 분석과 머신러닝 애플리케이션에 시간을 쓸 수 있습니다.
- 업무 맥락이 데이터와 함께 이동합니다. 의미 정의와 권한 모델, 계산 로직이 함께 따라오기 때문에 개발자가 비즈니스 로직을 역설계하거나 에이전트용 권한 모델을 다시 만드는 데 드는 시간이 줄어듭니다.

## 상세

인력 분석 사례는 의도된 작업 흐름을 잘 보여 줍니다. 미리 만들어진 Workday 커넥터로 AWS Glue에서 Workday Data Cloud에 접속하고, 직급·조직 계층·근속 계산이 이미 정의된 상태에서 보상, 근속, 몰입도, 성과 데이터셋을 탐색합니다. 이 인원 데이터를 Amazon S3에 Iceberg 테이블로 저장된 시장 보상 벤치마크 및 채용 파이프라인 데이터와 Athena나 SageMaker AI 노트북의 표준 SQL로 결합하고, SageMaker AI에서 이직 위험을 예측하는 모델을 학습시킵니다. 마지막으로 HR 담당자가 검토하고 조치할 수 있도록 고위험 이직 패턴을 표시하는 에이전트를 배포하는데, 이 에이전트는 준실시간 신호에는 Live Data Query를, 과거 추세 분석에는 배치 Iceberg 접근을 사용합니다. 저자들은 데이터가 거버넌스 환경을 벗어나지 않고, 유지할 맞춤형 파이프라인도 없으며, 모든 단계가 감사 가능하게 남는다는 점을 강조합니다.

이 통합은 정식 출시되었습니다. SageMaker Unified Studio 사용자는 Workday Live Data Query 커넥터나 Workday Iceberg REST 카탈로그 커넥터로 Workday Data Cloud에 접속할 수 있고, Live Data Query 연결은 AWS Glue 콘솔에서도 만들 수 있어 Athena, Amazon EMR, Glue ETL 작업에서 라이브 Workday 데이터를 질의할 수 있습니다. Glue와 Lake Formation 사용자는 Workday Iceberg REST 카탈로그를 연합 카탈로그로 등록할 수 있으며, AWS 데이터를 조회하려는 Workday 사용자는 Glue 데이터 카탈로그의 Iceberg REST 엔드포인트를 Workday Data Cloud에 외부 카탈로그로 등록하면 됩니다.

## 참고 자료

- 원문: [AWS Big Data 블로그](https://aws.amazon.com/blogs/big-data/introducing-the-workday-data-cloud-integration-with-aws)
