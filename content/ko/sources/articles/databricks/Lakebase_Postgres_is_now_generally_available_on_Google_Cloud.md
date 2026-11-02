---
title: "Lakebase Postgres가 이제 Google Cloud에서 일반 제공"
description: "Lakebase Postgres가 Google Cloud에서 GA되며, Databricks Data + AI Platform에서 서버리스 Postgres를 제공한다."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/lakebase-postgres-now-generally-available-google-cloud"
blog: databricks
published_date: 2026-11-03
---

# Lakebase Postgres가 이제 Google Cloud에서 일반 제공

**원문**: [databricks](https://www.databricks.com/blog/lakebase-postgres-now-generally-available-google-cloud) · **게시일**: 2026-11-02

## 개요

Lakebase Postgres가 Google Cloud에서 일반 제공되며, 팀은 Databricks Data + AI Platform 위에서 프로덕션급 서버리스 Postgres를 실행할 수 있다. Lakebase 아키텍처는 컴퓨트와 스토리지를 분리하여 리소스 충돌과 인프라 부담을 제거한다. 운영 데이터와 분석 데이터가 같은 저장소 계층을 공유하므로 파이프라인을 만들고 유지할 필요가 없다. 결과적으로 애플리케이션과 함께 확장하고, 거버넌스 모델을 공유하며, 총소유 비용을 줄이는 Postgres 데이터베이스를 얻는다.

## 핵심 기능

- 자동 확장과 제로 스케일: 트래픽에 맞게 컴퓨트가 조정되며 유휴 시 종료되어 사용하지 않는 용량에 비용을 지불하지 않는다.
- 인스턴트 브랜칭: 프로덕션 데이터의 격리된 제로 카피 브랜치를 몇 초 만에 생성한다.
- 특정 시점 복구: 버그나 실수로 인한 삭제 후 데이터베이스를 특정 시점으로 복원한다.

## 통합 플랫폼

운영 데이터와 분석 데이터가 동일한 저장소 기반을 공유하므로 분석, 애플리케이션, 에이전트가 파이프라인 없이 통합 플랫폼 위에서 실행된다. Lakebase Postgres on Google Cloud는 Google Cloud 인프라의 확장성과 신뢰성을 활용한다.

## 참고 자료

- 원문: [Lakebase Postgres가 이제 Google Cloud에서 일반 제공](https://www.databricks.com/blog/lakebase-postgres-now-generally-available-google-cloud)
