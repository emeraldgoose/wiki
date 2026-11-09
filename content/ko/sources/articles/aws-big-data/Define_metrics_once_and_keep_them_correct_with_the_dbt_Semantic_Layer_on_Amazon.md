---
title: "dbt 시맨틱 레이어로 Amazon Redshift에서 지표를 한 번만 정의하고 정확하게 유지하기"
description: "사전 집계된 골드 테이블은 평균 주문 금액을 280달러가 아니라 550달러로 조용히 보고한다. 오픈소스 dbt 시맨틱 레이어와 MetricFlow는 지표를 한 번 정의하고 Redshift에서 어떤 집계 단위로도 올바르게 다시 계산한다."
tags: [source, aws-big-data, data-engineering, semantic-layer, ko]
locale: ko
source_url: "https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift"
blog: aws-big-data
published_date: 2026-11-10
---

# dbt 시맨틱 레이어로 Amazon Redshift에서 지표를 한 번만 정의하고 정확하게 유지하기

**원문**: [Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift](https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift) · **게시일**: 2026-11-09

## 개요

잘 모델링된 골드 레이어는 이미 지표 표준화를 위한 시맨틱 레이어이며, 필요하기 전에 전용 도구를 도입하는 것은 과잉 설계다. 이 글이 다루는 것은 그 판단이 더 이상 통하지 않는 지점, 즉 사용자가 쿼리 시점에 임의로 고른 차원 조합으로 지표를 계산해야 하고 그중 일부가 비가산적인 경우다. 글은 오픈소스 dbt 시맨틱 레이어와 MetricFlow를 사용해 Amazon Redshift 위에서 동작하는 해법을 만들고, 평균 주문 금액을 한 번 정의한 뒤 일별·주별·매장별로 잘라도 값이 정확한지 확인한다.

논지는 두 가지 한계에서 출발한다. 골드 테이블은 하나의 집계 단위로 미리 집계되므로 모든 차원 조합을 제공하려면 조합마다 테이블이 필요하고 그 수는 2ⁿ으로 늘어난다. 아무도 그만큼 만들지 않고, 누군가 요청한 열몇 개만 만든 뒤 새 슬라이스마다 티켓을 처리한다. 그 탈출구로 넓은 팩트 테이블 하나를 노출하고 각 BI 도구가 자체적으로 GROUP BY를 하게 하면 유연성은 돌아오지만, 두 번째 문제에 곧바로 빠진다. 비가산 지표가 조용히 틀리는 것이다. 글은 AWS에서 지표 정의가 대체로 웨어하우스 바깥에 있었다는 점(대시보드와 Amazon Q를 위한 Quick Sight Topics, Glue 데이터 카탈로그 위에 지식 그래프 계층을 만드는 최신 AWS Context 서비스)을 짚으면서도, 초점은 Redshift 모델 옆에 Git으로 한 번 정의하는 거버넌스형 지표 계층에 둔다.

## 핵심 내용

- 예시는 의도적으로 작다. 한 매장의 주문 다섯 건으로, 2026년 1월 5일 월요일에 1,000달러 한 건, 1월 6일 화요일에 100달러 네 건이다. 일 단위 골드 테이블은 "이번 주 평균 주문 금액"에 두 일별 값을 평균해 550달러를 돌려주지만, 실제 주문에서 계산한 값은 1,400달러를 5로 나눈 280달러다. 실제 값의 거의 두 배인데도 그럴듯해 보여서 아무도 눈치채지 못한다.
- 전환율, 이익률, 고객 획득 비용, 순 사용자 수 같은 지표도 같은 함정에 빠진다. 주간 값은 주 단위 집계에서 매출 합계를 주문 수로 나눠 다시 계산해야 하는데, 사전 집계된 테이블에는 그에 필요한 정보가 없다.
- 해법은 선언적이다. `sem_orders.yml`의 시맨틱 모델에서 기본 엔터티 하나와 범주형·시간 차원, 두 개의 측정값(`order_total`은 금액 합계, `order_count`는 주문 ID 개수)을 선언하고, `average_order_value` 지표는 두 단순 지표의 비율로 정의해 MetricFlow가 요청된 집계 단위에서 항상 금액 합계를 주문 수로 나눈 값을 내도록 한다.
- `dbt_utils.date_spine`으로 만든 타임 스파인 모델을 `_models.yml`에 등록해 MetricFlow가 날짜를 다룰 수 있게 하며, 조작은 `mf` CLI(`mf validate-configs`, `mf list metrics`, `mf query`)로 한다.
- 결과는 두 명령으로 확인된다. 일 단위로 묶으면 1000.00과 100.00이 나오고, 주 단위로 묶으면 550.00이 아니라 280.00이 나오며, 같은 쿼리에서 근거가 되는 `total_revenue`(1400.00)와 `order_count`(5)도 확인할 수 있다. 전혀 다른 `order__store` 차원으로 잘라도 새 테이블은 필요 없다.
- `mf query --explain`은 생성된 SQL을 보여 준다. `date_trunc('week', ordered_at)`, `sum(amount)`, `count(order_id)`, `sum(amount) / nullif(count(order_id), 0)`을 1번 열로 그룹화하는 형태로, 주 단위 재계산이 실제로 일어난다는 점을 확인시켜 주며 이 SQL을 다른 도구에 그대로 옮길 수 있다.

## 상세

실습은 Amazon Redshift Serverless를 대상으로 하며 워크그룹을 만들 수 있는 계정과 쓸 수 있는 스키마, 연결 정보가 필요하다(IAM 인증도 가능하다). 8 RPU 워크그룹은 활성 쿼리 시간 기준 시간당 약 3달러이고 초 단위로 과금되며 쿼리당 최소 60초가 적용되므로, 이런 짧은 실습은 보통 1달러 미만이다. 프로비저닝은 콘솔에서 하거나 함께 제공되는 저장소의 AWS CDK 앱을 쓰면 되는데, 배포 스크립트는 인바운드 접근을 현재 IP로 제한하고 명시적으로 동의하지 않으면 0.0.0.0/0 같은 과도하게 넓은 CIDR을 거부한다. 환경은 `dbt-redshift==1.9.5`와 `dbt-metricflow==0.11.0`을 고정하며, 타임 스파인 YAML 때문에 dbt-core 1.9 이상이 필요하다. 최신 dbt-core에서는 사용 중단 알림이 뜨지만 이 프로젝트에서 동작은 같다.

소비 방식에서 오픈소스 dbt는 클라우드와 다르다. dbt Core에서는 검증과 노트북, 스크립트용 `mf query` CLI, 생성된 SQL을 도구나 스케줄러, 구체화 모델로 옮기는 `mf query --explain`, `dbt parse`가 만든 `semantic_manifest.json`을 읽는 BI 도구(예: Lightdash의 dbt MetricFlow 통합), 그리고 1급 커넥터가 없는 도구(예: Amazon Quick Sight)를 위해 지표를 다시 Redshift로 구체화하는 방법이 있다. 구체화는 생성된 SQL을 dbt 모델로 감싸거나, dbt Cloud에서 저장 쿼리와 내보내기를 스케줄로 실행하는 방식이며, 그 뒤에는 Quick Sight가 평범한 Amazon Redshift 테이블을 읽는다. Tableau나 Power BI가 JDBC·GraphQL 엔드포인트로 연결하는 완전 관리형 시맨틱 레이어 API는 dbt Cloud가 필요하지만 지표 정의는 동일하고 제공 계층만 다르므로, 나중에 옮겨 가도 4단계 YAML은 바뀌지 않는다. 정리는 스키마 삭제와 워크그룹 삭제, 또는 저장소의 destroy 스크립트 실행으로 한다.

## 참고 자료

- 원문: [Define metrics once and keep them correct with the dbt Semantic Layer on Amazon Redshift](https://aws.amazon.com/blogs/big-data/define-metrics-once-and-keep-them-correct-with-the-dbt-semantic-layer-on-amazon-redshift)
