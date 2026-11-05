---
title: "Delta Sharing에서 OpenSharing으로: 무엇이 바뀌었고 앞으로는"
description: "Delta Sharing이 에이전트 스킬, AI 모델, 비정형 데이터까지 sharing을 확장하는 개방형 벤더 중립 프로토콜인 OpenSharing으로 발전한 이야기."
tags: [source, databricks, data-engineering, ko]
locale: ko
source_url: "https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next"
blog: databricks
published_date: 2026-11-06
---

# Delta Sharing에서 OpenSharing으로: 무엇이 바뀌었고 앞으로는

**원문**: [databricks](https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next) · **게시일**: 2026-11-05

## 개요

Delta Sharing은 데이터를 복사하지 않고도 클라우드 간에 라이브 데이터를 교환할 수 있게 해 수천 개 조직이 쓰는 방식이었다. 2026년 6월, Databricks와 Linux Foundation은 이를 OpenSharing으로 발전시켰다고 발표했다. OpenSharing은 테이블뿐 아니라 에이전트 스킬, AI 모델, 비정형 데이터 등 AI 팀이 이제 의존하는 더 넓은 자산을 공유하기 위한 개방형 벤더 중립 프로토콜이다. Delta Sharing은 Lake와 Parquet 위에 구축된 개방형 프로토콜로 Linux Foundation에 기여되었고 28,000명 이상의 수신자에 도달했으며, OpenSharing보다 좁은 테이블 중심 범위였다. 내부 Databricks 간 공유는 이미 테이블을 넘어섰고, 에이전트 도입으로 플랫폼 간 더 많은 자산 유형에 대한 수요가 커졌다.

OpenSharing은 상호 운용성과 범위 문제를 동시에 다룬다. Apache Iceberg REST Catalog를 지원해 공급자가 Iceberg 호환 엔진의 수신자에게도 데이터를 공유할 수 있게 하며, 스토리지 생태계 통합을 통해 데이터를 먼저 마이그레이션하지 않고도 온프레미스나 프라이빗 클라우드의 공급자가 Unity Catalog에 연결되는 OpenSharing 서버를 운영할 수 있다. 데이터는 이동하지 않고, 서버가 임시 범위 지정 자격 증명을 발급하고 데이터 경로 밖에 위치하는 제로 카피 자격 증명 벤딩 모델을 유지한다. 기존 Delta Sharing 클라이언트와 통합은 계속 호환되며, 이는 단절이 아니라 진화이며 delta-io/delta-sharing 저장소가 OpenSharing-IO/OpenSharing 조직과 병행해 계속 존재한다.

OpenSharing은 개방형 소스 프로토콜과 Databricks 구현이라는 두 층으로 존재한다. Apache 2.0 라이선스의 개방 소스 프로토콜과 규격은 Linux Foundation AI & Data Foundation 산하에서 개발되고, Databricks OpenSharing은 Unity Catalog, Databricks Marketplace, Clean Rooms와 통합된 엔터프라이즈 구현이다. 개방 소스 Unity Catalog는 개방형 서버와 결합해 Databricks 밖에서 벤더 중립적인 카탈로그와 거버넌스를 제공할 수 있다. 프로토콜은 공유 대상을 테이블에서 Volume, Agent Skill, AI Model로 확장하는 Share, Schema, Asset 계층 구조를 도입한다.

## 핵심 내용

- OpenSharing은 크로스 플랫폼 제로 카피 sharing을 테이블에서 volume, 에이전트 스킬, AI 모델 등으로 확장한다.
- 프로토콜은 Apache 2.0으로 Linux Foundation AI & Data Foundation 산하에서 개발되며, Databricks 엔터프라이즈 구현과는 별도 층이다.
- 기존 Delta Sharing 클라이언트와 커넥터가 계속 호환되므로 롤아웃은 호환성을 깨는 변경이 아니라 진화다.
- Iceberg REST Catalog 지원으로 Iceberg 도구를 표준화한 수신자에게도 공유 범위가 넓어진다.
- 온프레미스와 프라이빗 클라우드 공급자는 데이터 마이그레이션 없이 Databricks Storage Ecosystem을 통해 서버를 운영할 수 있다.
- 제로 카피 자격 증명 벤딩 모델을 유지한다. 데이터는 그대로 두고 임시 자격 증명으로 접근을 부여한다.

## 상세

발표일은 2026년 6월 10일이다. 자산 계층 구조는 현재 Table, Volume, Agent Skill, Model 유형을 지정하며, Agent와 Page 또는 Glossary 유형은 커뮤니티 제안으로 남아 있다. 기능 보강으로 SecureConnect, 비공개 프리뷰의 Global Distribution, 베타의 Genie Agent Sharing, 공개 프리뷰의 Lakebase 테이블 및 변경 데이터 피드 공유가 있다. 전체 프로토콜 상세, 파트너 목록, 거버넌스 조건, 버전 관리 조건은 링크된 원문에 있다.

## 참고 자료

- 원문: [databricks](https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next)
