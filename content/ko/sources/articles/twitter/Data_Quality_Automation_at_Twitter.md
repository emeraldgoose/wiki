---
title: Twitter의 데이터 품질 자동화
description: 엑사바이트급 BigQuery 데이터에 Great Expectations + Airflow 검사를 얹은 데이터 품질 플랫폼(DQP)
tags: [source, twitter, x, data-quality, bigquery, airflow, great-expectations, ko]
locale: ko
source_url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter"
blog: twitter
date: '2022-09-15'
---

# Twitter의 데이터 품질 자동화

## 요약

Twitter 수집 프레임워크(GCP Dataflow + Airflow, 온프레미스 Hadoop → BigQuery)는 직원이 월 1천만 건 이상의 쿼리를 1엑사바이트 가까운 데이터에 실행하게 한다. 가용성을 해결한 뒤 남은 공백은 *품질*이었다. 핵심 광고 분석·ML 특징 생성·개인화 모델에 쓰이는 데이터셋에 수동 스팟체크(BigQuery UI·노트북의 손작성 SQL)만 있었고, 자동화된 단일 프레임워크가 없었다. 팀은 **데이터 품질 플랫폼(DQP)** 을 구축했다. 표준·맞춤 품질 메트릭을 만들고, 검증 실패를 알리며, 메트릭 추세를 모니터링하는 관리형·설정 기반·워크플로 기반 솔루션이며 전부 GCP 안에서 동작한다.

## 왜 데이터 품질인가

신선도·완전성·정확성·일관성이 데이터 품질을 결정한다. 자동 검사는 **신뢰**(저리스크 의사결정, 효율 향상), **생산성**(수동 검증 대신 핵심 구축에 집중), **매출 보호**(나쁜 데이터는 돈 잃음)를 제공한다.

## 아키텍처

- **검사 로직**: 오픈소스 [Great Expectations](https://greatexpectations.io/) + 자체 Stats Collector Library를 오퍼레이터로 래핑.
- **오케스트레이션/상태**: 리소스·주기 단위의 Airflow 워크플로.
- **전달**: YAML 설정을 CI/CD로 GCS에 배포 → Airflow 워커가 테스트 실행 → 결과를 **PubSub** 큐에 발행 → **Dataflow** 작업이 BigQuery 테이블에 적재 → **Looker**에서 디버깅·추세 분석.

## 효과(보고된 수치)

- **수익 분석 플랫폼**(수익 분석 데이터를 AdsManager에 수집·집계·제공): 자동 출력 검증으로 신규 기능 롤아웃 시간 약 **20% 단축**, 지속 측정으로 광고주 신뢰 상승.
- **Core Served Impressions**(400곳 이상 내부 다운스트림이 소비하는 핵심 직접 매출 데이터셋): 상·하류 편차에 대한 최초의 자동 가시성과 전 다운스트림 정렬 메트릭 확보 — 이전에는 전무.

## SW 엔지니어를 위한 시사점

- 데이터 *가용성* 해결 뒤에는 품질 마일스톤을 명시적으로 잡는다. 사용량(월 1천만 쿼리)이 조용한 오염의 폭발 반경을 키운다.
- 설정 기반 검사(CI/CD의 YAML)는 수천 데이터셋에 확장되고 손작성 SQL은 그렇지 못하다. Great Expectations가 검사 어휘를 제공하므로 팀은 *방법*이 아니라 *무엇을* 검사할지만 쓴다.
- 검사 결과는 알림만이 아니라 조회 가능한 데이터(BigQuery + Looker)로 적재한다. 추세 가시성이 시점 검증을 이상 탐지로 바꾼다.
- 검사 건수가 아니라 생산자(롤아웃 시간 −20%)와 소비자(400곳 이상 정렬 메트릭)에게 의미 있는 채택 지표를 보고한다.

## 참고

- 원문: https://blog.x.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter (Eduardo Luiz Ohe, Bi Ling Wu, 2022-09-15)
- 관련: `concepts/data-engineering/delta-lake.md`, `concepts/data-engineering/stream-processing.md`
