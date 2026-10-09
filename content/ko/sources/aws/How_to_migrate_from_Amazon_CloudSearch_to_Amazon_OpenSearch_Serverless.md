---
title: Amazon 클라우드서치에서 아마존 오픈서버리스로 마이그레이션 방법
description: Amazon CloudSearch에서 Amazon OpenSearch Serverless로 마이그레이션하는 단계별 가이드. 평가는 데이터 변환, 쿼리 마이그레이션 및 보안 정책 번역을 포함하여 최소한의 가동 중지 시간과 데이터 손실 없이 CloudSearch 도메인을 마이그레이션하는 방법을 따라할 수 있습니다.
date: 2026-09-10
tags: [aws, data-engineering, search, opensearch, cloudsearch, migration]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/"
blog: aws
---

# Amazon 클라우드서치에서 아마존 오픈서버리스로 마이그레이션 방법

**Authors**: AWS Big Data Blog · **Published**: 2026년 9월 10일 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/)

## 주의할 주요 차이점

* **독립적 스케일링** – OpenSearch Serverless는 인덱싱 및 검색 compute를 독립적으로 스케일링하고, 컬렉션이 사용되지 않을 때 compute를 zero로 스케일링할 수 있습니다(스토리지에 대해서만 비용을 지불합니다). 비용 구조는 [Amazon OpenSearch Serverless 관리 용량 제한](/opensearch-service/latest/developerguide/serverless-scaling.html)을 참조하세요.
* **레이어드 보안 모델** – OpenSearch Serverless는 암호화, 네트워크 및 데이터 액세스 정책을 별도 계층에서 적용합니다. 보안 모델은 [Amazon OpenSearch Serverless Security](/opensearch-service/latest/developerguide/serverless-security.html)를 참조하세요.

## 선행 조건

이 포스트를 따라하려면 다음이 필요합니다:

* AWS 계정.
* 인덱싱된 데이터가 있는 기존 Amazon CloudSearch 도메인.
* 내결함성 저장소에 사용 가능한 소스 데이터 (Amazon Simple Storage Service (Amazon S3) 또는 Amazon DynamoDB). CloudSearch는 기본 제공 내보내기 또는 백업 기능이 없으므로 CloudSearch로 재인젝션하기 위한 원본 소스 데이터가 필요합니다.
* Amazon OpenSearch Serverless 컬렉션, 암호화 정책, 네트워크 정책 및 데이터 액세스 정책을 생성하고 관리할 IAM 권한.
* 데이터를 로드할 Amazon OpenSearch Ingestion 파이프라인(또는 대체 인젝션 방법).

## 마이그레이션 계획

계획 단계는 성공이 무엇을 의미하는지 결정하는 단계입니다: 최소한의 가동 중지 시간, 데이터 손실 없음, 현재 기능 보존 및 사용자 지정 구성 유지. 인프라를 계획할 필요가 없는데 왜냐하면 OpenSearch Serverless가 컴퓨트를 프로비저닝하고 스케일링하기 때문입니다. 주요 계획 작업은 현재 CloudSearch 구성을 평가하여 대상을 재현하는 것입니다.

Amazon CloudSearch 콘솔에서 기존 설정을 문서화하세요. 현재 인스턴스 유형, 파티션 수, 복제 수를 기록하세요. 전체 문서 수 및 전체 데이터 크기를 캡처하고, 각 필드 정의를 기록하세요(필드 유형 및 각 필드의 검색, 페싯, 정렬 설정을 포함). 사용하는 분석기, 동의어, stopwords 또는 사용자 지정 rank 표현을 노트하세요. 2011년 또는 2013년 CloudSearch API 버전을 사용하는지 기록하세요. 2013년 API는 페싯팅 및 필터링 기능을 추가하여 대상을 모델링하는 방식을 변경했기 때문입니다.

 most CloudSearch 워크로드에 대해 OpenSearch Serverless가 적합하지만, 모든 경우에 해당하는 것은 아닙니다. 매우 낮은 읽기-after-쓰기 지연 시간(짧은 refresh 간격), 타이트하고 예측 가능한 쿼리 응답 시간, 또는 직접 인스턴스 구성을 필요로 하는 워크로드의 경우, 대신 Amazon OpenSearch Service 관리 클러스터 배포를 선택하고 워크로드 프로파일에 따라 크기 조정을 권장합니다 [여기서](/opensearch-service/latest/developerguide/sizing-domains.html) 확인이 가능합니다.

마이그레이션은 4개의 주요 관심사로 나뉩니다: 소스 데이터 형식, 쿼리, 필드 정의 및 액세스 정책. 세부 계획을 계획하기 전에 전체 마이그레이션을 한 번에 살펴보는 것이 도움이 됩니다. 다음 다이어그램은 4가지 단계로 마이그레이션을 매핑합니다: 소스 CloudSearch 환경, 데이터를 변환하고 이동하는 마이그레이션 파이프라인, OpenSearch Serverless 타겟, 그리고 cutover 및 operations.

![Migration workflow across four phases: source CloudSearch, migration pipeline, OpenSearch Serverless target, and cutover and operations](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-5903-1.png)

*그림 1: 4단계 마이그레이션 워크플로우*

소스 환경에서 Amazon CloudSearch 구성을 평가하고 소스 데이터(Amazon S3, Amazon DynamoDB 또는 기타 저장소)를 백업합니다. Source Data Format(SDF), URL 기반 쿼리 구문 및 보존해야 할 IAM 액세스 정책을 주의하세요. 마이그레이션 파이프라인에서 필드 유형을 매핑하고 CloudSearch JSON에서 OpenSearch 호환 JSON으로 데이터 형식을 변환하고, 쿼리를 OpenSearch query domain-specific language(DSL)로 변환하고, 보안을 구성하고, 데이터를 bulk ingest한 후 결과를 유효성 검증합니다. OpenSearch Serverless 타겟은 컬렉션, 인덱스 매핑, 인증된 문서, 암호화, 네트워크 및 데이터 액세스 정책을 보유하며 워크로드에 따라 스케일링되는 페이 퍼 유스 기반으로 작동합니다. cutover 및 operations 단계에서는 애플리케이션을 새 엔드포인트로 업데이트하고 클라이언트를 업데이트한 후 Amazon CloudWatch로 모니터링한 후 트래픽이 더 이상 남지 않으면 CloudSearch를 중단합니다.

## OpenSearch Service에서 데이터 모델링

OpenSearch Service는 인덱스 매핑을 사용하여 인덱스의 필드와 데이터 유형을 정의합니다. CloudSearch 스키마를 알고 있기 때문에 인덱스를 생성할 때 타겟 매핑을 명시적으로 정의하세요. `dynamic`을 `strict`로 설정하여 열리지 않은 필드를 가진 문서는 OpenSearch가 거부하도록 하여, 기본 OpenSearch 동작에서 정의되지 않은 필드에 대해 새로운 매핑을 생성하는 것을 방지하고 스키마 드리프트를 인젝션 시점에 잡습니다.

```json
PUT /imdb_movies { "mappings": { "dynamic": "strict", "properties": { "title": { "type": "text", "fields": { "keyword": { "type": "keyword" } } }, "genres": { "type": "keyword" }, "rating": { "type": "float" }, "release_date": { "type": "date" } ... } }
```

### 필드 유형 매핑

| CloudSearch | OpenSearch Service equivalent | Notes |
|---|---|---|
| text | text | 텍스트는 토큰화됩니다. stemming, synonyms, stopwords가 적용됩니다. 사용자 용어 매칭에 적합합니다. |
| literal | keyword | 토큰화되지 않음. exact-match 검색에 적합합니다. |
| int | integer | ranking, faceting 및 narrowing에 사용됩니다. |
| double | float or double | |
| date | date | |
| boolean | boolean | |
| latlon | geo_point | |
| text-array | text | OpenSearch는 natively arrays를 처리하므로 기본 text 유형에 매핑합니다. |
| literal-array | keyword | OpenSearch는 natively arrays를 처리하므로 기본 keyword 유형에 매핑합니다. |
| multi-value | nested or object | |

첫 번째 세부 사항에 가장 작은 numeric 유형을 선택하는 것이 중요합니다. CloudSearch가 사용하는 너비를 복사하는 대신 실제 데이터에 맞는 가장 좁은 형식을 선택하세요. CloudSearch는 정수를 64비트로 저장하지만, 대부분의 데이터셋은 이러한 큰 숫자를 보유하지 않습니다. `long` 또는 `double`은 값이 작을 때 `integer`, `short`, 또는 `float`보다 많은 디스크를 소비하며 이점이 없습니다. 각 필드의 실제 범위를 평가하고それを 가장 좁은 유형에 맞추세요. `long`은 `integer`의 약 21억 ceiling을 초과하는 실제 값을 보유하는 경우에 예약하세요. `double`이 필요한 경우를 제외하고는 `float` 대신 `double`을 사용하지 마세요. 작은 유형은 인덱스를 줄이고 쿼리를 가속화합니다.

두 번째로, `text` 필드에서 정렬하거나 집계할 경우 `keyword` sub-field를 추가하세요. preceding example mapping은 `title` 필드에 `keyword` sub-field가 있습니다. 점 표기법을 사용하여 필드에 액세스: `title.keyword`. 기본 OpenSearch는 분석된 `text` 필드를 정렬하거나 기본적으로 집계하지 않습니다.

앞서 언급한 바와 같이 여러 CloudSearch 도메인을 운영하는 경우, 이를 단일 OpenSearch Serverless 컬렉션 내에서 각각의 인덱스로 모델링하여 통합하는 것을 고려하세요.

## 데이터 이동

OpenSearch Service로 마이그레이션은 재인젠션(re-ingestion)입니다: 소스 문서를 변환하고 컬렉션에 색인화합니다. CloudSearch는 기본 제공 백업 또는 스냅샷 기능이 없습니다. 문서를 인덱싱 과정을 통해 전송하므로, 마이그레이션 전에 소스 데이터가 Amazon S3, Amazon DynamoDB 또는 기타 데이터베이스와 같은 내결함성 스토리지에 사용 가능한지 확인하세요.

변환은 형식 번역입니다. CloudSearch는 JSON 또는 XML 형식의 SDF를 수락하며, 문서 배치는 add 및 delete 작업의 컬렉션입니다. OpenSearch Service에서 기대하는 JSON은 CloudSearch가 사용하는 JSON과 다르므로, 각 소스 문서를 필드가 매핑된 OpenSearch 문서로 변환해야 합니다. 매핑에서 언급한 세부 사항을 처리하세요: 각 숫자 값을.emit 하여 선택한 필드에 맞는 좁은 유형에 맞추고, 날짜를 date 매핑과 일치하도록 형식화하고, strict mapping이 정의하지 않은 필드를 드롭하거나 rename하세요.

변환된 문서를 Amazon S3 버킷에 기록하면 변환된 문서가 다시 인젝션해야 할 때마다 읽을 수 있는 내결함성 스토리지에 안전하게 보존됩니다.

Amazon OpenSearch Ingestion을 사용하여 이를 로드하세요. Amazon OpenSearch Ingestion은 Amazon OpenSearch Service의 기능으로, 데이터를 인젝션, 필터, 변환, 풍부화, 라우팅하는 데 사용됩니다. Amazon S3 소스를 사용하는 OpenSearch Ingestion 파이프라인을 구성하세요 ( [OpenSearch Ingestion blueprint를 사용하여 시작](/opensearch-service/latest/developerguide/pipeline-blueprint.html)) 변환된 문서를 읽습니다. 파이프라인의 내장된 프로세서가 파이프라인에 쓰기 전 최종 변환을 적용하도록 허용합니다. Amazon S3에서 읽는 관리형 파이프라인은 반복 가능하고 restartable 하중을 제공하며, 대부분의 마이그레이션에 대해 권장되는 경로입니다.

## 정리

OpenSearch Serverless로 마이그레이션한 후에는 생성된 리소스가 아마도 생산성 리소스가 될 것입니다. 그렇지 않다면 ongoing cost를 피하기 위해 만든 Any OpenSearch Serverless 컬렉션 및 S3 버킷을 삭제하세요.

## 결론

이 포스트에서 Amazon CloudSearch와 Amazon OpenSearch Serverless를 비교하고 CloudSearch에서 의존하는 개념(필드 유형, 쿼리 구문, 자동 스케일링 및 액세스 제어)이 OpenSearch Service로 어떻게 번역되는지 살펴보았습니다. CloudSearch 구성을 평가하고, 명시적인 OpenSearch 매핑으로 데이터를 모델링하고, OpenSearch Ingestion을 사용하여 변환된 문서를 컬렉션에 이동하고, URL 기반 쿼리를 OpenSearch query DSL로 변환하고, 보안을 구성하고, cutover 전에 유효성 검증을 수행했습니다. OpenSearch Serverless는 CloudSearch와 동일한 hands-off operational 모델을 제공하며 richer query capabilities, granular data access policies 및 automatic scaling을 추가합니다. 시작하려면 AWS Management Console에서 OpenSearch Serverless 컬렉션을 생성하고 이 포스팅의 단계를 따르세요.

자세한 정보는 다음 리소스를 참조하세요:

* [Amazon OpenSearch Service Developer Guide](/opensearch-service/latest/developerguide/)
* [Amazon OpenSearch Serverless](/opensearch-service/latest/developerguide/serverless.html)
* [OpenSearch documentation](/opensearch.org/docs/latest/)
* [Amazon OpenSearch Service로 구축하는 4가지 방법](/blogs/big-data/four-ways-to-build-with-amazon-opensearch-service/)
* [Amazon OpenSearch Service 벡터 데이터베이스 기능 설명](/blogs/big-data/amazon-opensearch-services-vector-database-capabilities-explained/)

## About the authors

### Resources

* [Amazon Athena](/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon EMR](/blogs/big-data/category/analytics/amazon-emr?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Kinesis](/blogs/big-data/category/analytics/amazon-kinesis?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon MSK](/blogs/big-data/category/analytics/amazon-managed-streaming-for-apache-kafka/)
* [Amazon QuickSight](/blogs/big-data/category/analytics/amazon-quicksight?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Redshift](/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [AWS Glue](/blogs/big-data/category/analytics/aws-glue?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

### Follow

* [Twitter](https://twitter.com/awscloud)
* [Facebook](https://www.facebook.com/amazonwebservices)
* [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
* [Twitch](https://www.twitch.tv/aws)
* [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)