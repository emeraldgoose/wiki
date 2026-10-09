---
title: Every 팀은 데이터 팀입니다 — Amazon Redshift analytics를 ChatGPT Work에 가져오기
description: AWS Data Analytics plugin for ChatGPT Work는 비즈니스 팀이 governed data warehouse 및 data lake에서 자연어 질문을 하여 분석하고 공유 가능한 대시보드를 생성할 수 있게 합니다.
date: 2026-09-10
tags: [aws, data-analytics, chatgpt, redshift, business-intelligence, natural-language-sql]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/"
blog: aws
---

# Every 팀은 데이터 팀입니다 — Amazon Redshift analytics를 ChatGPT Work에 가져오기

**Authors**: AWS Big Data Blog · **Published**: 2026년 9월 10일 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/)

## AWS Data Analytics plugin에 대해

오늘, AWS는 ChatGPT Work의 새로운 Data agent를 위한 [AWS Data Analytics plugin](https://chatgpt.com/plugins/plugin_asdk_app_6a917708c64481918f7ddea0cef4b8e6?q=aws)을 발표합니다. 이 plugin은 조직 전체의 팀이 자연어로 질문을 하고 Amazon Redshift 데이터 웨어하우스 및 데이터 레이크에서 governed 데이터를 분석하고 공유 가능한 대시보드를 생성할 수 있게 합니다. 모두 ChatGPT Work 대화 내에서 진행됩니다.

수십만 명의 고객이 Amazon Redshift를 매일 선택합니다. 이는 업계 선두 수준의 가격 성능으로 가장 demanding 워크로드를 실행할 수 있기 때문입니다. 고객은 Amazon Redshift가 데이터 웨어하우스와 데이터 레이크를 한 곳에서 액세스할 수 있다는 점을 좋아합니다. 팀은 정리된 비즈니스 데이터와 운영, históricaI 및third-party 데이터(open formats like Apache Iceberg 를 데이터 레이크에 저장됨)를 결합할 수 있습니다. 이를 통해 비즈니스 중요 의사 결정을 내릴 수 있는 완전한 그림을 얻을 수 있습니다.

고객은 더 많은 사람들에게 신뢰할 수 있는 데이터에 액세스할 수 있기를 요청해 왔습니다. analysts와 engineers가 SQL을 작성하는 사람만이 아니라, sales leaders, operations managers 및 finance teams가 결과에 의존하는 사람입니다. 영업 리더는 이번 분기에 고객 파이프라인이 어떻게 변했는지 알고 싶어 합니다. operations manager는 왜 fulfillment times가 지난 달에 변경되었는지 이해하고 싶어 합니다. 그래서 AWS Data Analytics plugin을 구축하여 ChatGPT Work에 Amazon Redshift와 AWS analytics의 힘을 가져왔습니다.

> **"비즈니스 팀은 더 빠른 의사 결정을 내릴 수 있습니다. 데이터를 직접 소싱하고 themselves가 필요로 하는 대시보드를 구축할 수 있게 되면. AWS와의 작업은 더 많은 사람들에게 해당 능력을 제공하여 조직의 성능 변화를 이해하고 어디서 집중해야 할지 결정하는 데 도움을 줍니다."**

— Arpan Shah, OpenAI Technology General Manager

## 그것이 왜 구축되었는가

고객은 AWS에 더 많은 사람들에게 신뢰할 수 있는 데이터를 제공해 줄 것을 요청했습니다. analysts와 engineers만이 아니라, 결과를 의존하는 sales leaders, operations managers 및 finance teams입니다. 영업 리더는 이번 분기에 고객 파이프라인이 어떻게 변했는지 알고 싶어 합니다. operations manager는 왜 fulfillment times가 지난 달에 변경되었는지 이해하고 싶어 합니다. 그래서 우리가 AWS Data Analytics plugin을 구축하여 ChatGPT Work에 Amazon Redshift와 AWS analytics의 힘을 가져왔습니다.

## 어떻게 작동하는가

새로운 plugin은 모든 사람에게 의사 결정 경로를 단축합니다. Data agent in ChatGPT Work를 사용하여 직원은 매일-authorized 데이터를 Amazon Redshift에서 everyday 언어ASK 질의할 수 있습니다. 그런 다음 분석을 정교화하고 변동을 조사하고 결과를 대시보드 형태로 전환할 수 있으며 ChatGPT Work를 나갈 필요가 없습니다. plugin은 Amazon Redshift provisioned 클러버와 Serverless workgroups 모두와 작동합니다. 고객은 기존 multi-cluster 또는 multi-workgroup 환경에 통합하고 이미 설정한 비용 및 보안 제어를 이용할 수 있습니다.

### 대화 워크플로우

판매 운영팀을 지원하는 비즈니스 분석가 Maya를 예로 들어보겠습니다. 그녀는 다양한 세그먼트 및 지역 전반에 걸친 수익 성능을 이해하고 싶어 합니다.

Maya는 ChatGPT Work에 AWS Data Analytics plugin을 로드한 다음 다음과 같이 묻습니다.

> *"지난 30일간 이전 30일간과 비교하여 revenue metrics는 어떻게 되나요?"*

[![ChatGPT Work conversation asking for revenue metrics using the AWS Data Analytics plugin](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-1.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-1.png)

*그림 1: ChatGPT Work에서 AWS Data Analytics plugin을 사용하여 revenue metrics 문의*

plugin은 그녀의 질의를 SQL로 번역하거나 필요한 경우 쿼리 시퀀스로 변환하고 Amazon Redshift의 관련 데이터에 대해 실행합니다. 그녀의 analytics team이 유지관리하는 동일한 curated revenue 데이터에 기반한 key revenue performance metrics를 반환합니다.

[![Amazon Redshift에서 반환된 revenue performance metrics 표](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-2.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-2.png)

*그림 2: Amazon Redshift로부터 반환된 revenue performance metrics*

Maya는 gross margin이 감소하는 것을 noticed하고 follow-up 질문을 합니다.

> *"지난 90일간 product category 및 region별 revenue breakdown은 어떻게 되나요?"*

[![Revenue results segmented by product category and region for the past 90 days in ChatGPT Work](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-3.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-3.png)

*그림 3: 지난 90일간 product category 및 region별 revenue breakdown*

plugin은 컨텍스트를 앞으로 가져오고 결과를 세그먼트화하여 Maya가 각 세그먼트의 성능을 이해하도록 돕습니다. 그녀는 분석을 검토하고 특정 지역이 뒤처지는 이유나 특정 세그먼트가 왜 outperforming되는지 더 깊이 파고들기 위한 추가 질문을 할 수 있습니다.

이 대화 워크플로우는 데이터 모델, metric definitions 또는 analytics team이 확립한 governance practices를 대체하지 않습니다. 더 많은 직원이 직접 데이터를 사용하도록 지원하여 analysts에게 more high-value work의 시간을 할애하게 합니다.

## plugin 기능

대화 도중 AWS Data Analytics plugin은 다음과 같이 할 수 있습니다:

* **사용 가능한 schema, tables, columns, 데이터 types** 사용자에게 제공.
* **자연어 질문을 Amazon Redshift SQL**로 번역.
* **고객의 Amazon Redshift 환경**에서 쿼리 실행.
* **표나 간결한 설명**으로 결과 제시.
* **follow-up 질문을 사용하여 필터, 비교 또는 결과 심화**.
* **분석을 interactive dashboard**로 전환하여 팀이 공유하고 탐색할 수 있음.

분석이 고객의 기존 데이터에서 실행되므로 팀은 이미 유지관리하고 있는 curated 데이터셋 및 business definitions을 계속 사용할 수 있습니다. Amazon Redshift 환경이 warehouse와 data lake 모두를 쿼리하는 고객은 plugin에 exposed된 governed datasets를 통해 해당 데이터를 사용할 수도 있습니다. AWS Data Analytics plugin은 또한 broader AWS data 및 analytics 서비스를 지원합니다. 여기에는 AWS Glue Data Catalog, Amazon S3 Tables, Amazon Athena 및 vector search on AWS 작동 능력이 포함됩니다.

## 시작 방법

ChatGPT Work에 AWS Data Analytics plugin을 설치하여 Amazon Redshift에 연결합니다. governed insights에 대화식으로 액세스하여 데이터를 제공합니다.

자세한 내용은 다음을 참조하세요:

* [AWS Data Analytics plugin](https://chatgpt.com/plugins/plugin_asdk_app_6a917708c64481918f7ddea0cef4b8e6?q=aws)
* [ChatGPT Work의 Data agent](https://chatgpt.com/plugins/Plugin_fc9843a6fb34819195d6c7802398a8a7)
* [OpenAI의 발표](https://openai.com/index/put-data-to-work/)

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