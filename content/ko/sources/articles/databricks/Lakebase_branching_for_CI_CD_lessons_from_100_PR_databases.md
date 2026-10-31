---
title: "Lakebase 브랜칭으로 CI/CD 개선: PR 데이터베이스 100개에서 얻은 교훈"
description: "Snorkel AI가 copy-on-write 방식의 Lakebase Postgres 브랜치로 각 pull request에 격리된 데이터베이스를 제공해 CI/CD 환경 프로비저닝을 분 단위에서 초 단위로 줄인 방법을 설명합니다."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases"
blog: databricks
published_date: 2026-10-31
---

# Lakebase 브랜칭으로 CI/CD 개선: PR 데이터베이스 100개에서 얻은 교훈

**원문**: [Databricks Blog](https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases) · **게시일**: 2026-10-31

## 개요

Snorkel AI는 AI 팀을 위한 데이터 개발 도구를 만드는 회사로, 전문 데이터 주석가와 프론티어 모델 제공업체가 사용합니다. 이 회사의 엔지니어는 Kubernetes 기반 CI 파이프라인으로 코드를 배포하며, 모든 open pull request와 임시 커밋마다 자체 ephemeral namespace를 만들어 브랜치를 배포하고 병합 전 전체 테스트 스위트를 실행합니다. 이 테스트는 실제 데이터로 실행될 때 가장 가치가 높고, Snorkel의 production database는 Amazon Aurora PostgreSQL cluster였기 때문에 각 PR namespace에는 production data의 자체 copy가 필요했습니다. copy를 restore하는 데 환경당 약 20분이 걸렸고, 개발자가 하루 종일 PR을 열고 merge queue가 실행마다 fresh environment를 필요로 할 때 이 시간은 너무 느렸습니다.

production을 Databricks Lakebase Postgres로 옮긴 뒤 Snorkel은 restore 단계를 copy-on-write branch로 대체했습니다. 새로운 PR branch는 p95 기준 60초 미만에 준비되고, standard Postgres database 형태로 제공되며, Aurora에 비해 comparable performance를 유지하면서 large JSONB와 LOB column까지 지원합니다. branch는 copy-on-write 방식이므로 약 2.5 TB production dataset 위에 약 100개의 concurrent PR branch가 존재해도 실제로 변경된 data에 대해서만 storage가 추가되고, branch TTL은 PR이 closed 또는 merged 될 때 ephemeral environment를 자동으로 정리합니다.

## 핵심 내용

- Lakebase는 production data의 격리된 PostgreSQL copy를 각 pull request에 제공하며, 준비 시간을 약 20분에서 1분 미만으로 줄입니다.
- copy-on-write branching 덕분에 약 2.5 TB dataset 위 100개 정도의 concurrent branch는 변경된 data에 대한 storage만 추가로 사용합니다.
- automatic branch expiration (TTL)은 pull request가 closed 또는 merged될 때 각 PR database를 자동으로 정리합니다.
- Lakebase가 standard Postgres interface를 제공하므로 기존 CI와 application code를 변경 없이 계속 사용할 수 있습니다.
- Aurora에서 Lakebase로의 migration 이후에도 query behavior와 large JSONB/LOB payload가 그대로 유지됩니다.
- private connectivity와 Okta SSO는 PR database에 대한 governed, secure environment를 지원합니다.

## 상세

이 글은 Snorkel AI의 CI/CD migration 사례 연구입니다. Lakebase 이전에는 realistically test database를 프로비저닝하는 것이 bottleneck이었습니다. 각 environment가 production Aurora cluster의 snapshot을 restore해야 했고, 약 20분이 소요되었습니다. Lakebase branch creation은 이를 60초 미만으로 줄여, realistic end-to-end test를 rare resource가 아니라 pull request lifecycle의 일반적인 부분으로 다룰 수 있게 했습니다. storage 효율성은 copy-on-write semantics에서 나오며, concurrent branch는 parent와 실제로 다른 부분에서만 diverge합니다. 운영 가드레일로는 ephemeral branch의 TTL 기반 expiry와 access control을 위한 private networking 및 Okta SSO가 있습니다. application은 standard driver 위 Postgres에 계속 머무르므로 test code를 다시 작성하지 않아도 large JSONB와 LOB payload를 포함한 query behavior가 그대로 이어집니다.

## 참고 자료

- 원문: [Lakebase branching for CI/CD: lessons from 100 PR databases](https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases)
